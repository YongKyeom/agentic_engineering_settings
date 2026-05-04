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

Classify review feedback before acting on it:

- `accepted`: Apply or address now.
- `deferred`: Valid, but outside current scope.
- `rejected`: Conflicts with instructions, source of truth, or verified data.

Keep rejected feedback when the reason affects future work.

## Handoff

Use `docs/handoff/` when:

- Context is long.
- Work must continue in another session.
- Another agent or human needs current state.
- Important commands, decisions, or risks should not be lost.
