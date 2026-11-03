# 7. A Cycle ends when its Cycle Branch merges

## Decision

A Cycle ends when `cycle/<area>` is merged into `main` by a merge commit. The next `kit once` or `kit run` detects this by ancestry against the freshly fetched `origin/main`, deletes the branch locally and on the remote, and starts a new Cycle Branch from `origin/main`. An unmerged branch is reopened untouched.

## Why

The loop goes straight from merge to the next grill with no cleanup step, no new command, and no CLI parsing of the Charter.

## Cost

Squash and rebase merges are not detected: the branch counts as unmerged and is reopened. Users must not rely on deleting Cycle Branches themselves, and the CLI deletes remote branches on their behalf.
