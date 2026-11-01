import json
import subprocess
import sys
from pathlib import Path

import pytest

from kit import cli

FAKE_AGENT = """
import pathlib, sys
prompt = sys.argv[-1]
log = pathlib.Path(__file__).with_name("calls.log")
calls = log.read_text().splitlines() if log.exists() else []
kind = "review" if "# Review" in prompt else "implement"
calls.append(kind)
log.write_text("\\n".join(calls))
implements = calls.count("implement")
if kind == "implement" and implements >= {complete_after}:
    print("<promise>COMPLETE</promise>")
if kind == "review":
    print("<promise>CLEAN</promise>")
"""


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture(autouse=True)
def git_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
        monkeypatch.setenv(key, "Test")
    for key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
        monkeypatch.setenv(key, "test@example.com")


def product(tmp_path: Path, complete_after: int = 2) -> Path:
    root = tmp_path / "product"
    root.mkdir()
    cli.init(root)
    config = json.loads((root / ".agents/kit.json").read_text())
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT.replace("{complete_after}", str(complete_after)))
    config["agent"] = [sys.executable, str(fake)]
    config["commands"] = {"test": "true"}
    (root / ".agents/kit.json").write_text(json.dumps(config))
    git(root, "add", "-A")
    git(root, "commit", "-m", "init")
    return root


def calls(tmp_path: Path) -> list[str]:
    return (tmp_path / "calls.log").read_text().splitlines()


def test_init_writes_template_and_never_overwrites(tmp_path: Path) -> None:
    (tmp_path / "CHARTER.md").write_text("mine")
    written = cli.init(tmp_path)

    assert (tmp_path / "CHARTER.md").read_text() == "mine"
    assert tmp_path / "CHARTER.md" not in written
    assert (tmp_path / ".agents/kit.json").exists()
    assert (tmp_path / "data/out").is_dir()
    assert (tmp_path / ".git").exists()
    assert cli.init(tmp_path) == []


def test_init_adds_ignore_lines_once(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text("node_modules/")
    cli.init(tmp_path)
    cli.init(tmp_path)

    lines = (tmp_path / ".gitignore").read_text().splitlines()
    assert lines[0] == "node_modules/"
    assert lines.count("data/") == 1
    assert ".worktrees/" in lines


def test_prompt_uses_skill_body_without_frontmatter(tmp_path: Path) -> None:
    root = product(tmp_path)
    text = cli.prompt("implement", "core", root)

    assert text.startswith("# Implement")
    assert "disable-model-invocation" not in text
    assert ".agents/cycles/core/" in text


def test_run_builds_until_complete_then_reviews(tmp_path: Path) -> None:
    root = product(tmp_path, complete_after=2)

    assert cli.run(root, "core", max_iterations=5, local=True) == 0
    assert calls(tmp_path) == ["implement", "implement", "review"]
    assert (root / ".worktrees/core").is_dir()
    assert git(root, "branch", "--list", "cycle/core")


def test_run_stops_at_iteration_cap(tmp_path: Path) -> None:
    root = product(tmp_path, complete_after=99)

    assert cli.run(root, "core", max_iterations=3, local=True) == 1
    assert calls(tmp_path) == ["implement"] * 3


def test_close_abandon_tags_branch_and_frees_area(tmp_path: Path) -> None:
    root = product(tmp_path)
    cli.workspace(root, "core")

    assert cli.close(root, "core", abandon=True) == 0
    assert git(root, "tag", "--list", "abandoned/core-*")
    assert not git(root, "branch", "--list", "cycle/core")
    assert not (root / ".worktrees/core").exists()


def test_close_runs_checks_and_deletes_plan(tmp_path: Path) -> None:
    root = product(tmp_path)
    ws = cli.workspace(root, "core")
    plan = ws / ".agents/cycles/core"
    plan.mkdir(parents=True)
    (plan / "prd.md").write_text("# Feature")
    git(ws, "add", "-A")
    git(ws, "commit", "-m", "plan")

    assert cli.close(root, "core", abandon=False) == 0
    assert "close: core" in git(root, "log", "cycle/core", "--oneline", "-1")
    assert not (root / ".worktrees/core").exists()


def test_close_stops_when_checks_fail(tmp_path: Path) -> None:
    root = product(tmp_path)
    config = json.loads((root / ".agents/kit.json").read_text())
    config["commands"] = {"test": "false"}
    (root / ".agents/kit.json").write_text(json.dumps(config))
    git(root, "commit", "-am", "failing check")
    cli.workspace(root, "core")

    assert cli.close(root, "core", abandon=False) == 1
    assert (root / ".worktrees/core").exists()
