---
name: git-commit-helper
description: Generate project-conformant Korean git commit messages from staged or unstaged diffs. Use when the user asks for a commit message, commit review, staging guidance, or help turning git changes into a commit that follows this workspace's AGENTS.md convention.
---

# Git Commit Helper

## Core Rule

Follow the current workspace `AGENTS.md` first. If this skill conflicts with a
repository instruction, the repository instruction wins.

For this project, use this commit format:

```text
[type] Korean summary

- 변경 요약
- 변경 이유
- 검증 또는 영향
```

Do not use Conventional Commits such as `feat(scope): summary` unless the current
repository explicitly asks for that format.

## Branch Strategy

| 브랜치 | 역할 |
|---|---|
| `main` | 안정 브랜치. lint·type·test를 모두 통과한 상태를 유지한다. 직접 커밋하지 않고 `dev`에서만 병합한다 |
| `dev` | 통합 브랜치. 일상 작업의 기본 대상 |
| `feature/<주제>` | 주요 기능 단위 작업. `dev`에서 분기해 `dev`로 병합 |
| `fix/<주제>` | 버그 수정. `dev`에서 분기해 `dev`로 병합 |

규칙:

- 주요 기능은 최신 `dev`에서 `feature/` 브랜치를 만든다. 기능 구현과 독립 검수, 필수 수정이 끝나면 `dev`에 병합한다.
- 기능을 `dev`에 통합한 뒤 발견한 버그는 최신 `dev`에서 `fix/` 브랜치를 만들고, 회귀 테스트와 검수를 마친 뒤 `dev`에 병합한다.
- 문서 수정·설정 변경·작은 변경은 별도 브랜치 없이 **`main`이 아닌 현재 작업 브랜치**에서 처리한다.
- 작업 브랜치는 `git merge --no-ff`로 병합하고 병합 후 삭제한다. 기능 단위가 머지 커밋으로 보이게 한다. 특별한 충돌 정리 사유가 없으면 `rebase`나 fast-forward 병합으로 이 이력을 펴지 않는다.
- **브랜치에서 내려진 기술 결정의 ADR은 같은 브랜치에 포함해 함께 병합한다.** 결정 기록과 구현을 이력에서 분리하지 않는다 (`docs/decisions/` 참조).
- `dev` → `main` 병합은 개발 단계 완료 시점에 한다.
- 릴리스·핫픽스 전용 브랜치는 두지 않는다.

## Commit Title

Format:

```text
[type] summary
```

Allowed types:

- `feat`: Add or modify a feature.
- `fix`: Fix a bug.
- `perf`: Improve performance.
- `refactor`: Change structure without intended behavior change.
- `docs`: Change documentation.
- `test`: Add or update tests.
- `chore`: Change tooling, dependency, or maintenance files.
- `merge`: Integrate a completed feature or fix branch into its target branch.
- `revert`: Revert a previous commit.

Rules:

- Keep the title under 70 characters.
- Use a concrete summary, not vague words such as `수정`, `테스트`, or `임시`.
- Add an issue number at the end when available: `[#123]`.

Examples:

```text
[fix] 사용자별 시간순 split 누수 방지 [#42]
[docs] 학위논문 표그림 개선 계획 정리 [#5]
[refactor] TGA 학습 단계별 책임 분리 [#101]
```

### Commit Body

Use one to five Korean bullet points.

Recommended order:

- What changed.
- Why it changed.
- Impact or risk.
- Validation performed.

병합 커밋도 본문을 생략하지 않는다. 기능 범위, 사용자 승인이나 주요 결정, 독립 검수 결과, 실제로 실행한 검증을 적는다. 
브랜치 안의 개별 커밋 제목을 그대로 나열하기보다 통합된 기능 단위를 설명한다.

```text
[merge] Stage 3 실사용 기록 도구 통합

- 중단 후 이어 쓰는 운동 기록 CLI와 append-only 원장을 통합
- 사용자 승인에 따라 14일 실사용과 Stage 4~9 개발을 병행하도록 경계 유지
- 독립 code review와 packet review의 필수 지적 반영
- Ruff, mypy, 전체 pytest와 프로세스 재시작 smoke 통과
```

Example:

```text
- 사용자별 시간순 split에서 마지막 interaction 검증 로직 보강
- 과거 데이터 누수를 막기 위해 masking 조건 추가
```

## Workflow

1. Inspect the worktree:

   ```bash
   git status --short
   git diff --stat
   git diff
   git diff --staged --stat
   git diff --staged
   ```

2. Separate unrelated changes before drafting the message.

3. If only staged changes should be committed, base the message on
   `git diff --staged`.

4. If nothing is staged and the user asks for a commit message, say whether the
   draft is based on unstaged changes.

5. Do not stage files, commit, amend, or reset unless the user explicitly asks.

6. Never use destructive git commands such as `git reset --hard` or
   `git checkout --` unless the user explicitly approves them.

## Output Style

When the user asks for a commit message, provide only the ready-to-use commit
message unless they also ask for analysis.

When the user asks for review before committing, report:

- suggested split, if changes are unrelated;
- proposed commit message;
- validation gaps, if tests were not run.

## Multi-Commit Guidance

Split commits when changes have different purposes, for example:

- code behavior change plus thesis formatting change;
- experiment script change plus generated result update;
- source code change plus unrelated documentation cleanup.

Keep one commit when the changes are one logical unit and the body can explain
the relationship clearly.

## Checklist

- Subject uses `[type] summary`.
- Type is one of the allowed lowercase keywords.
- Subject is 70 characters or fewer.
- Body has 1 to 5 Korean bullet points.
- Body explains change, reason, and validation or impact.
- No vague subject such as `수정` or `테스트`.
- No unrelated changes are mixed without explanation.
