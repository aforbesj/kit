---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
Issue 9 made `stream()` SIGKILL the command's process group on Ctrl-C and call `on_kill`. But `run()` streams the sandboxed implement and review agents (`cli.py` `run()`, both `stream(agent(...), cwd)` calls) with no `on_kill`, and `agent()`/`docker_run()` give their container no `--name`. Since the agent runs in its own session, Ctrl-C reaches only `kit`, which SIGKILLs the `docker run` client. Docker can't proxy SIGKILL, so the `--rm` container keeps running `claude --dangerously-skip-permissions` and editing the mounted worktree after `kit` prints `interrupted: Ctrl-C`. On `main` the client got SIGINT in the terminal's process group and proxied it to the container (sig-proxy is on by default). Issue 9 names this case ("the `docker run` client and its container") but only the local path is fixed. Not measured here: the review sandbox has no Docker; this comes from reading the code and Docker's signal behaviour.

## Acceptance
- [ ] A failing test first: `test_ctrl_c_stops_the_sandbox_agent` drives `run()` (not `--local`) with `stream` patched to raise KeyboardInterrupt, and asserts that the sandbox agent command carries `--name <name>` and that `docker kill <name>` (or the `on_kill` passed to `stream`) is called. It must fail on the current code.
- [ ] The implement and review agents in the sandbox run as named containers, and `run()` passes `on_kill=functools.partial(docker_kill, name)` to `stream`, as QA steps already do. `--local` behaviour is unchanged.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k "ctrl_c"
