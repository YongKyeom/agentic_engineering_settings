#!/usr/bin/env bash
# 개발 환경 셋업: Shell (oh-my-zsh, 플러그인, 테마) + Terminal (tmux + TPM)
# 대상: macOS (brew), Linux/WSL (apt)

set -euo pipefail

OS="$(uname -s)"
ZSHRC="$HOME/.zshrc"
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

echo "→ OS: $OS"
echo ""

# 패키지 설치 헬퍼
pkg_install() {
  if [[ "$OS" == "Darwin" ]]; then
    brew install "$1"
  else
    sudo apt-get install -y "$1"
  fi
}

# ── 1. oh-my-zsh ──────────────────────────────────────────────────────────────
if [ -d "$HOME/.oh-my-zsh" ]; then
  echo "✓ oh-my-zsh already installed"
else
  echo "→ Installing oh-my-zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
  echo "✓ oh-my-zsh installed"
fi
echo ""

# ── 2. 플러그인 ────────────────────────────────────────────────────────────────
install_zsh_plugin() {
  local name="$1" repo="$2"
  local dir="$ZSH_CUSTOM/plugins/$name"
  if [ -d "$dir" ]; then
    echo "✓ $name already installed"
  else
    echo "→ Installing $name..."
    git clone --depth=1 "$repo" "$dir"
    echo "✓ $name installed"
  fi
}

install_zsh_plugin "zsh-autosuggestions" "https://github.com/zsh-users/zsh-autosuggestions"
install_zsh_plugin "zsh-syntax-highlighting" "https://github.com/zsh-users/zsh-syntax-highlighting"

# fzf (oh-my-zsh 플러그인은 별도, 바이너리는 brew/apt)
if ! command -v fzf >/dev/null 2>&1; then
  echo "→ Installing fzf..."
  pkg_install fzf
  echo "✓ fzf installed"
else
  echo "✓ fzf already installed"
fi

# zoxide
if ! command -v zoxide >/dev/null 2>&1; then
  echo "→ Installing zoxide..."
  pkg_install zoxide
  echo "✓ zoxide installed"
else
  echo "✓ zoxide already installed"
fi
echo ""

# ── 3. powerlevel10k 테마 ──────────────────────────────────────────────────────
P10K_DIR="$ZSH_CUSTOM/themes/powerlevel10k"
if [ -d "$P10K_DIR" ]; then
  echo "✓ powerlevel10k already installed"
else
  echo "→ Installing powerlevel10k..."
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$P10K_DIR"
  echo "✓ powerlevel10k installed"
fi
echo ""

# ── 4. .zshrc 업데이트 ─────────────────────────────────────────────────────────
# 테마
if grep -q 'ZSH_THEME=' "$ZSHRC" 2>/dev/null; then
  sed -i.bak 's|ZSH_THEME="[^"]*"|ZSH_THEME="powerlevel10k/powerlevel10k"|' "$ZSHRC"
  echo "✓ ZSH_THEME → powerlevel10k"
else
  echo 'ZSH_THEME="powerlevel10k/powerlevel10k"' >> "$ZSHRC"
  echo "✓ ZSH_THEME added"
fi

# plugins 라인에 누락된 플러그인 추가
REQUIRED_PLUGINS=(zsh-autosuggestions zsh-syntax-highlighting fzf zoxide)
for plugin in "${REQUIRED_PLUGINS[@]}"; do
  if grep -q "^plugins=" "$ZSHRC" 2>/dev/null && grep "^plugins=" "$ZSHRC" | grep -q "$plugin"; then
    echo "✓ plugin already in .zshrc: $plugin"
  else
    sed -i.bak "s/^plugins=(\(.*\))/plugins=(\1 $plugin)/" "$ZSHRC"
    echo "✓ plugin added to .zshrc: $plugin"
  fi
done

# zoxide init
if ! grep -q 'zoxide init' "$ZSHRC" 2>/dev/null; then
  echo 'eval "$(zoxide init zsh)"' >> "$ZSHRC"
  echo "✓ zoxide init added"
fi
echo ""

# ── 5. CLI 도구 ────────────────────────────────────────────────────────────────
for tool in btop ncdu; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "✓ $tool already installed"
  else
    echo "→ Installing $tool..."
    pkg_install "$tool"
    echo "✓ $tool installed"
  fi
done
echo ""

# ── 7. tmux ────────────────────────────────────────────────────────────────────
if command -v tmux >/dev/null 2>&1; then
  echo "✓ tmux already installed ($(tmux -V))"
else
  echo "→ Installing tmux..."
  pkg_install tmux
  echo "✓ tmux installed"
fi
echo ""

# ── 8. TPM (Tmux Plugin Manager) ───────────────────────────────────────────────
TPM_DIR="$HOME/.tmux/plugins/tpm"
if [ -d "$TPM_DIR" ]; then
  echo "✓ TPM already installed"
else
  echo "→ Installing TPM..."
  git clone --depth=1 https://github.com/tmux-plugins/tpm "$TPM_DIR"
  echo "✓ TPM installed"
fi
echo ""

# ── 9. ~/.tmux.conf ────────────────────────────────────────────────────────────
TMUX_CONF="$HOME/.tmux.conf"
if [ -f "$TMUX_CONF" ]; then
  echo "⚠ ~/.tmux.conf already exists. Skipping."
else
  echo "→ Writing ~/.tmux.conf..."
  cat > "$TMUX_CONF" << 'TMUXEOF'
# ── 플러그인 ──────────────────────────────────────────────────────────────────
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'catppuccin/tmux#v2.1.3'

# ── 마우스 / 복사 ──────────────────────────────────────────────────────────────
set -g mouse on
set -g @yank_with_mouse on
set -g copy-command "pbcopy"

# ── vi 키바인딩 ────────────────────────────────────────────────────────────────
setw -g mode-keys vi

# ── 창/패널 번호 1부터 ──────────────────────────────────────────────────────────
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on

# ── True Color ─────────────────────────────────────────────────────────────────
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"

# ── 상태바 ─────────────────────────────────────────────────────────────────────
set -g status-position top

# ── Catppuccin Mocha ───────────────────────────────────────────────────────────
set -g @catppuccin_flavor 'mocha'

# ── 세션 자동 저장/복원 ────────────────────────────────────────────────────────
set -g @continuum-restore 'on'

# ── TPM 초기화 (파일 맨 아래 유지) ────────────────────────────────────────────
run '~/.tmux/plugins/tpm/tpm'
TMUXEOF
  echo "✓ ~/.tmux.conf created"
fi
echo ""

# ── 10. p10k 설정 복원 ─────────────────────────────────────────────────────────
P10K_SRC="$(cd "$(dirname "$0")" && pwd)/p10k.zsh"
if [ -f "$HOME/.p10k.zsh" ]; then
  echo "⚠ ~/.p10k.zsh already exists. Skipping."
else
  if [ -f "$P10K_SRC" ]; then
    cp "$P10K_SRC" "$HOME/.p10k.zsh"
    echo "✓ ~/.p10k.zsh restored"
  else
    echo "⚠ setup/p10k.zsh not found. Run 'p10k configure' manually."
  fi
fi

# p10k 소스 라인 추가
if ! grep -q 'p10k.zsh' "$ZSHRC" 2>/dev/null; then
  echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> "$ZSHRC"
  echo "✓ p10k source line added"
fi
echo ""

# ── 11. TPM 플러그인 자동 설치 ─────────────────────────────────────────────────
echo "→ Installing tmux plugins via TPM..."
"$HOME/.tmux/plugins/tpm/scripts/install_plugins.sh"
echo "✓ tmux plugins installed"
echo ""

cat << 'EOF'
=========================================
✓ 셋업 완료
=========================================

다음 단계:
1. source ~/.zshrc  — 플러그인/테마 적용
2. tmux             — catppuccin mocha 확인
EOF
