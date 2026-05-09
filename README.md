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
├── AGENTS.md               # 전역 AI agent 운영 규칙 (Codex용, RTK 포함)
├── CLAUDE.md               # 전역 AI agent 운영 규칙 (Claude Code용, RTK 제외)
├── README.md               # 이 파일
├── setup/
│   ├── claude-code.md      # Claude Code 셋업 가이드
│   └── codex.md            # Codex 셋업 가이드
├── skills/
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
        └── agentic-engineering/
```

## Quick Start

새 머신에서 셋업할 때:

```sh
git clone <github-repo-url> agent_settings
cd agent_settings

# Claude Code
./setup/claude-code.sh                # 기본
./setup/claude-code.sh --with-slidev  # Slidev 포함

# Codex
./setup/codex.sh
./setup/codex.sh --with-slidev
```

스크립트는 자동화 가능한 부분만 처리한다. Claude Dashboard 플러그인 설치 등 수동 단계는 셋업 가이드 참고.

- **Claude Code 셋업 가이드**: [`setup/claude-code.md`](setup/claude-code.md)
- **Codex 셋업 가이드**: [`setup/codex.md`](setup/codex.md)

## 관리하는 Skill 목록

| Skill | 설명 |
|-------|------|
| `handoff` | 컨텍스트 전달 및 세션 이어받기 |
| `humanizer` | AI 문체 제거, 자연스러운 산문 |
| `git-commit-helper` | 커밋 메시지 작성 |
| `requirements-clarity` | 요구사항 명확화 |
| `qa-test-planner` | 테스트 계획 수립 |
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

## Skill 관리 원칙

`skills/`에는 직접 관리할 custom/third-party skill만 둔다. 공식 system skill이나 공식 플러그인에서 다시 설치할 수 있는 범용 skill은 보관하지 않는다.

새 skill을 추가할 때:

1. `~/.codex/skills/<skill-name>/` 또는 `~/.claude/commands/<skill-name>.md`에 설치하거나 수정한다.
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
