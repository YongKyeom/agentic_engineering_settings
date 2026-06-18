#!/usr/bin/env bash
# Codex 환경 셋업. 자동화 가능한 단계만 처리.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "→ Repo root: $REPO_ROOT"
echo ""

# 1. RTK
if command -v rtk >/dev/null 2>&1; then
  echo "✓ RTK already installed ($(rtk --version 2>/dev/null || echo unknown))"
else
  echo "→ Installing RTK..."
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
  if command -v rtk >/dev/null 2>&1; then
    rtk init -g
    echo "✓ RTK installed"
  else
    echo "⚠ RTK installer finished but 'rtk' not on PATH yet."
    echo "   새 셸을 열거나 PATH를 다시 로드한 뒤 'rtk init -g'를 직접 실행하라."
  fi
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
