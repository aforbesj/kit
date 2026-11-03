# Close a Cycle and start the next

## Problem

Going from one Cycle to the next takes manual Git cleanup. After a merge, the local and remote Cycle Branches remain, so the next `kit once` or `kit run` checks out the merged branch instead of starting fresh. A new Cycle Branch starts from whatever the root checkout holds, which may be an old `main`. `kit close` destroys uncommitted work in the checkout, `--abandon` leaves its remote branch behind and its tag local, and a finished Feature stays in the Charter. The loop should move straight from merge to the next grill.

## End state

A Cycle ends when its Cycle Branch merges. `kit close` still only opens the PR. After the merge, `kit once <area>` or `kit run <area>` is the only step needed to start the next Cycle: it removes the merged Cycle Branch and creates a new one from the latest `main`. No command is added, and the CLI does not read the Charter.

## Done when

- With `cycle/<area>` merged into `main` by a merge commit and no checkout present, creating the checkout deletes the old branch locally and on the remote, and the new `cycle/<area>` HEAD equals the latest `origin/main`. (test)
- When the root checkout is clean and on `main`, creating the checkout fast-forwards it to `origin/main`. (test)
- When the root checkout is dirty or on another branch, it is left unchanged, and the new Cycle Branch still starts from the latest `origin/main`. (test)
- With an unmerged `cycle/<area>`, creating the checkout reopens that branch with its commits intact, deletes nothing, and prints "Cycle still open: not merged into `main`". (test)
- With no remote, or when the fetch fails, creating the checkout prints a warning, starts from local `main`, and does not exit with an error. (test)
- `kit close <area>` on a checkout with uncommitted changes returns 1, and the checkout, its changes and the remote are unchanged. (test)
- `kit close <area> --abandon` on a checkout with uncommitted changes returns 1, creates no tag, and leaves the checkout, its changes and the branch unchanged. (test)
- A successful `kit close <area>` prints the next steps: merge, `kit once <area>`, `/kit:grill`. (test)
- `kit close <area> --abandon` with a remote leaves the tag on the remote and `cycle/<area>` gone from the remote. (test)
- `kit close <area> --abandon` with no remote still returns 0 and keeps the tag locally. (test)
- The `retro` skill tells the agent to remove the finished Feature from `CHARTER.md` and name the next one. (test)
- Every command in `.agents/kit.json` passes. (test)

## Out of scope

- A new CLI command.
- The CLI reading or parsing the Charter.
- `kit close` merging the PR.
- A check that the retro ran before `kit close`.
- QA sign-off (Feature 4).
- Detecting squash merges: a squash-merged branch counts as unmerged and is reopened.

## What changes

- `src/kit/cli.py`: `workspace` and `close`.
- `src/kit/plugin/skills/retro/SKILL.md`.
- `README.md`: the Close step.
- `tests/`.
- `CONTEXT.md`: a Cycle ends when its Cycle Branch merges.
- Sample data: none
