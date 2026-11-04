"""kit: four commands that run the Cycle loop (init, once, run, close), and doctor to check the machine."""

from __future__ import annotations

import argparse
import functools
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
from collections.abc import Callable
from datetime import date, datetime, timedelta
from importlib import metadata
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).parent
TEMPLATE = PACKAGE / "template"
SKILLS = PACKAGE / "plugin" / "skills"
STANDARDS = PACKAGE / "standards"
SANDBOX = PACKAGE / "sandbox"
TOKENS = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")
IGNORE_LINES = ("data/", ".worktrees/", ".agents/handoff.md", "qa.md", "qa-logs/")
COMPLETE = "<promise>COMPLETE</promise>"
CLEAN = "<promise>CLEAN</promise>"

Config = dict[str, Any]


def git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def init(root: Path) -> list[Path]:
    """Copy the Product template into root, writing only missing files."""
    if not (root / ".git").exists():
        git(root, "init", "-q", "-b", "main")
    written: list[Path] = []
    for source in sorted(TEMPLATE.rglob("*")):
        target = root / source.relative_to(TEMPLATE)
        if source.is_dir() or target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        written.append(target)
    (root / "data" / "out").mkdir(parents=True, exist_ok=True)
    _add_ignore_lines(root / ".gitignore")
    return written


def _add_ignore_lines(path: Path) -> None:
    text = path.read_text() if path.exists() else ""
    missing = [line for line in IGNORE_LINES if line not in text.splitlines()]
    if missing:
        prefix = "\n" if text and not text.endswith("\n") else ""
        path.write_text(text + prefix + "\n".join(missing) + "\n")


def load_config(root: Path) -> Config:
    path = root / ".agents" / "kit.json"
    if not path.exists():
        raise SystemExit("No .agents/kit.json here. Run `kit init` first.")
    config: Config = json.loads(path.read_text())
    return config


def _numbers(version: str) -> tuple[int, ...] | None:
    parts = version.split(".")
    return tuple(int(p) for p in parts) if parts and all(p.isdigit() for p in parts) else None


def version_warning(root: Path) -> str | None:
    """One warning line when the installed kit is older than the Product's `kit.json`; else None."""
    try:
        wanted = json.loads((root / ".agents" / "kit.json").read_text()).get("kit")
        installed = metadata.version("kit-cycle")
    except (OSError, ValueError, AttributeError, metadata.PackageNotFoundError):
        return None
    if not isinstance(wanted, str):
        return None
    have, need = _numbers(installed), _numbers(wanted)
    if have is None or need is None or have >= need:
        return None
    return f"Warning: kit {installed} is older than this Product's {wanted}. Fix: ./setup.sh in the Kit checkout"


def warn_version(root: Path) -> None:
    if message := version_warning(root):
        print(message)


def workspace(root: Path, area: str) -> Path:
    """The Area's own checkout on branch cycle/<area>, created on first use."""
    path = root / ".worktrees" / area
    if not path.exists():
        branch = f"cycle/{area}"
        base = _latest_main(root)
        known = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", branch], check=False, cwd=root, capture_output=True
        )
        if known.returncode == 0 and not _merged(root, branch, base):
            print("Cycle still open: not merged into `main`")
            git(root, "worktree", "add", "-q", str(path), branch)
            return path
        if known.returncode == 0:
            git(root, "branch", "-q", "-D", branch)
            if "origin" in git(root, "remote").split():
                subprocess.run(
                    ["git", "push", "-q", "origin", "--delete", branch], check=False, cwd=root, capture_output=True
                )
        git(root, "worktree", "add", "-q", "-b", branch, str(path), base)
    return path


def _merged(root: Path, branch: str, base: str) -> bool:
    done = subprocess.run(
        ["git", "merge-base", "--is-ancestor", branch, base], check=False, cwd=root, capture_output=True
    )
    return done.returncode == 0


def _latest_main(root: Path) -> str:
    """The ref a new Cycle Branch starts from: origin/main after a fetch, else local main."""
    main = load_config(root).get("main", "main") if (root / ".agents" / "kit.json").exists() else "main"
    if not git(root, "remote"):
        print(f"Warning: no remote; starting from local {main}.")
        return main
    fetched = subprocess.run(["git", "fetch", "-q", "origin"], check=False, cwd=root, capture_output=True)
    if fetched.returncode != 0:
        print(f"Warning: fetch from origin failed; starting from local {main}.")
        return main
    if git(root, "branch", "--show-current") == main and not git(root, "status", "--porcelain"):
        subprocess.run(
            ["git", "merge", "-q", "--ff-only", f"origin/{main}"], check=False, cwd=root, capture_output=True
        )
    return f"origin/{main}"


def prompt(skill: str, area: str, cwd: Path, extra: str = "") -> str:
    text = (SKILLS / skill / "SKILL.md").read_text()
    body = text.split("---", 2)[2] if text.startswith("---") else text
    parts = [
        body.strip(),
        f"Area: {area}. Cycle folder: .agents/cycles/{area}/",
        "Recent commits:\n" + git(cwd, "log", "--oneline", "-5"),
    ]
    return "\n\n".join([*parts, extra] if extra else parts)


def standards(config: Config, cwd: Path) -> str:
    stack = STANDARDS / f"{config.get('stack', 'python')}.md"
    project = cwd / ".agents" / "standards.md"
    texts = [p.read_text() for p in (stack, project) if p.exists()]
    return "\n\n".join(texts)


def agent(
    config: Config,
    root: Path,
    cwd: Path,
    model: str,
    text: str,
    *,
    hands_off: bool,
    local: bool,
    name: str | None = None,
) -> list[str]:
    base: list[str] = [*config.get("agent", ["claude"]), *plugin_args(root, cwd)]
    if not hands_off:
        return [*base, "--permission-mode", "acceptEdits", "--model", model, text]
    if local:
        return [*base, "-p", "--permission-mode", "acceptEdits", "--model", model, text]
    secrets = [arg for key in TOKENS if key in os.environ for arg in ("-e", key)]
    tail = [*base, "-p", "--dangerously-skip-permissions", "--model", model, text]
    return docker_run(config, root, cwd, tail, secrets, name)


def docker_run(
    config: Config, root: Path, cwd: Path, tail: list[str], secrets: list[str] | None = None, name: str | None = None
) -> list[str]:
    """The sandbox `docker run` command: same image, mounts and working directory for the agent and QA steps.

    A `name` lets the caller `docker kill` the container; killing the `docker run` client alone would leave it running.
    """
    repo = str(root.resolve())
    return [
        "docker", "run", "--rm", *(["--name", name] if name else []), *(secrets or []), *git_identity(root), "-e", f"TZ={posix_tz(datetime.now().astimezone().utcoffset())}",
        "-v", f"{repo}:{repo}",
        "-v", f"{repo}/data:{repo}/data:ro",
        "-v", f"{repo}/data/out:{repo}/data/out",
        "-v", f"{venv_volume(root, cwd)}:{VENV_PATH}", "-e", f"UV_PROJECT_ENVIRONMENT={VENV_PATH}",
        "-w", str(cwd.resolve()), image_name(config),
        *tail,
    ]  # fmt: skip


VENV_PATH = "/home/kit/venv"


def is_kit(root: Path) -> bool:
    """True when the Product is the Kit itself: pyproject name `kit-cycle` (ADR 0010)."""
    try:
        return tomllib.loads((root / "pyproject.toml").read_text()).get("project", {}).get("name") == "kit-cycle"
    except (OSError, tomllib.TOMLDecodeError):
        return False


def plugin_args(root: Path, cwd: Path) -> list[str]:
    """When the Product is the Kit, load the worktree's own plugin (ADR 0010)."""
    return ["--plugin-dir", str(cwd.resolve() / "src" / "kit" / "plugin")] if is_kit(root) else []


def hand_off(root: Path, area: str, argv: list[str]) -> int | None:
    """When the Product is the Kit, run the worktree's own CLI and return its exit code (ADR 0010).

    Returns None when there is nothing to hand off to: another Product, or already handed off.
    """
    if os.environ.get("KIT_SELF") == "1" or not is_kit(root):
        return None
    try:
        cwd = workspace(root, area)
    except KeyboardInterrupt:
        stop("interrupted", "Ctrl-C")
        return 130
    command = ["uv", "run", "--project", str(cwd), "kit", *argv]
    try:
        return subprocess.run(command, check=False, cwd=root, env={**os.environ, "KIT_SELF": "1"}).returncode
    except KeyboardInterrupt:
        return 130  # the child got the same Ctrl-C and printed the Stop reason


def venv_volume(root: Path, cwd: Path) -> str:
    """The Docker volume holding this worktree's sandbox .venv: kit-venv-<product>-<area>."""

    def clean(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-.") or "x"

    return f"kit-venv-{clean(root.resolve().name)}-{clean(cwd.resolve().name)}"


def image_name(config: Config) -> str:
    return config.get("sandbox", {}).get("image", "kit-sandbox")


def git_identity(root: Path) -> list[str]:
    """docker -e flags so the sandbox commits as the host's git user; it has no gitconfig of its own."""
    flags: list[str] = []
    for field in ("name", "email"):
        value = _output(["git", "config", f"user.{field}"], root)
        if value:
            flags += [arg for role in ("AUTHOR", "COMMITTER") for arg in ("-e", f"GIT_{role}_{field.upper()}={value}")]
    return flags


def posix_tz(offset: timedelta | None) -> str:
    """The UTC offset as a POSIX TZ string, e.g. -0500 becomes <-0500>5 (POSIX inverts the sign)."""
    minutes = round((offset or timedelta()).total_seconds() / 60)
    sign = "+" if minutes >= 0 else "-"
    hours, rest = divmod(abs(minutes), 60)
    posix_sign = "-" if minutes > 0 else ""
    clock = f"{hours}:{rest:02d}" if rest else str(hours)
    return f"<{sign}{hours:02d}{rest:02d}>{posix_sign}{clock}"


def _output(command: list[str], cwd: Path | None = None) -> str:
    """A command's stdout, or "" when it is missing or fails."""
    try:
        done = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    except OSError:
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def _ok(command: list[str]) -> bool:
    try:
        return subprocess.run(command, check=False, capture_output=True).returncode == 0
    except OSError:
        return False


def sandbox_ids() -> tuple[int, int]:
    """The UID and GID the sandbox user gets: the host's, so the bind-mounted repo stays readable and writable.

    A root host maps to 1000, because Claude Code refuses to skip permission prompts as root.
    """
    uid, gid = os.getuid(), os.getgid()
    return (uid, gid) if uid else (1000, 1000)


def sandbox(image: str) -> None:
    """Make sure Docker answers and the sandbox image fits this machine, building it on first use."""
    if not shutil.which("docker"):
        raise SystemExit("Docker is not installed. `kit doctor` shows the fix; `kit run --local` skips the sandbox.")
    if not _ok(["docker", "info"]):
        raise SystemExit("Docker is not running. Start it, or use `kit run --local` to skip the sandbox.")
    uid, gid = sandbox_ids()
    want = f"{uid}:{gid}"
    if not _ok(["docker", "image", "inspect", image]):
        print(f"Building the sandbox image {image} (first run only)...")
    else:
        probe = f'test -d {VENV_PATH} && echo "$(id -u):$(id -g)"'
        have = _output(["docker", "run", "--rm", image, "sh", "-c", probe])
        if have == want:
            return
        built = f"user {have}" if have else f"no {VENV_PATH}"
        print(f"Rebuilding the sandbox image {image} (it has {built}; this machine needs user {want})...")
    build = ["docker", "build", "--build-arg", f"UID={uid}", "--build-arg", f"GID={gid}", "-t", image, str(SANDBOX)]
    subprocess.run(build, check=True)


def system() -> str:
    """mac, wsl or linux: the fixes differ between them."""
    if sys.platform == "darwin":
        return "mac"
    release = Path("/proc/sys/kernel/osrelease")
    if release.exists() and "microsoft" in release.read_text().lower():
        return "wsl"
    return "linux"


def checks(root: Path, kind: str) -> list[tuple[str, bool, bool, str]]:
    """(name, ok, required, fix) for everything the Cycle loop needs on this machine."""
    shell_rc = "~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bashrc"
    docker_fix = {
        "mac": "brew install --cask orbstack, then open OrbStack (Docker Desktop also works)",
        "wsl": "install Docker Desktop for Windows, then Settings > Resources > WSL integration > this distro",
        "linux": "curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker $USER, then log in again",
    }[kind]
    docker_up = _ok(["docker", "info"])
    image = image_name(load_config(root)) if (root / ".agents" / "kit.json").exists() else "kit-sandbox"
    return [
        ("git", bool(shutil.which("git")), True,
         "xcode-select --install" if kind == "mac" else "sudo apt install -y git"),
        ("git identity", bool(_output(["git", "config", "user.email"], root)), True,
         'git config --global user.name "Your Name" && git config --global user.email you@example.com'),
        ("claude", bool(shutil.which("claude")), True, "curl -fsSL https://claude.ai/install.sh | bash"),
        ("gh (PRs on close)", bool(shutil.which("gh")), False,
         "brew install gh" if kind == "mac" else "sudo apt install -y gh"),
        ("docker (hands-off runs)", docker_up, False,
         docker_fix if not shutil.which("docker") else "start Docker (OrbStack, Docker Desktop or dockerd)"),
        (f"sandbox image {image}", docker_up and _ok(["docker", "image", "inspect", image]), False,
         "built on the first `kit run`"),
        ("token (hands-off runs)", any(key in os.environ for key in TOKENS), False,
         f"claude setup-token, then add export CLAUDE_CODE_OAUTH_TOKEN=... to {shell_rc}"),
    ]  # fmt: skip


def doctor(root: Path) -> int:
    """Print what this machine has and the fix for what it lacks. Fails only on what every Cycle needs."""
    kind = system()
    print(f"kit doctor ({kind})")
    warn_version(root)
    if (root / ".agents" / "kit.json").exists() and not load_config(root).get("launch"):
        print("Warning: no `launch` command in .agents/kit.json; /kit:qa will ask for it.")
    missing = False
    for name, ok, required, fix in checks(root, kind):
        mark = "ok  " if ok else ("FAIL" if required else "skip")
        print(f"  {mark} {name}" + ("" if ok else f"\n         fix: {fix}"))
        missing = missing or (required and not ok)
    return 1 if missing else 0


def docker_kill(name: str) -> None:
    """Kill a named sandbox container; killing the `docker run` client alone would leave it running."""
    subprocess.run(["docker", "kill", name], check=False, capture_output=True)


class StepTimeout(Exception):
    """A command ran past its timeout and was killed with its whole process group."""

    def __init__(self, output: str, seconds: float) -> None:
        super().__init__(f"timed out after {seconds:g}s")
        self.output = output
        self.seconds = seconds


def stream(
    command: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: float | None = None, on_kill: Callable[[], None] | None = None
) -> tuple[str, int]:  # fmt: skip
    """Run a command, echo its output live, and return its output and exit code.

    Past `timeout` seconds the command's whole process group is killed and StepTimeout is raised.
    If reading is interrupted (Ctrl-C), the group is killed too before the exception propagates.
    """
    process = subprocess.Popen(
        command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True
    )  # fmt: skip
    assert process.stdout is not None
    timed_out = threading.Event()

    def kill() -> None:
        if on_kill:
            on_kill()
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def time_out() -> None:
        timed_out.set()
        kill()

    timer = threading.Timer(timeout, time_out) if timeout is not None else None
    if timer:
        timer.start()
    lines: list[str] = []
    try:
        for line in process.stdout:
            sys.stdout.write(line)
            lines.append(line)
        code = process.wait()
    except BaseException:  # Ctrl-C and the like: the command has its own session, so stop it here
        kill()
        raise
    finally:
        if timer:
            timer.cancel()
    if timed_out.is_set():
        raise StepTimeout("".join(lines), timeout or 0)
    return "".join(lines), code


def stop(category: str, detail: str) -> None:
    """Print the Stop reason: why `kit run` ended. Always the last line."""
    print(f"Stop reason: {category}: {detail or 'no detail'}")


def dirty_files(cwd: Path) -> list[str]:
    """Paths `git status` reports as uncommitted (staged, modified or untracked)."""
    # Not git(): it strips the leading space of ` M path`, which would eat the path's first character.
    done = subprocess.run(
        ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    entries = done.stdout.split("\0")
    files: list[str] = []
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if not entry:
            continue
        files.append(entry[3:])
        if entry[0] in "RC":  # renames and copies carry the old path as the next entry
            i += 1
    return files


def stop_dirty(area: str, files: list[str], where: str) -> None:
    """Explain a dirty tree: the files and the commands to keep or discard them. Never touches git."""
    print("dirty tree:")
    for name in files:
        print(f"  {name}")
    tree = f".worktrees/{area}"
    print(f'keep:    git -C {tree} add -A && git -C {tree} commit -m "<n>: <title>"')
    print(f"discard: git -C {tree} reset -q --hard && git -C {tree} clean -fd")
    print(f"then: kit run {area}")
    stop("dirty tree", f"{where} {len(files)} uncommitted: {', '.join(files)}")


def _issues(cwd: Path, area: str) -> list[Path]:
    return sorted((cwd / ".agents" / "cycles" / area / "issues").glob("*.md"))


def _last_issue(cwd: Path, area: str) -> str:
    issues = _issues(cwd, area)
    return max(issues, key=lambda path: path.stat().st_mtime).stem if issues else "none"


def _last_line(output: str) -> str:
    return next((line.strip() for line in reversed(output.splitlines()) if line.strip()), "no output")


def once(root: Path, area: str, issue: str | None) -> int:
    """A hands-on session in the Area's checkout: planning, or one named Issue."""
    config = load_config(root)
    warn_version(root)
    cwd = workspace(root, area)
    models: dict[str, str] = config.get("models", {})
    if issue:
        text = prompt("implement", area, cwd, f"Build Issue {issue}.")
        command = agent(config, root, cwd, models.get("implement", "sonnet"), text, hands_off=False, local=True)
    else:
        command = [*config.get("agent", ["claude"]), *plugin_args(root, cwd), "--model", models.get("plan", "opus")]
    code = subprocess.run(command, check=False, cwd=cwd).returncode
    if files := dirty_files(cwd):
        stop_dirty(area, files, "after once,")
    return code


QA_STEP = re.compile(r"^\d+\.\s+`(.+?)`\s*:?\s*(.*)$")


def _qa_section(prd: str, heading: str) -> list[tuple[str, str]]:
    steps: list[tuple[str, str]] = []
    inside = False
    for line in prd.splitlines():
        if line.startswith("#"):
            inside = line.strip() == heading
        elif inside and (match := QA_STEP.match(line.strip())):
            steps.append((match.group(1), match.group(2)))
    return steps


def qa_steps(prd: str) -> list[tuple[str, str]]:
    """The PRD's `## QA steps` (before `### Host steps`) as (command, rest of the line) pairs."""
    return _qa_section(prd, "## QA steps")


def qa_host_steps(prd: str) -> list[tuple[str, str]]:
    """The PRD's `### Host steps`, which must run on the host."""
    return _qa_section(prd, "### Host steps")


SECRET_NAME = re.compile(r"TOKEN|SECRET|KEY|PASSWORD|^(AWS_|GH_|GITHUB_|ANTHROPIC_)")


def scrubbed_env(home: Path) -> dict[str, str]:
    """The environment without credentials, with HOME pointing at a throwaway directory."""
    env = {k: v for k, v in os.environ.items() if not SECRET_NAME.search(k.upper())}
    env["HOME"] = str(home)
    return env


DEFAULT_TIMEOUT = 300.0
TIMEOUT = re.compile(r"timeout:\s*(\d+)\s*([sm])\b", re.IGNORECASE)


def step_timeout(rest: str) -> float:
    """Seconds a step may run: its `timeout: 10m` / `timeout: 1s`, else 300."""
    match = TIMEOUT.search(rest)
    if not match:
        return DEFAULT_TIMEOUT
    return float(int(match.group(1)) * (60 if match.group(2).lower() == "m" else 1))


def prd_text(cwd: Path, area: str) -> str:
    prd = cwd / ".agents" / "cycles" / area / "prd.md"
    return prd.read_text() if prd.exists() else ""


def run_qa(config: Config, root: Path, cwd: Path, area: str, local: bool) -> int:
    """Run every QA step literally, record qa.md and qa-logs/NN.log, and return how many passed."""
    return qa_round(config, root, cwd, area, local)[0]


def qa_round(
    config: Config, root: Path, cwd: Path, area: str, local: bool
) -> tuple[int, list[tuple[int, str, str, int]]]:
    """Like run_qa, plus the failures as (step number, command, output tail, exit code)."""
    prd = cwd / ".agents" / "cycles" / area / "prd.md"
    text = prd.read_text() if prd.exists() else ""
    steps = [(c, e, False) for c, e in qa_steps(text)] + [(c, e, True) for c, e in qa_host_steps(text)]
    folder = prd.parent
    logs = folder / "qa-logs"
    logs.mkdir(parents=True, exist_ok=True)
    entries = ["# QA results\n"]
    passed = 0
    failures: list[tuple[int, str, str, int]] = []
    for number, (command, expect, host) in enumerate(steps, 1):
        started = time.monotonic()
        limit = step_timeout(expect)
        timed_out = False
        try:
            if host:
                with tempfile.TemporaryDirectory() as home:
                    output, code = stream(["sh", "-c", command], cwd, scrubbed_env(Path(home)), timeout=limit)
            elif local:
                output, code = stream(["sh", "-c", command], cwd, timeout=limit)
            else:
                name = f"kit-qa-{os.getpid()}-{number}"
                full = docker_run(config, root, cwd, ["sh", "-c", command], name=name)
                output, code = stream(full, cwd, timeout=limit, on_kill=functools.partial(docker_kill, name))
        except StepTimeout as late:
            output, code, timed_out = late.output, 124, True
        seconds = time.monotonic() - started
        (logs / f"{number:02d}.log").write_text(output)
        passed += code == 0
        tail = "\n".join(output.splitlines()[-20:])
        if code != 0:
            failures.append((number, command, tail, code))
        note = f"Timed out after {limit:g}s (killed)\n" if timed_out else ""
        entries.append(
            f"## Step {number}: `{command}`\n\nYou should see: {expect}\n\n"
            f"{note}Exit code: {code}\nDuration: {seconds:.1f}s\nLog: {logs / f'{number:02d}.log'}\n\n```\n{tail}\n```\n"
        )
    (folder / "qa.md").write_text("\n".join(entries))
    return passed, failures


def qa_failure_note(failures: list[tuple[int, str, str, int]]) -> str:
    """Prompt text handing failing QA steps to the next implement pass."""
    lines = ["QA steps failed after review was clean. Write a `priority: bug` Issue for each, fix it and commit:"]
    for number, command, tail, code in failures:
        lines.append(f"\nQA step {number}: `{command}` (exit {code})\n```\n{tail}\n```")
    return "\n".join(lines)


def run(root: Path, area: str, max_iterations: int, local: bool) -> int:
    """Hands-off Build: one Issue per pass until COMPLETE, then a fresh review."""
    config = load_config(root)
    warn_version(root)
    cwd = root
    try:
        if not local:
            sandbox(image_name(config))
        cwd = workspace(root, area)
        if files := dirty_files(cwd):
            stop_dirty(area, files, "before start,")
            return 1
        (root / "data" / "out").mkdir(parents=True, exist_ok=True)
        models: dict[str, str] = config.get("models", {})
        passes = 0
        failing: list[tuple[int, str, str, int]] = []
        for _ in range(max_iterations):
            passes += 1
            build = prompt("implement", area, cwd, qa_failure_note(failing) if failing else "")
            failing = []
            name = f"kit-implement-{os.getpid()}-{passes}"
            output, code = stream(
                agent(
                    config, root, cwd, models.get("implement", "sonnet"), build, hands_off=True, local=local, name=name
                ),
                cwd,
                on_kill=None if local else functools.partial(docker_kill, name),
            )
            if code != 0:
                stop("agent failed", f"implement exited {code}: {_last_line(output)}")
                return code
            if files := dirty_files(cwd):
                stop_dirty(area, files, f"pass {passes} (implement) left")
                return 1
            if COMPLETE not in output:
                continue
            check = prompt("review", area, cwd, standards(config, cwd))
            name = f"kit-review-{os.getpid()}-{passes}"
            output, code = stream(
                agent(config, root, cwd, models.get("review", "opus"), check, hands_off=True, local=local, name=name),
                cwd,
                on_kill=None if local else functools.partial(docker_kill, name),
            )
            if code != 0:
                stop("agent failed", f"review exited {code}: {_last_line(output)}")
                return code
            if files := dirty_files(cwd):
                stop_dirty(area, files, f"pass {passes} (review) left")
                return 1
            if CLEAN in output:
                steps = len(qa_steps(prd_text(cwd, area))) + len(qa_host_steps(prd_text(cwd, area)))
                if steps:
                    passed, failing = qa_round(config, root, cwd, area, local)
                    if not failing:
                        stop("complete", f"QA steps {passed}/{steps} passed, run /kit:qa")
                        return 0
                    continue
                print(f"Build done. Next: `kit once {area}` and run /kit:qa.")
                stop("complete", "no QA steps in PRD")
                return 0
    except KeyboardInterrupt:
        stop("interrupted", "Ctrl-C")
        return 130
    if failing:
        stop("cap reached", f"QA step {failing[0][0]} still failing")
        return 1
    stop("cap reached", f"{max_iterations} passes, last Issue {_last_issue(cwd, area)}")
    return 1


def close(root: Path, area: str, abandon: bool) -> int:
    """End a Cycle: tag it as abandoned, or pass the merge Gate and hand it to a PR."""
    cwd = root / ".worktrees" / area
    branch = f"cycle/{area}"
    if cwd.exists() and git(cwd, "status", "--porcelain"):
        print(f"Uncommitted changes in {cwd}. Commit or discard them, then close again.")
        return 1
    if abandon:
        tag = f"abandoned/{area}-{date.today().isoformat()}"
        git(root, "tag", tag, branch)
        if git(root, "remote"):
            subprocess.run(["git", "push", "-q", "origin", tag], check=False, cwd=root)
            subprocess.run(["git", "push", "-q", "origin", "--delete", branch], check=False, cwd=root)
        print(f"Abandoned. Kept as tag {tag}; the lesson belongs in CHARTER.md.")
        return 0 if _free(root, cwd, branch, delete_branch=True) else 1
    if not cwd.exists():
        print(f"No checkout at {cwd}. If `kit close {area}` already opened the PR, the Cycle is closed; nothing to do.")
        return 1
    config = load_config(root)
    main = config.get("main", "main")
    if subprocess.run(["git", "rebase", main], check=False, cwd=cwd).returncode != 0:
        subprocess.run(["git", "rebase", "--abort"], check=False, cwd=cwd)
        print(
            f"Rebase conflict. Run `kit once {area}` and ask the agent to rebase onto {main} with the smallest change."
        )
        return 1
    for name, command in config.get("commands", {}).items():
        if subprocess.run(command, shell=True, check=False, cwd=cwd).returncode != 0:
            print(f"Check failed: {name}. Fix it, then close again.")
            return 1
    plan = cwd / ".agents" / "cycles" / area
    if plan.exists():
        shutil.rmtree(plan)
        git(cwd, "add", "-A")
        git(cwd, "commit", "-q", "-m", f"close: {area}")
    if git(root, "remote"):
        git(cwd, "push", "-q", "-u", "origin", branch)
        if shutil.which("gh"):
            subprocess.run(["gh", "pr", "create", "--fill", "--base", main, "--head", branch], check=False, cwd=cwd)
        merge = "Merge the PR with a merge commit once CI passes and you have signed off."
    else:
        merge = f"No remote. After sign-off, merge: git merge --no-ff {branch}"
    print(f"Next:\n  1. {merge}\n  2. kit once {area}\n  3. /kit:grill")
    return 0 if _free(root, cwd, branch, delete_branch=False) else 1


def _free(root: Path, cwd: Path, branch: str, delete_branch: bool) -> bool:
    """Remove the Area's checkout, sandbox volume and, if asked, branch. False when the checkout would not go."""
    if cwd.exists():
        done = subprocess.run(
            ["git", "worktree", "remove", "--force", str(cwd)], check=False, cwd=root, capture_output=True, text=True
        )
        if done.returncode != 0:
            print(
                f"Could not remove {cwd}: {done.stderr.strip()}\n"
                "Files the sandbox wrote as root block it. Clear them, then prune:\n"
                f'  docker run --rm -v "{cwd.parent}:/w" alpine rm -rf /w/{cwd.name} && git worktree prune'
            )
            return False
    try:
        subprocess.run(["docker", "volume", "rm", venv_volume(root, cwd)], check=False, capture_output=True)
    except OSError:
        pass  # no Docker installed: nothing to remove
    if delete_branch:
        git(root, "branch", "-D", branch)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kit", description="Run the Cycle loop.")
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("init", help="add the Product template; never overwrites")
    start.add_argument("path", nargs="?", default=".", help="folder for the Product, created if missing")
    hands_on = commands.add_parser("once", help="hands-on session in an Area's checkout")
    hands_on.add_argument("area")
    hands_on.add_argument("issue", nargs="?")
    build = commands.add_parser("run", help="hands-off Build in the sandbox")
    build.add_argument("area")
    build.add_argument("--max", type=int, default=None, help="iteration cap (default: kit.json)")
    build.add_argument("--local", action="store_true", help="skip the sandbox")
    end = commands.add_parser("close", help="pass the merge Gate, or abandon")
    end.add_argument("area")
    end.add_argument("--abandon", action="store_true")
    commands.add_parser("doctor", help="check this machine and print fixes")
    args = parser.parse_args(argv)

    root = Path.cwd()
    if args.command == "init":
        root = Path(args.path).resolve()
        root.mkdir(parents=True, exist_ok=True)
        for path in init(root):
            print(f"wrote {path.relative_to(root)}")
        here = "" if root == Path.cwd() else f"cd {args.path} && "
        print(f"Next: {here}claude, then run /kit:grill for the Charter.")
        return 0
    if args.command == "doctor":
        return doctor(root)
    if args.command in ("once", "run"):
        handed = hand_off(root, args.area, sys.argv[1:] if argv is None else argv)
        if handed is not None:
            return handed
    if args.command == "once":
        return once(root, args.area, args.issue)
    if args.command == "run":
        cap = args.max or load_config(root).get("maxIterations", 20)
        return run(root, args.area, cap, args.local)
    return close(root, args.area, args.abandon)


if __name__ == "__main__":
    sys.exit(main())
