# Leave a Build running and trust how it stopped

Appetite: 2 hours, 8 Issues, 2 QA rounds

## Problem

When `kit run` stops, you can't tell why, or what state it left. The CLI never checks the tree, so a failed pass or a failed commit leaves work staged but not committed, and only `kit close` notices (Issues 003, 005 and 006 last Cycle). Nothing compares the installed `kit` with the version in `kit.json`. The host and the sandbox share one `.venv` and each rebuilds it for its own Python. A Cycle that changes the Kit builds and QAs with `main`'s installed skills and CLI, not the ones it is changing.

## End state

- `kit run` starts only on a clean tree and checks the tree after every pass. It never stages or commits for the agent (ADR 0009).
- Every `kit run` ends with one Stop reason line: a category plus a short detail.
- A dirty tree, at start or after a pass, lists the files and prints the exact commands to keep or discard them, then `kit run`.
- `kit once` ends with the same Stop reason when the tree is dirty, as a warning only.
- `kit doctor`, `kit once` and `kit run` warn when the installed `kit` (`kit-cycle` package metadata) is older than `kit.json`'s `"kit"`. They never block on it.
- In the sandbox, `UV_PROJECT_ENVIRONMENT` points at a Docker volume named `kit-venv-<product>-<area>`, one per worktree, created on first use. The repo's `.venv` belongs to the host alone. `kit close` deletes the volume.
- When the Product is the Kit (`pyproject` name `kit-cycle`), `kit once` and `kit run` hand off to the worktree's own CLI and launch `claude` with `--plugin-dir <worktree>/src/kit/plugin`. Every other Product is unchanged (ADR 0010). Research confirmed that `--plugin-dir` takes priority over the installed `kit@kit` plugin.

## Done when

- `kit run` on a dirty tree exits non-zero before any agent starts. It prints `dirty tree:` with the files, a `keep:` command, a `discard:` command and `then: kit run`. (test)
- A pass that leaves uncommitted files stops `kit run` before the next pass, exits non-zero and prints the `dirty tree` Stop reason with the pass number and the files. (test)
- No code path in `kit run` or `kit once` runs `git add` or `git commit`. (test)
- Each of the 5 ways `kit run` can end prints exactly one Stop reason as its last line, each with a non-empty detail. The five, with what each detail contains:
  - **complete:** the Issues done, and that review was clean.
  - **cap reached:** N passes, and the last Issue.
  - **agent failed:** the phase, the exit code, and the last error line.
  - **dirty tree:** the pass number and the files.
  - **interrupted:** Ctrl-C.

  (test)
- When `kit once` ends on a dirty tree, it prints the `dirty tree` Stop reason and keeps `claude`'s exit code. (test)
- When the installed `kit` is older than `kit.json`, `kit doctor`, `kit once` and `kit run` each print one version warning and keep their exit code. When it is equal or newer, there is no warning. (test)
- The sandbox command mounts `kit-venv-<product>-<area>` and sets `UV_PROJECT_ENVIRONMENT` to its mount path. Two Areas of the same Product get two different volume names. (test)
- After a sandboxed `kit run`, the host's `.venv/bin/python` points where it did before. (test)
- `kit close` removes the Area's `kit-venv-<product>-<area>` volume. If the volume doesn't exist, it succeeds. (test)
- In a Product whose `pyproject` name is `kit-cycle`, `kit once` and `kit run` run the worktree's CLI and pass `--plugin-dir <worktree>/src/kit/plugin`. In any other Product, they do neither. (test)
- `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass. (test)

## Out of scope

- Committing, or retrying, on the agent's behalf.
- Blocking on a version mismatch, or upgrading `kit` automatically.
- A model setting for lookups (recorded as a Raise).
- Parallel agents inside one Cycle. Changing the skill text's commit steps.

## What changes

- `src/kit/cli.py`: `run`, `once`, `close`, `doctor`, `agent`/`sandbox`, a Stop reason and a version check.
- `src/kit/__init__.py`, if the version check needs it.
- `tests/`.
- Sample data: none.
