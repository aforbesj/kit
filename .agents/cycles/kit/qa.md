# QA: Leave a Build running and trust how it stopped

Round 1 of 2. Build: 13 Issues done (8 planned, plus 5 bug Issues from 4 review rounds). Checked on the host, where Docker is available.

## Done when, measured

| Done when | Result |
|---|---|
| `kit run` on a dirty tree exits non-zero before any agent starts, with files, keep, discard, then | ✅ Run by hand from the root with the worktree CLI: exit 1, no agent, all four lines |
| A pass that leaves files stops the run, with pass number and files | ✅ Tests, plus the review's probe: `pass 1 (implement) left 1 uncommitted: CHARTER.md` |
| No `git add` or `git commit` in `run` or `once` | ✅ Spy test |
| 5 endings, one Stop reason each, with detail | ✅ Tests (Ctrl-C under hand-off fixed in 009) |
| `kit once` dirty: Stop reason, keeps claude's exit code | ✅ Test |
| Version warning when older, none when equal or newer, exit unchanged | ✅ Tests. Here installed = Product = 0.2.0, so no warning |
| Sandbox mounts `kit-venv-<product>-<area>` and sets `UV_PROJECT_ENVIRONMENT`; two Areas, two names | ✅ Test of the command's shape |
| Host `.venv/bin/python` unchanged after a sandboxed run | ❌ **Fails.** `test_sandbox_leaves_host_venv_alone` ran for the first time here (skipped in every review: no Docker in the sandbox). `uv sync` exits 2, because the new volume is mounted root-owned at `/home/kit/venv` and the sandbox user `kit` can't write to it. Every sandboxed `uv run` would fail. |
| `kit close` removes the volume, succeeds if it's missing | ✅ Test of the command's shape (Docker faked as missing) |
| Kit Product: worktree CLI and `--plugin-dir`; other Products unchanged | ✅ Tests. The hand-off ran for real above: the root's command used the worktree's gate |
| pyright, ruff, pytest pass | ❌ pyright 0 errors, ruff clean, pytest **99 passed, 1 failed** (the volume test above) |

## Also seen

- **The trap that ADR 0010 names.** From the root, `kit run kit` uses the installed CLI, which is `main`'s and has none of this Cycle's code. With a dirty tree, it started a real agent silently instead of refusing. It was stopped before it changed or committed anything. Once this Cycle merges, the hand-off covers it. Until then, run the worktree CLI: `uv run --project .worktrees/kit kit …`.
- The start gate's wording, `start left 1 uncommitted`, reads as if "start" left the files.

## See it work

From `~/code/aforbesj/kit`:
```
touch .worktrees/kit/x && uv run -q --project .worktrees/kit kit run kit --local; rm .worktrees/kit/x
uv run --project .worktrees/kit pytest -q tests/test_cli.py::test_sandbox_leaves_host_venv_alone
docker run --rm -v kit-venv-probe:/home/kit/venv kit-sandbox touch /home/kit/venv/x; docker volume rm kit-venv-probe
```

## Worth reading in the diff

- `src/kit/cli.py`: `stop`, `dirty_files`, `stop_dirty` (about :334 to :380), and `run`.
- `src/kit/cli.py`: `is_kit`, `plugin_args`, `hand_off`, `venv_volume` (about :181 to :220).
- `src/kit/sandbox/Dockerfile`: unchanged. The volume fix belongs here (create `/home/kit/venv` as `kit`, so Docker copies its ownership into a new volume).

---

# Round 2 of 2

Build: 014 and 015 done, review clean (round 5). Checked on the host, where Docker is available.

| Check | Result |
|---|---|
| Old image without `/home/kit/venv` is rebuilt by `sandbox()` | ✅ Before: image lacked the folder. `cli.sandbox("kit-sandbox")` printed `Rebuilding the sandbox image kit-sandbox (it lacks /home/kit/venv)...`. After: the folder is there |
| New volume writable as `kit` | ✅ `touch /home/kit/venv/x` in a new `kit-venv-probe` volume: WRITABLE |
| Host `.venv/bin/python` unchanged after a sandboxed run | ✅ `test_sandbox_leaves_host_venv_alone` passes. No `kit-venv-*` volumes are left behind |
| Start gate wording | ✅ From the root, with the worktree CLI: `Stop reason: dirty tree: before start, 1 uncommitted: qa-probe.txt`, exit 1 |
| pyright, ruff, pytest | ✅ 0 errors, clean, **101 passed, 0 skipped** |

Every Done when line from round 1 now passes.
