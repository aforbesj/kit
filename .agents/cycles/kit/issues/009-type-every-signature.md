---
status: open
mode: hands-off
priority: bug
blocked_by: []
---
The Python standards require every function signature to be typed. Issue 008 added `tests/test_format.py` with `def test_ruff_format_is_clean():`, which has no return type. Every other function in `src` and `tests` is annotated. Pyright did not catch it because `pyproject.toml` sets `strict = ["src"]` only, so `tests/` is checked in basic mode.

## Acceptance
- [ ] A test in `tests/test_format.py` parses every `.py` file under `src` and `tests` with `ast` and asserts that each function has a return annotation and every parameter except `self` and `cls` is annotated, naming the file, line and function on failure. It fails before the fix, naming `tests/test_format.py` and `test_ruff_format_is_clean`.
- [ ] `test_ruff_format_is_clean` is annotated `-> None`. No other file changes apart from the test.
- [ ] Every command in `.agents/kit.json` passes, and `uv run ruff format --check` is clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check && uv run ruff format --check
