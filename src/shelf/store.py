"""JSON file persistence with atomic writes (research R1, R3, R4)."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from shelf.models import Book, ReadingList


class StoreError(Exception):
    """The data file exists but cannot be used. It is never overwritten."""


def data_path() -> Path:
    return Path(os.environ.get("SHELF_FILE", Path.home() / ".shelf.json"))


def load(path: Path | None = None) -> ReadingList:
    path = path or data_path()
    if not path.exists():
        return ReadingList()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StoreError(f"cannot read {path}: {exc}") from exc
    return ReadingList(
        next_id=raw["next_id"],
        books=[Book.from_dict(b) for b in raw["books"]],
    )


def save(reading_list: ReadingList, path: Path | None = None) -> None:
    path = path or data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".shelf-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(reading_list.to_dict(), fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
