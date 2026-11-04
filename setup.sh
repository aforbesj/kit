#!/usr/bin/env bash
# Set up the Kit on macOS, Linux or WSL2. Safe to rerun: it skips what is already there.
#   ./setup.sh              install what is missing; asks before installing Docker
#   ./setup.sh --yes        never ask
#   ./setup.sh --no-docker  skip Docker; hands-off runs then need `kit run --local`
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YES=0
DOCKER=1
for arg in "$@"; do
  case "$arg" in
    -y | --yes) YES=1 ;;
    --no-docker) DOCKER=0 ;;
    -h | --help) sed -n '2,5p' "$0" | sed 's/^# //'; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)" >&2; exit 2 ;;
  esac
done

if [ "$(uname -s)" = Darwin ]; then
  OS=mac
elif grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then
  OS=wsl
else
  OS=linux
fi
case "$(basename "${SHELL:-bash}")" in zsh) RC="$HOME/.zshrc" ;; *) RC="$HOME/.bashrc" ;; esac
case ":$PATH:" in *":$HOME/.local/bin:"*) ON_PATH=1 ;; *) ON_PATH=0 ;; esac
export PATH="$HOME/.local/bin:$PATH"

step() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }
ask() {
  [ "$YES" = 1 ] && return 0
  [ -t 0 ] || return 1
  read -r -p "$1 [y/N] " reply
  [[ "$reply" =~ ^[Yy] ]]
}
pkg() {
  if have apt-get; then sudo apt-get update -qq && sudo apt-get install -y "$@"
  elif have dnf; then sudo dnf install -y "$@"
  elif have pacman; then sudo pacman -S --noconfirm "$@"
  else echo "Install $* with your package manager." >&2; return 1
  fi
}
docker_up() { have docker && docker info >/dev/null 2>&1; }

step "Kit setup for $OS"

step "git and curl"
if [ "$OS" = mac ]; then
  if ! xcode-select -p >/dev/null 2>&1; then
    xcode-select --install || true
    echo "Finish the Command Line Tools install in the window that opened, then rerun ./setup.sh"
    exit 1
  fi
else
  have git && have curl || pkg git curl ca-certificates || exit 1
fi
echo "ok"

step "git identity (commits need it)"
if [ -z "$(git config --global user.email || true)" ]; then
  if [ -t 0 ] && [ "$YES" = 0 ]; then
    read -r -p "Your name for commits: " name
    read -r -p "Your email for commits: " email
    git config --global user.name "$name"
    git config --global user.email "$email"
  else
    echo "Not set. Run: git config --global user.name \"Your Name\" && git config --global user.email you@example.com"
  fi
fi
echo "$(git config --global user.name || true) <$(git config --global user.email || true)>"

step "uv (Python and the kit CLI)"
have uv || curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

step "Claude Code"
have claude || curl -fsSL https://claude.ai/install.sh | bash
claude --version

step "kit CLI (editable: git pull updates it)"
uv tool install --force --editable "$KIT" >/dev/null
# uv, claude and kit all install to ~/.local/bin; neither installer reliably puts it on PATH.
if [ "$ON_PATH" = 0 ] && ! grep -qs '.local/bin' "$RC"; then
  printf '\n# Kit: uv, claude and kit live here\nexport PATH="$HOME/.local/bin:$PATH"\n' >>"$RC"
  echo "added ~/.local/bin to PATH in $RC"
fi
kit --help >/dev/null && echo "kit -> $(command -v kit)"

step "Kit plugin for Claude Code"
claude plugin marketplace add "$KIT" >/dev/null 2>&1 || claude plugin marketplace update kit >/dev/null 2>&1 || true
if claude plugin install kit@kit >/dev/null 2>&1 || claude plugin list 2>/dev/null | grep -q kit@kit; then
  echo "installed kit@kit"
else
  echo "Could not install it from here. In Claude Code run: /plugin marketplace add $KIT  then  /plugin install kit@kit"
fi

step "gh (opens PRs on kit close)"
if ! have gh; then
  if [ "$OS" = mac ] && have brew; then brew install gh
  else pkg gh || echo "Optional: install gh from https://cli.github.com"
  fi
fi
have gh && gh --version | head -1

step "Docker (sandbox for hands-off runs)"
if [ "$DOCKER" = 0 ]; then
  echo "Skipped. Use kit run --local, or rerun without --no-docker."
elif docker_up; then
  echo "running"
elif [ "$OS" = mac ]; then
  if ! have docker && ask "Install OrbStack, a light Docker for Mac (via Homebrew)?"; then
    have brew || { echo "Needs Homebrew: https://brew.sh" >&2; exit 1; }
    brew install --cask orbstack
  fi
  if have docker || [ -d /Applications/OrbStack.app ] || [ -d /Applications/Docker.app ]; then
    open -a OrbStack 2>/dev/null || open -a Docker 2>/dev/null || true
    echo "Waiting for Docker to start..."
    for _ in $(seq 60); do docker_up && break; sleep 2; done
  fi
elif [ "$OS" = wsl ]; then
  echo "Install Docker Desktop for Windows, then Settings > Resources > WSL integration > enable this distro, and rerun."
elif ! have docker && ask "Install Docker Engine (get.docker.com, needs sudo)?"; then
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
  echo "Log out and back in so your user can reach Docker, then rerun."
fi
if docker_up; then
  docker image inspect kit-sandbox >/dev/null 2>&1 || docker build -t kit-sandbox "$KIT/src/kit/sandbox"
  echo "sandbox image ready"
elif [ "$DOCKER" = 1 ]; then
  echo "Docker is not running yet; kit run builds the sandbox once it is."
fi

step "Check"
kit doctor || true

cat <<EOF

Done. Open a new terminal (or: exec \$SHELL) so PATH picks up kit and claude.
  claude                        log in once
  kit init ~/code/my-product    start a Product
  cd ~/code/my-product && claude, then /kit:grill
Hands-off runs need a token in the sandbox: claude setup-token, then add
  export CLAUDE_CODE_OAUTH_TOKEN=...   to $RC
EOF
