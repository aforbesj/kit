---
status: todo
mode: hands-off
priority: tracer
blocked_by: []
---
The thinnest path from a Raise to a ranked list. When an idea for a Feature comes up while building, `implement` appends a line `raised: <idea>` to `progress.txt`. The retro reads those lines and matches each against the Area's Features in `CHARTER.md`. A match bumps that Feature's `(raised N×)` count, at most once per Cycle; a new idea joins at 1×. The retro then removes the finished Feature, sorts by count with ties to the most recently raised, drops the lowest past 6, and shows the list as a Top 3 and a Bottom 3. The retro stops saying "name the next one". An empty list still points to `/kit:brainstorm` after the merge. Rewrite the tests in `tests/test_skills.py` that assert the old wording.

## Acceptance
- [ ] `implement/SKILL.md` tells the agent to append `raised: <idea>` to `progress.txt` when an idea for a Feature comes up
- [ ] `retro/SKILL.md` counts `raised:` lines once per Feature per Cycle, adds new ideas at 1×, removes the finished Feature, sorts with ties to the most recent, caps at 6, shows the Top 3 and Bottom 3
- [ ] `retro/SKILL.md` no longer contains "name the next one" and still sends an empty Area to `/kit:brainstorm` after the merge
- [ ] Tests in `tests/test_skills.py` check each of the above

## Verify
uv run pytest -q tests/test_skills.py
