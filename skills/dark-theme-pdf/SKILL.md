---
name: dark-theme-pdf
description: Build a presentation/slide deck and export it as a PDF in the saved dark + magenta "house" theme — dark background (#0c0d12), magenta accent (#ff2d78), Pretendard font, pink-underline headers, and ready-made card / callout / diagram / image-caption / checklist / source-link components. Use whenever the user wants slides or a deck PDF in this dark theme, references "dark-theme-pdf" / "다크 테마 발표자료", or asks to reuse the look of a previous dark deck. This skill supplies the design system + authoring patterns and delegates the actual Slidev scaffold / export / visual-verify loop to the presentation-slidev skill.
---

# dark-theme-pdf

다크 + 마젠타 디자인 시스템으로 발표자료를 빠르게 만들고 PDF 로 내보내는 스킬.

역할 분리가 핵심이다:
- **이 스킬** = "어떻게 보이는가" — 디자인 시스템(`assets/style.css`) + 슬라이드 골격(`assets/slides.template.md`) + 작성 패턴.
- **presentation-slidev 스킬** = "어떻게 PDF 로 굽는가" — scaffold, `slidev export`, 렌더→PDF 읽기→반복 검수.

따라서 빌드/검수 단계는 직접 재구현하지 말고 **presentation-slidev 를 호출해 따른다.**

## 워크플로

### 0. 먼저 사용자에게 확인 (반드시)
- **발표자 블록** — 이름/직함과 소속 줄들. **소속은 발표마다 달라질 수 있으므로 하드코딩하지 말고 매 호출 되묻는다.**
- **덱 범위** — 주제, 청중/톤, 대략 슬라이드 수, 필요한 섹션.
- **작업 폴더 위치** — 기본값은 현재 작업 디렉터리 아래 `./<주제>-deck/`. 사용자가 정하면 그곳에.

### 1. Scaffold
이 스킬 디렉터리의 `assets/` 에서 작업 폴더로 복사한다(이 스킬 경로 = `~/.claude/skills/dark-theme-pdf/`):
- `assets/style.css` → 작업폴더 `style.css` (그대로, 수정 거의 불필요)
- `assets/package.json` → 작업폴더 `package.json` (그대로)
- `assets/slides.template.md` → 작업폴더 `slides.md`
이미지가 있으면 작업폴더에 `images/` 를 만들고 거기에 둔다. 의존성 설치: `npm install` (필요 시 `npx playwright install chromium`).

### 2. 작성
- 0단계에서 받은 발표자 블록을 표지에 채운다.
- 템플릿의 플레이스홀더를 실제 내용으로 교체하고, 안 쓰는 예시 슬라이드는 지운다.
- 아래 **컴포넌트** 패턴을 사용한다. 한 슬라이드 한 메시지, 담백한 톤(과장·드라마 어투 금지).

### 3. 빌드 · 검수 — presentation-slidev 에 위임
`presentation-slidev` 스킬의 절차를 따른다:
- 작업폴더에서 `npx slidev export --output slides.pdf`
- 렌더된 `slides.pdf` 를 **직접 읽어** 오버플로 · 잘림 · 정렬 · 대비 · 가독성 점검
- 문제를 `slides.md`(내용/구조) 또는 `style.css`(스타일)에서 고치고 재렌더, 깨끗해질 때까지 반복
- macOS 에 `timeout` 이 없으면 `perl -e 'alarm 240; exec @ARGV' -- npx slidev export ...` 로 감쌀 수 있다.

### 4. 전달
최종 `slides.pdf` 경로를 알리고, 필요하면 파일을 사용자에게 전달한다.

## 컴포넌트 (전체 골격은 assets/slides.template.md 참조)
| 용도 | 패턴 |
|---|---|
| 표지 | `layout: center` + `class: text-center` · `.eyebrow` · 큰 제목 · 부제 · `.author` 블록 |
| 본문 슬라이드 | `# 제목` 뒤 `<div class="slide-body"> … </div>` → 세로 중앙정렬 + 핑크 밑줄 헤더 |
| 어젠다 / 일반 불릿 | `slide-body` 안에 카드 없이 마크다운 `1.`·`-` 리스트 (style.css 가 다크 스타일링) |
| 2열 텍스트 | `layout: two-cols` + `::right::` (네이티브 grid 2열). slide-body 불필요, 헤더 핑크 밑줄 적용됨 |
| stat / KPI 카드 | `.card` 안에 `.num`(`pink`/`teal`/`purple`) + `.lbl` — 큰 숫자 강조 |
| 큰 선언문 | `layout: statement` + `# 한 문장` — 전환·강조 |
| PART 디바이더 | `class: divider` · `.eyebrow` / `.dtitle` / `.dsub` (좌측정렬) |
| 비교/출처 카드 | `grid grid-cols-2`(또는 3) + `.card` (+ 본문은 `.desc`) |
| 주의 박스 | `.callout` (강조 변형 `.callout teal`) |
| 아키텍처 도식 | `.diagram` > `.dnode`(강조 `.dnode.accent`) + `.darrow` |
| 이미지+캡션 | `<img class="shot" style="max-height:60vh">` + `.caption`. 스크린샷 · **Mermaid/수식/차트(흰 배경 이미지)** 공통 |
| 체크리스트 | `.checklist` > `.item` > `.cb`(체크박스) + 텍스트 |
| 출처 링크 | `<a class="src" href="…">표시경로</a> |
| 표 / 코드 | 일반 마크다운 표·펜스 코드블록 (style.css 가 자동 다크 스타일링) |

## 디자인 토큰
배경 `#0c0d12` · 마젠타 `#ff2d78` · teal `#2dd4bf` · purple `#a78bfa` · 카드 `#15161e` · 폰트 Pretendard(style.css 의 CDN @import 로 로드).

## 작성 규칙 · 이미 해결한 함정
- 프론트매터: `theme: default` + `fonts: { provider: none, sans: Pretendard }`.
- 본문 슬라이드는 `# 제목` + `<div class="slide-body">…</div>`. 표지/디바이더/클로징은 `layout: center` 또는 `class: divider` (slide-body 불필요).
- 이미지는 작업폴더 `./images/` 상대경로. **선행 `/` 금지**(Slidev fs.allow 위반), 프론트매터에 **`mdc: true` 금지**(`<img>` 깨짐).
- 한국어 줄바꿈은 style.css 의 `word-break: keep-all` 이 처리. 캡션/콜아웃은 한 줄에 욱여넣지 말고 의미 단위로 `<br/>`.
- 캡션은 `.caption`(본문과 동일 크기, `text-sm` 으로 줄이지 말 것). URL 링크는 `.src`(break-all 로 줄바꿈).
- **출처 URL 은 추측/날조 금지** — 실제 resolve 되는 것만 넣는다(불확실하면 WebFetch 로 검증).
- 디자인은 전부 클래스로 제공된다. 새 변형이 필요하면 style.css 에 클래스를 추가하되 토큰(`--pink` 등)을 재사용한다.

## 수식 · 다이어그램 · 차트 — 흰 배경 이미지로 (권장)
Mermaid · LaTeX/KaTeX · 차트는 **라이브로 다크테마링하지 말고, 흰 배경으로 렌더한 PNG/SVG 를 `.shot` 으로 삽입**한다. 다크 슬라이드 위에서 테두리·그림자로 프레임된 흰 "종이 카드"처럼 보인다(수식 케이스로 렌더 검증 — Mermaid·차트도 동일 삽입 메커니즘). 삽입은 "이미지+캡션" 패턴 그대로 — `<img class="shot" style="max-height:…">` + `.caption`.
- **⚠ presentation-slidev 위임 주의** — 그 스킬은 라이브 mermaid 코드블록과 `$LaTeX$` 수식을 가르치지만, **이 다크 테마에선 라이브 렌더가 어두운 배경에서 깨져 안 보인다.** 빌드를 위임하더라도 다이어그램·수식은 반드시 아래 흰 배경 이미지 방식으로 만든다.
- **Mermaid** — `mmdc`(mermaid CLI) 또는 `mermaid-diagrams` 스킬로 PNG/SVG 생성(흰/기본 배경). 아주 단순한 도식이면 이 스킬의 `.diagram` / `.dnode` 직접 작성도 대안.
- **LaTeX/KaTeX** — matplotlib mathtext 로 흰 배경 렌더(`fig.patch.set_facecolor("white")` + `savefig(facecolor="white", bbox_inches="tight")`), 또는 LaTeX→PNG 도구. mathtext 는 일부 매크로 미지원(예: `\lVert`/`\rVert` → `\|` 로 대체).
- **차트/그래프** — 같은 원리로 matplotlib 등에서 사전 렌더한 PNG 를 `.shot`. 라이브 차트(echarts)를 다크로 테마링하면 축·눈금·레이블 색을 일일이 잡아야 해 비권장.

## 확장 시 (미검증 — 첫 사용 때 렌더 확인)
- **`image-right` / `image-left`** — 이미지가 `object-fit: cover` 로 잘리므로 **사진·세로형**엔 적합하나 **와이드 스크린샷·다이어그램엔 부적합**(그건 중앙 `.shot` 패턴을 쓴다).
- **그 외 Slidev 레이아웃**(`full`·`quote`·`fact` 등) — 우리 스타일은 `.slidev-layout.default`(+ `.two-columns` 헤더)에만 scope 되어 있어 적용되지 않는다. 쓰려면 해당 레이아웃 클래스에 맞춰 style.css 에 규칙을 추가하고 렌더로 확인한다.
