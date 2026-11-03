# Sandbox for hands-off runs. `kit run` builds it on first use.
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates nodejs npm \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code pnpm \
 && pip install --no-cache-dir uv \
 && git config --system --add safe.directory '*'

# Claude Code refuses to skip permission prompts as root.
RUN useradd --create-home kit
USER kit
# Docker copies this folder's owner into each new named volume mounted here (the venv).
RUN mkdir /home/kit/venv
