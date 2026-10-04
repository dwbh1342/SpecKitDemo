# Spec Kit Sandbox Guide

This repo is a fresh `specify init` (Spec Kit **v1.0.13**, Claude Code integration, `git` extension)
plus one fully worked feature — **001-reading-list**, a small Python CLI called `shelf` — so you can
see every artifact filled in, then run the real commands yourself on feature 002.

---

## 1. What `specify init` installed

| Path | What it is | Who uses it |
|------|------------|-------------|
| `.claude/skills/speckit-*/SKILL.md` | The agent-side commands (`/speckit-specify`, `/speckit-plan`, …). Each is a prompt the agent follows. | Your coding agent |
| `.specify/templates/*.md` | Skeletons for spec, plan, tasks, checklist, constitution. Commands copy and fill them. | Commands |
| `.specify/scripts/bash/*.sh` | Deterministic helpers: resolve the current feature, copy templates, emit JSON paths. | Commands |
| `.specify/memory/constitution.md` | Project-wide rules. Every plan must pass its gates. | plan, analyze, converge |
| `.specify/extensions/git/` + `extensions.yml` | Hooks: create a feature branch before `specify`, offer commits after each step. | Commands (via hooks) |
| `.specify/feature.json` | *Gitignored* pointer to the active feature dir — how `plan`/`tasks` find your spec. | Scripts |
| `.specify/workflows/speckit/workflow.yml` | Optional scripted run of specify → plan → tasks → implement with review gates. | `specify workflow run` |

## 2. How the artifacts chain together

```text
constitution.md ─────────────── gates every plan, checked again by analyze & converge
       │
/speckit-specify  →  spec.md  (+ checklists/requirements.md)      WHAT / WHY — no tech
       │                FR-###, SC-###, US#/AC#  ← stable IDs everything traces to
/speckit-clarify  →  (optional) answers written back into spec.md
       │
/speckit-plan     →  plan.md, research.md, data-model.md,          HOW
       │              contracts/, quickstart.md
/speckit-tasks    →  tasks.md   T### grouped by user story, tests first, [P] = parallel
       │
/speckit-analyze  →  (optional) read-only consistency report across spec/plan/tasks
       │
/speckit-implement → code + checks off tasks
       │
/speckit-converge →  compares code to spec/plan/tasks/constitution;
                     appends "Phase N: Convergence" tasks OR reports ✅ Converged
       └──── loop implement ↔ converge until Converged
```

The thread to pull on: **FR-010** ("every data command has a machine-readable format") appears in
`spec.md` → becomes `--json` rules in `contracts/cli.md` → tasks T012/T017/T021 → code in `cli.py` →
and was caught by converge as a gap (T026) because `add` was missed.

## 3. Step through the worked example

Every stage is a git tag on branch `001-reading-list` (merged into `main`):

| Tag | Command it represents | Look at |
|-----|----------------------|---------|
| `stage-0-init` | `specify init` | the bare scaffold |
| `stage-1-constitution` | `/speckit-constitution` | `.specify/memory/constitution.md` |
| `stage-2-specify` | `/speckit-specify` | `specs/001-reading-list/spec.md`, `checklists/` |
| `stage-3-plan` | `/speckit-plan` | `plan.md` (Constitution Check table), `research.md`, `data-model.md`, `contracts/cli.md`, `quickstart.md` |
| `stage-4-tasks` | `/speckit-tasks` | `tasks.md` |
| `stage-5-implement` | `/speckit-implement` | `src/`, `tests/`, all tasks checked ✓ |
| `stage-6-converge` | `/speckit-converge` | new **Phase 7: Convergence** in `tasks.md` |
| `stage-7-converged` | `/speckit-implement` again | fixes; a second converge would report Converged |

```bash
git log --oneline --graph --all
git diff stage-2-specify stage-3-plan --stat     # what plan produced
git diff stage-5-implement stage-6-converge      # what converge appended
git show stage-6-converge:specs/001-reading-list/tasks.md | tail -8
```

**Teaching point at stage 5:** all 24 tasks are checked and all 27 tests pass, yet the feature
isn't done. Converge treats checkboxes as claims, not evidence, and finds two `partial` gaps:
`add` lacks `--json` (FR-010) and a valid-JSON-but-wrong-shape data file crashes with a traceback
instead of a clean error (FR-012). You can reproduce both by checking out `stage-5-implement`.

Run the app and tests (Python 3.11+, nothing to install):

```bash
export PYTHONPATH=src SHELF_FILE=/tmp/shelf.json
python -m shelf add "Dune" "Frank Herbert" && python -m shelf list
python -m unittest -v
```

## 4. Your turn — feature 002 with the real commands

Prereqs: [uv](https://docs.astral.sh/uv/), Python 3.11+, Claude Code.

```bash
uv tool install specify-cli     # gives you the `specify` CLI
specify check                   # verifies tools/agents
cd speckit-sandbox && claude    # launch the agent in this folder
```

Then, one at a time in the agent chat, reviewing each output before the next:

```text
/speckit-specify Let me remove a book from my list and edit a book's title or author. Removing should ask for confirmation unless I pass --yes.
/speckit-clarify
/speckit-plan Same stack as 001. Reuse the existing store and service modules.
/speckit-tasks
/speckit-analyze
/speckit-implement
/speckit-converge
```

Things worth watching for:
- The `before_specify` hook creates branch `002-…` automatically (git extension).
- `spec.md` should say nothing about Python — if it does, that's a spec-quality failure.
- The plan's Constitution Check must still show Standard Library Only and Test-First passing.
- FR-002 in 001 promised IDs are never reused — a good test of whether the agent reads prior specs.
- Edit/remove was explicitly deferred in 001's Assumptions; see whether the agent notices.

## 5. Useful CLI commands (terminal, not agent)

```bash
specify integration status              # which agent integration is installed
specify integration switch copilot      # swap to GitHub Copilot (skills → .github/)
specify extension list                  # installed extensions (git)
specify extension add bug               # opt-in bug-fix process (assess → fix → test)
specify extension add assess            # opt-in idea-assessment process
specify artifact --help                 # introspect commands, templates, hooks
specify workflow run speckit -i spec="…"  # scripted specify→plan→tasks→implement with gates
specify self check                      # newer CLI release available?
```

## 6. Knobs you may want to try

- `.specify/extensions/git/git-config.yml` → `auto_commit.default: true` to commit after every step,
  or `commit_style: conventional` for agent-written Conventional Commits.
- `.specify/init-options.json` → `"feature_numbering": "timestamp"` for `YYYYMMDD-HHMMSS-…` dirs.
- Edit `.specify/templates/spec-template.md` to see how template changes flow into new specs
  (or use a **preset** to do the same thing in a shareable way).
- `.claude/` can hold agent state; Spec Kit suggests reviewing what you commit from it.
