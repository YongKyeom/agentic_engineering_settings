#!/usr/bin/env bash
# Claude Code 환경 셋업.
# 자동화 가능한 단계만 처리. 플러그인 설치는 셸에서 불가능하므로
# 스크립트 실행 후 수동 단계 안내를 따라가야 한다.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "→ Repo root: $REPO_ROOT"
echo ""

# 1. RTK (Rust Token Killer)
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

# 2. 전역 CLAUDE.md
echo "→ Installing ~/.claude/CLAUDE.md"
mkdir -p ~/.claude
{ echo "@RTK.md"; echo ""; cat "$REPO_ROOT/CLAUDE.md"; } > ~/.claude/CLAUDE.md
echo "✓ ~/.claude/CLAUDE.md updated"
echo ""

# 3. 스킬 설치
echo "→ Installing skills to ~/.claude/commands/"
mkdir -p ~/.claude/commands
for dir in "$REPO_ROOT"/skills/*/; do
  name=$(basename "$dir")
  if [ -f "$dir/SKILL.md" ]; then
    cp "$dir/SKILL.md" ~/.claude/commands/"${name}.md"
    echo "  ✓ $name"
  fi
done
echo ""

# 4. settings.json
SETTINGS=~/.claude/settings.json
if [ -f "$SETTINGS" ]; then
  echo "⚠ $SETTINGS already exists. Skipping."
  echo "   기존 설정과 충돌을 피하기 위해 덮어쓰지 않는다."
  echo "   'setup/claude-code.md'의 4번 섹션을 참고해 수동으로 병합하라."
else
  echo "→ Writing default $SETTINGS"
  cat > "$SETTINGS" <<'JSON'
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "65536"
  },
  "permissions": {
    "defaultMode": "auto",
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git show:*)",
      "Bash(git branch:*)",
      "Bash(git fetch:*)",
      "Bash(git add:*)",
      "Bash(git stash:*)",
      "Bash(git blame:*)",
      "Bash(git remote -v)",
      "Bash(git rev-parse:*)",
      "Bash(git ls-files:*)",
      "Bash(git worktree:*)",
      "Bash(ls:*)",
      "Bash(pwd)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(rg:*)",
      "Bash(find:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(date)",
      "Bash(stat:*)",
      "Bash(file:*)",
      "Bash(tree:*)",
      "Read",
      "Glob",
      "Grep",
      "WebFetch",
      "WebSearch"
    ],
    "ask": [
      "Bash(rm:*)",
      "Bash(mv:*)",
      "Bash(chmod:*)",
      "Bash(sudo:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git reset --hard:*)",
      "Bash(git checkout:*)",
      "Bash(git restore:*)",
      "Bash(git clean:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(git branch -D:*)"
    ]
  },
  "effortLevel": "xhigh",
  "advisorModel": "claude-opus-4-7",
  "verbose": true
}
JSON
  echo "✓ Default settings.json created"
fi
echo ""

# 5. Slidev (옵션)
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

# 마무리
cat <<EOF
=========================================
✓ 자동화 가능한 셋업 완료
=========================================

수동으로 처리할 다음 단계:

1. Claude Code 실행
2. Claude Dashboard 플러그인 설치 (Claude Code 세션 안에서):
     /plugin marketplace add uppinote20/claude-dashboard
     /plugin install claude-dashboard
     /reload-plugins
     /claude-dashboard:setup

3. (옵션) Slidev 설치하지 않았으면:
     ./setup/claude-code.sh --with-slidev

자세한 내용은 setup/claude-code.md 참고.
EOF
