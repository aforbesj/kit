---
name: implement
description: Build exactly one Issue, test first, and commit.
disable-model-invocation: true
---

# Implement

Build **one** Issue from `.agents/cycles/<area>/issues/`, then stop.

1. Read `prd.md` and `progress.txt` in the Cycle folder.
2. If an Issue was named, take it. Otherwise take the unblocked hands-off Issue with `status: todo` and the highest priority, in this order: bug, infra, tracer, polish, refactor. If none is left, print `<promise>COMPLETE</promise>` and stop.
3. Set it to `status: doing`.
4. Use the Explore subagent for codebase questions; read only the files you change.
5. Write a failing test for the Acceptance first. Make it pass. Refactor.
6. Keep modules **deep**: a small interface over a substantial inside. Follow the module interfaces the PRD names; extend them only where the Issue requires.
7. Run every command in `.agents/kit.json` `commands` until all pass, plus the Issue's Verify.
8. Set `status: done`, append three lines to `progress.txt` (Issue, what changed, anything the next pass must know), and commit with message `<issue-number>: <title>`.

When an idea for a Feature comes up, append `raised: <idea>` to `progress.txt`.

**Done when** all commands pass and the commit exists. One Issue per pass.
