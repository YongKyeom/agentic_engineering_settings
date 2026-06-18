# AI Agent Settings

Codex / Claude Code 개발환경을 다른 머신에서도 같은 방식으로 재현하기 위한 설정 저장소.

## 핵심 목적

- 전역 agent 운영 규칙(`AGENTS.md`, `CLAUDE.md`)을 GitHub로 관리
- 직접 관리할 custom/third-party skill을 `skills/` 아래에 실제 파일로 보관
- Python 프로젝트 템플릿을 `python-project/`에 보관

이 레포 자체는 Python 프로젝트가 아니다. 루트에서 `uv init`을 하지 않는다.

## Repository 구조

```text
.
├── AGENTS.md               # 전역 AI agent 운영 규칙 (Codex용)
├── CLAUDE.md               # 전역 AI agent 운영 규칙 (Claude Code용)
├── README.md               # 이 파일
├── setup/
│   ├── claude-code.md      # Claude Code 셋업 가이드
│   ├── claude-code.sh      # Claude Code 자동 셋업 스크립트
│   ├── codex.sh            # Codex 자동 셋업 스크립트
│   ├── dev-env.sh          # 개발 환경 셋업 스크립트 (shell + tmux)
│   ├── zshrc               # ~/.zshrc 템플릿 (dev-env.sh가 복사)
│   └── p10k.zsh            # powerlevel10k 프롬프트 설정 백업
├── skills/
│   ├── README.md
│   └── <skill-name>/
│       └── SKILL.md
└── python-project/         # Python 프로젝트 템플릿
    ├── AGENTS.md
    ├── CLAUDE.md
    └── docs/
        ├── README.md
        ├── plan/
        ├── handoff/
        ├── decisions/
        └── agentic-engineering.md
```

## Quick Start

새 머신에서 셋업할 때:

```sh
git clone <github-repo-url> agent_settings
cd agent_settings

# 1. 개발 환경 (oh-my-zsh, powerlevel10k, tmux + TPM, claude alias)
./setup/dev-env.sh

# 2. Claude Code
./setup/claude-code.sh                # 기본
./setup/claude-code.sh --with-slidev  # Slidev 포함

# 2. Codex (Claude Code 대신)
./setup/codex.sh
./setup/codex.sh --with-slidev
```

`dev-env.sh`는 `~/.zshrc`, `~/.tmux.conf`, `~/.p10k.zsh`를 항상 repo 기준으로 덮어쓴다. 기존 설정이 있어도 그대로 덮어씌워진다.

`setup/codex.sh`는 RTK 설치/탐지 후 Codex core PATH에서도 `rtk`가 보이도록 보조한다. 자세한 fallback과 검증 방법은 setup 폴더 가이드를 참고한다.

스크립트는 자동화 가능한 부분만 처리한다. Claude Dashboard 플러그인 설치 등 수동 단계는 셋업 가이드 참고.

- **Claude Code 셋업 가이드**: [`setup/claude-code.md`](setup/claude-code.md)
- **setup 폴더 가이드**: [`setup/README.md`](setup/README.md)

실행 후 `source ~/.zshrc` → `tmux` 순으로 확인.

### oh-my-zsh

| 항목 | 내용 |
|------|------|
| 테마 | `powerlevel10k` — 프롬프트 스타일, 설정은 `setup/p10k.zsh` 백업 |
| `zsh-autosuggestions` | 히스토리 기반 자동완성 |
| `zsh-syntax-highlighting` | 명령어 실시간 문법 하이라이트 |
| `fzf` | 퍼지 파인더 (Ctrl+R 히스토리, Ctrl+T 파일 탐색) |
| `zoxide` | 스마트 디렉토리 이동 (`z <keyword>`) |

### tmux + TPM

| 플러그인 | 설명 |
|----------|------|
| `tmux-sensible` | 합리적인 기본값 모음 |
| `tmux-resurrect` | 세션 저장/복원 (`Ctrl+b Ctrl+s / Ctrl+r`) |
| `tmux-continuum` | 세션 자동 저장 (resurrect 연동) |
| `tmux-yank` | 드래그 선택 → 클립보드 자동 복사 |
| `dracula/tmux` | 상태바 테마 (cwd, git, CPU, RAM, 시간) |

### CLI 도구

| 도구 | 설명 |
|------|------|
| `btop` | 시스템 모니터 (CPU, 메모리, 프로세스) |
| `ncdu` | 디스크 사용량 시각화 |

## 관리하는 Skill 목록

| Skill | 설명 |
|-------|------|
| `handoff` | 컨텍스트 전달 및 세션 이어받기 |
| `humanizer` | AI 문체 제거, 자연스러운 산문 |
| `git-commit-helper` | 커밋 메시지 작성 |
| `requirements-clarity` | 요구사항 명확화 |
| `agent-md-refactor` | AGENTS.md / CLAUDE.md 리팩터 |
| `skill-judge` | 스킬 검토 및 수정 |
| `lesson-learned` | 반복 실수에서 규칙 추출 |
| `writing-clearly-and-concisely` | 명확하고 간결한 글쓰기 |
| `karpathy-guidelines` | Karpathy 코딩 원칙 (과잉 구현 방지, 외과적 수정) |
| `packet-review` | 플랜 문서 대비 현재 구현 리뷰 (drift, 미흡, must-close 항목) |
| `presentation-slidev` | Slidev로 발표자료 작성 및 반복 수정 (학위논문/사이드 프로젝트) |
| `c4-architecture` | C4 아키텍처 다이어그램 |
| `mermaid-diagrams` | Mermaid 다이어그램 |
| `excalidraw` | 러프 스케치 다이어그램 |
| `code-review` | diff 기준 코드 리뷰 (버그, 타입, 스타일, 보안). Claude Code 내장(`/code-review`), Codex는 custom skill |
| `deep-research` | 멀티 소스 fan-out 리서치 → 사실 검증 → 인용 포함 리포트. Claude Code 내장(`/deep-research`), Codex는 custom skill |

## Skill 관리 원칙

`skills/`에는 직접 관리할 custom/third-party skill만 둔다. 공식 system skill이나 공식 플러그인에서 다시 설치할 수 있는 범용 skill은 보관하지 않는다.

새 skill을 추가할 때:

1. `~/.codex/skills/<skill-name>/` 또는 `~/.claude/skills/<skill-name>/`에 설치하거나 수정한다.
2. 동작을 확인한다.
3. 이 레포의 `skills/<skill-name>/SKILL.md`에 복사한다.
4. `AGENTS.md`와 `CLAUDE.md`의 Related Skills 섹션에 항목을 추가한다.
5. 변경사항을 Git으로 commit한다.

수정이 필요하면 원본을 덮어쓰기보다 별도 이름의 custom skill로 복사해서 관리한다.

## Python 프로젝트 템플릿

새 Python 프로젝트에 이 구조를 복사해서 사용한다.

```sh
cp -R python-project/. <target-python-project>/
```

복사 후 해당 프로젝트에 맞게 `AGENTS.md`, `CLAUDE.md`, `docs/` 내용을 수정한다.
