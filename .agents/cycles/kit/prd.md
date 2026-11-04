# Sign off QA from recorded results

Appetite: 3 hours, 8 Issues, 2 QA rounds

## Problem

Nothing launches what a Cycle built before the human's QA. `/kit:qa` only writes `qa.md` with "See it work" commands for the human to run by hand, often after hunting for the right folder. The sandbox has no Docker, so steps that need the host only run for real in QA: last Cycle's Docker test was skipped in every review and failed only on the host. And no config says how to open the Product, so every QA starts by working that out.

## End state

- The PRD carries locked **QA steps** (`## QA steps`, with a `### Host steps` sub-list for steps that must run on the host). Each step is one literal command run from the worktree root, what you should see, the Done when line it proves, and an optional `timeout:` (default 5 minutes).
- After `review clean`, `kit run` runs every QA step itself, with no agent (ADR 0011). Steps run in the sandbox container by default. Host steps run on the host with a scrubbed environment (no tokens or cloud credentials), a throwaway `HOME`, the worktree as working directory, and a timeout that kills the step's whole process tree.
- Each step's result is recorded in `.agents/cycles/<area>/qa.md`: the step, what you should see, exit code, duration, and the last ~20 lines of output, with paths to anything it wrote. The full log goes to `.agents/cycles/<area>/qa-logs/NN.log`. `kit close` deletes both with the Cycle folder.
- A failing step (non-zero exit or timeout) is passed, with its output, into the next implement pass's prompt. That agent writes the `priority: bug` Issue, fixes it and commits, as review does; the CLI never writes into the repo (ADR 0009). `kit run` loops until the steps pass or `maxIterations` is hit. These loops are not QA rounds.
- `qa.md` and `qa-logs/` are git-ignored, so writing them never dirties the tree. `kit init` adds the ignore line.
- `kit run` ends with `complete: QA steps N/N passed, run /kit:qa`, `cap reached: QA step N still failing`, or `complete: no QA steps in PRD`.
- `kit.json` has a `launch` key: one command that opens the Product. The template ships `"launch": ""`. `kit doctor` warns while it is empty.
- `/kit:qa` shows the recorded results, shows then runs `launch` on the host unscrubbed, and leaves the Product open for the human's **Hunt**. If `launch` is empty it asks once and writes it into `kit.json` with the `qa:` commit. Hunt bugs become `priority: bug` Issues; Feature ideas become `raised:` lines. Still one QA round, one `qa:` commit.
- `/kit:to-prd` won't finish without at least one QA step, and rejects steps that need a manual action.
- `kit once` never runs QA steps.

## Done when

- After `review clean`, `kit run` runs each `## QA steps` command inside the sandbox command, and each `### Host steps` command on the host, in PRD order. With `--local`, both run on the host. (test)
- A host step's environment has no variable whose name contains `TOKEN`, `SECRET`, `KEY` or `PASSWORD`, or starts with `AWS_`, `GH_`, `GITHUB_` or `ANTHROPIC_`. Its `HOME` is a fresh empty directory and its working directory is the worktree. (test)
- A step with no `timeout:` is killed at 300 s, and one with `timeout: 1s` at 1 s. A timed-out step's child processes are gone afterwards, and it counts as failed. (test)
- `qa.md` has one entry per step with: the step, what you should see, the exit code, the duration, and at most 20 output lines. `qa-logs/NN.log` holds the full output. (test)
- A failing step's command and output appear in the next implement pass's prompt, with the instruction to write a `priority: bug` Issue. The CLI writes no Issue and makes no commit. (test)
- Writing `qa.md` and `qa-logs/` leaves `git status` clean, in the Kit and in a fresh `kit init` Product. (test)
- The 3 new endings each print exactly one Stop reason as the last line, with the counts filled in: `complete: QA steps N/N passed, run /kit:qa`, `cap reached: QA step N still failing`, `complete: no QA steps in PRD`. (test)
- The template's `kit.json` has `"launch": ""`. `kit doctor` prints one `launch` warning when it is empty and none when it is set, and keeps its exit code. (test)
- The `to-prd` skill requires `## QA steps` with at least one step and names `### Host steps`. The `qa` skill shows the results, runs `launch`, names the Hunt, and asks for `launch` when it is empty. (test)
- `kit once <area> <issue>` runs no QA step. (test)
- `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass. (test)

## QA steps

1. `uv run pyright && uv run ruff check && uv run pytest -q`: see exit 0. Proves: the checks pass.
2. `test "$(whoami)" = kit`: see exit 0. Proves: QA steps run in the sandbox by default.

### Host steps

3. `! env | grep -qiE '(TOKEN|SECRET|KEY|PASSWORD)|^(AWS_|GH_|GITHUB_|ANTHROPIC_)'`: see exit 0. Proves: host steps get a scrubbed environment.
4. `test ! -e "$HOME/.ssh" && test "$PWD" = "$(git rev-parse --show-toplevel)"`: see exit 0. Proves: throwaway `HOME`, worktree as working directory.
5. `.venv/bin/python -m pytest -q tests/test_cli.py -k sandbox_leaves_host_venv_alone | grep -q "1 passed"`: see exit 0, not skipped. Timeout: 10m. Proves: host steps can use Docker.

## Out of scope

- An agent running QA steps, judging their output, or Hunting.
- GUI automation (clicking, screenshots). Anything that needs a person belongs to the Hunt.
- Running QA steps from `kit once` or `kit close`.
- Mounting the Docker socket into the sandbox.

## What changes

- `src/kit/cli.py`: parse QA steps from the PRD, run them in the sandbox or on the host, write `qa.md` and `qa-logs/`, loop on failure, the new Stop reasons, the `launch` doctor check.
- `src/kit/plugin/skills/qa/SKILL.md`, `src/kit/plugin/skills/to-prd/SKILL.md`.
- `src/kit/template/.agents/kit.json`, `.agents/kit.json`: the `launch` key.
- `.gitignore` and `kit init`'s ignore lines: `qa.md`, `qa-logs/`.
- `tests/test_cli.py`, `tests/test_skills.py`.
- Sample data: none.

