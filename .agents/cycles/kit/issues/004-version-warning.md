---
status: todo
mode: hands-off
priority: polish
blocked_by: []
---
Read the installed `kit` version with `importlib.metadata.version("kit-cycle")` and compare it with the `"kit"` field in the Product's `.agents/kit.json`. When the installed one is older, `kit doctor`, `kit once` and `kit run` each print one line, for example: `Warning: kit 0.1.0 is older than this Product's 0.2.0. Fix: ./setup.sh in the Kit checkout`. Nothing is blocked and exit codes don't change. Print nothing when it's equal or newer, when the field is missing, or when the version can't be read.

## Acceptance
- [ ] Older: each of the three commands prints exactly one warning, and its exit code is unchanged.
- [ ] Equal, newer, field missing, version unreadable: no warning.
- [ ] Versions compare as numbers, so 0.10.0 is newer than 0.9.0.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k version && uv run pyright && uv run ruff check
