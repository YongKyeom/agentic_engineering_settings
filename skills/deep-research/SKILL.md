# Deep Research

주제나 질문에 대해 여러 소스를 fan-out으로 조사하고, 사실 검증을 거쳐 인용 포함 리포트를 생성한다.

## Usage

```
/deep-research <topic or question>
```

## Process

1. **Decompose**: 질문을 세부 하위 질문으로 분해
2. **Fan-out**: 웹, 공식 문서, 논문 등 여러 소스를 병렬 탐색
3. **Verify**: 소스 간 사실 교차 검증, 모순 항목 표시
4. **Synthesize**: 인용 포함 구조화 리포트 생성

## Output Format

- **Summary**: 핵심 질문에 대한 2~3문장 답변
- **Key Findings**: 출처 인용 포함 불릿 포인트
- **Trade-offs / Caveats**: 소스 간 불일치 또는 미커버 영역
- **Sources**: 참조한 URL 및 문서 목록

## Rules

- 모든 사실에 출처를 명시한다. 근거 없는 단언 금지
- 소스가 충돌하면 한쪽을 택하지 않고 충돌 자체를 보고한다
- 신뢰도 낮은 항목은 명시적으로 표시한다
- 리포트는 간결하게 유지하고 상세 내용은 소스 링크로 대체한다
