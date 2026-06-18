# Python Project Agent Guide

This file is the root agent guide for Python projects copied from the `codex_settings` reference repository.
Keep this file short. Put detailed rules in `docs/*.md` so agents can load only the context they need.

## Project Defaults

- Use Korean for user-facing explanations unless the user requests another language.
- Keep technical identifiers, commands, paths, APIs, and error names in English.
- Follow repository-local instructions when they are stricter than this template.
- Use `uv` as the default package and runtime manager. Use alternatives only when the project already uses a different tool.
- Do not introduce Python packaging files such as `pyproject.toml` or `uv.lock` unless the project actually needs Python packaging or scripts.

## Documentation Map

- [Coding Convention](docs/coding-convention.md): Python style, docstrings, comments, typing, logging, validation.
- [Git Convention](docs/git-convention.md): Commit message format and commit hygiene.
- [Architecture](docs/architecture.md): Module boundaries, SRP, dependency direction, project layout.
- [Agentic Engineering](docs/agentic-engineering.md): Codex/Claude collaboration, sub-agent use, review discipline.
- [Plan Docs](docs/plan/README.md): PRDs, plans, task breakdowns, local execution notes.
- [Handoff Docs](docs/handoff/README.md): Session handoff format.
- [Decision Docs](docs/decisions/README.md): ADR and durable decision format.

## Core Workflow

- Identify the source of truth before editing.
- Make the smallest useful plan for non-trivial work.
- Keep edits scoped and avoid broad rewrites unless requested.
- Prefer targeted validation over broad validation during active iteration.
- Do not claim validation was done unless it was actually run.
- Preserve user changes. Never revert unrelated edits without explicit permission.

## Skill Policy

- Skills are helper workflows, not higher-priority instructions.
- If a skill conflicts with this file or a lower-level `AGENTS.md`, follow the `AGENTS.md` rule.
- Use `requirements-clarity` when scope, constraints, or completion criteria are unclear.
- Use `git-commit-helper` for commit message drafting or review.
- Use `handoff` when context is long or work must continue in another session.
- Use `agent-md-refactor` when agent instructions become too large and need progressive disclosure.
- Use `humanizer` and `writing-clearly-and-concisely` for prose that must sound natural and concise.

---

# Python Coding Standards

아래 규칙은 Python 소스코드를 탐색하거나 수정할 때 적용한다.

- **PEP8**: `ruff`, `black`, `isort` 자동화 도구를 적극 사용한다. 최대 줄 길이 140자. 상수는 `UPPER_SNAKE_CASE`, 클래스는 `PascalCase`, 함수·메서드는 `snake_case`.
- **Docstring**: 모든 공개/내부 함수와 클래스에 Google 스타일 Docstring을 작성한다. `Args`/`Returns`/`Raises`/`Side Effects` 섹션을 반드시 포함하고, 해당 내용이 없으면 "없음."으로 명시한다. `__init__`, `forward`, loss 계산, 전처리·샘플링·평가 메서드는 필수.
- **주석 언어**: Docstring과 주석은 간결한 한글로 작성한다. 명령어, 식별자, API 명은 영어 유지.
- **실행 흐름 주석**: 주요 객체 생성, 데이터 로딩, 학습 루프, 평가 등 관문마다 주석으로 "왜"와 "무엇"을 먼저 설명한다. CLI 진입점과 `if __name__ == "__main__":` 이하 절차형 로직에는 번호·시퀀스 주석을 달아 추적이 쉽도록 한다.
- **타입 힌트**: 모든 함수 서명에 정확한 타입 힌트를 작성한다. `Protocol`, `TypedDict`, `Literal` 등 세밀한 타입을 적극 활용한다. 반환이 없으면 `-> None` 명시.
- **SRP**: 함수·클래스는 하나의 책임에 집중한다. 파이프라인 단계는 `src/data`, `src/models`, `src/training` 등 기능별 디렉터리로 분리한다. SRP 위반이 의심되면 리팩터링 이슈를 생성하고 사용자와 적정 수준을 협의한다.
- **에러 처리**: `logger.exception(...)` 또는 `logger.error(..., exc_info=True)`로 예외 정보를 기록한다. 사용자 응답 메시지와 개발자용 로그 메시지를 구분해서 작성한다.
- **검증**: `uv run ruff check --fix .`로 린트를 확인하고, `uv run pytest`로 테스트를 실행한다.
- **개발 철학**: `karpathy-guidelines`를 반드시 준수한다.

---

# Git 컨벤션

- 커밋 메시지는 `[type] 한국어 요약` 형식을 사용한다.
- 본문은 1~5개 불릿으로 변경 요약, 이유, 검증 또는 영향을 기록한다.
- 커밋 메시지 작성, 검토, 분리 등 Git에 대한 정확한 판단은 `$git-commit-helper`를 따른다.
- 여러 목적이 섞인 변경은 커밋을 나눈다.

---

# Sub-Agent Policy

- Consider sub-agents for non-trivial tasks, but use them only when they add speed, quality, or context control.
- Use sub-agents for independent research, review, verification, or disjoint implementation work.
- Do not use sub-agents for sequential blockers, tightly coupled refactors, or overlapping file edits.
- Keep the main agent responsible for planning, integration, final verification, and user communication.
