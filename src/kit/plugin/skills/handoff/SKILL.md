---
name: handoff
description: Use when the session's context passes about 80k tokens (handoffTokens in .agents/kit.json), or the human asks for a handoff.
---

# Handoff

Quality drops as context grows, so move to a fresh one.

1. Write `.agents/handoff.md`: the goal, decisions made, files touched, the exact next step. Under 30 lines.
2. Tell the human: run `/clear`, then say "read .agents/handoff.md and continue".

A fresh context plus a handoff behaves the same every time; a compacted one depends on what the summary kept.
