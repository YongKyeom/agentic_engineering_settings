#!/usr/bin/env bash
# 최신 RTK와 전역 native hook을 설치한다.
set -euo pipefail
client="${1:-all}"
case "$client" in codex|claude|all) ;; *) echo "Usage: $0 [codex|claude|all]" >&2; exit 1 ;; esac

find_rtk_binary() {
  if command -v rtk >/dev/null 2>&1; then
    command -v rtk
    return 0
  fi

  if [ -x "$HOME/.local/bin/rtk" ]; then
    printf '%s\n' "$HOME/.local/bin/rtk"
    return 0
  fi

  return 1
}

ensure_rtk_for_codex_core_path() {
  local rtk_path rtk_version target target_dir target_version

  if ! rtk_path="$(find_rtk_binary)"; then
    return 0
  fi

  rtk_version="$("$rtk_path" --version 2>/dev/null || true)"
  target="/usr/local/bin/rtk"
  target_dir="$(dirname "$target")"

  if [ "$rtk_path" = "$target" ]; then
    echo "✓ RTK available at $target for Codex core PATH"
    return 0
  fi

  if [ -x "$target" ]; then
    target_version="$("$target" --version 2>/dev/null || true)"
  else
    target_version=""
  fi

  if [ -n "$target_version" ] && [ "$target_version" = "$rtk_version" ]; then
    echo "✓ RTK available at $target for Codex core PATH"
    return 0
  fi

  if [ -d "$target_dir" ] && [ -w "$target_dir" ]; then
    if ln -sf "$rtk_path" "$target"; then
      echo "✓ RTK linked to $target for Codex core PATH"
      return 0
    fi
    echo "⚠ Failed to link RTK to $target; continuing."
  fi

  if command -v sudo >/dev/null 2>&1 && [ -t 0 ]; then
    echo "→ Linking RTK to $target for Codex core PATH"
    echo "   sudo may ask for your password."
    if sudo mkdir -p "$target_dir" && sudo ln -sf "$rtk_path" "$target"; then
      echo "✓ RTK linked to $target"
      return 0
    fi
  fi

  echo "⚠ RTK is installed at $rtk_path, but $target was not created."
  echo "   Codex with shell_environment_policy.inherit = \"core\" may not see rtk."
  echo "   Run manually if needed:"
  echo "     sudo ln -sf \"$rtk_path\" \"$target\""
}

backup_dir="$HOME/.local/state/agent-setup/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$backup_dir"
for file in .codex/AGENTS.md .codex/hooks.json .claude/CLAUDE.md .claude/settings.json; do
  if [ -f "$HOME/$file" ]; then
    mkdir -p "$backup_dir/$(dirname "$file")"
    cp -p "$HOME/$file" "$backup_dir/$file"
  fi
done
echo "Backup: $backup_dir"

if command -v brew >/dev/null 2>&1 && brew list --formula rtk >/dev/null 2>&1; then
  brew update
  brew upgrade rtk
else
  installer="$(mktemp)"
  trap 'rm -f "$installer"' EXIT
  curl -fLsS https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh -o "$installer"
  sh "$installer"
fi
export PATH="$PATH:$HOME/.local/bin"
rtk --version
if [ "$client" = codex ] || [ "$client" = all ]; then
  rtk init -g --codex
  ensure_rtk_for_codex_core_path
fi
if [ "$client" = claude ] || [ "$client" = all ]; then
  rtk init -g --auto-patch
fi
