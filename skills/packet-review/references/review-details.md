# Packet review details

Use these prompts when a bundle's contracts or risks need deeper inspection. They are examples, not a requirement to manufacture findings in every category.

## Risk prompts

| Area | Questions and evidence |
|---|---|
| Direction and completeness | Does the implementation follow the latest Plan, ADRs, user decisions, and acceptance criteria? Are promised behaviors implemented and meaningfully tested? Check unapproved scope, hidden fallback, conflicting sources of truth, required legacy compatibility, migration, authority, and failure semantics. |
| Correctness and contracts | Trace edge cases, closed enums, digest/replay binding, transaction and state transitions, ordering, idempotency, and fail-closed requirements where applicable. Inspect nested validation and trust-boundary bypasses such as `model_construct`. Tests should assert outcomes and invariants, not just successful execution. |
| Types, security, and privacy | Check incorrect narrowing, unchecked `Any`, raw exceptions crossing typed boundaries, injection, secret/private-data exposure, and authority escalation. User-controlled content must not silently become trusted instructions, identifiers, or persisted evidence. Apply the project's actual trust model. |
| Performance and operations | Inspect repeated semantic replay, CPU work blocking async paths, N+1 access, unbounded loops/memory, unnecessary provider calls, and misleading benchmarks. Capacity claims need representative fixtures and measurements; identify unmeasured claims rather than inventing numbers. |
| Maintainability | Check dependency direction, mixed responsibilities, duplicated policy, hidden coupling, stale docs, and version ownership. Size is evidence only when it obscures responsibilities or makes defects hard to isolate. |

## Evidence tables

Use only the tables needed to make the verdict reviewable. Retain the required snapshot, uncertainty, and acceptance information even in a shorter response.

```markdown
## Integrated Packet Review — <bundle>

Verdict: <ACCEPT / ACCEPT WITH DEFERRED ITEMS / REJECT>
Snapshot: <commit plus working-tree identity or other source fingerprint>
Scope: <included behavior and files; exclusions>

| Requirement | Met / Gap / Unverified | Evidence |
|---|---|---|

| ID / Severity | File:line | Trigger, mechanism, and impact | Reproduction or reasoning | Proposed action |
|---|---|---|---|---|

| Check | Source / environment | Command and exit code | Actual result / artifact | Limits |
|---|---|---|---|---|

| Finding | Accepted / Deferred / Rejected | Reason and acceptance impact | Owner | Deadline or revisit condition |
|---|---|---|---|---|
```

Clearly identify proposed dispositions awaiting the lead's decision. A rejected finding needs a source-based reason; a deferred material risk needs an owner and revisit condition. Reuse earlier evidence only after checking its source and affected behavior remain applicable.
