---
status: open
mode: hands-off
priority: bug
blocked_by: []
---
The grill tells the agent to append `raised: <idea>` to a bare `progress.txt`, but the grill runs before `/kit:to-prd` creates `.agents/cycles/<area>/`, so no Cycle `progress.txt` exists yet and the agent has no path to it. A Raise from the Cycle grill can land in a root `progress.txt` that the retro never reads and `kit close` does not remove, so it gets merged into `main`. The PRD's End state says the line goes to the Cycle's `progress.txt`. Name the full path in the grill, `.agents/cycles/<area>/progress.txt` (create it if missing), by editing the existing sentence in place so the grill body does not grow.

## Acceptance
- [ ] A failing test in `tests/test_skills.py` first asserts that `grill/SKILL.md` says to append `raised: <idea>` to `.agents/cycles/<area>/progress.txt`
- [ ] `grill/SKILL.md` names that path and says to create the file if missing
- [ ] `test_skills_record_raises` still passes for all 4 skills
- [ ] `grill/SKILL.md` has grown by no more than 3 lines since the `pick:` commit

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
