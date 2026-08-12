# Decisions Directory Rules

This directory holds ADRs. The writing procedure, numbering, 6-section template,
and supersede model are owned by the `decision-record` skill; `README.md` has the
folder convention. Ask the agent "ADR 남겨줘" to create one.

- An ADR is committed as shared documentation (unlike `plan/` and `handoff/`).
- When a decision is made on a `feature/` or `fix/` branch, put its ADR in the SAME branch and merge it together with the implementation
  — never split the decision record from the code it justifies in history (see `docs/git-convention.md`).

## ADR Scope Gate

Before creating or editing an ADR, inspect the related feature as one unit: its authority owner, API flow, persistence or migration chain, failure and rollback boundary, and verification gate.

- Update an existing ADR when the change strengthens the same feature, authority boundary, API flow, or migration chain.
- Put implementation order, progress, packet status, and test results in `docs/plan/`; do not duplicate them into a new ADR.
- Create a new ADR only for a durable architecture, dependency, module-boundary, storage, or public-contract decision that existing ADRs cannot explain.
- Do not assign separate ADR numbers to small findings from the same feature review. Consolidate background, decision, rejected alternatives, impact, and verification gates first.
- Create a superseding ADR only when the prior direction is reversed. Wording cleanup, evidence updates, and implementation-status corrections amend the existing ADR.
- Before choosing a new number, search `README.md` and related ADRs by feature, authority, table, route, and contract names; record why an existing ADR is insufficient.
