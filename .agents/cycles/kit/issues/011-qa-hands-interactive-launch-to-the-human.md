---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
`/kit:qa` can't leave an interactive Product open for the Hunt: anything the agent starts (a `claude` session, a shell, a TUI) runs inside its own tool call and ends with it. Found in QA round 1, when `launch` was `claude --plugin-dir src/kit/plugin`. Change step 2 of `src/kit/plugin/skills/qa/SKILL.md`: when `launch` is interactive, the agent shows the exact command and tells the human to run it from the worktree root in a new terminal; only a background command (a server) is started by the agent itself, and it says how to stop it.

## Acceptance
- [ ] The qa skill tells the agent to hand an interactive `launch` to the human as a command to run in a new terminal, from the worktree root.
- [ ] The qa skill starts only background `launch` commands itself, and says how to stop them.
- [ ] A test in `tests/test_skills.py` pins both.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_skills.py -k qa
