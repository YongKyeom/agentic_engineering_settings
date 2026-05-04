# Decisions

이 폴더는 오래 유지되어야 하는 기술 결정을 기록하는 공간입니다.
Architecture Decision Record, dependency 선택, 모듈 경계 변경, 데이터 저장 방식 변경처럼 팀이나 미래 작업자가 알아야 하는 결정을 여기에 남깁니다.

`plan/`이나 `handoff/`와 달리, 이 폴더의 문서는 공유 지식으로 commit하는 것을 기본으로 합니다.
다만 사소한 구현 메모까지 ADR로 만들 필요는 없습니다.

## 언제 작성하는가

다음에 해당하면 decision 문서를 작성합니다.

- 아키텍처나 모듈 경계가 바뀝니다.
- dependency, framework, storage, API contract를 선택합니다.
- 되돌리기 어려운 방향을 정합니다.
- 성능, 보안, 운영, 유지보수 tradeoff가 있습니다.
- 나중에 “왜 이렇게 했는지” 다시 설명해야 할 가능성이 큽니다.

다음은 보통 decision 문서가 필요 없습니다.

- 단순 typo 수정.
- 작은 함수 내부 리팩터링.
- 테스트 이름 변경.
- 일회성 로컬 실험.
- 사용자에게 공유할 필요 없는 임시 계획.

## 파일명 규칙

번호와 짧은 제목을 사용합니다.

```text
0001-short-title.md
0002-use-postgres-for-event-store.md
0003-split-training-and-evaluation-modules.md
```

번호는 시간 순서대로 증가시킵니다.
이미 작성된 decision을 수정해 과거 결정을 덮어쓰기보다, 새 decision으로 supersede하는 편이 추적에 유리합니다.

## Status 값

- `Accepted`: 현재 채택된 결정입니다.
- `Deferred`: 결정이 필요하지만 아직 보류했습니다.
- `Rejected`: 검토했지만 채택하지 않았습니다.
- `Superseded`: 더 새로운 decision이 이 결정을 대체했습니다.

## ADR Template

```md
# 0001. Short title

## Status

Accepted | Deferred | Rejected | Superseded

## Context

왜 이 결정이 필요했는지 적습니다.
문제 상황, 제약 조건, 대안, source of truth를 포함합니다.

## Decision

무엇을 선택했는지 명확히 적습니다.
선택하지 않은 대안이 중요하면 함께 언급합니다.

## Consequences

이 선택으로 생기는 장점, 단점, tradeoff, 후속 작업을 적습니다.
검증이나 migration이 필요하면 함께 적습니다.
```

## 작성 원칙

- 결정의 배경과 이유를 남깁니다.
- “좋아서 선택했다”가 아니라 어떤 제약 때문에 선택했는지 씁니다.
- 장점뿐 아니라 비용과 위험도 함께 적습니다.
- 이미 실행한 검증과 아직 남은 검증을 구분합니다.
- 결정이 바뀌면 기존 문서를 조용히 고치지 말고 새 decision을 만들거나 `Superseded`로 표시합니다.
