---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
Run the Brainstorm after the merge, not on the Cycle branch. In QA the human chose this order: the Feature merges first, and a Brainstorm may come days later as the start of new work. In `src/kit/plugin/skills/retro/SKILL.md`, when the Area has no next Feature, tell the human to run `kit close <area>` first and then, after the merge, `/kit:brainstorm` from the latest `main`. In the README Close row, say the same thing: after the merge, run `/kit:grill` for the next Feature, or `/kit:brainstorm` if the Area has none.

## Acceptance
- [ ] The retro skill names `kit close <area>` before `/kit:brainstorm`, and says the Brainstorm comes after the merge
- [ ] The README Close row names `/kit:brainstorm` after the merge, as the alternative to `/kit:grill`
- [ ] The retro skill still contains "Remove the finished Feature from `CHARTER.md` and name the next one"
- [ ] Tests in `tests/` check the order in both files

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
