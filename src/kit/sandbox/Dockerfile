# Sandbox for hands-off runs. `kit run` builds it on first use.
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates nodejs npm \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code pnpm \
 && pip install --no-cache-dir uv \
 && git config --system --add safe.directory '*'

# Claude Code refuses to skip permission prompts as root. `kit run` passes the host's UID and GID,
# so files in the bind-mounted repo stay readable and writable on both sides; -o allows IDs the base image already uses.
ARG UID=1000
ARG GID=1000
RUN groupadd -o -g "$GID" kit && useradd -o --create-home -u "$UID" -g "$GID" kit
USER kit
# Docker copies this folder's owner into each new named volume mounted here (the venv).
RUN mkdir /home/kit/venv
