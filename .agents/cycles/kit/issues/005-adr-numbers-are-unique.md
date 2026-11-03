---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
Two ADRs are numbered 0001. Rename `docs/adr/0001-cycle-ends-at-merge.md` to `docs/adr/0007-cycle-ends-at-merge.md` with `git mv`, change its heading from `# 1.` to `# 7.`, and update any reference to the old path. Add a test in `tests/test_skills.py` that no two files in `docs/adr/` share a number prefix.

## Acceptance
- [ ] `docs/adr/0007-cycle-ends-at-merge.md` exists with heading `# 7. ...`; the old path is gone and nothing references it
- [ ] A test fails if two ADRs share a number

## Verify
uv run pytest -q tests/test_skills.py
