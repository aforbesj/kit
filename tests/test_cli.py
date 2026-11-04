import json
import re
import subprocess
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any

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


def test_init_creates_named_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert cli.main(["init", "new-product"]) == 0
    assert (tmp_path / "new-product/.agents/kit.json").exists()


def test_sandbox_run_passes_git_identity(tmp_path: Path) -> None:
    root = product(tmp_path)
    git(root, "config", "user.name", "Ada")
    git(root, "config", "user.email", "ada@example.com")
    config = cli.load_config(root)

    command = cli.agent(config, root, root, "sonnet", "go", hands_off=True, local=False)

    assert command[:2] == ["docker", "run"]
    assert "GIT_COMMITTER_NAME=Ada" in command
    assert "GIT_AUTHOR_EMAIL=ada@example.com" in command


def test_sandbox_mounts_a_venv_volume_per_worktree(tmp_path: Path) -> None:
    root = product(tmp_path)
    config = cli.load_config(root)
    areas = [root / "wt" / name for name in ("core", "other area")]
    for area in areas:
        area.mkdir(parents=True)

    commands = [cli.agent(config, root, area, "sonnet", "go", hands_off=True, local=False) for area in areas]

    names = []
    for command in commands:
        volume = next(arg for arg in command if arg.endswith(f":{cli.VENV_PATH}"))
        names.append(volume.split(":")[0])
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", names[-1])
        assert f"UV_PROJECT_ENVIRONMENT={cli.VENV_PATH}" in command
    assert names == ["kit-venv-product-core", "kit-venv-product-other-area"]


def test_plugin_dir_only_in_the_kit_product(tmp_path: Path) -> None:
    root = product(tmp_path)
    config = cli.load_config(root)
    cwd = root / "wt"
    cwd.mkdir()
    plugin = str(cwd.resolve() / "src" / "kit" / "plugin")

    def commands() -> list[list[str]]:
        return [
            cli.agent(config, root, cwd, "sonnet", "go", hands_off=hands_off, local=local)
            for hands_off, local in ((False, True), (True, True), (True, False))
        ]

    assert all("--plugin-dir" not in c for c in commands())
    (root / "pyproject.toml").write_text('[project]\nname = "other"\n')
    assert all("--plugin-dir" not in c for c in commands())
    (root / "pyproject.toml").write_text('[project]\nname = "kit-cycle"\n')
    for command in commands():
        assert command[command.index("--plugin-dir") + 1] == plugin


@pytest.mark.parametrize(
    ("hours", "expected"),
    [(-5, "<-0500>5"), (2, "<+0200>-2"), (5.5, "<+0530>-5:30"), (-3.5, "<-0330>3:30"), (0, "<+0000>0")],
)
def test_posix_tz_inverts_the_offset_sign(hours: float, expected: str) -> None:
    assert cli.posix_tz(timedelta(hours=hours)) == expected


def test_sandbox_run_passes_host_utc_offset(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    monkeypatch.setattr(cli, "posix_tz", lambda _offset: "<-0500>5")

    command = cli.agent(cli.load_config(root), root, root, "sonnet", "go", hands_off=True, local=False)

    assert "TZ=<-0500>5" in command


def test_run_without_docker_explains_instead_of_crashing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    monkeypatch.setattr(cli.shutil, "which", lambda _name: None)

    with pytest.raises(SystemExit, match="--local"):
        cli.run(root, "core", max_iterations=1, local=False)
    assert not (root / ".worktrees/core").exists()


def test_doctor_fails_only_on_required(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    git(root, "config", "user.email", "ada@example.com")
    monkeypatch.setattr(cli, "_ok", lambda _command: False)
    monkeypatch.setattr(cli.shutil, "which", lambda name: None if name in ("docker", "gh") else f"/bin/{name}")
    assert cli.doctor(root) == 0

    monkeypatch.setattr(cli.shutil, "which", lambda name: None if name == "claude" else f"/bin/{name}")
    assert cli.doctor(root) == 1


def test_sandbox_image_ships_with_the_package() -> None:
    assert (cli.SANDBOX / "Dockerfile").is_file()


@pytest.mark.parametrize("abandon", [False, True])
def test_close_refuses_dirty_checkout(tmp_path: Path, abandon: bool) -> None:
    root = product(tmp_path)
    ws = cli.workspace(root, "core")
    (ws / "scratch.txt").write_text("unsaved")

    assert cli.close(root, "core", abandon=abandon) == 1
    assert (ws / "scratch.txt").read_text() == "unsaved"
    assert git(root, "branch", "--list", "cycle/core")
    assert not git(root, "tag", "--list", "abandoned/*")


def with_origin(tmp_path: Path, root: Path) -> Path:
    origin = tmp_path / "origin.git"
    git(tmp_path, "init", "-q", "--bare", str(origin))
    git(root, "remote", "add", "origin", str(origin))
    git(root, "push", "-q", "origin", "HEAD:main")
    return origin


def test_workspace_branches_from_latest_origin_main(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "-b", "main", str(origin), str(other))
    (other / "new.txt").write_text("x")
    git(other, "add", "-A")
    git(other, "commit", "-m", "ahead")
    git(other, "push", "-q", "origin", "HEAD:main")

    ws = cli.workspace(root, "core")

    assert git(ws, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")


def test_workspace_without_remote_warns_and_uses_local_main(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)

    ws = cli.workspace(root, "core")

    assert git(ws, "rev-parse", "HEAD") == git(root, "rev-parse", "main")
    assert "warning" in capsys.readouterr().out.lower()


def test_workspace_with_failing_fetch_warns_and_uses_local_main(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = product(tmp_path)
    git(root, "remote", "add", "origin", str(tmp_path / "missing.git"))

    ws = cli.workspace(root, "core")

    assert git(ws, "rev-parse", "HEAD") == git(root, "rev-parse", "main")
    assert "warning" in capsys.readouterr().out.lower()


def cycle_branch_with_commit(root: Path, origin: Path) -> None:
    git(root, "switch", "-q", "-c", "cycle/core")
    (root / "work.txt").write_text("w")
    git(root, "add", "-A")
    git(root, "commit", "-m", "work")
    git(root, "push", "-q", "origin", "cycle/core")
    git(root, "switch", "-q", "main")


def test_workspace_removes_merged_branch_and_starts_fresh(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    cycle_branch_with_commit(root, origin)
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "-b", "main", str(origin), str(other))
    git(other, "merge", "-q", "--no-ff", "-m", "merge", "origin/cycle/core")
    git(other, "push", "-q", "origin", "HEAD:main")

    ws = cli.workspace(root, "core")

    assert git(ws, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")
    assert git(origin, "branch", "--list", "cycle/core") == ""


def test_workspace_reopens_unmerged_branch(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    cycle_branch_with_commit(root, origin)
    tip = git(root, "rev-parse", "cycle/core")

    ws = cli.workspace(root, "core")

    assert git(ws, "rev-parse", "HEAD") == tip
    assert git(origin, "rev-parse", "cycle/core") == tip
    assert "Cycle still open: not merged into `main`" in capsys.readouterr().out


def push_ahead(tmp_path: Path, origin: Path) -> Path:
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "-b", "main", str(origin), str(other))
    (other / "new.txt").write_text("x")
    git(other, "add", "-A")
    git(other, "commit", "-m", "ahead")
    git(other, "push", "-q", "origin", "HEAD:main")
    return other


def test_workspace_fast_forwards_clean_root_on_main(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    other = push_ahead(tmp_path, origin)
    git(root, "branch", "-M", "main")

    cli.workspace(root, "core")

    assert git(root, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")


def test_workspace_leaves_dirty_root_alone(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    other = push_ahead(tmp_path, origin)
    git(root, "branch", "-M", "main")
    before = git(root, "rev-parse", "HEAD")
    (root / "scratch.txt").write_text("wip")

    ws = cli.workspace(root, "core")

    assert git(root, "rev-parse", "HEAD") == before
    assert (root / "scratch.txt").read_text() == "wip"
    assert git(ws, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")


def test_workspace_leaves_root_on_other_branch_alone(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    other = push_ahead(tmp_path, origin)
    git(root, "branch", "-M", "main")
    git(root, "checkout", "-q", "-b", "side")
    before = git(root, "rev-parse", "HEAD")

    ws = cli.workspace(root, "core")

    assert git(root, "rev-parse", "HEAD") == before
    assert git(root, "branch", "--show-current") == "side"
    assert git(root, "rev-parse", "main") == before
    assert git(ws, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")


def test_close_abandon_with_remote_keeps_tag_there_and_drops_branch(tmp_path: Path) -> None:
    root = product(tmp_path)
    origin = with_origin(tmp_path, root)
    cli.workspace(root, "core")
    git(root, "push", "-q", "origin", "cycle/core")

    assert cli.close(root, "core", abandon=True) == 0
    assert git(origin, "tag", "--list", "abandoned/core-*")
    assert git(origin, "branch", "--list", "cycle/core") == ""


def test_close_abandon_without_remote_keeps_tag_locally(tmp_path: Path) -> None:
    root = product(tmp_path)
    cli.workspace(root, "core")

    assert cli.close(root, "core", abandon=True) == 0
    assert git(root, "tag", "--list", "abandoned/core-*")


def _assert_next_steps(out: str, merge: str, area: str) -> None:
    steps = [merge, f"kit once {area}", "/kit:grill"]
    positions = [out.find(step) for step in steps]
    assert all(p >= 0 for p in positions), out
    assert positions == sorted(positions)


def test_close_prints_next_steps_with_remote(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    with_origin(tmp_path, root)
    cli.workspace(root, "core")

    assert cli.close(root, "core", abandon=False) == 0
    _assert_next_steps(capsys.readouterr().out, "Merge", "core")


def test_close_prints_next_steps_without_remote(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    cli.workspace(root, "core")

    assert cli.close(root, "core", abandon=False) == 0
    _assert_next_steps(capsys.readouterr().out, "git merge --no-ff cycle/core", "core")


def test_retro_skill_removes_finished_feature_from_charter() -> None:
    text = (Path(__file__).parent.parent / "src/kit/plugin/skills/retro/SKILL.md").read_text()
    assert "Remove the finished Feature" in text
    assert "name the next one" not in text


def last_line(capsys: pytest.CaptureFixture[str]) -> str:
    return capsys.readouterr().out.strip().splitlines()[-1]


def test_stop_reason_complete(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path, complete_after=1)

    assert cli.run(root, "core", max_iterations=5, local=True) == 0
    line = last_line(capsys)
    assert line.startswith("Stop reason: complete: ")
    assert "review clean" in line


def test_stop_reason_cap_reached(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path, complete_after=99)

    assert cli.run(root, "core", max_iterations=2, local=True) != 0
    line = last_line(capsys)
    assert line.startswith("Stop reason: cap reached: ")
    assert "2 passes" in line


def test_stop_reason_agent_failed(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    failing = tmp_path / "failing.py"
    failing.write_text("import sys\nprint('boom happened')\nsys.exit(3)\n")
    config = json.loads((root / ".agents/kit.json").read_text())
    config["agent"] = [sys.executable, str(failing)]
    (root / ".agents/kit.json").write_text(json.dumps(config))

    assert cli.run(root, "core", max_iterations=2, local=True) == 3
    line = last_line(capsys)
    assert line.startswith("Stop reason: agent failed: ")
    assert "implement" in line and "3" in line and "boom happened" in line


def test_stop_reason_interrupted(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = product(tmp_path)

    def interrupt(command: list[str], cwd: Path) -> tuple[str, int]:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "stream", interrupt)

    assert cli.run(root, "core", max_iterations=2, local=True) != 0
    assert last_line(capsys) == "Stop reason: interrupted: Ctrl-C"


def test_self_host_hands_off_to_the_worktree_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    (root / "pyproject.toml").write_text('[project]\nname = "kit-cycle"\n')
    cwd = root / "wt"
    monkeypatch.chdir(root)
    monkeypatch.delenv("KIT_SELF", raising=False)
    monkeypatch.setattr(cli, "workspace", lambda r, a: cwd)
    calls: list[tuple[list[str], dict[str, str]]] = []

    def fake(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs["env"]))
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(cli.subprocess, "run", fake)
    assert cli.main(["run", "core", "--local"]) == 7
    assert cli.main(["once", "core", "001"]) == 7
    assert calls[0][0] == ["uv", "run", "--project", str(cwd), "kit", "run", "core", "--local"]
    assert calls[1][0][-3:] == ["once", "core", "001"]
    assert all(env["KIT_SELF"] == "1" for _, env in calls)

    # Already handed off, or another Product: no hand-off.
    monkeypatch.setenv("KIT_SELF", "1")
    assert cli.hand_off(root, "core", []) is None
    monkeypatch.delenv("KIT_SELF")
    (root / "pyproject.toml").write_text('[project]\nname = "other"\n')
    assert cli.hand_off(root, "core", []) is None


DIRTY_AGENT = """
import pathlib
pathlib.Path("stray.txt").write_text("x")
with open(pathlib.Path(__file__).with_name("dirty.n"), "a") as f:
    f.write("1")
"""


def test_run_stops_when_a_pass_leaves_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    fake = tmp_path / "dirty_agent.py"
    fake.write_text(DIRTY_AGENT)
    config = json.loads((root / ".agents/kit.json").read_text())
    config["agent"] = [sys.executable, str(fake)]
    (root / ".agents/kit.json").write_text(json.dumps(config))
    git(root, "commit", "-qam", "dirty agent")

    assert cli.run(root, "core", max_iterations=5, local=True) != 0

    out = capsys.readouterr().out
    assert out.count("Stop reason:") == 1
    assert "pass 1" in out and "stray.txt" in out
    assert "keep:" in out and "discard:" in out and "then: kit run core" in out
    assert (tmp_path / "dirty.n").read_text() == "1"
    assert out.splitlines()[-1].startswith("Stop reason: dirty tree: pass 1 (implement) left 1 uncommitted: ")
    keep = next(line for line in out.splitlines() if line.startswith("keep:"))
    discard = next(line for line in out.splitlines() if line.startswith("discard:"))
    assert ".worktrees/core" in keep and ".worktrees/core" in discard
    (root / "mine.txt").write_text("mine")
    subprocess.run(discard.removeprefix("discard:").strip(), shell=True, cwd=root, check=True)
    assert not (root / ".worktrees/core/stray.txt").exists()
    assert (root / "mine.txt").exists()


def test_discard_clears_staged_changes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    tree = cli.workspace(root, "core")
    (tree / "staged_new.txt").write_text("x")
    (tree / "kit.txt").write_text("tracked")
    git(tree, "add", "-A")
    git(tree, "commit", "-qm", "base")
    (tree / "kit.txt").write_text("changed")
    (tree / "staged_new.txt").write_text("y")
    (tree / "another.txt").write_text("z")
    git(tree, "add", "-A")
    cli.stop_dirty("core", cli.dirty_files(tree), "pass 1")
    out = capsys.readouterr().out
    discard = next(line for line in out.splitlines() if line.startswith("discard:"))
    (root / "mine.txt").write_text("mine")
    subprocess.run(discard.removeprefix("discard:").strip(), shell=True, cwd=root, check=True)
    assert cli.dirty_files(tree) == []
    assert (root / "mine.txt").exists()


def test_run_refuses_a_dirty_tree_at_start(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    (cli.workspace(root, "core") / "stray.txt").write_text("x")

    assert cli.run(root, "core", max_iterations=5, local=True) != 0

    out = capsys.readouterr().out
    assert "stray.txt" in out and "keep:" in out and "discard:" in out and "then: kit run core" in out
    assert out.splitlines()[-1] == "Stop reason: dirty tree: before start, 1 uncommitted: stray.txt"
    assert not (tmp_path / "calls.log").exists()


def test_once_warns_on_dirty_tree_and_keeps_exit_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = product(tmp_path)
    fake = tmp_path / "once_agent.py"
    fake.write_text("import pathlib, sys\npathlib.Path('stray.txt').write_text('x')\nsys.exit(4)\n")
    config = json.loads((root / ".agents/kit.json").read_text())
    config["agent"] = [sys.executable, str(fake)]
    (root / ".agents/kit.json").write_text(json.dumps(config))
    git(root, "commit", "-qam", "once agent")

    assert cli.once(root, "core", None) == 4

    out = capsys.readouterr().out
    assert "dirty tree:" in out and "stray.txt" in out
    assert out.splitlines()[-1] == "Stop reason: dirty tree: after once, 1 uncommitted: stray.txt"


def test_no_commit_by_run_or_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    seen: list[list[str]] = []
    real_run, real_popen = subprocess.run, subprocess.Popen

    def spy_run(command: Any, *args: Any, **kwargs: Any) -> Any:
        seen.append(list(command))
        return real_run(command, *args, **kwargs)

    def spy_popen(command: Any, *args: Any, **kwargs: Any) -> Any:
        seen.append(list(command))
        return real_popen(command, *args, **kwargs)

    monkeypatch.setattr(cli.subprocess, "run", spy_run)
    monkeypatch.setattr(cli.subprocess, "Popen", spy_popen)
    cli.once(root, "core", None)
    cli.run(root, "core", max_iterations=3, local=True)

    assert seen
    for command in seen:
        assert command[:2] not in (["git", "add"], ["git", "commit"])


@pytest.mark.parametrize(
    ("installed", "wanted", "warns"),
    [
        ("0.1.0", "0.2.0", True),
        ("0.9.0", "0.10.0", True),
        ("0.10.0", "0.9.0", False),
        ("0.2.0", "0.2.0", False),
        ("0.3.0", "0.2.0", False),
        ("0.1.0", None, False),
        ("garbage", "0.2.0", False),
    ],
)
def test_version_warning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, installed: str, wanted: str | None, warns: bool
) -> None:
    root = product(tmp_path)
    config = json.loads((root / ".agents/kit.json").read_text())
    config.pop("kit", None)
    if wanted:
        config["kit"] = wanted
    (root / ".agents/kit.json").write_text(json.dumps(config))
    monkeypatch.setattr(cli.metadata, "version", lambda _name: installed)
    assert (cli.version_warning(root) is not None) is warns


def test_version_warning_unreadable_version(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)

    def missing(_name: str) -> str:
        raise cli.metadata.PackageNotFoundError

    monkeypatch.setattr(cli.metadata, "version", missing)
    assert cli.version_warning(root) is None


def test_doctor_once_and_run_each_warn_once_and_keep_exit_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = product(tmp_path, complete_after=1)
    config = json.loads((root / ".agents/kit.json").read_text())
    config["kit"] = "99.0.0"
    (root / ".agents/kit.json").write_text(json.dumps(config))
    git(root, "commit", "-am", "version")
    git(root, "config", "user.email", "ada@example.com")
    monkeypatch.setattr(cli, "_ok", lambda _command: False)
    monkeypatch.setattr(cli.shutil, "which", lambda name: f"/bin/{name}")

    assert cli.doctor(root) == 0
    assert capsys.readouterr().out.count("Warning: kit") == 1
    assert cli.once(root, "core", None) == 0
    assert capsys.readouterr().out.count("Warning: kit") == 1
    assert cli.run(root, "core", max_iterations=3, local=True) == 0
    assert capsys.readouterr().out.count("Warning: kit") == 1


@pytest.mark.parametrize("abandon", [True, False])
def test_close_removes_venv_volume(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, abandon: bool) -> None:
    root = product(tmp_path)
    cli.workspace(root, "core")
    seen: list[list[str]] = []
    real = subprocess.run

    def spy(command: Any, *args: Any, **kwargs: Any) -> Any:
        if command[0] == "docker":
            seen.append(command)
            raise FileNotFoundError("docker")
        return real(command, *args, **kwargs)

    monkeypatch.setattr(cli.subprocess, "run", spy)
    monkeypatch.setattr(cli, "checks", lambda *a, **k: True, raising=False)

    cli.close(root, "core", abandon=abandon)

    assert ["docker", "volume", "rm", "kit-venv-product-core"] in seen


def test_interrupt_in_hand_off_returns_130_without_traceback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = product(tmp_path)
    (root / "pyproject.toml").write_text('[project]\nname = "kit-cycle"\n')
    monkeypatch.chdir(root)
    monkeypatch.delenv("KIT_SELF", raising=False)
    monkeypatch.setattr(cli, "workspace", lambda r, a: root / "wt")

    def interrupted(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli.subprocess, "run", interrupted)
    assert cli.main(["run", "core", "--local"]) == 130


@pytest.mark.parametrize("step", ["sandbox", "workspace"])
def test_interrupt_before_the_pass_loop_prints_stop_reason(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], step: str
) -> None:
    root = product(tmp_path)

    def interrupted(*args: Any, **kwargs: Any) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, step, interrupted)
    assert cli.run(root, "core", max_iterations=2, local=step == "workspace") == 130
    assert capsys.readouterr().out.splitlines()[-1] == "Stop reason: interrupted: Ctrl-C"


def _docker_available() -> bool:
    try:
        return subprocess.run(["docker", "info"], capture_output=True, check=False).returncode == 0
    except OSError:
        return False


@pytest.mark.skipif(not _docker_available(), reason="needs Docker")
def test_sandbox_leaves_host_venv_alone(tmp_path: Path) -> None:
    root = tmp_path / "venvprod"
    root.mkdir()
    (root / "pyproject.toml").write_text('[project]\nname = "venvprod"\nversion = "0"\nrequires-python = ">=3.9"\n')
    subprocess.run([sys.executable, "-m", "venv", str(root / ".venv")], check=True, capture_output=True)
    config: cli.Config = {"sandbox": {"image": "kit-sandbox"}}
    before = (root / ".venv" / "bin" / "python").resolve()
    volume = cli.venv_volume(root, root)
    cli.sandbox(cli.image_name(config))  # builds the image on a fresh machine, as `kit run` does (CI has none)
    try:
        command = cli.agent(config, root, root, "sonnet", "go", hands_off=True, local=False)
        sync = [*command[: command.index(cli.image_name(config)) + 1], "uv", "sync"]
        subprocess.run(sync, check=True, capture_output=True)

        assert (root / ".venv" / "bin" / "python").resolve() == before
        assert subprocess.run(["docker", "volume", "inspect", volume], capture_output=True, check=False).returncode == 0
    finally:
        subprocess.run(["docker", "volume", "rm", volume], capture_output=True, check=False)


def test_dirty_files_keeps_first_character_of_modified_tracked_file(tmp_path: Path) -> None:
    root = product(tmp_path)
    tree = cli.workspace(root, "core")
    (tree / "tracked.txt").write_text("a")
    git(tree, "add", "-A")
    git(tree, "commit", "-qm", "base")
    (tree / "tracked.txt").write_text("b")
    assert cli.dirty_files(tree) == ["tracked.txt"]


def test_sandbox_rebuilds_an_image_without_the_venv_folder(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[list[str]] = []

    def fake_ok(command: list[str]) -> bool:
        calls.append(command)
        return "test" not in command

    monkeypatch.setattr(cli.shutil, "which", lambda _: "/usr/bin/docker")
    monkeypatch.setattr(cli, "_ok", fake_ok)
    monkeypatch.setattr(cli.subprocess, "run", lambda command, **_: calls.append(command))
    cli.sandbox("kit-sandbox")
    assert calls[-1][:2] == ["docker", "build"]
    assert "USER kit\n" in (cli.SANDBOX / "Dockerfile").read_text()
    assert (cli.SANDBOX / "Dockerfile").read_text().index("USER kit") < (cli.SANDBOX / "Dockerfile").read_text().index(
        "mkdir /home/kit/venv"
    )
