# Setup Scripts

이 폴더는 새 머신에서 공통 개발환경과 AI agent 설정을 재현하기 위한 셋업 파일을 보관한다.

## 파일 역할

| 파일 | 역할 |
|------|------|
| `dev-env.sh` | zsh, oh-my-zsh, powerlevel10k, tmux, TPM, 기본 CLI 도구를 설치하고 `~/.zshrc`, `~/.tmux.conf`, `~/.p10k.zsh`를 이 레포 기준으로 덮어쓴다. |
| `zshrc` | `dev-env.sh`가 `~/.zshrc`로 복사하는 zsh 템플릿. |
| `p10k.zsh` | `dev-env.sh`가 `~/.p10k.zsh`로 복사하는 powerlevel10k 설정. |
| `claude-code.sh` | Claude Code 전역 설정, custom skills, Codex plugin, 기본 settings, alias를 설치한다. |
| `claude-code.md` | Claude Code 셋업 세부 가이드. Dashboard plugin처럼 수동 확인이 필요한 내용도 포함한다. |
| `codex.sh` | Codex 전역 지침, custom skills, RTK와 Serena를 설치한다. |
| `rtk.sh` | 최신 RTK와 Codex/Claude 전역 native hook을 설치한다. |
| `serena.sh` | Serena를 전역 설치하고 MCP와 RTK 공존 hook을 병합한다. |
| `configure-agent-hooks.py` | 기존 설정을 백업하고 관리 대상 hook과 MCP만 갱신한다. |

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

## RTK와 Serena 전역 설치

`uv`, Python 3, 해당 agent CLI가 설치되어 있어야 한다. RTK와 Serena만 설정하려면:

```sh
./setup/rtk.sh                 # 최신 RTK + Codex/Claude native hook
./setup/serena.sh              # uv tool install --upgrade serena-agent + MCP/hook 병합
# 한 클라이언트만 선택: 각 스크립트 뒤에 codex 또는 claude
```

`codex.sh`와 `claude-code.sh`도 위 두 스크립트를 호출한다. RTK는 Homebrew로 설치한 경우 `brew update`와 `brew upgrade rtk`, 그 외에는 공식 설치 스크립트를 사용한다. Serena는 `uv tool install --upgrade serena-agent`로 설치하거나 갱신한다. 실행 시점의 안정 버전을 사용하며, 2026-11-17 확인 버전은 RTK 1.2.0, Serena 2.1.0이다.

일반적인 수동 설치:

```sh
# macOS (Homebrew)
brew install rtk
# 기존 설치 갱신
brew update
brew upgrade rtk

# Linux 등 공식 설치 스크립트
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh -o /tmp/rtk-install.sh
sh /tmp/rtk-install.sh

uv tool install serena-agent
rtk init -g --codex
rtk init -g --auto-patch     # Claude; --codex와 --auto-patch는 함께 쓰지 않는다
codex mcp add serena -- serena start-mcp-server --context codex --project-from-cwd
claude mcp add --scope user serena -- serena start-mcp-server --context claude-code --project-from-cwd
```

MCP 등록 명령만으로 Serena hook이 설치되지는 않는다. `./setup/serena.sh`를 실행하면 아래 구성을 병합한다. 이미 설치된 Serena도 최신 버전으로 갱신하므로, 갱신 없이 hook만 다시 적용하려면 `python3 setup/configure-agent-hooks.py all`을 실행한다.

### 전역 설정과 hook 공존

| 대상 | 설정 파일 |
|------|-----------|
| Codex RTK 지침 | `~/.codex/RTK.md`, `~/.codex/AGENTS.md` |
| Codex MCP | `~/.codex/config.toml`의 `mcp_servers.serena` |
| Codex hook | `~/.codex/hooks.json` |
| Claude RTK 지침 | `~/.claude/RTK.md`, `~/.claude/CLAUDE.md` |
| Claude MCP | `~/.claude.json`의 사용자 범위 `mcpServers.serena` |
| Claude hook | `~/.claude/settings.json` |

`configure-agent-hooks.py`는 실행 파일을 자동 탐지해 절대 경로로 저장한다. GUI나 제한된 PATH에서도 hook과 MCP 실행 파일을 찾을 수 있다. Codex MCP는 공식 `codex mcp add`, Claude MCP는 사용자 범위 JSON 병합을 사용한다. 기존 전역 파일은 `~/.local/state/agent-setup/<timestamp>/`에 백업하며, 관리 대상 RTK/Serena hook만 교체하고 다른 hook과 설정은 보존한다. 재실행해도 관리 대상 hook은 중복되지 않는다.

| 이벤트 | Codex | Claude Code |
|--------|-------|-------------|
| `PreToolUse: Bash` | `rtk hook codex` + Serena `remind` | `rtk hook claude` + Serena `remind` |
| `PreToolUse: Read/Grep/Glob` | — | Serena `remind` |
| `PreToolUse: Serena MCP` | `plan-guard` 한 번 | `auto-approve` (클라이언트의 허용 모드에 따름) |
| `PostToolUse: Serena MCP` | `reset` | `reset` |
| `SessionStart: startup/resume` | `activate` | `activate` |
| `UserPromptSubmit` | `plan-context` | — |
| `SessionEnd` | `cleanup` | `cleanup` |

RTK는 셸 명령 rewrite를 담당하고 Serena는 reminder와 plan 제한을 담당한다. Serena 2.1.0의 reminder parser는 `rtk grep`, `rtk proxy rg` 같은 RTK prefix를 해석하지 못해 해당 명령을 검색 횟수에 집계하지 않는다. 원래 검색 명령과 Claude의 Read/Grep/Glob은 집계되며, plan guard와 reset은 별도로 동작한다. Bash hook은 같은 그룹에 등록하며, Serena MCP에는 별도 matcher를 사용한다. 이미지 예시의 중복 `plan-guard`와 머신별 다른 hook은 추가하지 않는다. 이전 `rtk-rewrite.sh` 등록도 native hook으로 교체한다. Codex hook의 Serena timeout은 기본 5초, `SessionEnd`는 지원 범위에 맞춰 3초다. `SessionEnd` 사용에는 Codex 0.145.0 이상이 필요하다.

전역 설정 후 Codex와 Claude Code를 재시작한다. Codex에서는 `/hooks`로 로드 상태를, 두 클라이언트에서는 `/mcp`로 Serena 연결을 확인한다. 프로젝트 hook에 대한 trust 요청이 있으면 해당 클라이언트에서 검토한다.

### 검증과 문제 해결

```sh
rtk --version
uv tool list
serena-hooks --help
codex mcp get serena
claude mcp get serena
```

회사 인증서 환경에서 uv가 `UnknownIssuer`로 실패하면 시스템 인증서가 신뢰되도록 구성한 후 `UV_SYSTEM_CERTS=true ./setup/serena.sh`를 사용할 수 있다. 이는 일반 설치에 필수인 옵션은 아니다.

일반 명령으로 `rtk`를 직접 실행할 때는 PATH에 설치 디렉터리가 필요하다. Codex의 `shell_environment_policy.inherit = "core"` 환경에서 찾지 못하면 RTK 설치 디렉터리를 해당 정책의 PATH에 추가하거나, 실행 가능한 절대 경로를 사용한다. 스크립트가 등록하는 hook과 MCP는 절대 경로를 사용한다. `rtk.sh codex`는 기존 설치 방식과 같이 `/usr/local/bin/rtk` symlink 생성을 시도한다. 권한이 없고 대화형 sudo도 사용할 수 없으면 복구 명령을 출력한다.

공식 참고: [RTK quick start](https://www.rtk-ai.app/docs/getting-started/quick-start/), [Serena client 설정](https://github.com/oraios/serena/blob/main/docs/02-usage/030_clients.md).
