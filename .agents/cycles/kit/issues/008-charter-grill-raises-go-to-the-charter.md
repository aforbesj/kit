---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The Charter grill runs outside any Cycle, yet the grill tells it to write `raised:` lines to `.agents/cycles/<area>/progress.txt`, which creates a Cycle file before any Cycle exists. Limit the `raised:` line to the Cycle grill. In a Charter grill, ideas go straight into the Area's Features in `CHARTER.md` at 1×, since that grill is already writing the Charter.

## Acceptance
- [ ] A failing test first: the grill's `raised:` line applies to the Cycle grill only, and the Charter grill puts new ideas in `CHARTER.md` at 1×
- [ ] No SKILL.md grows by more than 3 lines since the `pick:` commit

## Verify
uv run pytest -q tests/test_skills.py
