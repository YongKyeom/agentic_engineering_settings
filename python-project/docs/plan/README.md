# Plan Docs

이 폴더는 각 개발자가 로컬에서 계획을 정리하기 위한 공간입니다.
PRD 초안, task breakdown, 실험 계획, 실행 순서, 조사 메모처럼 작업 중에 필요한 문서를 여기에 둡니다.

중요한 기준은 “폴더 구조는 공유하지만, 개별 plan 파일은 기본적으로 공유하지 않는다”입니다.
즉, 이 폴더와 `.gitkeep`, `README.md`, `AGENTS.md`는 템플릿으로 Git에 남기고, 실제 계획 파일은 각 개발자의 로컬 작업물로 취급합니다.

## 사용 목적

- 기능 구현 전에 범위와 완료 기준을 정리합니다.
- 실험이나 리팩터링 전에 작업 순서를 쪼갭니다.
- Codex나 Claude에게 넘길 작업 단위를 명확히 합니다.
- 아직 공유 문서로 확정되지 않은 생각을 임시로 적습니다.
- 긴 작업에서 현재 위치와 다음 행동을 놓치지 않도록 합니다.

## Git 추적 기준

- 이 폴더 자체는 Git에 유지합니다.
- `.gitkeep`, `README.md`, `AGENTS.md`는 commit합니다.
- 개별 plan 파일은 기본적으로 commit하지 않습니다.
- 사용자가 명시적으로 공유 문서로 남기라고 했을 때만 plan 파일을 commit합니다.
- 공유해야 하는 장기 결정은 plan 파일이 아니라 `docs/decisions/`에 남깁니다.

## 권장 파일명

로컬에서 사용할 때는 아래처럼 날짜나 주제를 포함하면 찾기 쉽습니다.

```text
YYYY-MM-DD-topic-plan.md
feature-name-v1-prd.md
experiment-name-plan.md
refactor-target-plan.md
```

## Plan Template

```md
# Title

## Goal

이번 작업으로 달성하려는 목표를 적습니다.

## Source Of Truth

작업 기준이 되는 사용자 지시, issue, spec, 코드 파일, 논문, 문서를 적습니다.

## Scope

이번 작업에 포함되는 범위를 적습니다.

## Non-Goals

이번 작업에서 의도적으로 제외하는 범위를 적습니다.

## Tasks

- [ ] Task 1
- [ ] Task 2

## Validation

완료 전에 확인해야 할 테스트, lint, type check, manual check를 적습니다.

## Risks

실패 가능성, 모호한 요구사항, 의존성, 회귀 위험을 적습니다.
```

## Agent 사용 기준

Codex나 Claude는 이 폴더의 plan을 참고할 수 있지만, 오래된 plan을 최신 source of truth로 취급하면 안 됩니다.
사용자 지시, 현재 코드, 최신 decision 문서와 충돌하면 최신 source of truth를 우선합니다.
