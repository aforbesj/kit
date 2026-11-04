---
status: todo
mode: hands-off
priority: tracer
blocked_by: []
---
After `review clean`, `kit run` reads the PRD's `## QA steps` (numbered items: a backticked command, then what you should see and what it proves) and runs each command itself, no agent, with `sh -c` inside the sandbox container (same image, mounts and working directory as `agent()`), or on the host with `--local`. Each step's result goes into `.agents/cycles/<area>/qa.md`: the step, what you should see, the exit code, the duration, and at most the last 20 output lines. The full output goes to `.agents/cycles/<area>/qa-logs/NN.log`. When every step exits 0 the run ends with `Stop reason: complete: QA steps N/N passed, run /kit:qa`. `qa.md` and `qa-logs/` are git-ignored in the Kit's `.gitignore` and in `kit init`'s ignore lines, so writing them never dirties the tree (ADR 0009, ADR 0011).

## Acceptance
- [ ] After `review clean`, each `## QA steps` command runs inside the sandbox `docker run` command, in PRD order; with `--local`, on the host.
- [ ] `qa.md` has one entry per step with the step, what you should see, exit code, duration and at most 20 output lines; `qa-logs/NN.log` holds the full output.
- [ ] The last line is `Stop reason: complete: QA steps N/N passed, run /kit:qa` with N filled in.
- [ ] `git status` is clean after `qa.md` and `qa-logs/` are written, in the Kit and in a fresh `kit init` Product.
- [ ] `kit once <area> <issue>` runs no QA step.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k qa
