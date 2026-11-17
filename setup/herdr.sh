#!/usr/bin/env bash
# Herdr TUI, zsh 기본값, 패널 이동 키와 공식 agent 지침을 설치한다.
set -euo pipefail
client="${1:-all}"
case "$client" in codex|claude|all) ;; *) echo "Usage: $0 [codex|claude|all]" >&2; exit 1 ;; esac
script_dir="$(cd "$(dirname "$0")" && pwd)"
export PATH="$PATH:$HOME/.local/bin"
command -v uv >/dev/null 2>&1 || { echo "Install uv first: https://docs.astral.sh/uv/" >&2; exit 1; }

if ! command -v zsh >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install zsh
  elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y zsh
  else
    echo "Install zsh and rerun this script." >&2
    exit 1
  fi
fi

if ! command -v herdr >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install herdr
  else
    installer="$(mktemp)"
    trap 'rm -f "$installer"' EXIT
    curl -fLsS https://herdr.dev/install.sh -o "$installer"
    sh "$installer"
  fi
fi
herdr --version
uv run "$script_dir/configure-herdr.py" "$client"
