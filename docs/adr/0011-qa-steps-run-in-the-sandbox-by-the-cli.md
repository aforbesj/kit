# 11. QA steps run in the sandbox, by the CLI, not an agent

## Decision

After `review clean`, `kit run` runs the PRD's QA steps itself, literally, and records exit codes and output in `qa.md`. No agent runs on the host. Steps run in the sandbox container by default. Only steps listed under the PRD's `### Host steps` run on the host, with a scrubbed environment (no tokens or cloud credentials, a throwaway `HOME`), the worktree as working directory, and a timeout that kills the step's process tree. The human judges the results and Hunts in `/kit:qa`, where `launch` runs on the host unscrubbed because the human is watching.

## Why

QA steps execute code the Build agent wrote hands-off. On the host that code can reach the human's files, credentials and production services; in the sandbox it can only reach the repo. Running commands the human approved, rather than letting an agent decide, keeps QA contained and keeps the Build from judging itself.

## Cost

A step must be a literal command: anything that needs a person (clicking, judging a picture) belongs to the Hunt. Host steps still run Build-written code on the host, contained only by scrubbing and a timeout.
