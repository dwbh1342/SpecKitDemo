# Shelf

A tiny command-line reading-list tracker. It exists to demonstrate **GitHub Spec Kit** —
see [SANDBOX-GUIDE.md](./SANDBOX-GUIDE.md) for the walkthrough.

```bash
export PYTHONPATH=src
python -m shelf add "Dune" "Frank Herbert"
python -m shelf list
python -m shelf finish 1
python -m shelf year
python -m unittest -v
```

Requires Python 3.11+. No dependencies. Data lives in `~/.shelf.json` (override with `SHELF_FILE`).
