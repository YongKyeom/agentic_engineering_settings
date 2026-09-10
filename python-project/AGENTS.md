# Python Project Agent Guide

This file is the root agent guide for Python projects copied from the `codex_settings` reference repository.
Keep project-specific defaults and the project map concise. This file intentionally repeats shared baseline rules that must load for every task; use `docs/*.md` for detailed procedures and examples.

## Source of Truth

In case of a conflict, the following order of precedence applies:

1. 현재 사용자의 명시적 지시
2. [(선택) 작업 Plan](docs/plan/)
3. [ADR](docs/decisions/README.md)
4. [Architecture](docs/architecture.md)
5. ...

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

The rules below are sufficient for everyday work. [Agentic Engineering](docs/agentic-engineering.md) provides additional detail.

### Core Workflow

- Before editing, reconcile current user direction, the relevant Plan/Handoff, ADRs, and code. For non-trivial work, make the smallest useful plan with verifiable completion criteria.
- Keep changes scoped and preserve user edits. Never revert unrelated work without explicit permission.
- Update existing records as work progresses: short tasks in Handoff; long-running specifications, ownership, status, and lessons in the Plan. Create a separate Handoff only at the user's request.
- Verify claims against actual commands and artifacts. Recheck risky or unsupported boundaries narrowly; do not repeat valid checks mechanically.

### Delegation and Models

- The lead owns scope, delegation, adjudication, integration, final verification, commits, and user communication. Workers own bounded implementation or evidence gathering.
- Delegate only when independent exploration, review, verification, or disjoint implementation adds value. Keep sequential blockers and overlapping edits local or serialize them.

| 작업 | 기본 배정 | 상향 기준 |
|---|---|---|
| 작은 문서 정리, docstring, 링크·표기 확인 | Luna `high` | 문서 간 계약 판단이 필요하면 Terra `high` |
| 계약·수정 위치가 고정된 작은 구현·회귀 테스트 | Luna `xhigh` | 요구 해석·기존 구조와의 조율이 필요하면 Terra `high` |
| 일반 기능 구현·다중 문서 계약 반영 | Terra `high` | 반례가 반복되거나 state·graph·transaction 경계를 함께 바꾸면 sol `high` |
| 다중 모듈 설계, 원자성, 복잡한 상태 전이 | sol `high` | 반례가 반복되거나 안전 경계를 재설계하면 sol `xhigh` |
| 읽기 전용 탐색과 기계적 검증 | Luna `high` | 원인 추론이 필요하면 Terra `high` |
| 반복 테스트, 대용량 로그·artifact 분류 | Luna `high` | 원인 분석은 Terra `high`, 아키텍처 결함은 sol `high` |
| 독립 Packet Review | Terra `high` | write·보안·상태 정합성 위험이 높으면 sol `xhigh` |

- 모델·추론 강도는 위 표를 따르고, 추가 상향은 어려운 경계에만 적용한다. 단순 실행·문서화에 고성능 모델을 쓰지 않는다.
- 배정은 호출 단가뿐 아니라 총괄 검수·재설명·수정까지 포함한 토큰 비용으로 판단한다. 같은 유형의 실수가 반복되면 범위를 줄이거나 상향하며, 정상 진행 중인 워커를 비용 추정만으로 재시작하지 않는다.
- 문서 워커도 병렬 운용할 수 있지만 상위 문서·ADR·Plan·Handoff의 판정과 통합은 메인이 맡는다.
- 워커 보고는 기본 10줄 이내로 결론·변경 경로·검증 명령/exit code/수치·첫 실패·잔여 위험만 쓴다. 원문·전체 diff·로그 덩어리는 붙이지 않고 파일:줄 또는 artifact 경로/hash로 참조한다. 중요한 결함은 줄 때문에 생략하지 않는다.
- 총괄은 완료·차단 알림을 기준으로 움직인다. 완료 여부만 묻는 반복 polling이나 작업 중 diff 재열람을 피하고, 독립 작업 또는 대기 도구를 사용한다. 중간 확인은 충돌·안전 위험·실행 이상 등 개입할 이유가 있을 때만 한다.
- 통합 시에는 요약의 핵심 주장과 영향 경계를 원본·타깃 검증으로 확인한다. 워커가 읽은 자료 전체를 다시 읽거나 유효한 검증을 기계적으로 반복하지 않는다.

### 구현·검수·마감

- **구현 Packet**: 범위 확정 → 구현 → targeted test → 메인의 좁은 diff 확인 → 중간 commit·개발 브랜치 통합. 통합 직후 임시 워크트리·브랜치를 정리한다. 공유 대상 브랜치의 PR 절차는 우회하지 않는다.
- **검수 묶음**: 관련 Packet을 기능 경계에서 모아 동결하고 전체 gate·독립 packet-review를 한 번씩 수행한다(같은 후보에서 병렬 가능). 고위험 경계·PR 전달 전에도 검수하며, 작은 Packet마다 반복하거나 광역 code-review를 중복하지 않는다.
- **Must-Close**: 메인이 영향과 마감 시점을 정한다. 승인 우회·잘못된 write·상태 손상은 즉시 보완하거나 격리하고, 그 외 차단 결함은 묶음 마감까지 닫는다. 비차단 개선은 담당·재검토 조건을 정해 이월할 수 있다.
- **재검증**: 보완한 회귀·diff만 재확인한다. 전체 gate는 후속 변경이 이전 검증 범위를 벗어날 때만 반복하고 이유를 Plan에 남긴다. 문서만 바뀌면 렌더·링크·내용을 확인한다.
- **마감**: 구현·필수 보완 완료 → 문서 마감 → 메인 최종 검증 → 최종 commit·PR 전달. 중간 commit·통합을 최종 검수 승인으로 간주하지 않는다.

### Skills

Skills support these rules; current project instructions take precedence.
Use `karpathy-guidelines` for coding, `git-commit-helper` for commits, and `packet-review` for review bundles.
Use `requirements-clarity` for unresolved scope, `decision-record` for durable technical decisions, and `structured-prompt-template` for prompts and model-facing contracts.
Apply `humanizer` and `writing-clearly-and-concisely` to prose; use `handoff` only for a requested transfer.

---

## Python Coding Standards

아래 규칙은 Python 소스코드를 탐색하거나 수정할 때 적용한다.
아래는 상세규칙 [Coding Convention](docs/coding-convention.md) 에 대한 요약이며, 반드시 상세규칙을 준수한다.

- **PEP8**: 프로젝트에 설정된 `ruff`, `black`, `isort` 자동화 도구를 적극 사용한다. 줄 길이는 프로젝트 기본값을 따르고, 기본값이 없으면 140자. 상수는 `UPPER_SNAKE_CASE`, 클래스는 `PascalCase`, 함수·메서드는 `snake_case`.
- **Docstring**: 모든 공개/내부 함수와 클래스에 Google 스타일 Docstring을 작성한다. `Args`/`Returns`/`Raises`/`Side Effects` 섹션을 반드시 포함하고, 해당 내용이 없으면 "없음."으로 명시한다. `__init__`, `forward`, loss 계산, 전처리·샘플링·평가 메서드는 필수.
- **주석 언어**: Docstring과 주석은 간결한 한글로 작성한다. 명령어, 식별자, API 명은 영어 유지.
- **실행 흐름 주석**: 주요 객체 생성, 데이터 로딩, 학습 루프, 평가 등 관문마다 주석으로 "왜"와 "무엇"을 먼저 설명한다. CLI 진입점과 `if __name__ == "__main__":` 이하 절차형 로직에는 번호·시퀀스 주석을 달아 추적이 쉽도록 한다.
- **타입 힌트**: 모든 함수 서명에 정확한 타입 힌트를 작성한다. `Protocol`, `TypedDict`, `Literal` 등 세밀한 타입을 적극 활용한다. 반환이 없으면 `-> None` 명시.
- **SRP**: 함수·클래스는 하나의 책임에 집중한다. 파이프라인 단계는 기능별 디렉터리로 분리한다. SRP 위반이 의심되면 리팩터링 이슈를 생성하고 사용자와 적정 수준을 협의한다.
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
- 마크다운 문서는 ruff 대상에서 제외하고 줄바꿈/단락 구분은 의미 단위로 작성한다.

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
- **루트 README**: 시스템 전체 관점. 문제 정의, 아키텍처, 시작 방법
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

---

## 기본 검증

```sh
uv run ruff check .
uv run mypy src
uv run pytest
```