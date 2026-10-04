# Shelf Constitution

Shelf is a small command-line reading-list tracker used as a Spec Kit sandbox.
These principles govern every feature specified, planned, and implemented in this repository.

## Core Principles

### I. Spec Before Code

Every user-visible change MUST start as a feature specification under `specs/NNN-feature-name/`.
Specifications describe **what** users need and **why**; they MUST NOT prescribe languages,
libraries, or file layouts. Technical choices belong in `plan.md`. Code that cannot be traced
to a functional requirement (FR-###) or a task (T###) is treated as unrequested scope.

### II. Test-First (NON-NEGOTIABLE)

Every functional requirement MUST have at least one automated test. Tests for a user story are
written before its implementation and MUST fail before the implementation makes them pass
(red → green → refactor). A story is not done until its acceptance scenarios pass as tests.

### III. Standard Library Only

Shelf MUST run on a clean Python 3.11+ installation with zero third-party runtime dependencies.
Tests use the standard `unittest` module so the suite runs with `python -m unittest` and nothing
to install. Adding any dependency requires a constitution amendment.

### IV. Predictable CLI Contract

Every command MUST:
- write normal output to stdout and errors to stderr;
- exit `0` on success, `1` on user error (bad input, item not found), `2` on usage error;
- support `--json` for machine-readable output where it returns data.

The command contract lives in each feature's `contracts/` folder and is the source of truth for tests.

### V. Simplicity

Build the smallest thing that satisfies the spec. No speculative abstractions, plugin systems,
or configuration options until a specification asks for them. Any added complexity MUST be
justified in the plan's Complexity Tracking table.

## Additional Constraints

- **Data stays local**: Shelf stores data in a single human-readable JSON file. Default location
  is `~/.shelf.json`, overridable with the `SHELF_FILE` environment variable (used by tests).
- **No network access** at runtime.
- **Writes are atomic**: the data file is written to a temporary file and renamed into place so a
  crash cannot leave a half-written file.

## Development Workflow

- One feature per branch, named `NNN-short-name` to match its `specs/` directory.
- Order of work per feature: `/speckit-specify` → (`/speckit-clarify`) → `/speckit-plan` →
  `/speckit-tasks` → (`/speckit-analyze`) → `/speckit-implement` → `/speckit-converge`.
- Repeat implement → converge until converge reports **Converged**, then open a pull request.
- Pull requests MUST link the feature's `spec.md` and confirm `python -m unittest` passes.

## Governance

This constitution supersedes other conventions in the repository. Plans MUST complete a
Constitution Check gate before research and again after design; any violation MUST be recorded
in Complexity Tracking with a justification or the plan is rejected.

Amendments are made with `/speckit-constitution`, versioned with semantic versioning
(MAJOR: principle removed or redefined; MINOR: principle or section added; PATCH: wording only),
and committed on their own.

**Version**: 1.0.0 | **Ratified**: 2026-10-04 | **Last Amended**: 2026-10-04
