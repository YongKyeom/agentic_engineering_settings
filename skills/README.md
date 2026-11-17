# Skills

이 폴더는 직접 관리하는 custom/third-party agent skill을 보관한다.
공식 system skill이나 공식 plugin으로 다시 설치할 수 있는 범용 skill은 원칙적으로 보관하지 않는다.

## Skill 목록

| Skill | 용도 | 주 사용처 |
|-------|------|-----------|
| `agent-md-refactor` | 필수 실행 요약과 의미를 보존하며 agent 지침 재구성 | 실제 적재 방식·문서 책임·링크를 확인하는 구조 정리 |
| `code-review` | 국소 diff·파일·hotfix 검토, 명시적으로 요청한 수정 | 읽기 전용 기본; 기능 인수 검수와 범위 구분 |
| `dark-theme-pdf` | 다크+마젠타 하우스 테마로 발표자료 작성 후 PDF 내보내기 | 다크 테마 덱, `presentation-slidev`에 빌드 위임 |
| `decision-record` | 기존 기록을 우선 보완하며 지속적인 기술 결정과 근거 기록 | 공유 ADR 작성·갱신; Git 작업은 요청 권한에 따름 |
| `deep-research` | 여러 원자료를 비교·검증하고 출처가 있는 답변 작성 | 자료의 독립성·시점·상충 결과와 확인 한계 구분 |
| `excalidraw` | 편집 가능한 스케치와 기존 scene의 생성·조회·수정 | 작은 수정은 직접 처리; 큰 작업만 필요시 총괄이 위임 |
| `git-commit-helper` | 한국어 커밋 메시지 작성과 커밋 분리 판단 | staged/unstaged diff 검토 |
| `handoff` | 요청받은 인계·협업 문서 작성, 기존 기록 갱신, 작업 재개 | 사용자 요청에 따른 인계; 문맥 길이만으로 새 파일을 만들지 않음 |
| `humanizer` | 사실·조건·저자 말투를 보존하며 번역투·과한 수사 개선 | 한국어와 영문 산문의 자연스러운 표현 |
| `karpathy-guidelines` | 과잉 구현 방지, 외과적 수정, 검증 기준 명확화 | 코드 작성/수정 전반 |
| `lesson-learned` | 실제 코드 변경에서 재사용 가능한 엔지니어링 교훈 추출 | 회고, 반복 실수 정리 |
| `mermaid-diagrams` | 질문에 맞는 Mermaid 작성·수정·렌더 검증 | 실제 renderer 버전·문서 크기에 맞는 표현 선택 |
| `packet-review` | 동결된 기능 묶음의 계획 정합성·코드 품질 통합 리뷰 | 기능 인수 경계·고위험 변경·PR 전달 전; 대형 묶음은 범위 분할 후 단일 판정 |
| `presentation-slidev` | Slidev 발표자료 작성과 PDF 렌더링 워크플로우 | 학위논문/기술 발표 |
| `requirements-clarity` | 기존 문맥을 조사하고 구현을 바꾸는 미결 결정만 확인 | 요구사항·권한·완료 기준의 불확실성 해소 |
| `skill-judge` | skill의 발동·사용자 의도·권한·실제 동작을 근거로 검수 | 형식 요건과 설계 권고를 구분하는 패키지 리뷰 |
| `structured-prompt-template` | provider-neutral tagged Jinja2 system prompt 설계·검증 | native Tool calling, OpenAI-compatible API, vLLM, text-only Tool protocol |
| `writing-clearly-and-concisely` | 의미·정보량을 보존하며 구조와 문장을 명료화 | 문서·커밋 메시지·설명·UI 문구 |

## 세부 설명

### Agent Instruction

`agent-md-refactor`는 instruction 파일의 구조와 중복을 정리할 때 사용한다.
필수 Python·Git·검증·위임 요약은 프로젝트 규칙에 따라 루트에 남기고, 상세 내용은 실제 적재 방식에 맞게 분리한다.
줄 수를 맞추기 위해 규칙을 지우거나, 단순 링크만으로 자동 적재된다고 가정하지 않는다.

`skill-judge`는 skill 자체를 평가할 때 사용한다.
발동 조건, 사용자 의도·권한 보존, 유용한 지침, 의미 보존, 참고 자료, 실제 동작을 함께 본다.
기본 결과는 파일·줄·영향·검증 근거를 갖춘 지적이며, 점수는 요청한 경우에만 보조 수단으로 사용한다.
형식 검사 통과와 실제 작업 성공을 구분하며, 검수만 요청받았으면 수정·전역 설치로 범위를 넓히지 않는다.

### Prompt Engineering

`structured-prompt-template`는 XML 스타일 section tag와 Jinja2로 system prompt를 설계하거나 검토할 때 사용한다.
Skill·Tool manifest의 authority를 분리하고, native schema 중복 없이 닫힌 context, escaping, byte budget을 검증한다.

### Coding Workflow

`karpathy-guidelines`는 코드 작업의 기본 안전장치다.
불필요한 추상화와 넓은 refactor를 피하고, 작은 변경과 명확한 검증 기준을 우선한다.

`code-review`는 국소 변경의 구체적인 결함을 검토하며, 기본은 읽기 전용이다. `--fix`나 명시적인 수정 요청이 있으면 승인된 범위 안에서 보완하고 영향받은 검증을 수행한다.
이 저장소의 Claude 설치 스크립트는 built-in 기능과의 중복을 피하려고 이 custom skill의 복사를 생략한다.

`packet-review`는 frozen packet을 active plan·ADR과 대조하면서 구현 품질까지 함께 검토한다.
작은 packet은 한 reviewer가 보고, 큰 packet은 module·contract·risk 영역을 겹치지 않게 나눈 뒤 하나의 verdict로 통합한다.
같은 범위에 broad `code-review`를 추가로 돌리지는 않는다.

### Research And Retrospective

`deep-research`는 여러 소스의 원문을 읽고, 독립적인 근거와 수집 시점·버전·조건을 대조한다. 인용·추론·미확인을 구분하며 소스 수나 보고서 파일을 강제하지 않는다.
이 저장소의 Claude 설치 스크립트는 built-in 기능과의 중복을 피하려고 이 custom skill의 복사를 생략한다.

`lesson-learned`는 최근 코드 변경이나 디버깅 사건에서 재사용 가능한 원칙을 뽑는다. 요청한 diff·사건과 필요한 문맥을 근거로 원인·tradeoff·다음 행동을 설명하며, 관찰하지 않은 성과나 의도를 만들지 않는다. 회고가 곧 코드 수정·스킬 갱신·개인 메모리 저장 권한을 뜻하지 않는다.

### Writing

`writing-clearly-and-concisely`는 일반적인 명료화와 문서 문장 개선에 쓴다.
필요한 내용을 보존하며 구조·어휘·조건의 배치를 다듬고, 영문 고전 참고서는 필요한 경우에만 읽는다.

`humanizer`는 더 직접적으로 AI 문체, 번역투, 과장된 표현을 제거한다.
원문에 없는 사실·감정·의견을 추가하지 않으며, 한국어 높임말·문장 종결·부정과 불확실성을 보존한다.
두 skill은 각각 독립적으로 동작한다. 구조·명료화와 문체 개선이 함께 필요한 경우에만 조합한다.

### Planning And Handoff

`requirements-clarity`는 미결 결정이 실제 구현·범위·권한·완료 기준을 바꿀 때 사용한다.
관련 코드·Plan·계약을 먼저 확인하고, 답이 꼭 필요한 결정만 질문하며 독립 작업은 계속한다.
파일 경로가 있어도 요구가 모호하면 사용할 수 있고, 큰 작업이어도 이미 명확하면 바로 진행한다.
점수·반복 질의·별도 PRD 생성은 요구하지 않으며 프로젝트의 기존 기록을 갱신한다.

`handoff`는 사용자가 인계·협업 문서를 요청하거나 기존 기록을 갱신하고 작업을 재개할 때 사용한다.
문맥이 길어졌다는 이유로 새 문서를 만들지 않는다. 장기 작업의 상세 스펙·검증·시행착오는 Plan에 유지하고,
Handoff에는 현재 단계·차단 사유·다음 조치와 Plan 링크를 남긴다.
새 파일의 기본 이름은 `YYYYMMDD_<topic>-handoff.md`, Plan은 `YYYYMMDD_<slug>-plan.md`이며, 사용자가 지정한 이름이나 갱신 중인 기존 파일명은 따른다.

`decision-record`는 아키텍처, dependency, 모듈 경계처럼 오래 유지해야 하는 기술 결정을 ADR로 기록할 때 사용한다.
기존 ADR 보완 가능성을 먼저 확인하고, 채번·6절 템플릿·supersede 절차는 스킬을 따른다. 산출물은 각 프로젝트의
`docs/decisions/`에서 공유하며, commit·push·PR은 작업 권한 범위에서 수행한다.

### Diagrams And Presentations

`mermaid-diagrams`는 일반 Mermaid 다이어그램에 사용한다.
flowchart, sequence diagram, ERD, state diagram과 시스템 구조를 설명하는 기술 다이어그램에 사용한다.

`excalidraw`는 기존 ID·geometry·text/arrow binding·이미지 자산을 보존하며 scene을 편집한다. 크기와 관련 요소부터 좁혀 읽고, 큰 비교·배치 작업만 유용할 때 총괄이 위임한다. JSON 구조 검사와 실제 편집·렌더 확인을 구분한다.

`presentation-slidev`는 Slidev로 발표자료를 만들고 PDF로 렌더링할 때 사용한다.
코드, Mermaid, 수식, 반복 렌더링이 많은 기술 발표에 맞춰져 있다.

`dark-theme-pdf`는 다크+마젠타 하우스 테마(배경 `#0c0d12`, 강조 `#ff2d78`, Pretendard)로 발표자료를 만들 때 사용한다.
디자인 시스템(`assets/style.css`)과 슬라이드 골격, 컴포넌트 패턴만 제공하고 실제 scaffold/export/검수 루프는 `presentation-slidev`에 위임한다.

## 관리 원칙

- 프로젝트 지침·전역 규칙·스킬의 역할을 함께 대조한다. 필요한 실행 규칙은 반복해도 유지하며, 상세 스펙·실행 현황의 정본은 한 곳에서 갱신한다.
- 각 skill은 `skills/<skill-name>/SKILL.md`를 최소 단위로 둔다.
- 필요한 경우에만 `references/`, `scripts/`, `assets/`, `evals/`를 추가한다.
- `SKILL.md` frontmatter의 `description`은 trigger 역할을 하므로 가장 중요하다.
- 공식 system skill이나 plugin으로 재설치 가능한 범용 skill은 이 폴더에 복사하지 않는다.
- 특정 프로젝트 전용 skill은 공통 레포에 넣지 않는다.
- Claude Code built-in 기능과 중복되는 skill은 Codex용 custom skill로만 유지할 수 있다.

## 역할을 함께 고를 때

| 요청 | 우선 적용할 범위 | 추가 연결이 필요한 경우 |
|---|---|---|
| 요구가 미정인 구현 | `requirements-clarity`로 관련 문맥과 실제 미결 결정 확인 | 상세 작업은 기존 Plan에 유지 |
| 국소 코드 검토 / 기능 인수 | `code-review` / `packet-review`로 경계를 나눔 | 같은 범위의 광역 검수를 중복하지 않음 |
| 오래 유지할 기술 선택 / 작업 인계 / 회고 | `decision-record` / `handoff` / `lesson-learned` | 결정·상태·교훈의 정본을 구분하고 요청한 기록만 갱신 |
| 근거가 필요한 조사 | `deep-research` | 문서 작성·시각화는 결과를 전달하는 데 필요할 때 연결 |
| 구조·관계 설명 | 사용자가 고른 형식에 따라 `mermaid-diagrams` 또는 `excalidraw` | 표현 형식을 임의로 바꾸거나 모든 설명을 도식화하지 않음 |
| 문장·문서 구조 / 자연스러운 말투 | `writing-clearly-and-concisely` / `humanizer` | 의미·조건·확실성·저자 말투를 보존하며 필요할 때만 조합 |
| agent 지침 재구성 / skill 검수 | `agent-md-refactor` / `skill-judge` | 팀 공유에 필요한 중복은 보존하고 실제 이용 환경을 확인 |

앞 단계의 근거와 판정을 이어 사용하고, 현재 작업에 필요한 스킬을 해당 단계에 적용한다. 스킬 적용은 파일 수정·전역 설치·외부 전송의 권한을 넓히지 않는다.
