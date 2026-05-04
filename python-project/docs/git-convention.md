# Git Convention

Use this convention when drafting, reviewing, or creating commits.

## Commit Title

Format:

```text
[type] summary
```

Allowed types:

- `feat`: Add a feature.
- `fix`: Fix a bug.
- `perf`: Improve performance.
- `refactor`: Change structure without intended behavior change.
- `docs`: Change documentation.
- `test`: Add or update tests.
- `chore`: Change tooling, dependency, or maintenance files.
- `revert`: Revert a previous commit.

Rules:

- Keep the title under 70 characters.
- Use a concrete summary, not vague words such as `수정`, `테스트`, or `임시`.
- Add an issue number at the end when available: `[#123]`.

Example:

```text
[fix] 사용자별 시간순 split 누수 방지 [#42]
```

## Commit Body

Use one to five Korean bullet points.

Recommended order:

- What changed.
- Why it changed.
- Impact or risk.
- Validation performed.

Example:

```text
- 사용자별 시간순 split에서 마지막 interaction 검증 로직 보강
- 과거 데이터 누수를 막기 위해 masking 조건 추가
- `uv run pytest tests/test_split.py`로 회귀 확인
```

## Commit Hygiene

- Split unrelated changes into separate commits.
- Mention impact scope when a change can create merge conflicts.
- Do not claim tests or validation that were not run.
- Use `git-commit-helper` when drafting or reviewing the message.
