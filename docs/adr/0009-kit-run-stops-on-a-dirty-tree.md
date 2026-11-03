# 9. `kit run` stops on a dirty tree, never commits for the agent

## Decision

After every agent pass, `kit run` checks `git status`. If anything is uncommitted, it stops, lists the files and exits non-zero. It never stages or commits work itself, and it never gives the agent an extra pass to tidy up. Every run ends with a Stop reason.

## Why

A Build left running is only trustworthy if a dirty tree can't slip by. A loud stop shows the failure at the pass that caused it. An automatic `wip:` commit would hide it inside history.

## Cost

A run that a single `git commit` would have saved still stops, and the human restarts it by hand.
