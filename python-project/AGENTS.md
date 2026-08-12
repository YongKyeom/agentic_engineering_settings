# Python Project Agent Guide

This file is the root agent guide for Python projects copied from the `codex_settings` reference repository.
Keep project-specific defaults and the project map concise. This file intentionally repeats shared baseline rules that must load for every task; use `docs/*.md` for detailed procedures and examples.

## Project Defaults

- Use Korean for user-facing explanations unless the user requests another language.
- Keep technical identifiers, commands, paths, APIs, and error names in English.
- Follow repository-local instructions when they are stricter than this template.
- Use `uv` as the default package and runtime manager. Use alternatives only when the project already uses a different tool.
- Do not introduce Python packaging files such as `pyproject.toml` or `uv.lock` unless the project actually needs Python packaging or scripts.

## Project Map

### Working Rules

- [Coding Convention](docs/coding-convention.md): Python style, docstrings, comments, typing, logging, validation.
- [Git Convention](docs/git-convention.md): Commit message format and commit hygiene.
- [Architecture](docs/architecture.md): Module boundaries, SRP, dependency direction, project layout.
- [Agentic Engineering](docs/agentic-engineering.md): Codex/Claude collaboration, sub-agent use, review discipline.
- [Plans](docs/plan/README.md): PRDs, plans, task breakdowns, and local execution notes.
- [Handoffs](docs/handoff/README.md): Session handoff format and local tracking rules.
- [ADRs](docs/decisions/README.md): Durable technical decisions shared through Git.

### Code Areas

Use this backend agent-system example as a starting point. Replace it with the actual project layout during project initialization; for a non-agent project, map its own major boundaries instead. Do not retain paths that do not exist, and do not create directories solely to match the sample.

```text
src/<package>/
├── core/            # Pure domain rules, models, and contracts
├── app/             # Application use cases and composition root
│   ├── http/        # HTTP/SSE API, authentication boundary, and response mapping
│   └── storage/     # Repository, transaction, database, and external-service adapters
├── agents/          # LLM-facing application layer; no direct HTTP or ORM imports
│   ├── assets/      # Human-reviewed prompts, rules, skill, and Tool manifests
│   ├── common/      # Provider-neutral contracts, schemas, shared prompts, and shared Tools
│   ├── roles/       # Role declarations, role-specific contracts, and role registry
│   ├── knowledge/   # Domain-knowledge loaders and contracts
│   ├── skills/      # Runtime skill loading, context assembly, and hook contracts
│   ├── tools/       # Tool broker, manifest validation, lifecycle, and result envelopes
│   ├── policy/      # Input safety, execution authority, middleware, and output validation
│   ├── service/     # LLM facade, provider adapters, and checkpointing
│   ├── orchestration/ # Role graph and runtime assembly; the public execution boundary
│   ├── operations/  # Concurrency, rate limits, cost accounting, and operational contracts
│   └── evals/       # Evaluation scenarios, runners, rubrics, and result contracts
├── cli/             # Development and operations command entry points
└── main.py          # Application startup entry point
tests/               # Tests organized to mirror the relevant source area
```

For each major area, link to its actual directory and its `README.md` or `AGENTS.md` when more local guidance is needed.

---

The sections below are shared baselines. Keep them unchanged; add project-specific rules above or in scoped `AGENTS.md` files.

## Agent Operating Rules

For detailed delegation, parallelism, review, and handoff rules, see [Agentic Engineering](docs/agentic-engineering.md).

### Core Workflow

- Before editing, reconcile the current user direction, relevant Plan and Handoff, ADRs, and code.
- Keep the relevant Plan and Handoff current as scope, changes, and progress evolve.
- Make the smallest useful plan for non-trivial work.
- Keep edits scoped and avoid broad rewrites unless requested.
- Prefer targeted validation over broad validation during active iteration.
- Do not claim validation was done unless it was actually run.
- Preserve user changes. Never revert unrelated edits without explicit permission.

### Sub-Agent Policy

- Consider sub-agents for non-trivial tasks, but use them only when they add speed, quality, or context control.
- Use sub-agents for independent research, review, verification, or disjoint implementation work.
- Do not use sub-agents for sequential blockers, tightly coupled refactors, or overlapping file edits.
- Keep the main agent responsible for planning, integration, final verification, and user communication.

### Skill Policy

- Skills are helper workflows, not higher-priority instructions.
- If a skill conflicts with this file or a lower-level `AGENTS.md`, follow the `AGENTS.md` rule.
- Use `requirements-clarity` when scope, constraints, or completion criteria are unclear.
- Use `git-commit-helper` for commit message drafting or review.
- Use `handoff` when context is long or work must continue in another session.
- Use `decision-record` when a durable technical decision needs to be recorded in `docs/decisions/`.
- Use `structured-prompt-template` when designing, modifying, or auditing provider-neutral system prompts, Skill and Tool catalogs, priority rules, workflows, or output contracts.
- Use `humanizer` and `writing-clearly-and-concisely` for prose that must sound natural and concise.
- Use `karpathy-guidelines` for every coding process

---

## Python Coding Standards

아래 규칙은 Python 소스코드를 탐색하거나 수정할 때 적용한다.
아래는 상세규칙 [Coding Convention](docs/coding-convention.md) 에 대한 요약이며, 반드시 상세규칙을 준수한다.

- **PEP8**: 프로젝트에 설정된 `ruff`, `black`, `isort` 자동화 도구를 적극 사용한다. 줄 길이는 프로젝트 기본값을 따르고, 기본값이 없으면 140자. 상수는 `UPPER_SNAKE_CASE`, 클래스는 `PascalCase`, 함수·메서드는 `snake_case`.
- **Docstring**: 모든 공개/내부 함수와 클래스에 Google 스타일 Docstring을 작성한다. `Args`/`Returns`/`Raises`/`Side Effects` 섹션을 반드시 포함하고, 해당 내용이 없으면 "없음."으로 명시한다. `__init__`, `forward`, loss 계산, 전처리·샘플링·평가 메서드는 필수.
- **주석 언어**: Docstring과 주석은 간결한 한글로 작성한다. 명령어, 식별자, API 명은 영어 유지.
- **실행 흐름 주석**: 주요 객체 생성, 데이터 로딩, 학습 루프, 평가 등 관문마다 주석으로 "왜"와 "무엇"을 먼저 설명한다. CLI 진입점과 `if __name__ == "__main__":` 이하 절차형 로직에는 번호·시퀀스 주석을 달아 추적이 쉽도록 한다.
- **타입 힌트**: 모든 함수 서명에 정확한 타입 힌트를 작성한다. `Protocol`, `TypedDict`, `Literal` 등 세밀한 타입을 적극 활용한다. 반환이 없으면 `-> None` 명시.
- **SRP**: 함수·클래스는 하나의 책임에 집중한다. 파이프라인 단계는 `src/data`, `src/models`, `src/training` 등 기능별 디렉터리로 분리한다. SRP 위반이 의심되면 리팩터링 이슈를 생성하고 사용자와 적정 수준을 협의한다.
- **에러 처리**: `logger.exception(...)` 또는 `logger.error(..., exc_info=True)`로 예외 정보를 기록한다. 사용자 응답 메시지와 개발자용 로그 메시지를 구분해서 작성한다.
- **검증**: 수정한 Python 영역을 먼저 `uv run ruff check path/to/file.py`, `uv run pytest tests/test_target.py`로 확인한다. 자동 수정이 필요할 때만 `uv run ruff check --fix path/to/file.py`를 실행하고 diff를 검토한다.
- **개발 철학**: `karpathy-guidelines`를 반드시 준수한다.

---

## 문서화 표준

### 모듈 상단 docstring

모든 `.py` 파일 상단에 **그 모듈이 무엇을 어떻게 하는지** 상세히 쓴다. 한 줄 요약으로 끝내지 않는다.

- 모듈의 책임, 주요 진입점, 데이터 흐름, 다른 모듈과의 관계
- **아스키 다이어그램을 적극 사용한다** — 파이프라인 단계, 상태 전이, 계층 구조는 그림이 문장보다 빠르다
- 설계 문서 § 번호를 출처로 남긴다
- 비자명한 판단(왜 이 알고리즘인지, 무엇을 의도적으로 하지 않았는지)을 적는다

```
예) 배분 파이프라인
    projection ──scale──▶ tier 절삭 ──place──▶ 세션 버킷 ──order──▶ WeekPlan
                                          │
                                          └─ 하드 제약 3종 검증 (48h · 25세트 · Tier1)
```

### 클래스·함수 docstring

Google 스타일 + `Args`/`Returns`/`Raises`/`Side Effects`는 기본이고, 여기에 더한다.

- 알고리즘이 비자명하면 **단계별 설명**을 넣는다
- 경계 조건과 그 근거를 적는다
- 왜 이렇게 했는지가 코드에서 안 보이면 반드시 쓴다

### README

- **폴더별 README**: `src/.../README.md` — 그 폴더의 책임, 모듈 지도, 진입점, 의존 방향
- **루트 README**: 시스템 전체 관점. 문제 정의, 아키텍처, 핫·콜드 패스, 시작 방법
- **사람이 읽는 문서다.** AI 문체(과장된 형용사, 불필요한 병렬 구조, "~을 통해" 남발)를 쓰지 않는다. `humanizer`·`writing-clearly-and-concisely` 스킬을 적용한다
- **Mermaid·C4 다이어그램**을 적극 쓴다 — 시스템 컨텍스트·컨테이너·시퀀스·상태 전이가 후보
- 루트 README는 전체 시스템을 아는 주체가 쓴다. 모듈 docstring은 해당 모듈만 주로 보면 되므로 분업 가능하다

---

## Git 컨벤션

아래는 [Git Convention](docs/git-convention.md)과 `git-commit-helper`의 요약이며, 반드시 상세규칙을 준수한다.

- 커밋 메시지는 `[type] 한국어 요약` 형식을 사용한다.
- 본문은 1~5개 불릿으로 변경 요약, 이유, 검증 또는 영향을 기록한다.
- 여러 목적이 섞인 변경은 커밋을 나눈다.
- 병합 커밋도 본문을 생략하지 않는다.
