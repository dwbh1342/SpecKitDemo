# Research: Reading List Tracker

Phase 0 output of `/speckit-plan`. Each entry resolves an open technical question from plan.md.

## R1. Storage format

- **Decision**: One JSON file with a top-level object `{ "next_id": int, "books": [...] }`.
- **Rationale**: Human-readable (constitution: Data stays local), stdlib `json`, trivially fast at 1,000 books.
- **Alternatives considered**: SQLite (stdlib, but opaque to readers and more than needed — Principle V); CSV (no clean place for `next_id`, awkward optional fields).

## R2. Never-reused identifiers (FR-002)

- **Decision**: Persist a `next_id` counter rather than computing `max(id) + 1`.
- **Rationale**: `max + 1` would reuse an ID after a future delete feature removes the highest book.
- **Alternatives considered**: UUIDs (unique but unfriendly to type at a terminal).

## R3. Atomic writes (FR-012, SC-004)

- **Decision**: Write to a temp file in the same directory, `flush` + `os.fsync`, then `os.replace` onto the target.
- **Rationale**: `os.replace` is atomic on POSIX and Windows when source and target are on the same filesystem.
- **Alternatives considered**: Writing in place (can leave a truncated file); backup-then-write (two files to reason about).

## R4. Corrupted data file (FR-012)

- **Decision**: On `JSONDecodeError` or wrong shape, raise `StoreError`; CLI prints to stderr and exits 1. No write occurs.
- **Rationale**: Never destroy data the user may be able to recover by hand.

## R5. CLI framework

- **Decision**: `argparse` with subcommands `add`, `list`, `finish`, `year`.
- **Rationale**: Stdlib (Principle III); built-in `--help` supports SC-001; usage errors exit 2 automatically, matching Principle IV.
- **Alternatives considered**: click/typer (third-party, rejected by Principle III).

## R6. "Today" in tests

- **Decision**: Service functions accept a `today: date` parameter; the CLI passes `date.today()`. CLI tests can override via `SHELF_TODAY=YYYY-MM-DD`.
- **Rationale**: Makes FR-007/FR-009 deterministic in tests without mocking.
