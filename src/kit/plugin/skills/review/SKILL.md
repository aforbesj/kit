---
name: review
description: Validate the Cycle on Sample data and review its diff against the standards and PRD.
disable-model-invocation: true
---

# Review

You did not write this code. Check it with fresh eyes.

1. Read `.agents/cycles/<area>/prd.md` and `git diff main...HEAD`.
2. **Validation**: if the PRD names a Sample data folder, run the Feature on it, write results to `data/out/<area>/`, and check every `(validation)` line of Done when. Record each number you measured.
3. **Review** the diff on two axes:
   - Standards: the stack standards and project differences given below.
   - Spec: every Done when line and Acceptance box is met; nothing outside the PRD's scope changed.
4. For each failure, write a new Issue (`priority: bug`, `mode: hands-off`) whose Acceptance starts with a failing test that reproduces it.
5. Append a summary to `progress.txt`: what passed, the measured numbers, the Issues written. Commit.

When an idea for a Feature comes up, append `raised: <idea>` to `progress.txt`.

If you wrote no Issues, print `<promise>CLEAN</promise>`.
