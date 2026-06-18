# Setup Scripts

이 폴더는 새 머신에서 공통 개발환경과 AI agent 설정을 재현하기 위한 셋업 파일을 보관한다.

## 파일 역할

| 파일 | 역할 |
|------|------|
| `dev-env.sh` | zsh, oh-my-zsh, powerlevel10k, tmux, TPM, 기본 CLI 도구를 설치하고 `~/.zshrc`, `~/.tmux.conf`, `~/.p10k.zsh`를 이 레포 기준으로 덮어쓴다. |
| `zshrc` | `dev-env.sh`가 `~/.zshrc`로 복사하는 zsh 템플릿. |
| `p10k.zsh` | `dev-env.sh`가 `~/.p10k.zsh`로 복사하는 powerlevel10k 설정. |
| `claude-code.sh` | Claude Code 전역 설정, custom commands, Codex plugin, 기본 settings, alias를 설치한다. |
| `claude-code.md` | Claude Code 셋업 세부 가이드. Dashboard plugin처럼 수동 확인이 필요한 내용도 포함한다. |
| `codex.sh` | Codex 전역 `AGENTS.md`와 custom skills를 설치한다. |

## 실행 순서

```sh
# 1. 공통 shell/tmux 환경
./setup/dev-env.sh

# 2-A. Claude Code 환경
./setup/claude-code.sh
./setup/claude-code.sh --with-slidev

# 2-B. Codex 환경
./setup/codex.sh
./setup/codex.sh --with-slidev
```

`dev-env.sh`는 dotfile을 덮어쓰는 것이 의도된 동작이다. 개인 설정을 보존해야 하는 머신에서는 실행 전에 백업한다.
