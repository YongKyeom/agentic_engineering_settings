---
name: handoff
description: Create a concise handoff package for the user, another agent, or a future session. Use when work is ending, context is long, work must continue elsewhere, or the user says things like "wrap up", "save progress", "continue later", "handoff", "pass this to the next session", or "context is getting long".
---

# Handoff

Handoff is the smallest transfer package that lets another agent or the user continue the work without rereading the whole session.

## Core Principles

- The default handoff location is the final answer to the user.
- If the work is unfinished or another agent must continue, include a mid-work handoff in the final answer.
- If long-term tracking is needed or the next worker must continue from files, write a handoff file under `docs/handoff/`.
- Use the filename format `YYYYMMDD_<topic>.md`.
- Example: `20260331_rdb-agent-docs-handoff.md`.
- For a small single-file change, the final answer handoff can be enough when `git diff` tells the story clearly.
- Keep handoffs concise. Capture decisions and next action, not the whole transcript.

## File Location

When writing a file handoff, prefer:

```text
docs/handoff/YYYYMMDD_<topic>.md
```

Use `docs/handoff/`, not a root `HANDOFF.md`, unless a repository explicitly instructs otherwise.

Handoff files are usually local session artifacts. Do not commit them unless the user explicitly wants them preserved as shared project documentation.

## Required Sections

Every substantial handoff should include these sections.

1. **Status**
   - One of: `완료`, `진행 중`, `보류`.

2. **Work Scope**
   - Summarize the handoff scope in one or two lines.

3. **Changed Files**
   - List only files actually changed.

4. **Key Changes**
   - Explain what changed and why in two to five bullets.

5. **Important Decisions**
   - Record decisions and the reason, so the next worker does not reverse them accidentally.

6. **Validation**
   - List commands run, manual checks performed, and evidence.
   - If no validation was run, state that explicitly.

7. **Key Files**
   - List files the next worker should inspect first and why.

8. **Cautions**
   - Record known gotchas, avoidance rules, current assumptions, and boundaries between docs and code.

9. **Remaining Risks**
   - List only risks that can immediately matter.

10. **Next Actions**
   - Write concrete next steps that the user or next agent can execute immediately.
   - The first item should be an immediate next step, not a vague goal.

11. **Previous Handoff Reference**
   - If continuing from an earlier handoff, list its filename.
   - If none exists, write `없음`.

12. **Local Artifact Handling**
   - State whether logs, CSV files, XLSX files, temporary outputs, or generated artifacts were created, ignored, or committed.

## Markdown Template

Use this template for file handoffs or final-answer handoff sections.

```markdown
# Handoff: <title>

## 상태

- 완료 / 진행 중 / 보류

## 작업 범위

- ...

## 변경 파일

- `path/to/file` - ...

## 핵심 변경 내용

- ...

## 주요 결정사항

- ...

## 검증

- 실행한 명령: ...
- 수동 확인: ...
- 검증하지 못한 항목: ...

## 핵심 파일

- `path/to/file` - 다음 작업자가 먼저 봐야 하는 이유

## 주의사항

- ...

## 남은 리스크

- ...

## 다음 액션

- [ ] Immediate next step
- [ ] ...

## 이전 handoff 참조

- 없음 / `YYYYMMDD_<topic>.md`

## 로컬 산출물 처리 여부

- 생성 없음 / 로컬만 생성 / 커밋함
```

## Usage Examples

- When handing off in the final answer: include the handoff sections directly in the final response.
- When another agent must continue: summarize current state, changed files, incomplete validation, and next actions.
- When file-based continuity is needed: create `docs/handoff/YYYYMMDD_<topic>.md`.
- When only documentation changed: focus on changed files, link/structure checks, and whether `git diff --check` was run.

## Self-Checklist

Before finishing a handoff, check:

- Did the branch or recent key commit change after the handoff was drafted?
- Are the key file paths still valid?
- Can the next worker start from the first item under `다음 액션`?
- If a decision must be reversed later, did you leave the reason in the handoff or final answer?
- Did you clearly state whether validation was run?
