from __future__ import annotations

import pickle
from dataclasses import dataclass, field, fields
from functools import partial
from typing import Literal, Optional

from hugedict.prelude import HugeMutableMapping, RocksDBDict, RocksDBOptions
from kgdata.wikidata.db import WikidataDB
from ned.actors.dataset import NEDDatasetActor, ned_dsdict_cache_filename
from ned.actors.entity_recognition import EntityRecognitionActor
from ned.actors.evaluate_helper import EvalArgs, evaluate
from ned.candidate_generation.oracle_semtyper import OracleSemTyper, OracleSemTyperArgs
from ned.candidate_generation.pyserini_wrapper import PyseriniArgs, PyseriniWrapper
from ned.data_models.prelude import (
    DatasetCandidateEntities,
    CandidateEntity,
    NEDExample,
)
from ream.cache_helper import CacheArgsHelper
from ream.dataset_helper import DatasetDict
from ream.prelude import FS, ActorState, DatasetQuery, EnumParams, Cache, ReamWorkspace
from timer import Timer
from sm.misc.funcs import assert_not_null
from osin.integrations.ream import OsinActor


@dataclass
class CGParams(EnumParams):
    method: Literal["pyserini", "oracle_semtyper"] = field(
        metadata={
            "help": "Candidate generation method",
            "variants": {
                "pyserini": PyseriniWrapper,
                "oracle_semtyper": OracleSemTyper,
            },
        }
    )
    pyserini: Optional[PyseriniArgs] = None
    oracle_semtyper: Optional[OracleSemTyperArgs] = None
    cache: bool = field(
        default=True,
        metadata={"help": "Whether to cache candidate generation results. "},
    )


class CGDatasetDict(DatasetDict[DatasetCandidateEntities]):
    serde = (DatasetCandidateEntities.save, DatasetCandidateEntities.load, "parq")


class CanGenActor(
    OsinActor[
        NEDExample,
        CGParams,
    ]
):
    """
    Evaluating different methods in generating candidate entities for Record Linkage problem

    Each example is the whole table because a method may want to use other information such
    as headers or the surrounding context of the cell to generate candidates.
    """

    """CHANGELOG:
    - 200: new ream
    - 21x: same dataset shares the same cache dir for key-value store only.
    """
    NAME = "Candidate Generation"
    VERSION = 213
    EXP_VERSION = 3

    def __init__(
        self,
        params: CGParams,
        dataset_actor: NEDDatasetActor,
        entity_recognition_actor: EntityRecognitionActor,
    ):
        super().__init__(params, dep_actors=[dataset_actor, entity_recognition_actor])
        self.db = WikidataDB.get_instance()
        self.dataset_actor = dataset_actor
        self.entity_recognition_actor = entity_recognition_actor
        self.dataset_name = ""

    def run(self, example: NEDExample) -> DatasetCandidateEntities:
        return self.batch_run([example])

    def batch_run(self, examples: list[NEDExample]) -> DatasetCandidateEntities:
        entity_columns = self.entity_recognition_actor.batch_run(examples)
        return self.get_method(self.dataset_name).get_candidates(
            examples, entity_columns
        )

    def get_provenance(self):
        return self.entity_recognition_actor.get_provenance()

    @Cache.cls.file(
        cls=CGDatasetDict,
        cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance),
        mem_persist=True,
        compression="lz4",
        log_serde_time=True,
    )
    def run_dataset(self, dataset_query: str):
        dsdict = self.dataset_actor.run(dataset_query)
        er_dsdict = self.entity_recognition_actor.run_dataset(dataset_query)

        out = CGDatasetDict(dsdict.name, {}, er_dsdict.provenance)
        method = self.get_method(dsdict.name)
        timer = Timer()
        for name, ds in dsdict.items():
            with timer.watch("run candidate generation"):
                out[name] = method.get_candidates(ds, er_dsdict[name])
        timer.report(self.logger.debug)
        return out

    def evaluate(self, evalargs: EvalArgs):
        for dsquery_s in evalargs.dsqueries:
            dsquery = DatasetQuery.from_string(dsquery_s)
            dsdict = self.dataset_actor.run(dsquery_s)
            er_dsdict = self.entity_recognition_actor.run_dataset(dsquery_s)
            cangen_dsdict = self.run_dataset(dsquery_s)

            for name, examples in dsdict.items():
                candidates = cangen_dsdict[name]
                entity_columns = er_dsdict[name]
                self.logger.debug("Running evaluation on dataset {}", dsquery_s)
                dsname = dsquery.get_query(name)
                with self.new_exp_run(
                    dataset=dsname, exprun_type=evalargs.exprun_type
                ) as exprun:
                    evaluate(
                        examples,
                        entity_columns,
                        candidates,
                        eval_ignore_nil=evalargs.eval_ignore_nil,
                        eval_ignore_non_entity_cell=evalargs.eval_ignore_non_entity_cell,
                        dsname=dsname,
                        logger=self.logger,
                        exprun=exprun,
                        report_unique=True,
                        exprun_type=evalargs.exprun_type,
                    )
                    if exprun is not None:
                        exprun.update_output(
                            primitive={"workdir": str(self.get_working_fs().root)}
                        )

    @Cache.mem()
    def _get_kv_cache(
        self, dataset_name: str
    ) -> HugeMutableMapping[str, list[CandidateEntity]]:
        deps = [actor.get_actor_state() for actor in self.dep_actors]
        if self.params.method == "pyserini":
            state = ActorState.create(
                PyseriniWrapper, self.params.pyserini, dependencies=deps
            )
        elif self.params.method == "oracle_semtyper":
            # leverage the fact that oracle_semtyper is just a wrapper of pyserini
            # so the cache is the same
            args = PyseriniArgs(
                **{
                    field.name: getattr(self.params.oracle_semtyper, field.name)
                    for field in fields(PyseriniArgs)
                }
            )
            state = ActorState.create(PyseriniWrapper, args, dependencies=deps)
        else:
            raise NotImplementedError()

        cache_dir = ReamWorkspace.get_instance().reserve_working_dir(state)
        self.logger.debug(
            "Using directory: {} for key-value store caching",
            cache_dir,
        )
        wfs = FS(cache_dir)
        # old code, try this if the new code doesn't work
        # wfs = self.get_working_fs()

        dsdir = wfs.get(dataset_name + "_cache_db", {}, save_key=True)
        if not dsdir.exists():
            with wfs.acquire_write_lock(), dsdir.reserve_and_track() as realdir:
                dbpath = str(realdir)
        else:
            dbpath = str(dsdir.get())

        return RocksDBDict(
            path=dbpath,
            options=RocksDBOptions(create_if_missing=True),
            deser_key=partial(str, encoding="utf-8"),
            deser_value=pickle.loads,
            ser_value=pickle.dumps,
            readonly=False,
        )

    @Cache.mem()
    def get_method(self, dataset_name: str):
        kvstore = self._get_kv_cache(dataset_name) if self.params.cache else None

        if self.params.method == "pyserini":
            return PyseriniWrapper(assert_not_null(self.params.pyserini), kvstore)
        elif self.params.method == "oracle_semtyper":
            args = assert_not_null(self.params.oracle_semtyper)
            return OracleSemTyper(
                PyseriniWrapper(args, kvstore),
                args,
            )
        else:
            raise NotImplementedError(self.params.method)
