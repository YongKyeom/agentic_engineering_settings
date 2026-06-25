---
# dark-theme-pdf 템플릿 — 채워 넣고 불필요한 슬라이드는 지우세요.
# 이미지는 이 파일 옆 ./images/ 에 두고 상대경로로 참조합니다 (선행 / 금지, mdc:true 금지).
theme: default
title: "{ { 발표 제목 } }"   # YAML 값엔 따옴표 필수 ({ { } } 가 flow-mapping 으로 파싱돼 깨짐)
fonts:
  provider: none
  sans: Pretendard
transition: slide-left
layout: center
class: text-center
---

<!-- ───────── 표지 (발표자 블록은 호출 시 사용자에게 확인한 값으로 채움) ───────── -->
<div class="eyebrow">{ { EYEBROW · 예: 주제 키워드 · 날짜 } }</div>

<div class="text-6xl font-extrabold mt-6 mb-6" style="line-height:1.16; letter-spacing:-0.02em">
{ { 메인 제목 1줄 } }<br/>{ { 메인 제목 2줄 } }
</div>

<div class="text-xl text-gray-400 mb-14">{ { 부제 } }</div>

<div class="author">
  <div class="name">{ { 발표자 이름/직함 } }</div>
  { { 소속 1줄 } }<br/>
  { { 소속 2줄 } }<br/>
  <span class="org-dim">{ { 조직 · 날짜 } }</span>
</div>

---
layout: default
---

<!-- ───────── 어젠다 / 목차 · 카드 없이 일반 마크다운 불릿 ───────── -->
# { { 어젠다 제목 · 예: 오늘 다룰 내용 } }

<div class="slide-body">

1. { { 섹션 1 } }
2. { { 섹션 2 } }
3. { { 섹션 3 } }

- { { 보조 불릿 — 카드 없이 본문에 바로 } }
- { { 불릿 항목 } }

</div>

---
layout: default
---

<!-- ───────── 본문 + 표 ───────── -->
<div class="eyebrow">SECTION</div>

# { { 슬라이드 제목 } }

<div class="slide-body">

<div class="text-gray-300 mb-2">{ { 한 줄 리드 — 이 슬라이드의 한 메시지 } }</div>

| 항목 | 값 |
|---|---|
| **{ { 행1 } }** | { { 값1 } } |
| **{ { 행2 } }** | { { 값2 } } |

<div class="callout mt-4">
<b>주의</b> — { { 콜아웃 본문. teal 변형은 class="callout teal" } }
</div>

</div>

---
layout: default
---

<!-- ───────── 2열 비교 카드 (3열은 grid-cols-3) ───────── -->
# { { 비교 제목 } }

<div class="slide-body">

<div class="text-gray-300 mb-2">{ { 비교 리드 } }</div>

<div class="grid grid-cols-2 gap-6">
<div class="card">
<div class="text-lg font-bold mb-2">{ { A 제목 } } <span class="text-sm text-gray-500 font-normal">· { { A 부제 } }</span></div>

- ✓ { { 장점 } }
- ✓ { { 장점 } }
- ✗ { { 단점 } }

</div>
<div class="card">
<div class="text-lg font-bold mb-2">{ { B 제목 } } <span class="text-sm text-gray-500 font-normal">· { { B 부제 } }</span></div>

- ✓ { { 장점 } }
- ✓ { { 장점 } }
- ✗ { { 단점 } }

</div>
</div>

<div class="callout mt-5">🔑 <b>핵심</b> — { { 비교의 결론 한 줄 } }</div>

</div>

---
layout: two-cols
---

<!-- ───────── 2열 텍스트 (Slidev 네이티브 two-cols · 좌/우 분할) ─────────
     주의: two-cols 는 slide-body 를 쓰지 않는다(자체 grid). ::right:: 로 두 열을 가른다. -->
# { { 왼쪽 제목 } }

- { { 왼쪽 항목 } }
- { { 왼쪽 항목 } }

::right::

# { { 오른쪽 제목 } }

- { { 오른쪽 항목 } }
- { { 오른쪽 항목 } }

---
layout: default
---

<!-- ───────── stat / KPI 카드 (큰 숫자 · .num/.lbl) ───────── -->
# { { 지표 슬라이드 제목 } }

<div class="slide-body">

<div class="grid grid-cols-3 gap-6">
<div class="card"><div class="num pink">{ { 숫자 } }</div><div class="lbl">{ { 라벨 } }</div></div>
<div class="card"><div class="num teal">{ { 숫자 } }</div><div class="lbl">{ { 라벨 } }</div></div>
<div class="card"><div class="num purple">{ { 숫자 } }</div><div class="lbl">{ { 라벨 } }</div></div>
</div>

</div>

---
layout: default
---

<!-- ───────── 아키텍처 다이어그램 (다크 카드 노드 · 직접 작성) ───────── -->
# { { 다이어그램 제목 } }

<div class="slide-body">

<div class="eyebrow mb-3">{ { 경로 라벨 } }</div>
<div class="diagram">
  <div class="flex flex-col gap-3">
    <div class="dnode">{ { 노드 } }<small>{ { 부연 } }</small></div>
    <div class="dnode">{ { 노드 } }<small>{ { 부연 } }</small></div>
  </div>
  <div class="darrow">→</div>
  <div class="dnode accent">{ { 강조 노드 } }<small>{ { 부연 } }</small></div>
</div>
<div class="text-sm text-gray-400 mt-3">{ { 한 줄 설명 } }</div>

</div>

---
layout: statement
---

<!-- ───────── 큰 선언문 (전환·강조 한 줄 · Slidev 네이티브 statement) ───────── -->
# { { 강조하고 싶은 한 문장 } }

---
layout: default
class: divider
---

<!-- ───────── PART 섹션 디바이더 (좌측정렬) ───────── -->
<div class="slide-body">

<div class="eyebrow">PART 1</div>
<div class="dtitle">{ { 섹션 제목 } }</div>
<div class="dsub">{ { 섹션 부제 } }</div>

</div>

---
layout: default
---

<!-- ───────── 코드 슬라이드 ───────── -->
# { { 코드 슬라이드 제목 } }

<div class="slide-body">

```bash
{ { 명령 또는 설정 } }
```

실행 — `{ { 실행 명령 } }`

<div class="callout mt-3">{ { 주의/팁 } }</div>

</div>

---
layout: default
---

<!-- ───────── 이미지 + 캡션 (스크린샷 · 또는 Mermaid/수식/차트를 흰 배경 이미지로) ───────── -->
# { { 이미지 슬라이드 제목 } }

<div class="slide-body">

<img src="./images/{ { 파일명 } }.png" class="shot mx-auto" style="max-height:60vh" />

<div class="caption mt-5">
{ { 캡션 1줄 — 화면 사실만 담백하게 } }<br/>
{ { 캡션 2줄 — 의미 단위로 줄바꿈 } }
</div>

</div>

---
layout: default
---

<!-- ───────── 출처/근거 카드 (3열) ───────── -->
# { { 근거 슬라이드 제목 } }

<div class="slide-body">

<div class="text-gray-300 mb-4">{ { 근거의 요지 한 줄 } }</div>

<div class="grid grid-cols-3 gap-5">
<div class="card">
<div class="text-base font-bold mb-1">{ { 출처명 } }</div>
<div class="desc">{ { 무엇을 뒷받침하는지 } }</div>
<a class="src" href="{ { 실제 검증된 URL } }">{ { 표시용 도메인/경로 } }</a>
</div>
<!-- 카드 2, 3 동일 패턴 -->
</div>

<div class="callout mt-5"><b>단,</b> { { 정직한 한계/단서 } }</div>

</div>

---
layout: center
class: text-center
---

<!-- ───────── 체크리스트 / 클로징 ───────── -->
<div class="eyebrow">SUMMARY</div>

<div class="text-4xl font-extrabold mt-4 mb-10">{ { 체크리스트 제목 } }</div>

<div class="checklist">
<div class="item"><span class="cb"></span><span>{ { 항목 1 } }</span></div>
<div class="item"><span class="cb"></span><span>{ { 항목 2 } }</span></div>
<div class="item"><span class="cb"></span><span>{ { 항목 3 } }</span></div>
</div>

<div class="eyebrow mt-10">THANK YOU</div>
