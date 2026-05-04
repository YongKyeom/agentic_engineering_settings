# Codex Settings

이 레포는 내 Codex/Claude 개발환경을 다른 머신에서도 같은 방식으로 재현하기 위한 설정 저장소다.

핵심 목적은 세 가지다.

- 전역 `AGENTS.md` 설정을 GitHub로 관리한다.
- 직접 관리할 custom/third-party skill을 `skills/` 아래에 실제 파일로 보관한다.
- Python 프로젝트를 만들 때 참고할 프로젝트별 `AGENTS.md`와 문서 구조를 `python-project/`에 보관한다.

이 레포 자체는 Python 프로젝트가 아니다. 루트에서 `uv init`을 하지 않는다.

## Repository 구조

```text
.
├── AGENTS.md
├── README.md
├── skills/
│   ├── <skill-name>/
│   │   └── SKILL.md
└── python-project/
    ├── AGENTS.md
    └── docs/
        ├── README.md
        ├── plan/
        ├── handoff/
        ├── decisions/
        └── agentic-engineering/
```

## 각 파일과 폴더의 역할

### `AGENTS.md`

전역 Codex 운영 규칙이다.

새 환경에서는 이 파일을 `~/.codex/AGENTS.md`로 복사하거나 symlink해서 사용한다.

### `skills/`

직접 관리할 custom/third-party skill을 실제 파일로 보관한다.

각 skill은 보통 다음 구조를 가진다.

```text
skills/<skill-name>/SKILL.md
```

공식 Codex system skill이나 공식 플러그인에서 다시 설치할 수 있는 범용 skill은 이 레포에 보관하지 않는다. 이 레포의 `skills/`에는 직접 들고 다닐 custom/third-party skill만 둔다.

## 추천 skill 리스트

아래 항목은 이 레포에 vendoring하지 않는다.
새 환경에서 필요하면 Codex 공식 skill, 공식 plugin, 또는 기존 설치 도구로 다시 설치한다.

### Codex system skill

Codex 환경에서 기본 제공되는 성격의 skill이다.
보통 별도 관리하지 않는다.

- `skill-installer`
- `skill-creator`
- `plugin-creator`
- `openai-docs`
- `imagegen`

### 공식 plugin 또는 런타임 계열 skill

Codex 공식 plugin이나 runtime 기능으로 다시 설치하거나 사용할 수 있는 항목이다.
레포에 넣으면 파일 수만 늘고, 버전 충돌 가능성이 생기므로 추천 리스트로만 남긴다.

- `doc`
- `pdf`
- `imagegen`
- `jupyter-notebook`
- `screenshot`

### 이 레포에 보관할 skill

아래처럼 개인 workflow, 회사 workflow, third-party 기반 수정본, 직접 만든 skill만 `skills/`에 둔다.

- `handoff`
- `humanizer`
- `git-commit-helper`
- `requirements-clarity`
- `qa-test-planner`
- `agent-md-refactor`
- `skill-judge`
- `lesson-learned`
- `writing-clearly-and-concisely`

### `python-project/`

새 Python 프로젝트에서 참고할 템플릿이다.

프로젝트별 plan, handoff, decision, agentic engineering 문서는 루트가 아니라 각 프로젝트 안에 있어야 하므로 이 구조는 `python-project/docs/` 아래에 둔다.

## 새 환경에 설치하는 방법

### 1. Repository clone

```sh
git clone <github-repo-url> codex_settings
cd codex_settings
```

### 2. 전역 AGENTS.md 설치

Symlink 방식은 이 레포의 변경사항이 바로 전역 설정에 반영된다.

```sh
mkdir -p ~/.codex
ln -sfn "$PWD/AGENTS.md" ~/.codex/AGENTS.md
```

Copy 방식은 현재 내용을 한 번만 복사한다.

```sh
mkdir -p ~/.codex
cp AGENTS.md ~/.codex/AGENTS.md
```

개인적으로는 이 레포를 source of truth로 둘 목적이면 symlink 방식이 낫다.

### 3. Skill 설치

기본 설치는 이 레포의 `skills/` 내용을 `~/.codex/skills/`로 복사하면 된다.
이 명령은 이 레포에서 직접 관리하는 skill만 설치한다.

```sh
mkdir -p ~/.codex/skills
cp -R skills/. ~/.codex/skills/
```

이미 설치된 skill을 이 레포의 버전으로 덮어쓰고 싶으면 같은 명령을 다시 실행한다.

정확히 이 레포의 `skills/`와 로컬 `~/.codex/skills/`를 맞추고 싶다면 `rsync --delete`를 쓸 수 있다.
단, 이 방식은 로컬에만 있던 skill을 지울 수 있으므로 새 머신 초기 셋업 때만 쓰는 편이 안전하다.

```sh
rsync -a --delete skills/ ~/.codex/skills/
```

설치 후 Codex를 재시작해야 새 skill이 인식된다.

### 4. Python 프로젝트 템플릿 사용

새 Python 프로젝트에서 이 구조를 참고하거나 복사한다.

```sh
cp -R python-project/. <target-python-project>/
```

복사 후 해당 프로젝트에 맞게 `AGENTS.md`와 `docs/` 내용을 수정한다.

## Skill 관리 원칙

`skills/`에는 직접 관리할 custom/third-party skill만 둔다.

새 skill을 추가할 때는 다음 순서로 처리한다.

1. `~/.codex/skills/<skill-name>/`에 skill을 설치하거나 수정한다.
2. 동작을 확인한다.
3. 이 레포의 `skills/<skill-name>/`에 복사한다.
4. 변경사항을 Git으로 commit한다.
5. 다른 환경에서는 이 레포의 `skills/`를 `~/.codex/skills/`로 복사한다.

Official/system skill이나 Codex 공식 플러그인에서 다시 설치 가능한 skill은 보관하지 않는다.
수정이 필요하면 원본을 덮어쓰기보다 별도 이름의 custom skill로 복사해서 관리한다.

## 현재 환경의 skill을 다시 반영하는 방법

현재 머신의 설치 상태를 이 레포에 다시 반영할 때도 전체 `~/.codex/skills`를 그대로 복사하지 않는다.
공식/system/plugin 계열은 제외하고, 직접 관리할 skill만 선택해서 복사한다.

```sh
cp -R ~/.codex/skills/<skill-name> skills/<skill-name>
```

그 다음 `skills/<skill-name>/SKILL.md`를 확인하고 commit한다.
