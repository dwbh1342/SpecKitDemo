# Data Model: Reading List Tracker

## Book

| Field | Type | Rules | Source |
|-------|------|-------|--------|
| `id` | int ≥ 1 | Assigned from `ReadingList.next_id`; never reused | FR-002 |
| `title` | str | Trimmed; non-empty | FR-001, FR-003 |
| `author` | str | Trimmed; non-empty | FR-001, FR-003 |
| `status` | `"to-read"` \| `"finished"` | Starts `to-read` | FR-005, FR-007 |
| `added_on` | ISO date `YYYY-MM-DD` | Set on add | Key Entities |
| `finished_on` | ISO date or `null` | Set once when finished; never changed after | FR-007, FR-008 |

**Uniqueness**: (`title.casefold()`, `author.casefold()`) after trimming must be unique (FR-004).

### State transitions

```text
to-read ──finish──▶ finished
finished ──finish──▶ finished   (no-op; finished_on unchanged, user told "already finished")
```

## ReadingList (file root)

| Field | Type | Rules |
|-------|------|-------|
| `next_id` | int ≥ 1 | Incremented on every successful add |
| `books` | list[Book] | Kept in insertion order (FR-005) |

### Example file

```json
{
  "next_id": 3,
  "books": [
    {"id": 1, "title": "Dune", "author": "Frank Herbert", "status": "finished",
     "added_on": "2026-10-01", "finished_on": "2026-10-04"},
    {"id": 2, "title": "Kindred", "author": "Octavia E. Butler", "status": "to-read",
     "added_on": "2026-10-02", "finished_on": null}
  ]
}
```

A missing file is equivalent to `{"next_id": 1, "books": []}`.
