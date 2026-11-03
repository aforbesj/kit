---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
Issue 005 put brainstorm inside the Cycle loop: the description in `src/kit/plugin/.claude-plugin/plugin.json` (copied in `.claude-plugin/marketplace.json`) reads "The Cycle loop: brainstorm, grill, plan, split, build, review, QA, retro." A Brainstorm is not part of a Cycle. It comes before a Charter grill, outside any Cycle. Change both descriptions to "Brainstorm, then the Cycle loop: grill, plan, split, build, review, QA, retro."

## Acceptance
- [ ] Start by changing `test_plugin_description_names_brainstorm_before_grill` in `tests/test_skills.py` so it asserts the description does not contain "loop: brainstorm" and still names brainstorm ahead of grill, ignoring case (it fails today)
- [ ] Both descriptions read "Brainstorm, then the Cycle loop: grill, plan, split, build, review, QA, retro."; `test_marketplace_description_matches_plugin_manifest` still passes

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
