---
name: packet-review
description: Review a frozen functional bundle against its active Plan, acceptance criteria, and code-quality contracts. Use at a feature acceptance boundary, for high-risk changes, or before PR delivery. Combine direction, completeness, and implementation review in one read-only verdict; use code-review for a small diff or hotfix without repeating the same broad review.
---

# Packet Review

Review a complete functional bundle, such as input → apply → query/recovery, against its agreed behavior and implementation. A small implementation Packet or intermediate commit does not by itself require a broad gate. Explicit user instructions and project rules take priority over this workflow.

## Scope and authority

- Default to read-only review. Findings do not authorize source edits, provider calls, live-data changes, commits, merges, or publishing. An explicit fix request may authorize a separate bounded correction; do not infer that permission from a verdict.
- Use the active Plan and latest user decisions to establish the boundary, supported by relevant ADRs and contracts. If no Plan exists, use the supplied acceptance criteria and identify the missing baseline; do not invent requirements or create a Plan merely to review.
- Review only the agreed bundle and dependencies needed to assess it. Do not include unrelated dirty-worktree files.
- Reuse valid, unaffected evidence. Do not add a duplicate broad `code-review` or full-suite run over the same bundle; required project gates and checks invalidated by later changes still apply.

## Workflow

1. **Establish the snapshot.** Record the bundle, intended behavior, acceptance criteria, relevant files, source/commit and working-tree state. A commit alone does not identify uncommitted changes. Check for source drift before issuing a final verdict; changed areas and their affected contracts need re-review. If a freeze is unavailable, provide explicitly provisional findings and identify what remains to finalize.
2. **Read the relevant evidence.** Inspect the Plan/criteria, ADRs, source, tests, diff, and only the history needed to resolve a question. Verify producer-reported hashes and results when they support acceptance; do not treat the producer's report as independent verification.
3. **Review direction and quality together.** Trace promised behavior, failure/recovery paths, and tests, then assess correctness, types, security/privacy, performance, operations, and maintainability. Use [review-details.md](references/review-details.md) for detailed risk prompts or a larger bundle's evidence tables. Apply only relevant prompts; demand tests for material behavior and invariants rather than tests that mirror every line.
4. **Verify proportionally.** Reproduce important findings with the narrowest safe local check. Inspect a test's side effects before running it; use isolated temporary output where needed. Record the command, exit code, actual result, target source, and useful artifact path or hash. Distinguish Mock, real-model, Live, and external evidence; label unrun or inaccessible checks.
5. **Integrate one verdict.** Deduplicate findings, resolve conflicts against the source of truth or a narrow reproduction, and separate confirmed failures from static risks and unknowns. The lead adjudicates feedback as accepted, deferred, or rejected; a reviewer proposes dispositions rather than claiming the lead's authority.

## Review partitioning

One coherent reviewer pass is enough for a small bundle. When a large surface would benefit from parallel review and delegation is allowed, the main agent assigns complementary primary scopes by module, contract, or risk. Workers do not delegate further.

Each assignment must include the objective, bundle/snapshot, source priority, files to inspect, read-only boundary, forbidden side effects, expected evidence, and verification criteria. Allow limited interface overlap when needed, but avoid duplicate full-bundle passes. Ask reviewers for file/line evidence and concrete failure conditions, then consolidate their results into one verdict.

## Findings and acceptance

- **Critical:** security/privacy breach, authority or data corruption, wrong required result, broken required workflow, or a design contradiction blocking acceptance.
- **Warning:** material edge-case, type, performance, compatibility, or maintainability risk. Explain its impact and whether it blocks this bundle.
- **Suggestion:** bounded improvement that does not block acceptance. Style preferences alone do not justify a blocking finding.

For each Critical or Warning, provide `file:line`, triggering conditions, mechanism and impact, and a reproduction or exact reasoning. Mark unverified concerns as such. Missing evidence for a required gate is an acceptance gap even if no defect has been reproduced.

Use the project's verdict scheme when defined; otherwise:

| Verdict | Required evidence |
|---|---|
| ACCEPT | Required criteria and gates supported; no open Critical or Warning |
| ACCEPT WITH DEFERRED ITEMS | No open Critical or blocking Warning; lead-approved non-blocking deferrals have a reason, owner, and revisit condition |
| REJECT | Open blocking finding or required acceptance evidence missing |

Recommend immediate containment of approval bypasses, unsafe writes, or state corruption; close other blockers before acceptance. This recommendation does not authorize the reviewer to mutate code or production state. A deferred item must explain its remaining acceptance impact.

## Output and evidence ownership

Start with the verdict and reviewed snapshot, then give requirement coverage, prioritized findings, verification actually performed, gaps, and proposed dispositions. Use a compact result for a small bundle; larger reviews can use the reference's tables. Do not claim end-to-end validation from a narrow test or a static reading.

The active Plan owns the bundle boundary, current status, verification, and final disposition. The lead updates its existing rows after adjudication when authorized by the task/project workflow. Keep raw logs separate and link useful evidence. Handoff holds the Plan link, current stage, blockers, and next action; this review does not itself require creating a Handoff or report file.
