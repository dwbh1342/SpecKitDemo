# Quickstart Validation: Reading List Tracker

Proves the feature works end to end. Details of commands and output live in
[contracts/cli.md](./contracts/cli.md); data shape in [data-model.md](./data-model.md).

## Prerequisites

- Python 3.11+
- From the repository root, use a throwaway data file:

```bash
export SHELF_FILE="$(mktemp -d)/shelf.json"
export PYTHONPATH=src
```

## Scenario 1 — Add and list (US1)

```bash
python -m shelf list                          # → "Your reading list is empty."
python -m shelf add "Dune" "Frank Herbert"    # → "Added #1: ..."
python -m shelf add "dune" "frank herbert"    # → error, exit 1 (duplicate)
python -m shelf list                          # → #1 [to-read] Dune — Frank Herbert
```

## Scenario 2 — Finish (US2)

```bash
python -m shelf finish 1                      # → "Finished #1: Dune (<today>)"
python -m shelf finish 1                      # → "already finished", same date
python -m shelf finish 99; echo $?            # → error ... 1
python -m shelf list --unread                 # → Dune not shown
```

## Scenario 3 — Year in review (US3)

```bash
python -m shelf year                          # → "Finished in <this year>: 1"
python -m shelf year 2024                     # → "No books finished in 2024."
python -m shelf year --json
```

## Automated suite

```bash
python -m unittest discover -s tests -v       # all acceptance scenarios (SC-003)
```
