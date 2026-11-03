---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
Make picking use the ranked list. The Cycle grill opens by showing the Area's Top 3 from `CHARTER.md` and lets the human pick any Feature on the list, or something new. The Charter grill fills each Area with a Top 3 and a Bottom 3: at most 6 Features, each with `(raised N×)`. The template `src/kit/template/CHARTER.md` shows that format under Areas and still names the Charter grill and the retro as the only editors.

## Acceptance
- [ ] The Cycle grill shows the Area's Top 3 and lets the human pick any Feature or something new
- [ ] The Charter grill fills each Area with a Top 3 and a Bottom 3, at most 6, with counts
- [ ] The template `CHARTER.md` shows the Top 3 / Bottom 3 format with `(raised N×)`
- [ ] Tests in `tests/test_skills.py` check each of the above

## Verify
uv run pytest -q tests/test_skills.py
