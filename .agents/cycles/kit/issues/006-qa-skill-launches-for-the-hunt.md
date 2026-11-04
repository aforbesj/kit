---
status: done
mode: hands-off
priority: tracer
blocked_by: [5]
---
Rewrite `src/kit/plugin/skills/qa/SKILL.md`. It now reads the `qa.md` that `kit run` recorded instead of writing one, and walks the human through each step's result against what they should see. It shows the `launch` command from `kit.json`, then runs it on the host, and leaves the Product open for the human's Hunt. If `launch` is empty, it asks the human once and writes the answer into `kit.json` with the round's `qa:` commit. Hunt bugs become `priority: bug` Issues; Feature ideas become `raised:` lines in `progress.txt`. The round counting, the Appetite question, one `qa:` commit per round and the abandon path stay as they are. "See it work" goes.

## Acceptance
- [x] The qa skill reads the recorded `qa.md` and no longer tells the agent to write it.
- [x] It shows then runs `launch`, and names the Hunt.
- [x] It asks for `launch` when empty and writes it into `kit.json` before the `qa:` commit.
- [x] Existing qa tests in `tests/test_skills.py` still pass; new tests pin the points above.
- [x] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_skills.py -k qa
