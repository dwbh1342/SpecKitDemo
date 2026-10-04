# Implementation Plan: Reading List Tracker

**Branch**: `001-reading-list` | **Date**: 2026-10-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-reading-list/spec.md`

**Plan input**: "Python 3.11 standard library only. Store data in a JSON file. Use argparse subcommands."

## Summary

A single-user terminal tool (`shelf`) that adds books, lists them, marks them finished, and summarizes
a year's finished books. Implemented as a small Python package with an argparse CLI, a pure-logic
service layer, and a JSON file store with atomic writes. See [research.md](./research.md) for the
decisions behind each choice.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: None (standard library: `argparse`, `json`, `dataclasses`, `datetime`, `pathlib`, `tempfile`, `os`)

**Storage**: Single JSON file; default `~/.shelf.json`, overridable with `SHELF_FILE`

**Testing**: `unittest` (stdlib), run with `python -m unittest`

**Target Platform**: macOS, Linux, Windows terminals

**Project Type**: CLI

**Performance Goals**: Any command < 1 s with 1,000 books (SC-002)

**Constraints**: No network; no third-party packages; atomic writes (SC-004)

**Scale/Scope**: One user, up to a few thousand books

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Pre-research | Post-design |
|-----------|------|:---:|:---:|
| I. Spec Before Code | Every module maps to FRs in spec.md | ✅ | ✅ |
| II. Test-First | Each user story has tests written before code (tasks.md orders tests first) | ✅ | ✅ |
| III. Standard Library Only | Zero runtime/test dependencies | ✅ | ✅ |
| IV. Predictable CLI Contract | stdout/stderr split, exit codes 0/1/2, `--json` on data commands | ✅ | ✅ — see [contracts/cli.md](./contracts/cli.md) |
| V. Simplicity | Three modules, no abstraction layers beyond store/service/cli | ✅ | ✅ |

No violations — Complexity Tracking left empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-reading-list/
├── plan.md              # This file
├── research.md          # Phase 0 decisions
├── data-model.md        # Phase 1 entities and file format
├── quickstart.md        # Phase 1 validation guide
├── contracts/
│   └── cli.md           # Phase 1 command contract
├── checklists/
│   └── requirements.md  # From /speckit-specify
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
src/shelf/
├── __init__.py
├── __main__.py      # enables `python -m shelf`
├── models.py        # Book dataclass, status constants
├── store.py         # load/save JSON with atomic replace
├── service.py       # add, list, finish, year_summary (pure logic, no I/O)
└── cli.py           # argparse subcommands, output formatting, exit codes

tests/
├── test_store.py
├── test_service.py
└── test_cli.py      # end-to-end via subprocess against a temp SHELF_FILE
```

**Structure Decision**: Single project with a `src/` layout. The service layer has no file or
terminal I/O, so acceptance scenarios can be tested directly and the CLI stays a thin adapter.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
