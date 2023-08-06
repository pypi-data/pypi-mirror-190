from collections import MutableMapping, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from loguru import logger
from ned.data_models.prelude import (
    CandidateEntity,
    NEDExample,
    DatasetCandidateEntities,
)


class CandidateRankingComplexMethod(ABC):
    """Candidate ranking method that find candidates from a cell and its surrounding context"""

    @abstractmethod
    def get_candidates(
        self,
        examples: List[NEDExample],
        entity_columns: list[list[int]],
    ) -> DatasetCandidateEntities:
        pass


class CandidateGenerationBasicMethod(CandidateRankingComplexMethod):
    """Candidate generation method that find candidates from text"""

    def __init__(
        self, kvstore: Optional[MutableMapping[str, list[CandidateEntity]]] = None
    ):
        self.kvstore = kvstore
        self.logger = logger.bind(name=self.__class__.__name__)

    @abstractmethod
    def get_candidates_by_queries(
        self, queries: List[str]
    ) -> Dict[str, List[CandidateEntity]]:
        """Generate list of candidate entities for each query."""
        pass

    def get_candidates(
        self, examples: List[NEDExample], entity_columns: list[list[int]]
    ) -> DatasetCandidateEntities:
        self.logger.debug("Create queries")
        queries = set()
        for ei, example in enumerate(examples):
            for ci in entity_columns[ei]:
                for cell in example.table.columns[ci].values:
                    queries.add(str(cell))

        self.logger.debug("find candidates")
        queries = list(queries)
        if self.kvstore is not None:
            original_queries = queries
            queries = [q for q in queries if q not in self.kvstore]
        else:
            original_queries = []

        search_results = self.get_candidates_by_queries(queries)

        if self.kvstore is not None:
            for q in queries:
                # sort the results by score and ids so that
                # the order is always deterministic
                self.kvstore[q] = search_results[q]
            for q in original_queries:
                if q not in search_results:
                    search_results[q] = self.kvstore[q]

        self.logger.debug("find candidates... done! populating the results")
        can_output: dict[
            str, dict[int, dict[int, list[CandidateEntity]]]
        ] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for ei, example in enumerate(examples):
            table_id = example.table.table_id
            for ci in entity_columns[ei]:
                for ri, cell in enumerate(example.table.columns[ci].values):
                    cell = example.table[ri, ci]
                    query = str(cell)
                    can_output[table_id][ci][ri] = search_results[query]

        return DatasetCandidateEntities.from_pymodel_candidates(can_output)
