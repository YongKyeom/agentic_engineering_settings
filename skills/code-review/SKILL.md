---
name: code-review
description: Review a code diff, hotfix, or specified files for actionable correctness, type, security, performance, and maintainability issues. Default to read-only; apply fixes when explicitly requested, including --fix. For acceptance of a frozen functional bundle against its Plan, use packet-review without repeating the same broad review.
---

# Code Review

diff나 지정 파일에서 실제로 문제가 되는 변경을 찾는다. 사용자 지시와 프로젝트 규칙을 우선하며, 선호하는 스타일을 버그로 보고하지 않는다.

## Usage

```
/code-review [--fix] [target]
```

- `target`: 파일, 디렉터리, git diff 범위. 생략하면 staged·unstaged 변경을 확인한다. 미추적 파일은 요청한 작업에 속할 때만 포함한다.
- 기본은 읽기 전용이다. `--fix`나 명시적인 수정 요청은 범위 내 Critical·Warning 수정 권한으로 취급하며 같은 승인을 다시 묻지 않는다. Suggestion은 별도 요청이 없으면 보고만 한다.
- 동결된 기능 묶음의 Plan 정합성·인수를 검토한다면 `packet-review`를 사용한다. 같은 범위의 유효한 통합 리뷰를 별도 broad 리뷰로 반복하지 않는다. 사용자에게 특정 리뷰 방식이 지정됐다면 그 요청을 따른다.

## 검토 절차

1. **범위와 기준 확인.** 대상 diff·파일, 적용되는 프로젝트 지침, 의도한 동작을 읽는다. 관련 규약이 있으면 따른다. `docs/coding-convention.md` 같은 경로가 있다고 가정하거나 다른 작업의 dirty 파일까지 범위를 넓히지 않는다.
2. **변경의 영향 추적.** 호출자·호출 대상·테스트·계약 중 판단에 필요한 부분을 읽고, 기존 결함과 이번 변경이 새로 만들거나 드러낸 결함을 구분한다. 지정 파일 전체 리뷰라면 그 범위를 기준으로 삼는다.
3. **위험 검토.** 결과·경계값·오류 복구, 타입과 검증 경계, 권한·입력·민감정보, 반복 호출·대용량 처리, 의존 방향·중복 정책·유지보수를 살핀다. 타입 힌트 누락이나 파일 크기만으로 결함을 확정하지 않는다.
4. **근거 확인.** 중요한 의심은 가장 좁은 안전한 재현이나 타깃 테스트로 확인한다. 프로젝트의 필수 검증은 지키되, 국소 문제 때문에 전체 suite를 반복하지 않는다. 외부 서비스 호출·실데이터 변경이 필요하면 기존 권한 범위를 먼저 확인한다.
5. **수정 모드라면 보완.** 필요한 부분만 고치고 영향받은 검증을 실행한 뒤 최종 diff를 다시 확인한다. `karpathy-guidelines`의 최소 변경 원칙을 적용한다. 동작하는 코드를 스타일 때문에 재작성하지 않으며 commit·merge·publish는 별도 권한을 따른다.

## 결과

- **Critical**: 보안·권한·데이터 손상, 잘못된 핵심 결과, 필수 흐름 중단처럼 수용 전에 반드시 닫아야 하는 결함.
- **Warning**: 구체적인 조건에서 발생하는 동작·타입·성능·호환성·유지보수 위험. 영향과 차단 여부를 설명한다.
- **Suggestion**: 수용을 막지 않는 개선. 프로젝트의 의무 규약 위반은 실제 영향에 맞게 판정한다.

결함을 심각도 순으로 제시하고 각 항목에 `파일:줄`, 발생 조건, 원인과 영향, 필요한 보완을 적는다. Critical·Warning에는 재현 결과 또는 정확한 코드 경로를 근거로 든다. 추정은 추정으로 표시하고, 확인되지 않은 우려를 관찰된 실패로 쓰지 않는다.

마지막에 검토 범위, 실제 실행한 검증과 결과, 미검증 영역을 짧게 남긴다. 수정했다면 변경 내용과 남은 항목을 구분한다. 발견한 결함이 없으면 그 사실과 검증 한계를 명시하며 항목 수를 채우지 않는다.
