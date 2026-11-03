---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The start gate's Stop reason reads `dirty tree: start left 1 uncommitted: <files>`, as if "start" left the files. Make the start gate say `dirty tree: before start, 1 uncommitted: <files>`, and make `kit once` say `dirty tree: after once, 1 uncommitted: <files>`. The after-pass wording, `pass N (<phase>) left ...`, stays as it is.

## Acceptance
- [ ] `kit run` on a dirty tree prints `Stop reason: dirty tree: before start, N uncommitted: <files>`.
- [ ] `kit once` ending dirty prints `Stop reason: dirty tree: after once, N uncommitted: <files>`.
- [ ] The after-pass message is unchanged.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k dirty && uv run pyright && uv run ruff check
