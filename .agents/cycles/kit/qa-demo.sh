#!/usr/bin/env bash
# QA demo: a throwaway origin + root checkout, then drive kit's workspace and close.
set -euo pipefail
KIT=${KIT_DIR:?set KIT_DIR to the kit worktree}
D=$(mktemp -d); cd "$D"
git init -q --bare -b main origin.git
git clone -q origin.git root 2>/dev/null; cd root
git commit -q --allow-empty -m init && git push -q -u origin main
py() { VIRTUAL_ENV= uv run --project "$KIT" python -c "import sys; from pathlib import Path; from kit import cli; r=cli.$1; print('->', r)"; }

echo "== 1. fresh Cycle Branch starts from origin/main"
py 'workspace(Path("."), "demo")'
git log --oneline -1 cycle/demo; git log --oneline -1 origin/main

echo "== 2. close refuses a dirty checkout"
touch .worktrees/demo/dirty.txt
py 'close(Path("."), "demo", True)' || true
rm .worktrees/demo/dirty.txt

echo "== 3. unmerged branch is reopened"
git -C .worktrees/demo commit -q --allow-empty -m "work"
git worktree remove .worktrees/demo
py 'workspace(Path("."), "demo")'

echo "== 4. merge it, then workspace deletes it (local+remote) and starts fresh"
git -C .worktrees/demo push -q -u origin cycle/demo
git worktree remove .worktrees/demo
git merge -q --no-ff -m "merge cycle/demo" cycle/demo && git push -q origin main
git checkout -q -b other && git checkout -q main   # root stays clean on main
py 'workspace(Path("."), "demo")'
echo "cycle/demo HEAD: $(git rev-parse --short cycle/demo)  origin/main: $(git rev-parse --short origin/main)"
echo "remote branches:"; git ls-remote --heads origin

echo "== 5. abandon pushes the tag and drops the remote branch"
git -C .worktrees/demo commit -q --allow-empty -m "doomed" && git -C .worktrees/demo push -q -u origin cycle/demo
py 'close(Path("."), "demo", True)'
git ls-remote origin
echo "demo dir: $D"
