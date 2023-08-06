import json
from dataclasses import dataclass, field
from typing import List, Literal, Optional

import numpy as np
from loguru import logger as glogger
from osin.apis.remote_exp import RemoteExpRun
from osin.types import OTable
from osin.types.primitive_type import NestedPrimitiveOutput
from tqdm import tqdm

import ned.metrics as ned_metrics
from ned.data_models.prelude import (
    DatasetCandidateEntities,
    NEDExample,
    NO_ENTITY,
    NIL_ENTITY,
    CellCandidateEntities,
)


@dataclass
class EvalArgs:
    dsqueries: List[str] = field(
        metadata={"help": "List of dataset queries to evaluate"}
    )
    exprun_type: Literal["cell", "table"] = field(
        default="table",
        metadata={
            "help": "If cell, then each example in Osin is a cell, if table, then each example is a table."
        },
    )
    eval_ignore_nil: bool = field(
        default=True,
        metadata={"help": "If True, ignore NIL entity when evaluating entity linking."},
    )
    eval_ignore_non_entity_cell: bool = field(
        default=True,
        metadata={
            "help": "If True, ignore non-entity cell when evaluating entity linking."
        },
    )


def evaluate(
    examples: List[NEDExample],
    entity_columns: List[List[int]],
    candidates: DatasetCandidateEntities,
    eval_ignore_nil: bool = True,
    eval_ignore_non_entity_cell: bool = True,
    dsname: str = "",
    logger=None,
    exprun: Optional[RemoteExpRun] = None,
    verbose: bool = True,
    report_unique: bool = True,
    exprun_type: Literal["cell", "table"] = "cell",
):
    logger = logger or glogger
    ytrue = []
    ypreds = []
    queries = {}
    top_ks = [1, 5, 20, 100, 1000]

    for ei, example in tqdm(
        enumerate(examples),
        disable=not verbose,
        desc="evaluating" + (" " + dsname if dsname != "" else ""),
    ):
        eytrue = []
        eypreds = []
        otbl = []

        nrows, ncols = example.cell_links.shape()
        pred_entity_columns = set(entity_columns[ei])

        for ci in pred_entity_columns.union(example.entity_columns):
            if ci not in example.entity_columns or ci not in pred_entity_columns:
                continue

            for ri in range(nrows):
                link = example.cell_links[ri, ci]

                if eval_ignore_non_entity_cell and link is None:
                    # link is None, the cell is not linked to any entity
                    continue

                if eval_ignore_nil and link is not None and len(link.entities) == 0:
                    # the cell is linked to NIL entity
                    continue

                if link is None:
                    gold_entities = {NO_ENTITY}
                elif len(link.entities) == 0:
                    gold_entities = {NIL_ENTITY}
                else:
                    gold_entities = {ent.id for ent in link.entities}

                query = str(example.table[ri, ci])
                if candidates.has_cell_candidates(example.table.table_id, ri, ci):
                    cans = candidates.get_cell_candidates(
                        example.table.table_id, ri, ci
                    )
                else:
                    cans = CellCandidateEntities.empty()

                # sort by negative score for stable descending order ([::-1] won't work correctly)
                sortedindex = np.argsort(-cans.score, kind="stable")
                can_ids = cans.id[sortedindex]

                assert len(gold_entities) > 0, "Does not handle NIL yet"
                eytrue.append(gold_entities)
                eypreds.append(can_ids)

                is_new = query not in queries
                if query not in queries:
                    queries[query] = [
                        {
                            "entities": gold_entities,
                            "candidate_ids": can_ids,
                        }
                    ]
                elif all(res["entities"] != gold_entities for res in queries[query]):
                    # same query but mapped to different entities, it is a new example
                    queries[query].append(
                        {
                            "entities": gold_entities,
                            "candidate_ids": can_ids,
                        }
                    )
                    is_new = True

                if exprun is not None:
                    if is_new and exprun_type == "cell":
                        otbl = []
                        max_rank = max(10000, len(cans) + 100)
                        rank = max_rank
                        for i, idx in enumerate(sortedindex):
                            can_id = cans.id[idx]
                            otbl.append(
                                {
                                    "id": can_id,
                                    "table": example.table.table_id,
                                    "row": ri,
                                    "label": str(cans.label[idx]),
                                    "score": float(cans.score[idx]),
                                    "found": can_id in gold_entities,
                                }
                            )
                            if can_id in gold_entities:
                                rank = i + 1
                        exprun.update_example_output(
                            example_id=query.replace("/", "-slash-")
                            if query != ""
                            else "<empty>",
                            example_name=query,
                            primitive={
                                "id": " | ".join(gold_entities),
                                "found": rank < max_rank,
                                "rank": rank,
                            },
                            complex={"candidates": OTable(otbl)},
                        )
                    elif exprun_type == "table":
                        max_rank = max(10000, len(cans) + 100)
                        otbl.append(
                            {
                                "row": ri,
                                "col": ci,
                                "cell": query,
                                "gold": " | ".join(gold_entities),
                                "rank": int(t[0]) + 1
                                if len(
                                    t := [
                                        i
                                        for i, idx in enumerate(sortedindex)
                                        if cans.id[idx] in gold_entities
                                    ]
                                )
                                > 0
                                else max_rank,
                            }
                        )

        ytrue.extend(eytrue)
        ypreds.extend(eypreds)

        if exprun_type == "table" and exprun is not None:
            # each example is a table
            exprun.update_example_output(
                example_id=str(ei),
                example_name=example.table.table_id,
                primitive={
                    "total": len(eytrue),
                    "mrr": ned_metrics.mrr(eytrue, eypreds),
                    "recall": ned_metrics.recall(eytrue, eypreds, top_ks),
                },  # type: ignore
                complex={
                    "candidates": OTable(otbl),
                    "columns": OTable(
                        [
                            {
                                "column": example.table.columns[ci].clean_name or "",
                                "column_index": ci,
                                "type_id": ctype.id,
                                "type_name": ctype.label,
                            }
                            for ci, ctypes in zip(
                                example.entity_columns, example.entity_column_types
                            )
                            for ctype in ctypes
                        ]
                    ),
                },  # type: ignore
            )
            otbl = []

    # sort the candidates by their score (bigger is better)
    recall = ned_metrics.recall(ytrue, ypreds, k=top_ks)
    mrr = ned_metrics.mrr(ytrue, ypreds)
    logger.info(
        "total = {} | mrr = {:.5f} | metrics: {}",
        len(ytrue),
        mrr,
        json.dumps(recall, indent=4),
    )

    if report_unique:
        unique_ytrue = []
        unique_ypreds = []
        for res in queries.values():
            for obj in res:
                unique_ytrue.append(obj["entities"])
                unique_ypreds.append(obj["candidate_ids"])

        unique_recall = ned_metrics.recall(unique_ytrue, unique_ypreds, k=top_ks)
        unique_mrr = ned_metrics.mrr(unique_ytrue, unique_ypreds)
        logger.info(
            "unique total = {} | unique mrr = {:.5f} | unique metrics: {}",
            len(unique_ytrue),
            unique_mrr,
            json.dumps(unique_recall, indent=4),
        )

    if exprun is not None:
        primitive = {
            "total": len(ytrue),
            "mrr": mrr,
            "recall": recall,
        }
        if report_unique:
            primitive.update(
                {
                    "unique_total": len(unique_ytrue),  # type: ignore
                    "unique_mrr": unique_mrr,  # type: ignore
                    "unique_recall": unique_recall,  # type: ignore
                }
            )
        exprun.update_output(
            primitive=primitive,
        )

    return {"recall": recall, "mrr": mrr, "total": len(ytrue)}
