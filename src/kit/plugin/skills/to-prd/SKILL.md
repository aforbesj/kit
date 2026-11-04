---
name: to-prd
description: Turn the finished Cycle grill into the Cycle's locked PRD.
disable-model-invocation: true
---

# To PRD

Write `.agents/cycles/<area>/prd.md` from the grill in this conversation. Ask for the Area if unclear. Write only what the grill settled; list anything unsettled under Open and stop.

```markdown
# <Feature>

Appetite: <elapsed time, Issues, QA rounds from the grill>

## Problem
<what is wrong, in a few sentences>

## End state
<what the data or system looks like when done>

## Done when
- <measurable target>
- <measurable target>

## QA steps

1. `<one literal command, run from the worktree root>`: see <what you should see>. Proves: <the Done when line>. Timeout: <optional, e.g. 10m; default 5m>

### Host steps

2. `<command that must run on the host, e.g. needs Docker>`: see <what you should see>. Proves: <the Done when line>.

## Out of scope
- <what this Cycle will not touch>

## What changes
- <modules or files touched>
- Sample data: data/<dated-folder>/  (or "none")
```

Write the Appetite the grill set; if the grill used the default, write `2 hours, 5 Issues, 2 QA rounds (default)`.

Every Done when line is a number or a yes/no check. Mark each one `(test)` if a test case can check it, `(validation)` if it needs Sample data.

Every QA step is a command `kit run` runs itself, with no agent: `see:` is what you should see, `proves:` is the Done when line it covers, and `timeout:` is optional (s or m). Steps run in the sandbox by default; list under `### Host steps` only those that must run on the host. Reject any step that needs a manual action (going to a folder, clicking, eyeballing a screen): that belongs to the human's Hunt in `/kit:qa`.

The PRD needs at least one QA step. This skill won't commit a PRD without at least one QA step: if the grill settled none, list it under Open and stop.

Commit the file with message `plan: <feature>`. From now on the PRD is **locked**: nobody edits it during the Cycle. Tell the human to run `/kit:to-issues`.
