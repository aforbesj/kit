---
status: done
mode: hands-off
priority: tracer
blocked_by: []
---
`kit.json` gains a `launch` key: one command that opens the Product for the human's Hunt. The template's `kit.json` and the Kit's own `.agents/kit.json` ship `"launch": ""`. `kit doctor` prints one warning while `launch` is empty or missing, saying `/kit:qa` will ask for it, and no warning once it is set. Its exit code is unchanged.

## Acceptance
- [x] `src/kit/template/.agents/kit.json` and `.agents/kit.json` have `"launch": ""`.
- [x] `kit doctor` prints exactly one `launch` warning when it is empty or missing, and none when it is set.
- [x] `kit doctor`'s exit code is the same either way.
- [x] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k launch
