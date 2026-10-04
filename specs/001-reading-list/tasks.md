---
description: "Task list for Reading List Tracker"
---

# Tasks: Reading List Tracker

**Input**: Design documents from `/specs/001-reading-list/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md

**Tests**: Included — required by Constitution II (Test-First) and SC-003.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create package skeleton `src/shelf/__init__.py` and `src/shelf/__main__.py` per plan.md structure
- [x] T002 [P] Create `tests/__init__.py` and a test helper that points `SHELF_FILE` at a temp directory in `tests/helpers.py`
- [x] T003 [P] Add Python entries (`__pycache__/`, `*.pyc`, `.shelf.json`) to `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create `Book` dataclass and status constants in `src/shelf/models.py` per data-model.md
- [x] T005 Write store tests (missing file → empty list, round-trip, corrupted file raises and is left untouched) in `tests/test_store.py` — confirm they FAIL
- [x] T006 Implement `load()` / `save()` with atomic `os.replace` and `StoreError` in `src/shelf/store.py` (research R1, R3, R4; FR-011, FR-012)
- [x] T007 Create argparse entry point with `add`/`list`/`finish`/`year` subparsers stubbed and the stderr/exit-code helper in `src/shelf/cli.py` (contracts/cli.md exit codes)

**Checkpoint**: Foundation ready — user story work can begin

---

## Phase 3: User Story 1 - Add and list books (Priority: P1) 🎯 MVP

**Goal**: Reader can add books and see their list.

**Independent Test**: Add two books, list them, confirm IDs/titles/authors/status.

### Tests for User Story 1 ⚠️ write first, confirm they FAIL

- [x] T008 [P] [US1] Service tests for US1/AC1–AC4 and FR-003 (empty title/author) in `tests/test_service.py`
- [x] T009 [P] [US1] CLI tests for `add` and `list` text output, `--json`, and exit codes in `tests/test_cli.py`

### Implementation for User Story 1

- [x] T010 [US1] Implement `add_book()` with trimming, validation, case-insensitive duplicate check, and `next_id` in `src/shelf/service.py` (FR-001–FR-004)
- [x] T011 [US1] Implement `list_books()` preserving insertion order in `src/shelf/service.py` (FR-005)
- [x] T012 [US1] Wire `add` and `list` subcommands with text and `--json` output in `src/shelf/cli.py` (FR-010)

**Checkpoint**: US1 fully functional — this is the MVP

---

## Phase 4: User Story 2 - Mark a book as finished (Priority: P2)

**Goal**: Reader can mark books finished and filter to unread.

**Independent Test**: Add a book, finish it, list it, confirm status and date.

### Tests for User Story 2 ⚠️ write first, confirm they FAIL

- [x] T013 [P] [US2] Service tests for US2/AC1–AC4 in `tests/test_service.py`
- [x] T014 [P] [US2] CLI tests for `finish` and `list --unread` in `tests/test_cli.py`

### Implementation for User Story 2

- [x] T015 [US2] Implement `finish_book(book_id, today)` that never overwrites `finished_on` in `src/shelf/service.py` (FR-007, FR-008)
- [x] T016 [US2] Add `unread_only` filter to `list_books()` in `src/shelf/service.py` (FR-006)
- [x] T017 [US2] Wire `finish` subcommand and `list --unread` in `src/shelf/cli.py`

**Checkpoint**: US1 and US2 both work independently

---

## Phase 5: User Story 3 - Year in review (Priority: P3)

**Goal**: Reader sees books finished in a year with a count.

**Independent Test**: Seed books finished in two years; request one year; confirm list and count.

### Tests for User Story 3 ⚠️ write first, confirm they FAIL

- [x] T018 [P] [US3] Service tests for US3/AC1–AC3 in `tests/test_service.py`
- [x] T019 [P] [US3] CLI tests for `year`, default year, and `--json` in `tests/test_cli.py`

### Implementation for User Story 3

- [x] T020 [US3] Implement `year_summary(year)` sorted by `finished_on` in `src/shelf/service.py` (FR-009)
- [x] T021 [US3] Wire `year [YEAR]` subcommand defaulting to the current year in `src/shelf/cli.py`

**Checkpoint**: All user stories independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T022 [P] Add performance test: every command under 1 s with 1,000 books in `tests/test_perf.py` (SC-002)
- [x] T023 [P] Document install/usage in `README.md`
- [x] T024 Run every scenario in `specs/001-reading-list/quickstart.md` and the full `python -m unittest` suite

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2)** → **User Stories (Phases 3–5)** → **Polish (Phase 6)**
- User stories run in priority order (P1 → P2 → P3) for a solo developer, or in parallel once Phase 2 is done.

### User Story Dependencies

- **US1**: depends only on Phase 2.
- **US2**: depends on Phase 2; its tests create books through the service, not through US1's CLI.
- **US3**: depends on Phase 2; its tests seed finished books directly.

### Within Each User Story

- Tests first and failing → service → CLI wiring.
- `service.py` and `cli.py` tasks within a story are sequential (same file).

### Parallel Opportunities

- T002, T003, T004 in parallel.
- Each story's two test tasks in parallel (different files).

## Parallel Example: User Story 1

```text
Task: "T008 Service tests for US1 in tests/test_service.py"
Task: "T009 CLI tests for add/list in tests/test_cli.py"
```

## Implementation Strategy

### MVP First

1. Phases 1–2 → 2. Phase 3 (US1) → 3. **STOP and validate** with quickstart Scenario 1.

### Incremental Delivery

Add US2, validate; add US3, validate; then Polish.

## Notes

- Commit after each phase checkpoint.
- Every task cites the requirement it serves so `/speckit-analyze` and `/speckit-converge` can trace it.

---

## Phase 7: Convergence

- [ ] T025 Raise `StoreError` (exit 1, file untouched) when the data file is valid JSON but not the expected shape, and add a test for it in `tests/test_store.py` per FR-012 (partial)
- [ ] T026 Add `--json` to `add` returning the created Book, and a CLI test for it in `tests/test_cli.py` per FR-010 (partial)
