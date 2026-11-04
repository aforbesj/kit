---
status: todo
mode: hands-off
priority: tracer
blocked_by: []
---
Update `src/kit/plugin/skills/to-prd/SKILL.md`. Its template gains `## QA steps` (numbered: a backticked command run from the worktree root, `see:` what you should see, `proves:` the Done when line, optional `timeout:`) and a `### Host steps` sub-list for steps that must run on the host. The skill won't commit a PRD without at least one QA step, and rejects any step that needs a manual action (going to a folder, clicking): that belongs to the Hunt.

## Acceptance
- [ ] The to-prd template has `## QA steps` and `### Host steps`, with the step format above.
- [ ] The skill says it won't commit without at least one QA step, and rejects manual steps.
- [ ] New tests in `tests/test_skills.py` pin both.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_skills.py -k to_prd
