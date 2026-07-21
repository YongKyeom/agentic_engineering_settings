---
name: decision-record
description: Record a durable technical decision as an ADR (Architecture Decision Record) in docs/decisions/. Use immediately after an architecture, module-boundary, dependency, framework, storage, or API-contract choice is settled, when a hard-to-reverse direction is set, when performance/security/operations tradeoffs were weighed, or when the user says "ADR", "결정 기록", "decision record", or asks to note down why something was decided. Do NOT use for typo fixes, small refactors, test renames, or one-off local experiments.
---

# decision-record

오래 유지해야 하는 기술 결정을 ADR로 기록하는 스킬. 목적은 미래 작업자에게 결정의 "왜"를 남기는 것이다.

## 1. ADR감인지 판정

작성한다:

- 아키텍처나 모듈 경계가 바뀐다.
- dependency, framework, storage, API contract를 선택한다.
- 되돌리기 어려운 방향을 정한다.
- 성능, 보안, 운영, 유지보수 tradeoff가 있다.
- 나중에 "왜 이렇게 했는지" 다시 설명할 가능성이 크다.

작성하지 않는다 (해당하면 여기서 종료):

- 단순 typo 수정, 작은 함수 내부 리팩터링, 테스트 이름 변경.
- 일회성 로컬 실험, 공유할 필요 없는 임시 계획.

## 2. 저장 위치

- 기본: 프로젝트의 `docs/decisions/`. 폴더가 없으면 만들지 사용자에게 확인한다.
- 프로젝트에 다른 ADR 위치 규약이 있으면 그것을 따른다.

## 3. 채번과 파일명

- 번호가 붙은 `NNNN-*.md` 파일만 대상으로 최대 번호 + 1 (README.md 등 번호 없는 파일은 무시). 번호는 4자리 zero-pad, 시간 순서대로 증가.
- 파일명은 짧은 영어 kebab-case. 문서 제목은 `# ADR-NNNN: 한국어 제목`.

```text
0003-business-agent-tool-loop.md
0006-supervisor-tool-loop-agent.md
```

## 4. 본문 작성

기본 구조. 규모는 결정 크기에 비례한다 — 작은 결정은 배경·결정·영향만, 큰 전환은 전체 섹션을 쓴다.
작성 전에 [references/example-adr.md](references/example-adr.md)를 읽고 밀도와 문체를 맞춘다.

```md
# ADR-NNNN: 제목 — 핵심을 요약하는 한 줄

- 상태: 유효
- 결정일: YYYY-MM-DD
- 관련: [NNNN-xxx.md](./NNNN-xxx.md), [../architecture.md](../architecture.md) §N

## 1. 배경

왜 이 결정이 필요했는지. 문제 상황, 제약 조건, 실측으로 확인된 문제를 적는다.

## 2. 결정

무엇을 선택했는지 명확히. 결정이 여러 갈래면 D1, D2… 번호를 붙인 표로 정리한다.

## 3. 기각한 대안

| 대안 | 기각 사유 |
|---|---|

## 4. 근거

실측 데이터, 재현 결과, 설계 문서 대조처럼 결정을 뒷받침하는 검증 가능한 증거.

## 5. 영향

이 선택으로 생기는 장점, 비용, 후속 작업, 검증 계획.

## 6. 개정 이력

- YYYY-MM-DD: 신설.
```

작성 원칙:

- 본문은 한국어로 쓴다. 파일명, 코드 식별자, API 명은 영어를 유지한다.
- "좋아서 선택했다"가 아니라 어떤 제약 때문에 선택했는지 쓴다.
- 기각한 대안과 그 사유를 남긴다 — 같은 대안이 다시 제안되는 것을 막는다.
- 근거는 실측·재현·문서 대조처럼 검증 가능한 사실로 적고, 이미 실행한 검증과 아직 남은 검증을 구분한다.
- 관련 ADR·설계 문서는 상호 링크한다. 필요하면 §섹션 단위까지 짚는다.
- 대화 컨텍스트에서 채우되, 모르는 항목을 추측으로 메꾸지 않는다 — 사실과 추정이 섞이면 기록 가치가 사라진다. 불명확하면 사용자에게 묻는다.

## 5. 결정이 바뀔 때

- 구현 결과 반영, 부분 개정, 세부 결정(D-n) 하나의 대체는 같은 ADR의 **개정 이력**에 날짜와 함께 추가한다.
- 결정의 방향 자체가 뒤집히면 새 ADR을 만들고, 옛 문서의 상태를 `대체됨(ADR-NNNN)`으로 바꾼 뒤 상호 링크한다.
- 어느 쪽이든 기존 내용을 조용히 고치지 않는다 — 결정 이력은 audit trail이라, 조용한 수정은 "당시의 왜"를 파괴한다.

## 상태 값

- `유효`: 현재 채택된 결정. 구현이 끝났으면 `유효 (구현 완료)`처럼 부기한다.
- `보류`: 결정이 필요하지만 아직 유보.
- `기각`: 검토했지만 채택하지 않음.
- `대체됨(ADR-NNNN)`: 더 새로운 decision이 이 결정을 대체함.
