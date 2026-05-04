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

## Commit Format

### Subject

```text
[type] summary
```

- Use one of: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `chore`, `revert`.
- Keep the subject within 70 characters.
- Prefer a concise Korean imperative-style summary.
- Add an issue number at the end if available: `[#123]`.
- Avoid vague summaries such as `수정`, `테스트`, `임시`, `업데이트`.

Examples:

```text
[fix] 사용자-아이템 타임스탬프 누수 방지
[docs] 학위논문 표그림 개선 계획 정리
[refactor] TGA 학습 단계별 책임 분리
```

### Body

Write 1 to 5 bullet points.

- Put the change summary first.
- Include why the change was needed.
- Include validation, test result, or expected impact when available.
- Mention risk or affected scope when the change may influence experiments,
  paper outputs, or formatting.

Example:

```text
[fix] 사용자-아이템 타임스탬프 누수 방지

- 사용자별 시간순 split에서 마지막 인터랙션 검증 로직 보강
- 과거 데이터 누수 방지를 위해 평가 마스킹 조건 추가
- `uv run pytest`로 split 관련 회귀 테스트 확인
```

## Type Selection

- `feat`: 신규 기능 추가.
- `fix`: 버그 수정 또는 정상 동작 복구.
- `perf`: 속도, 메모리, 스루풋 등 성능 개선.
- `refactor`: 동작 변화 없이 코드 구조 개선.
- `docs`: 문서, 논문, README, AGENTS, 주석 문서화 변경.
- `test`: 테스트 코드 추가, 수정, 리팩터링.
- `chore`: 빌드, 의존성, 도구 설정, 운영성 변경.
- `revert`: 이전 커밋 되돌리기.

For thesis, paper, Markdown, DOCX/PDF generation scripts, and documentation-only
changes, default to `docs` unless code behavior changed materially.

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
