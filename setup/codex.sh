#!/usr/bin/env bash
# Codex 환경 셋업. 자동화 가능한 단계만 처리.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "→ Repo root: $REPO_ROOT"
echo ""

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

run_rtk_init() {
  local rtk_path="$1"

  if "$rtk_path" init -g >/dev/null 2>&1; then
    return 0
  fi

  echo "⚠ rtk init -g failed; continuing."
  return 0
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

# 1. RTK
if rtk_path="$(find_rtk_binary)"; then
  echo "✓ RTK already installed ($("$rtk_path" --version 2>/dev/null || echo unknown))"
else
  echo "→ Installing RTK..."
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
  if rtk_path="$(find_rtk_binary)"; then
    echo "✓ RTK installed"
  else
    echo "⚠ RTK installer finished but 'rtk' not on PATH yet."
    echo "   새 셸을 열거나 PATH를 다시 로드한 뒤 'rtk init -g'를 직접 실행하라."
  fi
fi
if [ -n "${rtk_path:-}" ]; then
  run_rtk_init "$rtk_path"
  ensure_rtk_for_codex_core_path
fi
echo ""

# 2. 전역 AGENTS.md
echo "→ Installing ~/.codex/AGENTS.md"
mkdir -p ~/.codex
cp "$REPO_ROOT/AGENTS.md" ~/.codex/AGENTS.md
echo "✓ ~/.codex/AGENTS.md updated"
echo ""

# 3. 스킬 설치
echo "→ Installing skills to ~/.codex/skills/"
mkdir -p ~/.codex/skills
for dir in "$REPO_ROOT"/skills/*/; do
  name=$(basename "$dir")
  if [ -f "$dir/SKILL.md" ]; then
    mkdir -p ~/.codex/skills/"$name"
    cp -R "$dir/." ~/.codex/skills/"$name"/
    echo "  ✓ $name"
  fi
done
echo ""

# 4. Slidev (옵션)
if [ "${1:-}" = "--with-slidev" ]; then
  if command -v slidev >/dev/null 2>&1; then
    echo "✓ Slidev already installed"
  else
    echo "→ Installing Slidev CLI globally"
    npm install -g @slidev/cli
    echo "✓ Slidev installed"
  fi
  echo ""
fi

cat <<EOF
=========================================
✓ Codex 셋업 완료
=========================================

Codex를 재시작하면 새 skill이 인식된다.

(옵션) Slidev 설치하지 않았으면:
  ./setup/codex.sh --with-slidev

자세한 내용은 README.md와 setup/README.md 참고.
EOF
