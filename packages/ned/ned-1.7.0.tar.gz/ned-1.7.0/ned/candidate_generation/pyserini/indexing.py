from dataclasses import dataclass
from functools import partial
import os, yada
from pathlib import Path
from typing import Literal, Union
from kgdata.spark import does_result_dir_exist, get_spark_context
from kgdata.wikidata.config import WDDataDirCfg
from kgdata.wikidata.datasets.entity_metadata import entity_metadata
from kgdata.wikidata.datasets.entity_pagerank import entity_pagerank
from ned.candidate_generation.pyserini.configuration import IndexSettings
from ned.candidate_generation.pyserini.document import LuceneDocument
from pyspark import RDD
from ned.data_models.pymodels import Entity
from jnius import autoclass
import serde.json


@dataclass
class BuildIndexArgs:
    dataset: Literal["wikidata.entity"]
    data_dir: Path
    index_dir: Path
    settings: IndexSettings
    n_files: int = 256
    optimize: bool = False
    shuffle: bool = True

    def get_dataset(self) -> RDD[LuceneDocument]:
        if self.dataset == "wikidata.entity":
            return self.get_wikidata_entity_dataset()
        raise NotImplementedError(self.dataset)

    def get_wikidata_entity_dataset(self, lang: str = "en"):
        WDDataDirCfg.init(os.environ["WD_DIR"])

        return (
            entity_metadata(lang=lang)
            .get_rdd()
            .map(
                lambda r: LuceneDocument(
                    id=r.id,
                    label=str(r.label),
                    description=str(r.description),
                    aliases=Entity.encode_aliases(r.aliases),
                    popularity=1,
                )
            )
            .map(lambda x: (x.id, x))
            .leftOuterJoin(entity_pagerank(lang=lang).get_rdd())
            .map(lambda x: x[1][0].set("popularity", x[1][1] or 0.0))
            .filter(lambda doc: doc.label.strip() != "")
        )


def build_sparse_index(
    dataset: RDD[LuceneDocument],
    data_dir: Union[str, Path],
    index_dir: Union[str, Path],
    settings: IndexSettings,
    n_files: int,
    optimize: bool,
    shuffle: bool,
):
    """Build a pyserini index from the given dataset.

    Args:
        dataset: The dataset to build the index from.
        data_dir: The directory to store the serialized docs.
        index_dir: The directory to store the index.
        settings: The settings to use for the index.
        n_files: The number of files to store the docs (to avoid huge number of files).
        optimize: Whether to optimize the index.
    """
    data_dir = Path(data_dir)
    index_dir = Path(index_dir)

    if not does_result_dir_exist(data_dir):
        if settings.analyzer.need_pretokenize():
            dataset = dataset.map(
                partial(LuceneDocument.pretokenize, analyzer=settings.get_analyzer())
            )

        rdd = dataset.map(LuceneDocument.to_json)
        if n_files > 0:
            rdd = rdd.coalesce(n_files, shuffle=shuffle)
        rdd.saveAsTextFile(str(data_dir))

        for file in Path(data_dir).iterdir():
            if file.name.startswith("part-"):
                file.rename(file.parent / f"{file.stem}.jsonl")

        serde.json.ser(settings.to_dict(), data_dir / "_SUCCESS", indent=4)
    else:
        assert (
            IndexSettings.from_dict(serde.json.deser(data_dir / "_SUCCESS")) == settings
        )

    if not does_result_dir_exist(index_dir):
        index_dir.mkdir(parents=True, exist_ok=True)
        extra_args = []
        if settings.analyzer.need_pretokenize():
            extra_args.append(f"-pretokenized")

        if optimize:
            extra_args.append("-optimize")

        JIndexCollection = autoclass("io.anserini.index.IndexCollection")
        JIndexCollection.main(
            [
                "-collection",
                "JsonCollection",
                "-input",
                str(data_dir),
                "-index",
                str(index_dir),
                "-generator",
                "EnhancedLuceneDocumentGenerator",
                "-storePositions",
                "-storeDocvectors",
                "-storeRaw",
                "-threads",
                str(os.cpu_count()),
                "-memorybuffer",
                "8192",
                "-fields",
                "aliases description",
                "-floatFields",
                "popularity",
                "-featureFields",
                "popularity",
            ]
            + extra_args
        )
        (index_dir / "_SUCCESS").touch()
        serde.json.ser(settings.to_dict(), index_dir / "_SUCCESS", indent=4)
    else:
        assert (
            IndexSettings.from_dict(serde.json.deser(index_dir / "_SUCCESS"))
            == settings
        )


if __name__ == "__main__":
    args = yada.Parser1(BuildIndexArgs).parse_args()

    build_sparse_index(
        dataset=args.get_dataset(),
        data_dir=args.data_dir,
        index_dir=args.index_dir,
        settings=args.settings,
        n_files=args.n_files,
        optimize=args.optimize,
        shuffle=args.shuffle,
    )
