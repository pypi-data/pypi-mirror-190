from typing import Any, Literal, Callable
from dataclasses import dataclass

import orjson


@dataclass
class LuceneDocument:
    """Represent a document about an entity stored in Lucene."""

    id: str
    label: str
    aliases: str
    description: str
    popularity: float

    def pretokenize(self, analyzer: Callable[[str], str]):
        self.label = analyzer(self.label)
        self.aliases = analyzer(self.aliases)
        self.description = analyzer(self.description)
        return self

    def set(
        self,
        field: Literal["id", "label", "aliases", "description", "popularity"],
        value: Any,
    ):
        self.__dict__[field] = value
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "contents": self.label,
            "aliases": self.aliases,
            "description": self.description,
            "popularity": self.popularity,
        }

    def to_json(self):
        return orjson.dumps(self.to_dict())

    @staticmethod
    def from_dict(d):
        return LuceneDocument(
            d["id"],
            d["contents"],
            d["aliases"],
            d["description"],
            d["popularity"],
        )
