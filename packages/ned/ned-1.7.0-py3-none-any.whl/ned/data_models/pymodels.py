from __future__ import annotations
from copy import deepcopy

from dataclasses import dataclass
from typing import Any, cast
from typing_extensions import Self

from sm.inputs.table import ColumnBasedTable
from sm.inputs.link import WIKIDATA_NIL_ENTITY
from sm.misc.matrix import Matrix
from sm.outputs.semantic_model import SemanticModel
from kgdata.wikidata.models.multilingual import MultiLingualStringList


ALIAS_SEP_TOKEN = "\n"
ESCAPE_ALIAS_SEP_TOKEN = "\\-n"
NIL_ENTITY = str(WIKIDATA_NIL_ENTITY)  # Q0 -- NIL entity, does not exist in Wikidata
assert NIL_ENTITY == "Q0"
NO_ENTITY = "Q-1"  # no entity, used for cells that are not entities such as numbers


@dataclass
class Entity:
    id: str
    # information of the entity itself embedded so that
    # we do not need to query the entity database again
    label: str | None = None
    description: str | None = None
    aliases: str | None = None
    popularity: float | None = None

    def to_tuple(self):
        return (
            self.id,
            self.label,
            self.description,
            self.aliases,
            self.popularity,
        )

    @staticmethod
    def from_tuple(t):
        return Entity(*t)

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "aliases": self.aliases,
            "popularity": self.popularity,
        }

    @staticmethod
    def from_dict(d):
        return Entity(**d)

    @staticmethod
    def encode_aliases(aliases: MultiLingualStringList):
        values = aliases.lang2values[aliases.lang]
        assert all(ESCAPE_ALIAS_SEP_TOKEN not in v for v in values), values
        return ALIAS_SEP_TOKEN.join(
            value.replace(ALIAS_SEP_TOKEN, ESCAPE_ALIAS_SEP_TOKEN) for value in values
        )

    @staticmethod
    def decode_aliases(aliases: str) -> list:
        return [
            v.replace(ESCAPE_ALIAS_SEP_TOKEN, ALIAS_SEP_TOKEN)
            for v in aliases.split(ALIAS_SEP_TOKEN)
        ]

    @staticmethod
    def full_encode_aliases(aliases: MultiLingualStringList):
        main_lang = ""
        other_langs = {}
        for lang, values in aliases.lang2values.items():
            assert all(ESCAPE_ALIAS_SEP_TOKEN not in v for v in values)
            newvalues = ALIAS_SEP_TOKEN.join(
                value.replace(ALIAS_SEP_TOKEN, ESCAPE_ALIAS_SEP_TOKEN)
                for value in values
            )
            if lang == aliases.lang:
                main_lang = f"{lang}:{newvalues}"
            else:
                other_langs[lang] = f"{lang}:{newvalues}"

        out = [main_lang]
        out.extend(other_langs.values())
        return (ALIAS_SEP_TOKEN + ALIAS_SEP_TOKEN).join(out)

    @staticmethod
    def full_decode_aliases(aliases: str) -> MultiLingualStringList:
        lst = aliases.split(ALIAS_SEP_TOKEN + ALIAS_SEP_TOKEN)
        lang2values = []
        for item in lst:
            lang, values = item.split(":", 1)
            values = [
                v.replace(ESCAPE_ALIAS_SEP_TOKEN, ALIAS_SEP_TOKEN)
                for v in values.split(ALIAS_SEP_TOKEN)
            ]
            lang2values.append((lang, values))

        if len(lang2values) == 0:
            return MultiLingualStringList({}, "en")
        return MultiLingualStringList(dict(lang2values), lang2values[0][0])


@dataclass
class CandidateEntity:
    entity: Entity
    # score of the candidate entity
    score: float
    # method to retrieve the candidate entity
    provenance: str = ""

    def to_dict(self):
        return {
            "entity": self.entity.to_tuple(),
            "score": self.score,
            "provenance": self.provenance,
        }

    @classmethod
    def from_dict(cls, d: dict):
        d["entity"] = Entity.from_tuple(d["entity"])
        return cls(**d)


@dataclass
class CellLink:
    # if the cell is not linked any entity, self is None
    # if the cell does linked to an entity, but the list is empty, it means
    # the cell is linked to NIL.
    entities: list[Entity]
    # mapping from entity id to the range (exclusive)
    mentions: dict[str, tuple[int, int]]
    # candidates: list[CandidateEntity]

    def to_dict(self):
        return {
            "mentions": [(k, v[0], v[1]) for k, v in self.mentions.items()],
            "entities": [e.to_tuple() for e in self.entities],
            # "candidates": [c.to_dict() for c in self.candidates],
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            [Entity.from_tuple(e) for e in d["entities"]],
            {k: (s, e) for k, s, e in d["mentions"]},
            # [CandidateEntity.from_dict(c) for c in d["candidates"]],
        )


@dataclass
class NEDExample:
    table: ColumnBasedTable
    # list of columns that are entity columns (size != #columns)
    entity_columns: list[int]
    # list of types of entity columns, corresponding with entity_columns (size != #columns)
    entity_column_types: list[list[Entity]]
    # (row, col) -> cell link (can have more than one entity)
    cell_links: Matrix[CellLink | None]

    def to_dict(self):
        return {
            "table": self.table.to_dict(),
            "entity_columns": self.entity_columns,
            "entity_column_types": [
                [e.to_dict() for e in ents] for ents in self.entity_column_types
            ],
            "cell_links": [
                [l.to_dict() if l is not None else None for l in row]
                for row in self.cell_links.data
            ],
        }

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        obj["table"] = ColumnBasedTable.from_dict(obj["table"])
        obj["entity_column_types"] = [
            [Entity.from_dict(e) for e in ents] for ents in obj["entity_column_types"]
        ]
        obj["cell_links"] = Matrix(
            [
                [CellLink.from_dict(l) if l is not None else None for l in row]
                for row in obj["cell_links"]
            ]
        )
        return cls(**obj)

    def keep_columns(self, columns: list[int]):
        """Keep only the entities in the given columns. This allow us to evaluate/predict a subset of the columns."""
        entity_columns = []
        entity_column_types = []

        set_columns = set(columns)
        for ec in self.entity_columns:
            if ec in set_columns:
                entity_columns.append(ec)
        entity_columns = [ec for ec in self.entity_columns if ec in set_columns]
        entity_column_types = [
            ect if ec in set_columns else []
            for ec, ect in enumerate(self.entity_column_types)
        ]

        cell_links = self.cell_links.shallow_copy()
        for row in cell_links.data:
            for ci in range(len(row)):
                if ci not in set_columns:
                    row[ci] = None

        return NEDExample(self.table, entity_columns, entity_column_types, cell_links)
