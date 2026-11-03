from pathlib import Path

SKILLS = Path(__file__).parent.parent / "src/kit/plugin/skills"


def _brainstorm() -> str:
    return (SKILLS / "brainstorm/SKILL.md").read_text()


def _body(text: str) -> list[str]:
    return text.split("---\n", 2)[2].strip().splitlines()


def test_brainstorm_skill_is_manual_only() -> None:
    text = _brainstorm()
    assert "name: brainstorm\n" in text
    assert "disable-model-invocation: true\n" in text


def test_brainstorm_ends_at_grill_and_writes_no_file() -> None:
    body = _body(_brainstorm())
    assert "/kit:grill" in body[-1]
    assert not any(
        "write" in line.lower() and "file" in line.lower() and "no file" not in line.lower() for line in body
    )


def test_brainstorm_body_is_short() -> None:
    assert len(_body(_brainstorm())) <= 25


def test_grill_points_empty_charter_to_brainstorm_and_widens_after_one() -> None:
    text = (SKILLS / "grill/SKILL.md").read_text()
    assert "/kit:brainstorm" in text
    assert "Charter grill" in text
    assert "after a Brainstorm" in text
    assert "add Features" in text and "widen scope" in text


def test_template_charter_names_charter_grill_and_retro() -> None:
    text = (SKILLS.parent.parent / "template/CHARTER.md").read_text()
    assert "only a retro edits it" not in text
    assert "Charter grill" in text and "retro" in text


def test_retro_points_empty_area_to_brainstorm() -> None:
    text = (SKILLS / "retro/SKILL.md").read_text()
    assert "/kit:brainstorm" in text
    assert "Remove the finished Feature from `CHARTER.md` and name the next one" in text


ROOT = Path(__file__).parent.parent


def test_claude_md_copies_match_and_name_brainstorm() -> None:
    a = (ROOT / "CLAUDE.md").read_text()
    assert a == (ROOT / "src/kit/template/CLAUDE.md").read_text()
    phases = next(line for line in a.splitlines() if line.startswith("Phases:"))
    assert "Brainstorm" in phases


def test_readme_names_brainstorm_in_start_and_close() -> None:
    text = (ROOT / "README.md").read_text()
    start = text.split("## Start a Product")[1].split("## Run a Cycle")[0]
    close = next(line for line in text.splitlines() if line.startswith("| Close"))
    assert "/kit:brainstorm" in start
    assert "/kit:brainstorm" in close


def test_retro_runs_brainstorm_after_close_and_merge() -> None:
    text = (SKILLS / "retro/SKILL.md").read_text()
    assert text.index("kit close <area>") < text.index("/kit:brainstorm")
    assert "after the merge" in text


def test_readme_close_row_brainstorms_after_merge() -> None:
    text = (ROOT / "README.md").read_text()
    close = next(line for line in text.splitlines() if line.startswith("| Close"))
    assert close.index("After the merge") < close.index("/kit:brainstorm")
    assert close.index("/kit:grill") < close.index("/kit:brainstorm")


def test_plugin_description_names_brainstorm_before_grill() -> None:
    import json

    manifest = json.loads((SKILLS.parent / ".claude-plugin/plugin.json").read_text())
    desc = manifest["description"].lower()
    assert "loop: brainstorm" not in desc
    assert desc.index("brainstorm") < desc.index("grill")


def test_marketplace_description_matches_plugin_manifest() -> None:
    import json

    manifest = json.loads((SKILLS.parent / ".claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    entry = next(p for p in market["plugins"] if p["name"] == "kit")
    assert entry["description"] == manifest["description"]


def test_adr_numbers_are_unique() -> None:
    adrs = Path(__file__).parent.parent / "docs/adr"
    numbers = [p.name.split("-", 1)[0] for p in adrs.glob("*.md")]
    assert len(numbers) == len(set(numbers))


def test_cycle_ends_at_merge_is_adr_7() -> None:
    adrs = Path(__file__).parent.parent / "docs/adr"
    assert not (adrs / "0001-cycle-ends-at-merge.md").exists()
    text = (adrs / "0007-cycle-ends-at-merge.md").read_text()
    assert text.startswith("# 7. ")


DEFAULT_APPETITE = "2 hours, 5 Issues, 2 QA rounds"


def _skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text()


def test_grill_asks_cycle_appetite_first_with_default() -> None:
    text = _skill("grill")
    assert "Appetite" in text
    assert DEFAULT_APPETITE in text
    assert text.index("Appetite") < text.index("Map the decisions")


def test_grill_commits_pick_when_frontier_is_empty() -> None:
    assert "`pick: <feature>`" in _skill("grill")


def test_grill_pick_commit_lands_with_no_changes() -> None:
    text = _skill("grill")
    assert "--allow-empty" in text
    assert "pick: <feature>" in text


def test_to_prd_template_has_appetite_line() -> None:
    text = _skill("to-prd")
    assert "Appetite:" in text
    assert "(default)" in text


def test_retro_measures_cycle_against_appetite() -> None:
    text = _skill("retro")
    assert "Appetite" in text
    for word in ("`pick:`", "`qa:`", "Issue", DEFAULT_APPETITE):
        assert word in text
    assert "`pick:` commit to now" in text
    assert "`close:`" not in text


def test_to_issues_stops_before_committing_when_split_passes_appetite() -> None:
    text = _skill("to-issues")
    assert "Appetite" in text
    assert DEFAULT_APPETITE in text
    assert "shrink the split, or was the grill too big?" in text
    assert text.index("Appetite") < text.index("Write each approved Issue")


def test_qa_asks_when_a_round_passes_appetite_before_writing_issues() -> None:
    text = _skill("qa")
    assert "Appetite" in text
    assert "`qa:`" in text
    assert DEFAULT_APPETITE in text
    assert "a new Issue, or was the PRD wrong?" in text
    assert "`progress.txt`" in text.split("was the PRD wrong?")[1]
    assert text.index("was the PRD wrong?") < text.index("write a new Issue")


def test_brainstorm_asks_appetite_then_filters_before_directions() -> None:
    text = "\n".join(_body(_brainstorm()))
    assert "Appetite" in text
    assert text.index("Appetite") < text.index("rules Directions out") < text.index("five to eight")


def test_brainstorm_names_meeting_notes_and_transcripts_as_evidence() -> None:
    text = _brainstorm().lower()
    assert "meeting notes" in text and "transcripts" in text


def test_brainstorm_offers_five_to_eight_directions_including_no_software() -> None:
    text = _brainstorm()
    assert "five to eight" in text
    assert "builds no software" in text


def test_brainstorm_last_line_restates_direction_appetite_and_words() -> None:
    last = _body(_brainstorm())[-1]
    assert "Direction" in last and "Appetite" in last and "words" in last
    assert "/kit:grill" in last
