# Skills

이 폴더는 직접 관리하는 custom/third-party agent skill을 보관한다.
공식 system skill이나 공식 plugin으로 다시 설치할 수 있는 범용 skill은 원칙적으로 보관하지 않는다.

## Skill 목록

| Skill | 용도 | 주 사용처 |
|-------|------|-----------|
| `agent-md-refactor` | 긴 `AGENTS.md`, `CLAUDE.md`를 progressive disclosure 구조로 정리 | agent instruction 정리 |
| `c4-architecture` | C4 모델 기반 아키텍처 문서와 Mermaid 다이어그램 작성 | system/container/component/deployment 문서 |
| `code-review` | diff나 파일 기준 코드 리뷰 | Codex custom skill. Claude Code는 built-in 사용 |
| `dark-theme-pdf` | 다크+마젠타 하우스 테마로 발표자료 작성 후 PDF 내보내기 | 다크 테마 덱, `presentation-slidev`에 빌드 위임 |
| `deep-research` | 여러 소스 조사, 사실 검증, 인용 포함 리포트 작성 | Codex custom skill. Claude Code는 built-in 사용 |
| `excalidraw` | Excalidraw 파일 작업을 sub-agent에 위임 | `.excalidraw`, `.excalidraw.json` |
| `git-commit-helper` | 한국어 커밋 메시지 작성과 커밋 분리 판단 | staged/unstaged diff 검토 |
| `handoff` | 다음 세션이나 다른 agent가 이어받을 수 있는 인수인계 작성 | 긴 작업 종료, context 전환 |
| `humanizer` | AI 문체, 번역투, 과한 수사 제거 | 사용자-facing 산문 다듬기 |
| `karpathy-guidelines` | 과잉 구현 방지, 외과적 수정, 검증 기준 명확화 | 코드 작성/수정 전반 |
| `lesson-learned` | 실제 코드 변경에서 재사용 가능한 엔지니어링 교훈 추출 | 회고, 반복 실수 정리 |
| `mermaid-diagrams` | Mermaid 기반 다이어그램 작성 | flowchart, sequence, ERD, state 등 |
| `packet-review` | 현재 작업 packet이 active plan과 어긋나지 않는지 검토 | plan 기반 장기 작업 |
| `presentation-slidev` | Slidev 발표자료 작성과 PDF 렌더링 워크플로우 | 학위논문/기술 발표 |
| `requirements-clarity` | 모호한 요구사항을 구현 가능한 범위로 좁힘 | 구현 전 요구사항 정리 |
| `skill-judge` | skill 품질 평가와 개선점 도출 | `SKILL.md` 리뷰/개선 |
| `writing-clearly-and-concisely` | 명확하고 간결한 글쓰기 | 문서, 커밋 메시지, 설명문 |

## 세부 설명

### Agent Instruction

`agent-md-refactor`는 루트 instruction 파일이 너무 길어졌을 때 사용한다.
핵심 규칙만 루트에 남기고 세부 문서는 별도 파일로 분리하는 방식이다.

`skill-judge`는 skill 자체를 평가할 때 사용한다.
frontmatter description, trigger clarity, progressive disclosure, anti-pattern, token waste를 기준으로 본다.

### Coding Workflow

`karpathy-guidelines`는 코드 작업의 기본 안전장치다.
불필요한 추상화와 넓은 refactor를 피하고, 작은 변경과 명확한 검증 기준을 우선한다.

`code-review`는 Codex에서 custom skill로 사용한다.
Claude Code에서는 built-in `/code-review`가 있으므로 `setup/claude-code.sh`가 command로 복사하지 않는다.

`packet-review`는 active plan 문서가 있는 장기 작업에서 방향 이탈을 확인한다.
코드 리뷰와 달리 구현 품질보다 계획 대비 누락, drift, must-close 항목을 본다.

### Research And Retrospective

`deep-research`는 Codex에서 custom skill로 사용한다.
Claude Code에서는 built-in `/deep-research`가 있으므로 `setup/claude-code.sh`가 command로 복사하지 않는다.

`lesson-learned`는 최근 코드 변경이나 디버깅 결과에서 재사용 가능한 원칙을 뽑을 때 사용한다.
일반 조언이 아니라 실제 diff와 사건에 근거한 교훈을 남기는 것이 목적이다.

### Writing

`writing-clearly-and-concisely`는 일반적인 명료화와 문서 문장 개선에 쓴다.
Strunk 계열의 간결한 문장 원칙과 AI 문체 회피 기준을 함께 다룬다.

`humanizer`는 더 직접적으로 AI 문체, 번역투, 과장된 표현을 제거한다.
두 skill은 겹치는 부분이 있지만, `humanizer`는 자연스러운 사람 문체에 더 특화되어 있다.

### Planning And Handoff

`requirements-clarity`는 요구사항이 모호하거나 범위가 커서 바로 구현하면 위험할 때 사용한다.
단순한 버그 수정이나 구체적인 파일 수정 요청에는 쓰지 않는다.

`handoff`는 긴 작업을 끊거나 다음 세션으로 넘길 때 사용한다.
결정, 변경사항, 검증, 남은 위험을 짧게 정리하는 것이 핵심이다.

### Diagrams And Presentations

`c4-architecture`는 C4 모델이 필요한 소프트웨어 아키텍처 문서에 사용한다.
software system context, container, component, deployment 관점이 필요하면 이 skill이 우선이다.

`mermaid-diagrams`는 일반 Mermaid 다이어그램에 사용한다.
flowchart, sequence diagram, ERD, state diagram처럼 C4가 아닌 기술 다이어그램에 적합하다.

`excalidraw`는 Excalidraw JSON이 큰 파일이라는 점 때문에 sub-agent 위임을 기본으로 한다.
메인 agent가 직접 파일 전체를 읽어 context를 낭비하지 않도록 하는 목적이 크다.

`presentation-slidev`는 Slidev로 발표자료를 만들고 PDF로 렌더링할 때 사용한다.
코드, Mermaid, 수식, 반복 렌더링이 많은 기술 발표에 맞춰져 있다.

`dark-theme-pdf`는 다크+마젠타 하우스 테마(배경 `#0c0d12`, 강조 `#ff2d78`, Pretendard)로 발표자료를 만들 때 사용한다.
디자인 시스템(`assets/style.css`)과 슬라이드 골격, 컴포넌트 패턴만 제공하고 실제 scaffold/export/검수 루프는 `presentation-slidev`에 위임한다.

## 관리 원칙

- 각 skill은 `skills/<skill-name>/SKILL.md`를 최소 단위로 둔다.
- 필요한 경우에만 `references/`, `scripts/`, `assets/`, `evals/`를 추가한다.
- `SKILL.md` frontmatter의 `description`은 trigger 역할을 하므로 가장 중요하다.
- 공식 system skill이나 plugin으로 재설치 가능한 범용 skill은 이 폴더에 복사하지 않는다.
- 특정 프로젝트 전용 skill은 공통 레포에 넣지 않는다.
- Claude Code built-in 기능과 중복되는 skill은 Codex용 custom skill로만 유지할 수 있다.
