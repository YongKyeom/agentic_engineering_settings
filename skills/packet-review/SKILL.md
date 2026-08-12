---
name: packet-review
description: Perform an integrated read-only review of a frozen implementation packet against its active plan and code-quality contracts. Use before starting the next packet to detect direction drift, incomplete work, correctness bugs, type-safety issues, security or performance risks, and maintainability problems. Large packets may use multiple packet-review agents with partitioned scopes, but must not duplicate the packet through a separate broad code-review pass.
---

# Packet Review

Assess both plan alignment and code quality inside the packet-review workflow. A small packet needs one reviewer; a large packet may use several reviewers with explicit, complementary scopes.

## Workflow

1. Identify the active plan and the exact packet boundary.
   - Record the files, intended behavior, acceptance criteria, verification results, and frozen hashes when available.
   - Read only the relevant plan, ADRs, source, tests, `git diff`, and recent history needed to judge that packet.
   - If the packet is still moving, wait for a source freeze instead of reviewing a stale intermediate state.
2. Size the review surface.
   - Use one reviewer when the packet fits comfortably in one coherent pass.
   - For a large packet, split reviewers by disjoint module ownership, contract boundary, or risk area. Examples: core allocation invariants; storage and migration authority; web interaction and accessibility.
   - Give every reviewer the shared packet boundary and source-of-truth priority, plus its exclusive primary scope.
   - Permit small source overlap only where an interface must be checked from both sides. Do not ask multiple reviewers to reread the whole packet independently.
   - Prohibit edits, provider calls, artifact writes, and unrelated exploration.
   - Ask for evidence with file and line references, not a rewrite.
3. Review the packet in one pass across all dimensions below.
4. Reproduce important findings with the narrowest read-only check or targeted test.
5. If several packet reviewers were used, deduplicate their findings and produce one integrated verdict. Conflicting findings must be resolved against the source of truth or reproduced narrowly.
6. Classify each finding as accepted, deferred, or rejected. The main agent owns this decision and integration.

## Review Dimensions

### Direction and completeness

- Does the implementation follow the active plan, ADRs, and latest user decisions?
- Is every promised behavior implemented and directly tested?
- Did the packet introduce unapproved scope, hidden fallback, or a conflicting source of truth?
- Are legacy compatibility, migration, authority, and failure semantics preserved where required?

### Correctness and contracts

- Check edge cases, closed enums, digest and replay binding, transaction or state transitions, ordering, idempotency, and fail-closed behavior.
- Inspect nested validation and `model_construct` or equivalent trust-boundary bypasses.
- Confirm tests assert outcomes and invariants, not merely successful execution.

### Type safety, security, and privacy

- Flag incorrect narrowing, unchecked `Any`, raw exceptions crossing typed boundaries, secret or private data exposure, injection surfaces, and authority escalation.
- Confirm user-controlled content cannot silently become trusted instructions, identifiers, or persisted evidence.

### Performance and operations

- Look for repeated semantic replay, blocking CPU work in async paths, N+1 access, unbounded loops or memory, unnecessary provider calls, and misleading benchmarks.
- Require realistic fixtures for performance or capacity claims.

### Maintainability

- Check dependency direction, SRP, duplicated policy logic, hidden coupling, stale docs, and version ownership.
- Treat size alone as a warning only when responsibilities are actually mixed or defects become hard to isolate.

## Severity

- **Critical**: wrong result, authority or data corruption risk, security/privacy breach, broken required workflow, or a design contradiction that blocks the next packet.
- **Warning**: material edge-case, type, performance, compatibility, or maintainability risk that should normally close in this packet.
- **Suggestion**: bounded improvement that does not block acceptance.

Do not inflate severity for stylistic preferences. Include a minimal reproduction or exact reasoning for every Critical or Warning.

## Output

```markdown
## Integrated Packet Review — <packet>

### Verdict [ACCEPT / ACCEPT WITH DEFERRED ITEMS / REJECT]

### Direction and Completeness
| Requirement | Status | Evidence or gap |
|---|---|---|

### Findings
- C1 ...
- W1 ...
- S1 ...

### Verification
- Commands or read-only reproductions actually run
- Frozen hash or no-drift result

### Disposition
| Finding | Accepted / Deferred / Rejected | Reason and owner |
|---|---|---|

### Must Close Before Next Packet
- [ ] ...
```

An `ACCEPT` verdict requires no open Critical or Warning. Deferred Suggestions must name their later owner or stage.

## Anti-Patterns

- Never run a broad `code-review` after broad packet review of the same source packet. `packet-review` already includes correctness, type, security, performance, and maintainability.
- Never confuse multiple partitioned packet reviewers with duplicated full reviews. Parallel reviewers must have bounded primary scopes and one consolidated verdict.
- Use `code-review` separately only for a small hotfix with no active plan packet, or when the user explicitly asks for that workflow.
- Never review a moving diff and call the result final.
- Never accept producer-reported test output or hashes without an independent no-drift check when quality matters.
- Never widen a review into unrelated dirty-worktree files.
- Never present reviewer output as authority; the main agent must adjudicate it against the source of truth.
- Never rerun the full suite merely to reproduce one localized finding when a focused check can establish it.
