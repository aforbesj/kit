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

## Out of scope
- <what this Cycle will not touch>

## What changes
- <modules or files touched>
- Sample data: data/<dated-folder>/  (or "none")
```

Write the Appetite the grill set; if the grill used the default, write `2 hours, 5 Issues, 2 QA rounds (default)`.

Every Done when line is a number or a yes/no check. Mark each one `(test)` if a test case can check it, `(validation)` if it needs Sample data.

Commit the file with message `plan: <feature>`. From now on the PRD is **locked**: nobody edits it during the Cycle. Tell the human to run `/kit:to-issues`.
