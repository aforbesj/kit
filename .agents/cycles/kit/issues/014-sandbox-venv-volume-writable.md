---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The sandbox can't write its `.venv` volume. Docker creates the mount point of a new named volume owned by root when the image has no `/home/kit/venv`. The sandbox runs as `kit`, so `uv sync` exits 2 and every sandboxed `uv run` fails. In `src/kit/sandbox/Dockerfile`, create `/home/kit/venv` as user `kit` after `USER kit`, so Docker copies that ownership into each new volume. Rebuild the image when it lacks the folder, so existing machines pick up the fix. Without that, `kit run` keeps using the old image.

## Acceptance
- [ ] `docker run --rm -v kit-venv-probe:/home/kit/venv kit-sandbox touch /home/kit/venv/x` succeeds on a new volume.
- [ ] An image built before this fix is rebuilt by `kit run` (or `kit doctor` says how to rebuild it).
- [ ] `test_sandbox_leaves_host_venv_alone` passes on a machine with Docker, and it removes its volume afterwards.
- [ ] pyright, ruff and pytest pass.

## Verify
docker build -t kit-sandbox src/kit/sandbox && uv run pytest -q tests/test_cli.py::test_sandbox_leaves_host_venv_alone
