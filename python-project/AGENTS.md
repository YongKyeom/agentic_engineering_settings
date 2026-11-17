# Python Project Agent Guide

This file is a repository-local instruction template for new Python projects. Replace the project defaults, source-of-truth list, and code map with the target project's actual contracts and paths.
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
- [Document Writing](docs/AGENTS.md): Writing, source verification, document templates, and record ownership.
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

### 프로젝트별 책임 경계 작성

프로젝트를 시작할 때 아래 항목 중 해당하는 경계를 위 기본값과 코드 지도에 구체화한다. 실제 요구가 있는 항목만 남기며, 이 예시를 위해 구조나 런타임을 새로 만들지 않는다.

| 항목 | 지침에 명시할 내용 |
|---|---|
| 외부 시스템 연동 | 정본 데이터·권한·계약의 소유자, 허용하는 변경 범위, 승인·저장·재조회·실패 복구 경계 |
| Agent/LLM | 모델이 해석·제안할 범위, 코드가 보장할 권한·승인·상태 전이·검증, 실제 Tool 호출 경로 |
| Prompt·Skill·Tool | 전체 업무와 권한을 보여 주는 공통 계약, 요청별로 읽는 상세 Skill, Tool 등록·검증의 정본 |
| 상태·실행·관측 | 상태 소유자·갱신 방식, 세션·체크포인트 식별자, 재시도·중복 방지·중단·재시작, 로그·추적의 책임 |
| 테스트·운영 | 실제 테스트 선택 기준과 병렬 실행 정책, Mock·실모델·Live·외부 연동별 완료 기준과 미검증 범위 |

업무 규칙을 Prompt·Mock·fallback으로 추정하지 않는다. 외부 계약과 실제 코드로 확인한 범위만 규칙으로 고정한다.

---

The sections below are shared baselines. Keep them unchanged; add project-specific rules above or in scoped `AGENTS.md` files.

## Agent Operating Rules

The rules below are sufficient for everyday work. [Agentic Engineering](docs/agentic-engineering.md) provides additional detail.

### Core Workflow

- Before editing, reconcile current user direction, the relevant Plan/Handoff, ADRs, and code. Define the smallest useful scope and verifiable completion criteria.
- When RTK is installed, use explicit RTK-native commands; use `rtk proxy <command>` when exact output or wrapper limitations require it. Otherwise use the equivalent standard command.
- Preserve user edits and intended module boundaries. Review the whole semantic diff, including moves, merge-commit changes, callers, serialization, and shared fixtures. For rebase divergence, compare original and rewritten commits before deciding how to integrate. Never revert unrelated work without explicit permission.
- Update existing records as work progresses: short tasks in Handoff; long-running specifications, ownership, status, and lessons in the Plan. Create a separate Handoff only at the user's request.
- Verify claims against actual commands and artifacts. Trace model Tool calls through execution before choosing an instruction fix or a code fix. Do not reconstruct unverified business rules in code, prompts, or Mock. Recheck risky or unsupported boundaries narrowly; do not repeat valid checks mechanically.

### Delegation and Models

- The lead owns scope, sources of truth, delegation, adjudication, integration, final verification, commits, and user communication. Only the lead may assign workers; workers must not delegate. Workers own bounded implementation or evidence gathering.
- Delegate only when independent exploration, review, verification, or disjoint implementation adds value. Keep sequential blockers and overlapping edits local or serialize them.

| 작업 | 기본 배정 | 상향 기준 |
|---|---|---|
| 작은 문서 정리, docstring, 링크·표기 확인 | Luna `high` | 문서 간 계약 판단이 필요하면 Sol `medium` |
| 계약·수정 위치가 고정된 작은 구현·회귀 테스트 | Luna `high` | 요구 해석·기존 구조와의 조율이 필요하면 Sol `medium` |
| 일반 기능 구현 | Luna `xhigh` | 다중 문서 계약 반영은 Sol `high`; 복잡한 상태·트랜잭션 경계에서 범위가 명확하고 깊은 검증이 필요하면 Sol `xhigh`; 요구가 모호하거나 여러 영역을 함께 조율해야 하면 Astra `medium` |
| 다중 모듈 설계, 원자성 | Luna `xhigh`; 복잡한 상태 전이 Sol `high` | 반례가 반복되거나 안전 경계를 재설계하면 Sol `xhigh` or Astra `high` |
| 읽기 전용 탐색과 기계적 검증 | Luna `high` | 원인 추론이 필요하면 Sol `medium` |
| 반복 테스트, 대용량 로그·artifact 분류 | Luna `high` | 원인 분석은 Sol `medium`, 아키텍처 결함은 Astra `high` |
| 독립 Packet Review | Sol `high` | write·보안·상태 정합성 위험이 높으면 Astra `high` |

- 모델·추론 강도는 위 표를 따르고, 추가 상향은 어려운 경계에만 적용한다. 단순 실행·문서화에 고성능 모델을 쓰지 않는다.
- 배정은 호출 단가뿐 아니라 총괄 검수·재설명·수정까지 포함한 토큰 비용으로 판단한다. 같은 유형의 실수가 반복되면 범위를 줄이거나 상향하며, 정상 진행 중인 워커를 비용 추정만으로 재시작하지 않는다.
- 문서 워커도 병렬 운용할 수 있지만 상위 문서·ADR·Plan·Handoff의 판정과 통합은 메인이 맡는다.
- 워커 보고는 기본 10줄 이내로 결론·변경 경로·검증 명령/exit code/수치·첫 실패·잔여 위험만 쓴다. 원문·전체 diff·로그 덩어리는 붙이지 않고 파일:줄 또는 artifact 경로/hash로 참조한다. 중요한 결함은 줄 때문에 생략하지 않는다.
- 총괄은 완료·차단 알림을 기준으로 움직인다. 완료 여부만 묻는 반복 polling이나 작업 중 diff 재열람을 피하고, 독립 작업 또는 대기 도구를 사용한다. 중간 확인은 충돌·안전 위험·실행 이상 등 개입할 이유가 있을 때만 한다.
- 모델 이름은 실제 환경에서 사용 가능한 최신 계열에 매핑하고, 그 매핑과 지원 기능을 확인한다. 모델·추론 강도 선택은 작업의 경계와 필요한 검증 수준을 기준으로 한다.
- 위임에는 목표·조사 범위·허용 파일·정본 우선순위·금지 변경·보고 형식·검증 기준을 명시한다. 필요한 문맥만 전달하고 탐색·로그 출력량을 제한한다.
- 워커 결과는 원문·타깃 검증으로 확인하고 수용·보류·기각을 판단한다. 중요한 판정은 이유와 함께 Plan에 남긴다. 워커가 읽은 자료 전체를 다시 읽거나 유효한 검증을 기계적으로 반복하지 않는다.

### 구현·검수·마감

- **구현 Packet**: 범위 확정 → 구현 → 영향받는 테스트·정적 검사 → 메인의 좁은 diff 확인 → 중간 commit·개발 브랜치 통합. 작은 수정·커밋·Packet마다 전체 테스트를 반복하지 않는다. 통합 직후 임시 워크트리·브랜치를 정리하며 공유 대상 브랜치의 PR 절차는 우회하지 않는다.
- **검수 묶음**: 관련 Packet을 입력→적용→조회·복구의 완결된 기능으로 묶어 동결하고, 그 기능의 acceptance gate·독립 packet-review를 한 번씩 수행한다. 고위험 경계·PR 전달 전에도 필요한 검수를 하되 작은 Packet별 동일 gate·광역 code-review를 중복하지 않는다. 기능 gate는 저장소 전체 suite를 뜻하지 않는다.
- **Must-Close**: 메인이 영향과 마감 시점을 정한다. 승인 우회·잘못된 write·상태 손상은 즉시 보완하거나 격리하고, 그 외 차단 결함은 묶음 마감까지 닫는다. 비차단 개선은 담당·재검토 조건을 정해 이월할 수 있다.
- **재검증**: 후속 변경으로 무효화된 회귀·diff부터 다시 확인하고, 전체 gate는 반복하지 않은 이유를 Plan에 남긴다. 대상 SHA·명령·exit code·실행 결과를 기록하며, 검사되지 않은 테스트 수를 더하지 않는다. 새 변경에 영향받지 않은 기존 PASS는 재사용하고, 전체 gate 재실행은 광범위한 계약 변경 등 추가 영향 검증이 필요할 때 수행한다. 좁은 PASS를 전체 완료로 확대하지 않는다.
- **실행 비용**: selector·검증 이유·예상 시간 또는 deadline을 먼저 정한다. 작은 수정마다 별도 보고서·전체 문서 렌더를 만들지 않는다. 문서만 바뀌면 코드 테스트 대신 변경 구간의 내용·링크·렌더만 확인한다.
- **마감**: 구현·필수 보완 완료 → 문서 마감 → 메인 최종 검증 → 최종 commit·PR 전달. 최종 검증은 유효한 gate 근거와 이후 변경분을 확인하는 것이며, 같은 suite의 기계적 재실행이 아니다. 중간 commit·통합을 최종 검수 승인으로 간주하지 않는다.

상세 검증 범위는 [Agentic Engineering](docs/agentic-engineering.md#verification-scope)을 따른다.

### Skills

Skills support these rules; current project instructions take precedence.

| Work | Skill and expected result |
|---|---|
| Unresolved requirements | `requirements-clarity`: inspect existing context and resolve decisions that change scope, authority, behavior, or acceptance |
| Code changes | `karpathy-guidelines`: make the smallest justified change and validate the affected behavior |
| System prompts and model-facing contracts | `structured-prompt-template`: keep prompt structure, schema ownership, and provider contracts explicit |
| Local diff or hotfix review | `code-review`: identify concrete defects and apply fixes only within the requested mode |
| Frozen functional acceptance bundle | `packet-review`: review Plan alignment and implementation together; reuse valid evidence instead of repeating the same broad review |
| Document structure and wording | `writing-clearly-and-concisely` and `humanizer`: improve clarity and natural phrasing while preserving facts, conditions, uncertainty, and authorial voice |
| Durable technical decisions | `decision-record`: update a related ADR first and record the settled rationale and impact |
| Requested transfer or existing continuity note | `handoff`: keep current stage, evidence, blockers, and next action; detailed long-running work stays in the Plan |
| Commit-message preparation and review | `git-commit-helper`: describe the actual diff and verification within the authorized Git scope |

Carry established facts and still-valid verification between stages. Apply the skill for the current work without reopening settled contracts or duplicating review. Follow [Document Writing](docs/AGENTS.md) for the shared document workflow. New Handoff and Plan defaults are `YYYYMMDD_<topic>-handoff.md` and `YYYYMMDD_<slug>-plan.md`; preserve explicit user filenames and existing names when updating.

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
- **검증**: 수정한 Python 영역을 먼저 `uv run ruff check path/to/file.py`, `uv run pytest tests/test_target.py`로 확인한다. RTK가 있으면 `rtk proxy`로 감싼다. 자동 수정이 필요할 때만 `uv run ruff check --fix path/to/file.py`를 실행하고 diff를 검토한다.
- **개발 철학**: `karpathy-guidelines`를 반드시 준수한다.

---

## 문서화 표준

### 공통 작성·검수 원칙

- **목표는 독자가 필요한 내용을 읽고 정확하게 파악하는 것이다.** 의사결정·판단 이유·조건·예외·책임·진입점·수정 위치·의존 방향을 빠짐없이 담는다.
- **간결함은 정보 생략이 아니라 구조와 표현의 명료함이다.** 필요한 내용을 요약문으로 대체하거나 줄 수를 줄이는 것을 목표로 삼지 않는다. 아래의 "상세히"도 필요한 근거와 예외를 충분히 설명한다는 뜻이며, 배경과 원칙을 길게 반복한다는 뜻이 아닙니다.
- 책임·수정 위치·비교 항목은 **표**, 실행 흐름·의존 방향·상태 수명은 **도식**, 수행 절차는 **순서 목록**으로 정리한다. 정보에 맞는 형식을 적극 활용하고 판단 이유·조건·예외는 해당 항목 가까이에 둔다.
- 같은 원칙과 상세 설명은 정보 한 곳에 모으고 필요한 위치에서 핵심 맥락과 링크를 제공한다. 서술을 길게 이어 붙이거나 여러 문서에 반복해 독자가 핵심을 찾기 어렵게 만들지 않는다.
- 재구성 후에는 **수정 전후의 정보와 실제 코드를 대조**한다. 필요한 내용의 누락·의미 변화·모호한 표현이 없는지 확인하고, 렌더링 표·도식의 가독성과 링크도 검수한다.

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
- **시각 자료 적극 활용**: 구조를 먼저 이해할 수 있도록 아스키 다이어그램, Mermaid(시스템 컨텍스트, 시퀀스, 상태 전이도 등)를 적극적으로 포함한다
- 루트 README는 전체 시스템을 아는 주체가 쓴다. 모듈 docstring은 해당 모듈만 주로 보면 되므로 분업 가능하다
- 폴더 README는 소스를 열지 않아도 목적·책임·주요 흐름·의존 방향·분업 경계를 이해할 수 있게 쓴다. 필요한 정보는 `__init__.py` docstring과 겹쳐도 된다.

---

## Git 컨벤션

아래는 [Git Convention](docs/git-convention.md)과 `git-commit-helper`의 요약이며, 반드시 상세규칙을 준수한다.

- 커밋 메시지는 `[type] 한국어 요약` 형식을 사용한다.
- 본문은 1~5개 불릿으로 변경 요약, 이유, 검증 또는 영향을 기록한다.
- 여러 목적이 섞인 변경은 커밋을 나눈다.
- 병합 커밋도 본문을 생략하지 않는다.
- 실제 변경·push·PR 생성은 해당 작업의 권한 범위에서만 수행한다.

---

## 기본 검증

```sh
uv run ruff check .
uv run mypy src
uv run pytest
```
