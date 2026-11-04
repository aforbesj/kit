---
status: done
mode: hands-off
priority: tracer
blocked_by: [1]
---
When a QA step fails (non-zero exit or timeout), `kit run` doesn't stop. It passes the failing step's command and output into the next implement pass's prompt (`prompt(..., extra=...)`), telling the agent to write a `priority: bug` Issue for it, fix it and commit, the same way review files Issues. Then the loop carries on: implement, review, QA steps again. The CLI writes nothing into the repo and makes no commit (ADR 0009). These loops are not QA rounds. If `maxIterations` runs out while a step is still failing, the run ends with `Stop reason: cap reached: QA step N still failing`. A PRD with no `## QA steps` ends with `Stop reason: complete: no QA steps in PRD`.

## Acceptance
- [x] A failing step's command and output appear in the next implement prompt, with the instruction to write a `priority: bug` Issue.
- [x] The CLI writes no Issue file and runs no `git add` or `git commit`.
- [x] When passes run out with a step still failing, the last line is `Stop reason: cap reached: QA step N still failing`.
- [x] A PRD with no `## QA steps` ends with `Stop reason: complete: no QA steps in PRD`.
- [x] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k "qa and (fail or cap or no_qa)"
