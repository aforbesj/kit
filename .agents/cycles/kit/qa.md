# QA: Brainstorm what to build before a Charter grill

QA round 2, after bug Issues 004-006.

## Done when

| Done when | Result (from `progress.txt` Review 3, re-run at QA) |
|---|---|
| `brainstorm/SKILL.md` exists, `name: brainstorm`, `disable-model-invocation: true` | Met (001; test in `tests/test_skills.py`) |
| Brainstorm names `/kit:grill` as last step, no instruction to write a file | Met (001) |
| Brainstorm body is 25 lines or fewer | Met (body is 13 lines) |
| Grill names `/kit:brainstorm` for an empty Charter; Charter grill on a filled Charter after a Brainstorm | Met (001) |
| Retro names `/kit:brainstorm` for an Area with no next Feature; keeps "Remove the finished Feature..." | Met (002, order fixed in 004) |
| Template `CHARTER.md` drops "only a retro edits it", names Charter grill and retro | Met (002) |
| Both `CLAUDE.md` files identical; Phases line names Brainstorm | Met (003) |
| `README.md` names `/kit:brainstorm` in Start a Product and Close | Met (003, order fixed in 004) |
| pyright, ruff check, pytest pass | Met: pyright 0 errors, ruff clean, pytest 43 passed (re-run at QA) |

Bug Issues from round 1:
- 004: Brainstorm runs after `kit close` and the merge, from the latest `main` (retro skill + README Close row). Done.
- 005: `plugin.json` description names brainstorm. Done.
- 006 (found at Review 2): `marketplace.json` description matches `plugin.json`; a test keeps them in sync. Done.

## See it work

```sh
uv run pytest -q tests/test_skills.py
git diff a8747d0..HEAD -- src README.md .claude-plugin   # everything since round 1
tail -1 src/kit/plugin/skills/retro/SKILL.md
```

## Worth reading in the diff

- `src/kit/plugin/skills/retro/SKILL.md` last line: the brainstorm hint now comes after "run `kit close`", as an "after the merge" note.
- `README.md` Close row: "`/kit:brainstorm` instead, also after the merge".
- `src/kit/plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`: one-word change each.

## Findings

### Round 2

Human approved the order in 004 (retro, `kit close`, merge, then `/kit:brainstorm` from `main`) and the description sync in 006.

Bugs (new Issues):
- 007: the descriptions put brainstorm inside "The Cycle loop". A Brainstorm comes before a Charter grill, not inside a Cycle. Human confirmed it may still run when an Area runs out of Features, so only the wording changes.

For the retro (not this PRD):
- Build agents kept stopping with "set an identity and commit" (003, 005, 006 left staged but uncommitted). Cause: the `kit` on PATH was a stale non-editable uv tool install (v0.1.0, from before `git_identity`), so the sandbox got no git name or email. Fix on the host: `uv tool install --force --editable <kit repo>`. Kit idea: `kit doctor` could warn when the installed `kit` is older than the Product's `.agents/kit.json` "kit" version.

### Round 1

Human tried it with the branch's plugin (`claude --plugin-dir`): the Brainstorm works as wanted, grill step 1 is clear.

Bugs (new Issues):
- 004: Brainstorm comes after the merge, not on the Cycle branch (human's call: a Brainstorm may come days later as new work).
- 005: `plugin.json` description must name brainstorm (consistency with the other skills it lists).

For the retro (not this PRD):
- The Kit's own `CHARTER.md` In scope list omits brainstorm; the Charter is not edited mid-Cycle (ADR 0006), so the retro fixes it.
- QA should be agent-driven: an agent launches what was built, follows the qa.md steps, explores, and reports findings before the human judges. Today the human had to work out how to load the branch's CLI and plugin (`uv run kit init`, `claude --plugin-dir`). Applies to every Cycle, not just skills: UIs, CLIs, apps.
- Naming a Product after a Brainstorm: the folder is made by `kit init` before the Brainstorm settles what it is, so the name is a guess.
