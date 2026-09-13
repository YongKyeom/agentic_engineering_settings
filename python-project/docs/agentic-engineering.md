# Agentic Engineering

Use this guide for Codex, Claude, and human collaboration inside the project.

## Default Collaboration Model

- The main agent owns task framing, source-of-truth selection, integration, and final user communication.
- Sub-agents provide evidence, bounded patches, or review findings.
- Treat sub-agent output as evidence, not authority.
- The human owner decides product intent, priority, and approval.

## When To Use Sub-Agents

Use sub-agents when work is independent and useful in parallel:

- Codebase exploration with a narrow question.
- Independent review of a patch or plan.
- Verification that can run while implementation continues.
- Disjoint implementation work with non-overlapping file ownership.

Do not use sub-agents for:

- Small tasks.
- Sequential blockers.
- Tightly coupled refactors.
- Work that would create duplicate effort.
- Overlapping edits in the same files.

## Delegation Contract

Every delegated task should include:

- Objective.
- Scope and files to inspect.
- Files allowed to edit, if any.
- Source of truth and priority order.
- Constraints and forbidden changes.
- Expected output format.
- Verification criteria.

## Verification Scope

작은 수정의 검증과 기능 묶음의 인수 검증을 분리한다. `full gate`는 필요한 기능 acceptance 전체를 뜻하며,
저장소 전체 테스트 실행을 자동으로 뜻하지 않는다.

| 변경·마감 단위 | 실행할 검증 | 반복하지 않을 작업 |
|---|---|---|
| 함수·조건·타입·국소 버그 수정 | 실패를 재현하는 테스트와 영향받는 호출 경로, 수정 영역의 lint·type 검사 | 전체 suite, 무관한 통합 여정, 전체 문서 재검수 |
| 완결된 기능 묶음 | 입력·적용·조회·복구의 acceptance 회귀와 필요한 독립 검수 1회 | 내부 Packet별 동일 gate·광범위한 중복 리뷰 |
| 공통 계약의 광범위한 변경·최종 통합 | 전체 영향 범위에 필요한 suite와 통합 gate | 변경에 영향받지 않는 유효 증거의 기계적 재실행 |
| 문서·지침만 변경 | 내용·링크·변경 구간 렌더 | Python lint·type·pytest |

- 실행 전에 selector, 영향 근거, 예상 시간 또는 deadline을 정한다. 비싼 실행은 기능 묶음의 마감 시점에 모은다.
- 실패 수정 뒤에는 실패 사례와 추가 영향 경로만 먼저 재실행한다. 전체 gate를 다시 열 때는 어떤 기존 근거가 무효화됐는지 Plan에 짧게 적는다.
- 기존 PASS는 source·입력·계약과 검증 범위가 여전히 유효할 때 재사용한다. 새로 바뀐 경계까지 검증됐다고 확대하지 않는다.
- 승인 우회·잘못된 쓰기·상태 손상은 즉시 영향 검증한다. 묶음 검수는 필수 안전 검증을 미루거나 생략하는 근거가 아니다.
- 작은 수정마다 새 보고서나 전체 문서 렌더를 만들지 않는다. 기존 Plan의 현재 상태·결과를 갱신하고 기능 마감 때 정리한다.

## Review Discipline

- Separate implementation packets from review bundles. Define both scopes and dependencies in the Plan.
- For each implementation packet, run targeted tests and a narrow lead diff check, then allow intermediate commits and integration into the development branch. Clean up worker worktrees immediately after integration.
- Freeze a coherent bundle of related packets for one full gate and one integrated `packet-review`. These checks may run independently in parallel on the same candidate; adjudicate their combined results.
- Review at a completed feature boundary, a material shared-contract/state/transaction boundary, or before PR delivery. A high-risk small packet may justify its own review; small size alone does not require one.
- The review checks plan and ADR alignment, completeness, correctness, type safety, security and privacy, performance, and maintainability.
- Use one reviewer when sufficient. Split a large bundle by bounded module or risk ownership and consolidate one verdict.
- Do not assign a separate broad `code-review` over the same packet. That repeats source loading without adding a distinct acceptance gate.
- Use `code-review` separately only for a small hotfix without an active plan packet, or when the user explicitly requests it.

Classify review feedback before acting on it:

- `accepted`: Apply or address now.
- `deferred`: Valid, but outside current scope.
- `rejected`: Conflicts with instructions, source of truth, or verified data.

Keep rejected feedback when the reason affects future work.

- Give each must-close item a deadline and impact-based reason. Fix or isolate unsafe writes, approval bypasses, and state corruption immediately. Close other blocking defects at the bundle boundary; defer non-blocking improvements with an owner and revisit condition.
- Do not interpret "before the next packet" as a mandatory stop after every small implementation unit.
- Recheck only the affected regression and fix diff. Repeat the full gate only when later changes invalidate its coverage; record why. Validate documentation-only changes with rendering, links, and content checks.
- Finish implementation and required fixes, finalize documentation, then perform lead final verification. Intermediate commits are allowed; they are not final bundle approval or permission to bypass the PR boundary.

## Work Records and Handoff

Follow [docs writing guidance](AGENTS.md) for record ownership and status format.

- Update the existing Handoff for short tasks: status, result, and next action.
- Keep detailed specifications, ownership, verification, and lessons for long-running or multi-agent work in the Plan. Handoff holds only the summary and link.
- The lead updates the same Plan after delegation and adjudication so agents share one objective and current status.
- Create a separate Handoff or perform an explicit transfer only at the user's request, not merely because context is long.
