"""Entities from specs/001-reading-list/data-model.md."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

TO_READ = "to-read"
FINISHED = "finished"


@dataclass
class Book:
    id: int
    title: str
    author: str
    added_on: str
    status: str = TO_READ
    finished_on: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(**data)


@dataclass
class ReadingList:
    next_id: int = 1
    books: list[Book] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"next_id": self.next_id, "books": [b.to_dict() for b in self.books]}
