---
status: todo
mode: hands-on
priority: tracer
blocked_by: []
---
Add `src/kit/plugin/skills/brainstorm/SKILL.md` (`name: brainstorm`, `disable-model-invocation: true`). The skill widens a problem into many Directions, each with its cost, through conversation. It brings in evidence (Sample data, `progress.txt`, similar products) when that helps. It writes no file, records no rejected Directions, and ends when the human picks one Direction by telling them to run `/kit:grill` in the same session. Update `src/kit/plugin/skills/grill/SKILL.md` so that an empty Charter points the human to `/kit:brainstorm` first, and so that a grill right after a Brainstorm is a Charter grill even on a filled Charter, one that may add Features and widen scope. Use the words Brainstorm, Direction and Charter grill from `CONTEXT.md`.

## Acceptance
- [ ] `skills/brainstorm/SKILL.md` exists with `name: brainstorm` and `disable-model-invocation: true`
- [ ] The brainstorm skill names `/kit:grill` as its last step and has no instruction to write a file
- [ ] The brainstorm skill's body is 25 lines or fewer
- [ ] The grill skill names `/kit:brainstorm` for an empty Charter and runs a Charter grill on a filled Charter after a Brainstorm
- [ ] Tests in `tests/` check each line above

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
