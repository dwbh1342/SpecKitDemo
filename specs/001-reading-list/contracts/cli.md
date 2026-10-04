# CLI Contract: shelf

Invocation: `python -m shelf <command> [options]` (or `shelf` if installed as a script).
Data file: `$SHELF_FILE` if set, else `~/.shelf.json`.

## Exit codes (Constitution IV)

| Code | Meaning |
|------|---------|
| 0 | Success (including "list is empty" and "already finished") |
| 1 | User error: validation failure, duplicate, not found, unreadable data file |
| 2 | Usage error: unknown command, missing argument (argparse default) |

Errors go to **stderr** as `error: <message>`. Everything else goes to **stdout**.

## `add TITLE AUTHOR` — FR-001..004

| Case | stdout | stderr | exit |
|------|--------|--------|------|
| Success | `Added #1: Dune — Frank Herbert` | | 0 |
| Empty title/author | | `error: title and author are required` | 1 |
| Duplicate | | `error: "Dune" by Frank Herbert is already on your list (#1)` | 1 |

`--json` on success: the created Book object.

## `list [--unread] [--json]` — FR-005, FR-006, FR-010

Text: one line per book, in insertion order:

```text
#1  [finished]  Dune — Frank Herbert
#2  [to-read]   Kindred — Octavia E. Butler
```

Empty: `Your reading list is empty.` (exit 0). `--json`: array of Book objects (`[]` when empty).

## `finish ID [--json]` — FR-007, FR-008

| Case | stdout | stderr | exit |
|------|--------|--------|------|
| Success | `Finished #1: Dune (2026-10-04)` | | 0 |
| Already finished | `#1 was already finished on 2026-10-04` | | 0 |
| Not found | | `error: no book with id 99` | 1 |

`--json`: the Book object after the operation.

## `year [YEAR] [--json]` — FR-009, FR-010

Default `YEAR` is the current calendar year.

```text
Finished in 2026: 3
  2026-02-11  Dune — Frank Herbert
  2026-06-30  Kindred — Octavia E. Butler
  2026-10-04  Piranesi — Susanna Clarke
```

None: `No books finished in 2024.` (exit 0).
`--json`: `{"year": 2026, "count": 3, "books": [Book, ...]}` sorted by `finished_on`.
