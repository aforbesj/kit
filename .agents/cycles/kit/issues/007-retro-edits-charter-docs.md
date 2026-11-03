---
status: done
mode: hands-off
priority: polish
blocked_by: []
---
`src/kit/plugin/skills/retro/SKILL.md` tells the agent to remove the finished Feature from `CHARTER.md` and name the next one. The README Close step says that after the merge, `kit once <area>` starts the next Cycle from the latest `main`. `CONTEXT.md` keeps saying that a Cycle ends when its Cycle Branch merges. A test reads the retro skill and checks the Charter instruction.

## Acceptance
- [ ] The retro skill tells the agent to remove the finished Feature from `CHARTER.md` and name the next one. (test)
- [ ] The README Close step describes the flow: merge, `kit once <area>`, `/kit:grill`.
- [ ] `CONTEXT.md` says a Cycle ends when its Cycle Branch merges.
- [ ] Every command in `.agents/kit.json` passes. (test)

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
