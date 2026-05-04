# Python Project Docs Template

이 폴더는 Python 프로젝트에서 반복해서 쓰는 프로젝트별 문서 구조 템플릿입니다.
새 프로젝트를 만들 때 `python-project/`를 복사한 뒤, 실제 코드베이스와 팀 규칙에 맞게 내용을 조정합니다.

루트 `AGENTS.md`는 짧게 유지하고, 세부 규칙은 이 `docs/` 폴더의 문서로 분리합니다.
이렇게 하면 Codex나 Claude가 모든 규칙을 한 번에 읽지 않고, 필요한 문서만 선택해서 읽을 수 있습니다.

## 폴더 구조

```text
docs/
├── coding-convention.md     # Python 코드 스타일, docstring, typing, logging, validation 규칙
├── git-convention.md        # 커밋 메시지 형식과 Git 작업 규칙
├── architecture.md          # 모듈 경계, SRP, 의존성 방향, 프로젝트 구조 규칙
├── agentic-engineering.md   # Codex, Claude, sub-agent 협업 규칙
├── plan/                    # 로컬 계획, PRD, task breakdown, 실행 메모
├── handoff/                 # 로컬 세션 인수인계 메모
└── decisions/               # 공유해야 하는 기술 결정과 ADR
```

## 문서별 역할

`coding-convention.md`는 Python 코드를 작성하거나 수정할 때 적용하는 규칙입니다.
formatter, linter, docstring, comment, type hint, logging, validation 범위를 다룹니다.

`git-convention.md`는 commit message와 Git 작업 기준입니다.
회사나 팀에서 커밋 메시지 품질을 일정하게 유지하려면 이 문서를 기준으로 삼습니다.

`architecture.md`는 구조 변경이 필요한 작업에서 봅니다.
module boundary, dependency direction, configuration, long-lived architecture decision 기준을 정리합니다.

`agentic-engineering.md`는 Codex, Claude, human reviewer가 협업하는 방식입니다.
sub-agent를 언제 쓰고, review feedback을 어떻게 분류하고, handoff를 언제 남길지 정의합니다.

`plan/`은 각 개발자가 로컬에서 작업 계획을 세우는 공간입니다.
폴더 자체는 Git에 남기지만, 개별 plan 파일은 기본적으로 commit하지 않습니다.

`handoff/`는 긴 작업을 다른 세션이나 다른 agent thread로 넘길 때 쓰는 로컬 공간입니다.
폴더 자체는 Git에 남기지만, 개별 handoff 파일은 기본적으로 commit하지 않습니다.

`decisions/`는 공유해야 하는 장기 기술 결정을 기록하는 공간입니다.
ADR처럼 팀 전체가 알아야 하는 결정은 이곳에 commit합니다.

## 사용 원칙

- 루트 `AGENTS.md`에는 모든 작업에 적용되는 핵심 규칙과 문서 링크만 둡니다.
- 세부 규칙은 이 `docs/` 폴더에 주제별로 나눠 둡니다.
- 임시 계획과 세션 메모는 `plan/`, `handoff/`에 두고 기본적으로 commit하지 않습니다.
- 장기적으로 유지해야 하는 결정만 `decisions/`에 commit합니다.
- 프로젝트 규칙이 바뀌면 관련 문서를 함께 업데이트합니다.
