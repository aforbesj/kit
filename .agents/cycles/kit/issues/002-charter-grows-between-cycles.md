---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
Carry ADR 0006 into the template and the retro. The template `src/kit/template/CHARTER.md` drops "only a retro edits it" and says that only a Charter grill or a retro edits it. `src/kit/plugin/skills/retro/SKILL.md` tells the human to run `/kit:brainstorm` when the Area has no next Feature left, and keeps "Remove the finished Feature from `CHARTER.md` and name the next one".

## Acceptance
- [ ] The template `CHARTER.md` no longer says "only a retro edits it" and names the Charter grill and the retro
- [ ] The retro skill names `/kit:brainstorm` for an Area with no next Feature
- [ ] The retro skill still contains "Remove the finished Feature from `CHARTER.md` and name the next one"
- [ ] Tests in `tests/` check each line above

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
