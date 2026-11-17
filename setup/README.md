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
| `herdr.sh` | Herdr TUI와 zsh를 설치하고 터미널 기본값, 패널 이동 키, Codex/Claude 연동을 설정한다. |
| `configure-herdr.py` | 기존 TOML을 보존하면서 Herdr 설정을 병합하고 공식 Markdown과 전역 조건부 지침을 갱신한다. |
| `herdr.zsh` | 인자 없이 실행한 `herdr`를 현재 프로젝트의 고정 세션으로 연결한다. |

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

## Herdr 터미널과 agent 연동

`codex.sh`와 `claude-code.sh`는 Herdr 설정도 함께 적용한다. Herdr만 설치하거나 기존 환경에 설정을 병합하려면:

```sh
./setup/herdr.sh           # Codex와 Claude 모두 설정
./setup/herdr.sh codex     # Codex만 연동
./setup/herdr.sh claude    # Claude만 연동
```

macOS·Linux를 대상으로 하며 `uv`가 필요하다. zsh와 Herdr가 없으면 설치한다. Herdr는 Homebrew가 있으면 `brew install herdr`, 없으면 [공식 설치 스크립트](https://herdr.dev/tui/docs/install/)를 사용한다. 기존 바이너리는 유지한다. 설정 병합용 `tomlkit`은 `uv run`의 격리 환경에 설치하며, 일반 Python 프로젝트의 의존성은 바꾸지 않는다.

### 셸, 시작 위치, 이동 키

`~/.config/herdr/config.toml`에 아래 값을 병합한다. `default_shell`에는 탐지한 zsh의 절대 경로를 저장한다. `HERDR_CONFIG_PATH`를 지정했다면 해당 파일을 사용한다. 테마, 알림, 다른 키와 TOML 주석은 보존한다.

```toml
[terminal]
default_shell = "/bin/zsh" # 예시: 설치 환경에서 탐지한 경로
shell_mode = "auto"
new_cwd = "current"

[keys]
focus_pane_left = ["prefix+h", "prefix+left"]
focus_pane_down = ["prefix+j", "prefix+down"]
focus_pane_up = ["prefix+k", "prefix+up"]
focus_pane_right = ["prefix+l", "prefix+right"]
```

설치 스크립트는 `~/.config/agent-setup/herdr.zsh`를 설치하고 `~/.zshrc`에 불러오는 줄을 추가한다. `ZDOTDIR`이 설정되어 있으면 그 아래의 `.zshrc`를 사용한다. 새 zsh에서 프로젝트 경로로 이동한 뒤 `herdr`만 입력하면 프로젝트별 고정 세션에 연결한다. Git 저장소에서는 최상위 경로, 그 밖에서는 현재 경로의 SHA-256 앞 16자리를 사용해 `project-<hash>` 세션을 선택한다. 경로의 공백을 지원하며 같은 저장소의 하위 폴더는 세션을 공유한다.

새 프로젝트 세션의 첫 터미널은 `herdr`를 실행한 디렉터리에서 시작한다. 같은 프로젝트에 다시 연결하면 기존 패널과 작업 경로를 복원한다. `herdr config check` 같은 인자가 있는 명령과 `--session` 지정은 그대로 전달한다. Herdr 패널 안이거나 `HERDR_SESSION`·`HERDR_SOCKET_PATH`로 대상을 정한 경우에도 자동 선택을 건너뛴다. 기존 공용 세션은 보존하며 `command herdr`로 연결할 수 있다.

`current`는 Herdr 서버 프로세스의 실행 디렉터리를 사용한다. 기존 서버에 다시 연결해도 그 경로는 바뀌지 않으므로 이 설정만으로 프로젝트별 시작 위치를 보장하지는 않는다. 새 창이 원본 패널의 작업 디렉터리를 따라가게 하려면 `new_cwd = "follow"`로 바꾼다. [공식 설정 문서](https://herdr.dev/tui/docs/configuration/#terminal-defaults)에 각 정책이 정리되어 있다.

`shell_mode = "auto"`는 macOS에서 로그인 셸을 사용한다. 기존 패널의 셸과 디렉터리는 그대로이며 새로 만드는 패널부터 기본값을 사용한다. `prefix`는 기존 설정을 보존하며, 미설정 시 `Ctrl+b`다. 따라서 기본 설정에서는 `Ctrl+b` 다음 `h/j/k/l` 또는 방향키로 이동한다. tmux 안에서 중첩 실행하면 같은 prefix를 먼저 tmux가 받으므로 tmux의 전달 키를 사용하거나 둘 중 하나의 prefix를 변경한다.

### 공식 Markdown과 전역 지침

설치된 CLI의 `herdr --skill` 출력을 수정 없이 다음 파일에 저장한다.

| 대상 | 공식 Markdown | 조건부 실행 지침 |
| --- | --- | --- |
| Codex | `~/.codex/HERDR.md` | `~/.codex/AGENTS.md` |
| Claude | `~/.claude/HERDR.md` | `~/.claude/CLAUDE.md` |

`CODEX_HOME`과 `CLAUDE_CONFIG_DIR`을 지정하면 해당 경로를 사용한다. 전역 지침은 실행 환경의 `HERDR_ENV=1`을 확인하고, 요청된 Herdr 제어 작업에만 공식 파일을 읽도록 한다. Herdr 밖에서는 일반 셸 작업을 계속하며 다른 세션의 패널·agent를 조회하거나 제어하지 않는다. 공식 파일을 모든 작업에 자동으로 가져오는 `@` import는 사용하지 않는다.

Codex·Claude 상태 연동은 `herdr integration install codex` / `claude`로 설치한다. 기존 RTK·Serena hook을 유지하면서 Herdr가 관리하는 항목을 병합한다. 변경 전 설정과 전역 지침은 `~/.local/state/agent-setup/herdr-<timestamp>-<pid>/`에 백업한다. 설정 파일은 `herdr config check`를 통과한 뒤 적용한다.

### 확인과 갱신

```sh
rtk proxy herdr --version
rtk proxy herdr config check
rtk proxy herdr integration status
rtk proxy herdr server reload-config # 실행 중인 서버에 설정 반영

# Herdr 패널 안에서만 1이 출력되는지 확인
rtk proxy printenv HERDR_ENV
```

현재 세션에 연결되어 있다면 메뉴의 `reload config`로 클라이언트 키 설정도 다시 읽을 수 있다. 서버를 중지하거나 기존 패널을 닫을 필요는 없다.

Herdr 갱신은 설치 방식에 맞춘다. Homebrew에서는 `brew update` 후 `brew upgrade herdr`, 공식 설치 스크립트로 설치했다면 `herdr update`를 사용한다. 갱신 후 `./setup/herdr.sh`를 다시 실행하면 설치된 버전의 공식 Markdown과 연동을 갱신한다. 설치와 설정 병합만으로 셸이나 tmux를 자동 실행하지는 않는다.

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

MCP 실행 인자에 `--open-web-dashboard false`를 지정해 Serena가 시작될 때 대시보드를 브라우저에 자동으로 열지 않도록 한다. 대시보드 서버는 유지하므로 필요하면 표시된 로컬 주소로 직접 접속할 수 있다. 다른 실행 경로에서도 자동 열기를 끄려면 `~/.serena/serena_config.yml`의 `web_dashboard_open_on_launch`를 `false`로 설정한다.

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
