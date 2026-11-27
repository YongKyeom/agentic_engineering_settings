#!/usr/bin/env bash
# Codex 환경 셋업. 자동화 가능한 단계만 처리.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "→ Repo root: $REPO_ROOT"
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

# RTK 지침은 AGENTS.md 복사 후 연결한다.
bash "$REPO_ROOT/setup/rtk.sh" codex
bash "$REPO_ROOT/setup/serena.sh" codex
bash "$REPO_ROOT/setup/herdr.sh" codex
uv run "$REPO_ROOT/setup/configure-statusline.py"

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
