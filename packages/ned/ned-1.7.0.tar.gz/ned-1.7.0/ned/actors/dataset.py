from __future__ import annotations
from pathlib import Path
from slugify import slugify
import random
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping, Optional, cast
from ned.actors.evaluate_helper import EvalArgs
import ray
import numpy as np
import serde.jl
import serde.json
import serde.textline
from osin.integrations.ream import OsinActor
from osin.types import OTable
from rdflib.namespace import RDFS
from ream.prelude import Cache, DatasetDict, DatasetQuery
from sm_datasets import Datasets
from functools import partial
from grams.algorithm.literal_matchers.text_parser import TextParser
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models import WDEntity
from ned.data_models.prelude import CellLink, Entity, NEDExample
from sm.dataset import Example, FullTable
from sm.namespaces.wikidata import WikidataNamespace
from sm.prelude import M
from sm.misc.ray_helper import ray_map, get_instance, ray_put


@dataclass
class NEDDatasetParams:
    skip_non_unique_mention: bool = False


class NEDDatasetDict(DatasetDict[list[NEDExample]]):
    serde = (serde.jl.ser, partial(serde.jl.deser, cls=NEDExample), "jl")


def ned_dsdict_cache_filename(
    self, dsquery: str, provenance: str = "", compression: Optional[str] = None
):
    ext = f".{compression}" if compression is not None else ""
    return DatasetQuery.from_string(dsquery).dataset + ext


class NEDDatasetActor(OsinActor[str, NEDDatasetParams]):
    """An actor that will output the dataset for entity linking."""

    """CHANGELOG:
    - 401: add option to skip tables that the same mention at different cells are linked to different entities
    - 41x: add entity column types to the example, ignore tables with empty entity columns, 
    """

    NAME = "Dataset"
    VERSION = 413
    EXP_VERSION = 2

    def __init__(self, params: NEDDatasetParams):
        super().__init__(params)
        self.text_parser = TextParser.default()
        self.kgns = WikidataNamespace.create()

    @Cache.cls.file(
        cls=NEDDatasetDict,
        mem_persist=True,
        filename=partial(ned_dsdict_cache_filename, compression="lz4"),
        log_serde_time=True,
    )
    def run(
        self,
        query: str,
    ) -> NEDDatasetDict:
        dsquery = DatasetQuery.from_string(query)
        ned_examples = self.ned_examples(dsquery.dataset)

        infodir = self.get_working_fs().root / (f"info_" + slugify(dsquery.dataset))
        infodir.mkdir(exist_ok=True)

        if dsquery.shuffle:
            index = list(range(len(ned_examples)))
            random.Random(dsquery.seed).shuffle(index)

            shuffle_index = [ned_examples[i].table.table_id for i in index]
            serde.json.ser(
                shuffle_index,
                infodir / f"shuffle_{dsquery.seed or 'none'}.json",
            )
            id2e = {e.table.table_id: e for e in ned_examples}
            ned_examples = [id2e[i] for i in shuffle_index]

        if self.params.skip_non_unique_mention:
            non_unique_table_ids = [
                e.table.table_id for e in ned_examples if self.has_non_unique_mention(e)
            ]
            serde.textline.ser(
                non_unique_table_ids,
                infodir / f"non_unique_tables.txt",
            )
            non_unique_table_ids = set(non_unique_table_ids)
            ned_examples = [
                e for e in ned_examples if e.table.table_id not in non_unique_table_ids
            ]
            self.logger.info(
                "Skip {} tables with non-unique mentions",
                len(non_unique_table_ids),
            )

        return NEDDatasetDict.molt(dsquery.select(ned_examples))

    def evaluate(self, evalargs: EvalArgs):
        for query in evalargs.dsqueries:
            dsquery = DatasetQuery.from_string(query)
            dsdict = self.run(query)
            for name, examples in dsdict.items():
                n_cells = [np.prod(e.table.shape()) for e in examples]
                n_rows = [e.table.shape()[0] for e in examples]

                metrics = {
                    "# examples": len(examples),
                    "average # cells": float(np.mean(n_cells)),
                    "max # cells": float(np.max(n_cells)),
                    "min # cells": float(np.min(n_cells)),
                }
                for pth in [25, 50, 75, 90, 95, 99]:
                    metrics[f"{pth} percentile # cells"] = float(
                        np.percentile(n_cells, pth)
                    )

                metrics.update(
                    {
                        "average # rows": float(np.mean(n_rows)),
                        "max # rows": float(np.max(n_rows)),
                        "min # rows": float(np.min(n_rows)),
                    }
                )
                for pth in [25, 50, 75, 90, 95, 99]:
                    metrics[f"{pth} percentile # rows"] = float(
                        np.percentile(n_rows, pth)
                    )

                self.logger.info(
                    "Dataset {} - split {}:",
                    dsdict.name,
                    name,
                )
                for k, v in metrics.items():
                    self.logger.info("\t - {}: {}", k, v)

                with self.new_exp_run(dataset=dsquery.get_query(name)) as exprun:
                    if exprun is not None:
                        for ei, example in enumerate(examples):
                            columns = example.table.columns
                            header = [
                                c.clean_name or f"column-{i}"
                                for i, c in enumerate(columns)
                            ]

                            nrows, ncols = example.table.shape()
                            otbl = []
                            for ri in range(nrows):
                                otbl.append(
                                    dict(
                                        zip(
                                            header,
                                            (
                                                str(columns[ci].values[ri])
                                                for ci in range(ncols)
                                            ),
                                        )
                                    )
                                )
                            exprun.update_example_output(
                                example_id=str(ei),
                                example_name=example.table.table_id,
                                complex={"table": OTable(otbl)},
                            )

                        exprun.update_output(primitive=metrics)

    @Cache.jl.file(mem_persist=True, compression="lz4", cls=NEDExample)
    def ned_examples(self, dataset: str) -> list[NEDExample]:
        dbdir_ref = ray_put(WikidataDB.get_instance().database_dir)
        list_exs = ray_map(
            sm2ned_example.remote,
            [(dbdir_ref, item) for item in M.batch(48, self.sm_examples(dataset))],
            verbose=True,
            desc="generate ned examples",
        )
        return [e for lst in list_exs for e in lst]

    @Cache.pickle.file(mem_persist=True, compression="lz4")
    def sm_examples(self, dataset: str) -> list[Example[FullTable]]:
        ds = Datasets()
        db = WikidataDB.get_instance()
        examples = getattr(ds, dataset)()
        examples = ds.fix_redirection(
            examples, db.wdentities, db.wdredirections, self.kgns
        )
        return examples

    def has_non_unique_mention(self, example: NEDExample) -> bool:
        """Check if the example table has the same mention at different cells linked to different entities"""
        col2mention = defaultdict(lambda: defaultdict(set))

        for ri, ci, link in example.cell_links.enumerate_flat_iter():
            if link is None:
                continue

            text = example.table[ri, ci]
            assert isinstance(text, str), text

            for entid, (start, end) in link.mentions.items():
                mention = text[start:end]
                col2mention[ci][mention].add(entid)
                if len(col2mention[ci][mention]) > 1:
                    return True

        return False

    @classmethod
    def _get_cell_links(
        cls,
        example: Example[FullTable],
        wdents: Mapping[str, WDEntity],
        wdpopularity: Mapping[str, float],
    ) -> M.Matrix[CellLink | None]:
        cell_links = M.Matrix.default(
            example.table.table.shape(), cast(Optional[CellLink], None)
        )

        for ci, col in enumerate(example.table.table.columns):
            if not cls._is_column_entity(example, ci):
                continue
            for ri in range(len(col.values)):
                links = [
                    link
                    for link in example.table.links[ri, ci]
                    if len(link.entities) > 0
                ]
                if len(links) == 0:
                    continue

                mentions = {}
                ents = []
                for link in links:
                    for entid in link.entities:
                        _ent = wdents[entid]
                        ent = Entity(
                            id=_ent.id,
                            label=str(_ent.label),
                            description=str(_ent.description),
                            aliases=Entity.encode_aliases(_ent.aliases),
                            popularity=wdpopularity.get(_ent.id, 0.0),
                        )
                        ents.append(ent)
                        mentions[ent.id] = (link.start, link.end)

                cell_links[ri, ci] = CellLink(
                    entities=ents,
                    mentions=mentions,
                )
        return cell_links

    @classmethod
    def _is_column_entity(cls, example: Example[FullTable], ci: int):
        for sm in example.sms:
            stypes = sm.get_semantic_types_of_column(ci)
            if any(stype.predicate_abs_uri == str(RDFS.label) for stype in stypes):
                return True
        return False


@ray.remote
def sm2ned_example(
    dbdir: Path, sm_examples: list[Example[FullTable]]
) -> list[NEDExample]:
    text_parser = TextParser.default()
    kgns = WikidataNamespace.create()
    db = get_instance(
        lambda: WikidataDB(dbdir),
        f"kgdata.wikidata.db[{dbdir}]",
    )
    wdents = db.wdentities.cache()
    wdpopularity = db.wdpagerank
    new_examples = []

    for example in sm_examples:
        table = deepcopy(example.table.table)
        for col in table.columns:
            assert col.name is not None
            col.name = text_parser._norm_string(col.name)

        # normalize cells
        for ci, col in enumerate(table.columns):
            for ri, cell in enumerate(col.values):
                if isinstance(cell, str):
                    col.values[ri] = text_parser._norm_string(cell)

        entity_columns = []
        entity_column_types = []

        for ci in range(example.table.table.shape()[1]):
            if NEDDatasetActor._is_column_entity(example, ci):
                entity_columns.append(ci)
                ctypes = []
                for sm in example.sms:
                    for stype in sm.get_semantic_types_of_column(ci):
                        if stype.predicate_abs_uri == str(RDFS.label):
                            ctypes.append(kgns.get_entity_id(stype.class_abs_uri))
                entity_column_types.append(
                    [
                        Entity(
                            id=entid,
                            label=(_ent := db.wdentities[entid]).label,
                            description=_ent.description,
                            aliases=Entity.encode_aliases(_ent.aliases),
                            popularity=db.wdpagerank[entid],
                        )
                        for entid in M.filter_duplication(ctypes)
                    ]
                )

        if len(entity_columns) == 0:
            continue

        new_examples.append(
            NEDExample(
                table=example.table.table,
                entity_columns=entity_columns,
                entity_column_types=entity_column_types,
                cell_links=NEDDatasetActor._get_cell_links(
                    example, wdents, wdpopularity
                ),
            )
        )
    return new_examples
