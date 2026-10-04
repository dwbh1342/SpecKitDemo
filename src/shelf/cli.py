"""Command-line adapter. Contract: specs/001-reading-list/contracts/cli.md."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date

from shelf import service, store


def _today() -> date:
    override = os.environ.get("SHELF_TODAY")  # research R6: deterministic tests
    return date.fromisoformat(override) if override else date.today()


def _print_json(data) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _line(book) -> str:
    return f"#{book.id:<3} [{book.status}]{' ' * (9 - len(book.status))}{book.title} — {book.author}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shelf", description="Track books you want to read.")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add a book to your list")
    a.add_argument("title")
    a.add_argument("author")

    ls = sub.add_parser("list", help="show your reading list")
    ls.add_argument("--unread", action="store_true", help="only books not yet finished")
    ls.add_argument("--json", action="store_true")

    f = sub.add_parser("finish", help="mark a book as finished")
    f.add_argument("id", type=int)
    f.add_argument("--json", action="store_true")

    y = sub.add_parser("year", help="books finished in a year (default: this year)")
    y.add_argument("year", type=int, nargs="?")
    y.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)  # usage errors exit 2 (Constitution IV)
    today = _today()
    try:
        rl = store.load()

        if args.command == "add":
            book = service.add_book(rl, args.title, args.author, today)
            store.save(rl)
            print(f"Added #{book.id}: {book.title} — {book.author}")

        elif args.command == "list":
            books = service.list_books(rl, unread_only=args.unread)
            if args.json:
                _print_json([b.to_dict() for b in books])
            elif not books:
                print("Your reading list is empty.")
            else:
                for b in books:
                    print(_line(b))

        elif args.command == "finish":
            result = service.finish_book(rl, args.id, today)
            if not result.already_finished:
                store.save(rl)
            b = result.book
            if args.json:
                _print_json(b.to_dict())
            elif result.already_finished:
                print(f"#{b.id} was already finished on {b.finished_on}")
            else:
                print(f"Finished #{b.id}: {b.title} ({b.finished_on})")

        elif args.command == "year":
            year = args.year or today.year
            books = service.year_summary(rl, year)
            if args.json:
                _print_json({"year": year, "count": len(books), "books": [b.to_dict() for b in books]})
            elif not books:
                print(f"No books finished in {year}.")
            else:
                print(f"Finished in {year}: {len(books)}")
                for b in books:
                    print(f"  {b.finished_on}  {b.title} — {b.author}")

    except (service.ShelfError, store.StoreError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
