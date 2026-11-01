# Sandbox for hands-off runs. Build once: docker build -t kit-sandbox sandbox/
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates nodejs npm \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code pnpm \
 && pip install --no-cache-dir uv

# Claude Code refuses to skip permission prompts as root.
RUN useradd --create-home kit
USER kit
