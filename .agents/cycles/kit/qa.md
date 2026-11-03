# QA: Close a Cycle and start the next

Re-measured at QA (2026-11-03): pyright 0 errors, ruff check clean, ruff format clean (38 files), pytest 30 passed.

## Done when

| # | Done when | Result | Test (`tests/test_cli.py` unless noted) |
|---|---|---|---|
| 1 | Merged `cycle/<area>`, no checkout: old branch deleted locally and on remote, new HEAD = latest `origin/main` | pass | `test_workspace_removes_merged_branch_and_starts_fresh`, `test_workspace_branches_from_latest_origin_main` |
| 2 | Root clean and on `main`: fast-forwarded to `origin/main` | pass | `test_workspace_fast_forwards_clean_root_on_main` |
| 3 | Root dirty or on another branch: left unchanged, new branch still from `origin/main` | pass | `test_workspace_leaves_dirty_root_alone`, `test_workspace_leaves_root_on_other_branch_alone` |
| 4 | Unmerged `cycle/<area>`: reopened with commits, nothing deleted, prints "Cycle still open: not merged into `main`" | pass | `test_workspace_reopens_unmerged_branch` |
| 5 | No remote, or fetch fails: warns, starts from local `main`, no error | pass | `test_workspace_without_remote_warns_and_uses_local_main`, `test_workspace_with_failing_fetch_warns_and_uses_local_main` |
| 6 | `kit close` on dirty checkout: returns 1, nothing changed | pass | `test_close_refuses_dirty_checkout[False]` |
| 7 | `kit close --abandon` on dirty checkout: returns 1, no tag, nothing changed | pass | `test_close_refuses_dirty_checkout[True]` |
| 8 | Successful `kit close` prints next steps: merge, `kit once <area>`, `/kit:grill` | pass | `test_close_prints_next_steps_with_remote`, `..._without_remote` |
| 9 | `--abandon` with remote: tag on remote, `cycle/<area>` gone from remote | pass | `test_close_abandon_with_remote_keeps_tag_there_and_drops_branch` |
| 10 | `--abandon` with no remote: returns 0, tag kept locally | pass | `test_close_abandon_without_remote_keeps_tag_locally` |
| 11 | `retro` skill removes the finished Feature from `CHARTER.md` and names the next | pass | `test_retro_skill_removes_finished_feature_from_charter` |
| 12 | Every command in `.agents/kit.json` passes | pass | `tests/test_format.py` also guards format and typed signatures |

## See it work

```sh
uv run pyright && uv run ruff check && uv run pytest -q
KIT_DIR=$PWD .agents/cycles/kit/qa-demo.sh
```

The demo builds a throwaway bare `origin` and root checkout in a temp dir, then walks through: a fresh branch from `origin/main`, close refusing a dirty checkout, an unmerged branch being reopened, a merged branch deleted locally and remotely and recreated at `origin/main`, and `--abandon` pushing its tag and dropping the remote branch. It prints the temp dir at the end so you can poke around.

## Worth reading in the diff

- `src/kit/cli.py` `workspace`, `_merged`, `_latest_main` (lines 66-110): the whole start-fresh logic.
- `src/kit/cli.py` `close` (lines 289-332): dirty check, abandon pushes, next-steps message.
- `tests/test_cli.py` lines 185-380: the new tests and the bare-origin fixtures.
- `src/kit/plugin/skills/retro/SKILL.md`, `README.md` Close row, `CONTEXT.md` Cycle / Cycle Branch.

## Known notes from review (not Issues yet)

- `close --abandon` pushes without capturing output, so an unpushed Cycle Branch prints git's "remote ref does not exist" to stderr; it still returns 0.
- `close --abandon` checks for *any* remote but pushes to `origin`; `workspace` checks for `origin` by name.
- `close` still rebases onto local `main`, not `origin/main` (pre-existing, out of scope).
- A squash-merged branch is treated as unmerged and reopened (by design, per Out of scope).
- `uv.lock` has uncommitted drift from uv, outside the diff.

## Sign-off

Pending.
