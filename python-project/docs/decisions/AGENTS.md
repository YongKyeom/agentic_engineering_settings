# Decisions Directory Rules

This directory holds ADRs. Follow [the docs guide](../AGENTS.md#유형별-템플릿) for the writing procedure, numbering, 6-section template, and supersede model. Use `decision-record` for ADR authoring; `README.md` has the folder convention.

- An ADR is committed as shared documentation (unlike `plan/` and `handoff/`).
- ADR local-file links must point to Git-tracked files. Do not link to ignored or untracked plans, handoffs, artifacts, or other local files; move needed evidence into a tracked integration document or another suitable tracked document first. External references should be accessible to the team.
- When a decision is made on a `feature/` or `fix/` branch, put its ADR in the SAME branch and merge it together with the implementation
  — never split the decision record from the code it justifies in history (see `docs/git-convention.md`).
- Keep the decision date in the top metadata. Summarize current decisions, reasons, and impacts concisely in the body; keep dated progress and pre-change judgments in revision history. Detailed execution and test records belong in the Plan.

## ADR Scope Gate

Before creating or editing an ADR, inspect the related feature as one unit: its authority owner, API flow, persistence or migration chain, failure and rollback boundary, and verification gate.

- Update an existing ADR when the change strengthens the same feature, authority boundary, API flow, or migration chain.
- Put implementation order, progress, packet status, and test results in `docs/plan/`; do not duplicate them into a new ADR.
- Create a new ADR only for a durable architecture, dependency, module-boundary, storage, or public-contract decision that existing ADRs cannot explain.
- Do not assign separate ADR numbers to small findings from the same feature review. Consolidate background, decision, rejected alternatives, impact, and verification gates first.
- Create a superseding ADR only when the prior direction is reversed. Wording cleanup, evidence updates, and implementation-status corrections amend the existing ADR.
- Before choosing a new number, search `README.md` and related ADRs by feature, authority, table, route, and contract names; record why an existing ADR is insufficient.
