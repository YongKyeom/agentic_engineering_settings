---
name: code-review
description: Review code changes for bugs, type safety, style, security, and maintainability. Use after making changes to a codebase. Supports --fix to auto-apply Critical and Warning items.
---

# Code Review

diff 또는 지정 파일을 기준으로 코드 리뷰를 수행한다.

## Usage

```
/code-review [--fix] [target]
```

- `target`: 파일, 디렉터리, git diff 범위 (기본값: 미커밋 변경사항)
- `--fix`: 리뷰 후 Critical·Warning 항목 자동 수정 (수정 전 확인 요청)

## Review Dimensions

1. **Correctness**: 로직 오류, 경계값, None 처리, 엣지 케이스
2. **Type safety**: 타입 힌트 누락, 잘못된 타입, `Any` 남용
3. **Style**: 프로젝트 코딩 컨벤션 준수 (`karpathy-guidelines`, PEP8)
4. **Security**: 입력 검증, 인젝션 위험, 코드 내 시크릿
5. **Performance**: 불필요한 연산, N+1, 대용량 할당
6. **Maintainability**: SRP 위반, 과도한 복잡도, 네이밍

## Process

1. diff 또는 대상 파일 읽기
2. 각 dimension 순서대로 검토
3. 심각도별로 결과 보고: 🔴 Critical, 🟡 Warning, 🟢 Suggestion
4. `--fix` 옵션 시 Critical·Warning 항목을 사용자 확인 후 적용

## Rules

- `karpathy-guidelines` 준수: 외과적 수정, 과잉 구현 금지
- Python 프로젝트라면 `docs/coding-convention.md` 기준 적용
- 동작하는 코드를 스타일만을 위해 재작성하지 않는다
- Suggestion(🟢) 항목은 보고만 하고 자동 수정하지 않는다
