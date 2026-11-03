---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The retro breaks ties "to the most recently raised", but `(raised N×)` stores no date, so a later retro can't tell which Feature is more recent. Make every count carry the date it was last raised: `(raised N×, last YYYY-MM-DD)`. The retro sets `last` to today on each bump or new entry and breaks ties by the later date. The Charter grill and the template `CHARTER.md` use the same format.

## Acceptance
- [ ] A failing test first: `retro`, `grill` and the template `CHARTER.md` all show `(raised N×, last YYYY-MM-DD)`, and none shows a bare `(raised N×)`
- [ ] The retro sets `last` on each bump or new entry and breaks ties by the later `last`
- [ ] No SKILL.md grows by more than 3 lines since the `pick:` commit

## Verify
uv run pytest -q tests/test_skills.py
