---
status: open
mode: hands-off
priority: bug
blocked_by: []
---
The Python standards require `ruff format` to pass, and this Cycle's diff fails it. `uv run ruff format --check` reports two files: `src/kit/cli.py:107` (the `git merge --ff-only` call in `_latest_main` is over the line length) and `tests/test_cli.py:374` (the retro skill test wraps a line that fits on one). Nothing in `.agents/kit.json` runs the formatter, so the Build loop did not catch it.

## Acceptance
- [ ] A test in `tests/test_format.py` runs `ruff format --check` on `src` and `tests` with `subprocess` and asserts it returns 0. It fails before the fix.
- [ ] `uv run ruff format` is applied, and only the two files above change.
- [ ] Every command in `.agents/kit.json` passes, and `uv run ruff format --check` is clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check && uv run ruff format --check
