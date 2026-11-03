---
status: todo
mode: hands-off
priority: polish
blocked_by: [1, 2, 3]
---
Finish the docs and prove the change stayed small. The README Pick row says to choose the next Feature, usually from the Area's Top 3 in `CHARTER.md`. The Close row says the retro re-ranks the Features by Raises, and still sends an Area with no Features to `/kit:brainstorm` after the merge. Check that every `kit.json` command passes and that no SKILL.md body grew by more than 3 lines since the `pick:` commit.

## Acceptance
- [ ] The README Pick row names the Top 3; the Close row names re-ranking by Raises and keeps `/kit:brainstorm` after the merge
- [ ] A test in `tests/test_skills.py` checks both rows
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass
- [ ] No SKILL.md grew by more than 3 lines since the `pick:` commit

## Verify
uv run pyright && uv run ruff check && uv run pytest -q && p=$(git log --format=%h --grep='^pick: Rank the next Features' -1) && for f in src/kit/plugin/skills/*/SKILL.md; do a=$(git show $p:$f | wc -l); b=$(wc -l < $f); [ $((b-a)) -le 3 ] || { echo "$f grew $((b-a))"; exit 1; }; done && echo OK
