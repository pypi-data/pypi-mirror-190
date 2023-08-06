from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, MutableMapping, Optional
from kgdata.wikidata.db import WikidataDB

from ned.candidate_generation.common import CandidateGenerationBasicMethod
from ned.candidate_generation.pyserini.search import PyseriniSearcher
from ned.data_models.prelude import CandidateEntity, Entity


@dataclass
class PyseriniArgs:
    indice_dir: Path
    index_name: str
    limit: int = 1000
    query_types: List[Literal["default", "bow", "fuzzy"]] = field(
        default_factory=lambda: ["default"]
    )


class PyseriniWrapper(CandidateGenerationBasicMethod):
    __doc__ = PyseriniSearcher.__doc__
    VERSION = PyseriniSearcher.VERSION

    def __init__(
        self,
        args: PyseriniArgs,
        kvstore: Optional[MutableMapping[str, list[CandidateEntity]]] = None,
    ):
        super().__init__(kvstore)
        self.args = args
        self.search = PyseriniSearcher(self.args.indice_dir / self.args.index_name)
        self.batch_size = 512

    def get_candidates_by_queries(
        self, queries: List[str]
    ) -> Dict[str, List[CandidateEntity]]:
        search_res: Dict[str, Dict[str, CandidateEntity]] = {}
        for i in range(0, len(queries), self.batch_size):
            subqueries = queries[i : i + self.batch_size]

            for query_type in self.args.query_types:
                if query_type == "default":
                    subqueries2 = subqueries
                    pre_analyzed = False
                elif query_type == "bow":
                    subqueries2 = [
                        self.search.bow_query(query, field="contents")
                        for query in subqueries
                    ]
                    pre_analyzed = True
                elif query_type == "fuzzy":
                    subqueries2 = [
                        self.search.fuzzy_query(query, field="contents")
                        for query in subqueries
                    ]
                    pre_analyzed = True
                else:
                    raise ValueError(f"Unknown query type {query_type}")

                res = self.search.batch_search(
                    subqueries2, limit=self.args.limit, pre_analyzed=pre_analyzed
                )
                for query, cans in zip(subqueries, res):
                    provenance = f"{self.args.index_name}:{query_type}:"
                    if query not in search_res:
                        search_res[query] = {}

                    for i, can in enumerate(cans):
                        doc = can.doc
                        search_res[query][can.docid] = CandidateEntity(
                            entity=Entity(
                                id=can.docid,
                                label=doc.label,
                                description=doc.description,
                                aliases=doc.aliases,
                                popularity=doc.popularity,
                            ),
                            score=can.score,
                            provenance=provenance + str(i),
                        )

        return {query: list(cans.values()) for query, cans in search_res.items()}
