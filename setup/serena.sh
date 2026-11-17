#!/usr/bin/env bash
# Serena 전역 설치와 RTK 공존 hook 구성을 재현한다.
set -euo pipefail
client="${1:-all}"
case "$client" in codex|claude|all) ;; *) echo "Usage: $0 [codex|claude|all]" >&2; exit 1 ;; esac
script_dir="$(cd "$(dirname "$0")" && pwd)"
export PATH="$PATH:$HOME/.local/bin"
command -v uv >/dev/null 2>&1 || { echo "Install uv first: https://docs.astral.sh/uv/" >&2; exit 1; }
command -v rtk >/dev/null 2>&1 || { echo "Run setup/rtk.sh first." >&2; exit 1; }
uv tool install --upgrade serena-agent
export PATH="$(uv tool dir --bin):$PATH"
python3 "$script_dir/configure-agent-hooks.py" "$client"
