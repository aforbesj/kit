---
status: open
mode: hands-off
priority: bug
blocked_by: []
---
Two `(test)` Done when lines have no test. `kit once <area> <issue>` runs no QA step: nothing checks it, so a later change could make `once` run QA steps unnoticed. Writing `qa.md` and `qa-logs/` leaves `git status` clean in the Kit itself: only the fresh `kit init` Product is tested (`test_run_executes_qa_steps_and_records_them`); the Kit's own `.gitignore` is not.

## Acceptance
- [ ] A failing test first: `test_once_runs_no_qa_step` builds a Product with a PRD holding a `## QA steps` step and a `### Host steps` step that each write a marker file, runs `cli.once(root, "core", "001")` with a stub agent, and asserts neither marker exists and no `qa.md` or `qa-logs/` was written. Prove it fails by temporarily calling `qa_round` from `once`, then remove that call.
- [ ] A test that the Kit's own `.gitignore` (at the repo root) ignores `.agents/cycles/<area>/qa.md` and `.agents/cycles/<area>/qa-logs/01.log` (e.g. `git check-ignore`), and that `IGNORE_LINES` contains `qa.md` and `qa-logs/`.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k "once_runs_no_qa_step or gitignore"
