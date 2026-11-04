---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
Issue 3 made `stream()` start every command with `start_new_session=True` so a timeout can kill its process group. But `run()` and `once` also use `stream()` for the implement and review agents, so the agent no longer shares the terminal's process group: a Ctrl-C reaches only `kit`, which prints `interrupted: Ctrl-C` and exits while the agent (`claude -p`, or the `docker run` client and its container) keeps running and editing the worktree. Measured: `stream(["sh","-c","sleep 3; touch alive"])` with SIGINT sent to the parent's process group after 1 s: on `main` the child dies; on this branch `alive` is written 2 s after `kit` exited.

## Acceptance
- [x] A failing test first: `test_ctrl_c_stops_the_streamed_command` runs `stream(["sh", "-c", "sleep 2; touch <marker>"], tmp_path)` with a timer that sends SIGINT to the current process (or raises KeyboardInterrupt in the reading loop) after ~0.3 s, asserts KeyboardInterrupt propagates, waits ~2.5 s and asserts `<marker>` does not exist. It must fail on the current code.
- [x] On KeyboardInterrupt (or any exception) while reading, `stream()` kills the command's process group (and calls `on_kill`, so a named sandbox container is killed too) before re-raising. Timeouts still kill the whole group and raise StepTimeout.
- [x] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k "ctrl_c or timeout"
