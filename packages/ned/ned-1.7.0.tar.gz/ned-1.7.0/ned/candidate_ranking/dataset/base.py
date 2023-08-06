from __future__ import annotations

import numpy as np
from nptyping import Int32, NDArray, Object, Shape, Bool
from ream.data_model_helper import NumpyDataModel
from tqdm import tqdm

from ned.data_models.prelude import DatasetCandidateEntities, DatasetIndex
from ned.data_models.pymodels import NEDExample


class CRDatasetEnt(NumpyDataModel):
    # fmt: off
    __slots__ = [
        "index", "cell", "cell_id", 
        "table_index", "col_index", "row_index", 
        "entity_id", "entity_label", "entity_description", 
        "entity_aliases", "entity_popularity"
    ]
    # fmt: on
    # mapping from table_id => col_index => row_index => (start, end)
    index: dict[str, dict[int, dict[int, tuple[int, int]]]]
    cell: NDArray[Shape["*"], Object]  # content of the cell
    # unique number for each cell across all tables
    cell_id: NDArray[Shape["*"], Int32]
    table_index: NDArray[Shape["*"], Int32]  # table index of the cell
    col_index: NDArray[Shape["*"], Int32]  # column index of the cell
    row_index: NDArray[Shape["*"], Int32]  # row index of the cell
    entity_id: NDArray[Shape["*"], Object]
    entity_label: NDArray[Shape["*"], Object]
    entity_description: NDArray[Shape["*"], Object]
    entity_aliases: NDArray[Shape["*"], Object]
    entity_popularity: NDArray[Shape["*"], Object]

    @staticmethod
    def create(examples: list[NEDExample], candidates: DatasetCandidateEntities):
        index = {}
        cell = []
        cell_id = []
        table_index = []
        col_index = []
        row_index = []
        entity_id = []
        entity_label = []
        entity_description = []
        entity_aliases = []
        entity_popularity = []

        cell_index_offset = 0

        for ti, example in tqdm(enumerate(examples), desc="make base ent"):
            tid = example.table.table_id
            tindex = candidates.index[tid][-1]
            index[tid] = {}
            nrows, ncols = example.table.shape()
            for ci in tindex:
                cindex = tindex[ci][-1]
                index[tid][ci] = {}
                for ri in cindex:
                    cell_index = cell_index_offset + ri * ncols + ci
                    rowstart = len(cell)
                    link = example.cell_links[ri, ci]
                    text = example.table[ri, ci]
                    if link is not None:
                        for ent in link.entities:
                            cell.append(text)
                            cell_id.append(cell_index)
                            table_index.append(ti)
                            col_index.append(ci)
                            row_index.append(ri)
                            entity_id.append(ent.id)
                            entity_label.append(ent.label)
                            entity_description.append(ent.description)
                            entity_aliases.append(ent.aliases)
                            entity_popularity.append(ent.popularity)
                    index[tid][ci][ri] = (rowstart, len(cell))
            cell_index_offset += nrows * ncols

        return CRDatasetEnt(
            index=index,
            cell=np.asarray(cell, dtype=np.object_),
            cell_id=np.asarray(cell_id, dtype=np.int32),
            table_index=np.asarray(table_index, dtype=np.int32),
            col_index=np.asarray(col_index, dtype=np.int32),
            row_index=np.asarray(row_index, dtype=np.int32),
            entity_id=np.asarray(entity_id, dtype=np.object_),
            entity_label=np.asarray(entity_label, dtype=np.object_),
            entity_description=np.asarray(entity_description, dtype=np.object_),
            entity_aliases=np.asarray(entity_aliases, dtype=np.object_),
            entity_popularity=np.array(entity_popularity, dtype=np.float64),
        )


class CRDatasetCan(NumpyDataModel):
    # fmt: off
    __slots__ = [
        "cell", "cell_id", "table_index", "col_index", "is_correct"
    ]
    # fmt: on
    # the order of this object and candidates are the same
    cell: NDArray[Shape["*"], Object]  # content of the cell
    cell_id: NDArray[Shape["*"], Int32]  # unique number for each cell across all tables
    table_index: NDArray[Shape["*"], Int32]
    col_index: NDArray[Shape["*"], Int32]
    is_correct: NDArray[Shape["*"], Bool]  # whether the cell is correct

    @staticmethod
    def create(examples: list[NEDExample], candidates: DatasetCandidateEntities):
        cell = []
        cell_id = np.zeros_like(candidates.id, dtype=np.int32)
        table_index = np.zeros_like(candidates.id, dtype=np.int32)
        col_index = np.zeros_like(candidates.id, dtype=np.int32)
        is_correct = np.zeros_like(candidates.id, dtype=np.bool_)

        cell_index_offset = 0
        # using a pointer to make sure that the order of this object and candidates are the same
        pointer = 0

        for ti, example in tqdm(enumerate(examples), desc="make base can"):
            tid = example.table.table_id
            tindex = candidates.index[tid][-1]
            nrows, ncols = example.table.shape()
            for ci in tindex:
                cindex = tindex[ci][-1]
                for ri, (rstart, rend) in cindex.items():
                    if rstart != pointer:
                        # as long as candidates.index maintaining the order, this should not happen
                        raise ValueError(
                            "The order of candidates and examples are not the same"
                        )
                    # the order is matched, move the pointer forward
                    pointer = rend
                    cell_index = cell_index_offset + ri * ncols + ci
                    cans = candidates.get_cell_candidates(tid, ri, ci)
                    cell_id[rstart:rend] = cell_index
                    table_index[rstart:rend] = ti
                    col_index[rstart:rend] = ci
                    cell.extend([example.table[ri, ci]] * len(cans))

                    link = example.cell_links[ri, ci]
                    if link is None or len(link.entities) == 0:
                        is_correct[rstart:rend] = False
                    else:
                        gold_entities_id = np.asarray([ent.id for ent in link.entities])
                        is_correct[rstart:rend] = np.isin(
                            candidates.id[rstart:rend], gold_entities_id
                        )

            cell_index_offset += nrows * ncols

        return CRDatasetCan(
            cell=np.asarray(cell, dtype=np.object_),
            cell_id=cell_id,
            table_index=table_index,
            col_index=col_index,
            is_correct=is_correct,
        )


CRDatasetEnt.init()
CRDatasetCan.init()
