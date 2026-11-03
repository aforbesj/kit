---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
Widen Raise capture to the rest of the Cycle. The grill, review and qa skills each tell the agent to append `raised: <idea>` to `progress.txt` when an idea for a Feature comes up, using the same wording as `implement`. Then one test checks all four skills.

## Acceptance
- [ ] `grill`, `review` and `qa` SKILL.md each tell the agent to append `raised: <idea>` to `progress.txt`
- [ ] One test asserts this for all 4 skills (grill, implement, review, qa)

## Verify
uv run pytest -q tests/test_skills.py
