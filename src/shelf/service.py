"""Pure reading-list logic. No file or terminal I/O (plan: Structure Decision)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from shelf.models import FINISHED, TO_READ, Book, ReadingList


class ShelfError(Exception):
    """A user error: maps to exit code 1."""


@dataclass
class FinishResult:
    book: Book
    already_finished: bool


def _key(title: str, author: str) -> tuple[str, str]:
    return (title.casefold(), author.casefold())


def add_book(rl: ReadingList, title: str, author: str, today: date) -> Book:
    """FR-001..FR-004."""
    title, author = title.strip(), author.strip()
    if not title or not author:
        raise ShelfError("title and author are required")
    for existing in rl.books:
        if _key(existing.title, existing.author) == _key(title, author):
            raise ShelfError(
                f'"{existing.title}" by {existing.author} is already on your list (#{existing.id})'
            )
    book = Book(id=rl.next_id, title=title, author=author, added_on=today.isoformat())
    rl.books.append(book)
    rl.next_id += 1
    return book


def list_books(rl: ReadingList, unread_only: bool = False) -> list[Book]:
    """FR-005, FR-006."""
    if unread_only:
        return [b for b in rl.books if b.status == TO_READ]
    return list(rl.books)


def finish_book(rl: ReadingList, book_id: int, today: date) -> FinishResult:
    """FR-007, FR-008."""
    for book in rl.books:
        if book.id == book_id:
            if book.status == FINISHED:
                return FinishResult(book, already_finished=True)
            book.status = FINISHED
            book.finished_on = today.isoformat()
            return FinishResult(book, already_finished=False)
    raise ShelfError(f"no book with id {book_id}")


def year_summary(rl: ReadingList, year: int) -> list[Book]:
    """FR-009."""
    prefix = f"{year:04d}-"
    done = [b for b in rl.books if b.status == FINISHED and (b.finished_on or "").startswith(prefix)]
    return sorted(done, key=lambda b: b.finished_on)
