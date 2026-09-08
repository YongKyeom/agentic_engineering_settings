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
