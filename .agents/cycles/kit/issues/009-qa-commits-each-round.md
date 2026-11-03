---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
`qa` (`src/kit/plugin/skills/qa/SKILL.md`) counts QA rounds by `qa:` commits, but no skill says to make one. Add to `qa`: after writing `qa.md` and any new Issues for the round, commit with message `qa: <feature>`, so each round leaves exactly one `qa:` commit for the breaker and the retro to count. Pin with a test in `tests/test_skills.py`.

## Acceptance
- [ ] `qa` commits `qa: <feature>` once per round
- [ ] A test in `tests/test_skills.py` pins it

## Verify
uv run pytest -q tests/test_skills.py
