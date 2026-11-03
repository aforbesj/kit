---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
Issue 005 added brainstorm to the description in `src/kit/plugin/.claude-plugin/plugin.json`, but `.claude-plugin/marketplace.json` has its own copy of that description for the `kit` plugin, and it still reads "The Cycle loop: grill, plan, split, build, review, QA, retro." The marketplace description is what people see when they install the plugin, so it should match. Copy the `plugin.json` description into the marketplace entry.

## Acceptance
- [ ] Start with a failing test in `tests/test_skills.py`: the `kit` entry's `description` in `.claude-plugin/marketplace.json` equals the `description` in `src/kit/plugin/.claude-plugin/plugin.json` (it fails today)
- [ ] The marketplace description names brainstorm ahead of grill, and the test passes

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
