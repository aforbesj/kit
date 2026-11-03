# 10. A Kit Cycle builds and QAs with its own working copy

## Decision

When the Product is the Kit itself (`pyproject` name `kit-cycle`), `kit` hands off to the worktree's own CLI and launches `claude` with `--plugin-dir <worktree>/src/kit/plugin`. Every other Product keeps using the installed `kit` and plugin, unchanged. This is an exception for the Kit, not the normal path.

## Why

A Cycle that changes the Kit has to build and QA with the Kit it is changing. Otherwise QA tests `main` and the changes go unexercised until after they merge.

## Cost

The Kit takes a different path from every Product it serves, so a bug that only shows up on the installed path can get through a Kit Cycle.
