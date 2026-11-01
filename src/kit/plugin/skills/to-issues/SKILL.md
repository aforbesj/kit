---
name: to-issues
description: Split the Cycle's PRD into small, evenly sized Issues for human approval.
disable-model-invocation: true
---

# To Issues

Split `.agents/cycles/<area>/prd.md` into **vertical slices**: each Issue cuts through every layer it touches and is built, tested and verified in one pass.

1. Explore the code the PRD's What changes names.
2. Draft the list. The first Issue is the **tracer bullet**: the thinnest path from input to output. Later Issues widen it. Any Issue too big for one pass becomes two.
3. Show the list (title, one line, blockers, mode) and wait for the human's approval or edits.
4. Write each approved Issue to `.agents/cycles/<area>/issues/NNN-slug.md`:

```markdown
---
status: todo          # todo | doing | done
mode: hands-off       # hands-off | hands-on
priority: tracer      # bug | infra | tracer | polish | refactor
blocked_by: []        # Issue numbers
---
<one paragraph: what this slice does, end to end>

## Acceptance
- [ ] <check>

## Verify
<one command that proves it>
```

5. Commit with message `split: <feature>` and tell the human to start Build with `kit run <area>`.
