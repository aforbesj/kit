---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The plugin description lists the Cycle skills but leaves out brainstorm. In `src/kit/plugin/.claude-plugin/plugin.json`, add brainstorm to the description, ahead of grill. Add a test that the description names "brainstorm".

## Acceptance
- [ ] `plugin.json` description names brainstorm
- [ ] A test in `tests/` checks it

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
