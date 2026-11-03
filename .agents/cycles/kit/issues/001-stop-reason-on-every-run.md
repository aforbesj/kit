---
status: done
mode: hands-off
priority: tracer
blocked_by: []
---
Make every `kit run` end with exactly one Stop reason as its last line: a category plus a short detail. Change `stream` in `src/kit/cli.py` to return the output and the exit code instead of raising `SystemExit`. Make `run` print one of these 4 Stop reasons:
- `complete`: the Issues done, and that review was clean.
- `cap reached`: N passes, and the last Issue worked on.
- `agent failed`: the phase (implement or review), the exit code, and the agent's last non-empty output line.
- `interrupted`: Ctrl-C, caught as `KeyboardInterrupt`.

Exit 0 only on complete. Put the formatting in one small function that 002 and 003 reuse.

## Acceptance
- [ ] Each of the 4 endings prints exactly one Stop reason line, the last line, with a non-empty detail (tests fake the agent with `config["agent"]`).
- [ ] `agent failed` names the phase, the exit code and the last error line.
- [ ] Exit code is 0 for complete and non-zero for the other three.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k stop_reason && uv run pyright && uv run ruff check
