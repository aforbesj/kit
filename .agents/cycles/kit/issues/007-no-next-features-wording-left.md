---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
"Next Features" still appears where the list is now a ranked Top 3 / Bottom 3: the retro's lesson table row ("Scope, Areas, next Features"), the Charter definition in `CONTEXT.md`, and both copies of `CLAUDE.md` (root and `src/kit/template/`, which must stay identical). Change each to say the Area's ranked Features. Leave this Kit's own `CHARTER.md` alone; the retro edits that.

## Acceptance
- [ ] A failing test first: no "next Features" in `retro/SKILL.md`, `CONTEXT.md`, `CLAUDE.md` or `src/kit/template/CLAUDE.md`
- [ ] Both `CLAUDE.md` copies are still identical
- [ ] No SKILL.md grows by more than 3 lines since the `pick:` commit

## Verify
uv run pytest -q tests/test_skills.py && ! git grep -n "next Features" -- src CONTEXT.md CLAUDE.md README.md
