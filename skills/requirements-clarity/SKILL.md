---
name: requirements-clarity
description: Resolve requirements whose missing scope, behavior, or acceptance decisions would materially change implementation. Use for ambiguous feature requests or unresolved product contracts; handle clear fixes directly without a clarification ceremony.
---

# Requirements Clarity

Turn uncertainty into enough shared understanding to perform the user's task. Preserve the requested product, constraints, and authorized scope.

## Establish what is already known

Read the current request and relevant existing context before asking questions: project instructions, active Plan or Handoff, requirements, related code, tests, and integration contracts. Use the project's source-of-truth order to resolve differences. Inspect only the context needed for this request.

Separate:

- Confirmed requirements and constraints, with their source.
- Reversible implementation choices that can follow existing conventions.
- Missing user or external-owner decisions that would change behavior, scope, authority, or acceptance.

A file path, code snippet, or named function does not prove the requirements are clear. Complexity alone does not justify more questions. If the task is already actionable, proceed with the requested work.

## Clarify decisions that affect the work

Use these as reasoning lenses, rather than questions the user must always answer:

- **Why?** Identify the problem and intended outcome; do not invent business metrics or challenge an already settled need.
- **Simpler?** Check whether existing behavior or a smaller change satisfies the request. Preserve explicit user choices when considering alternatives.

Ask only when a missing answer would materially change the work and cannot reasonably be inferred or found in available sources. Explain the decision and its consequence briefly. Offer concrete options when useful; ask the smallest useful set of questions instead of working through a fixed questionnaire.

For example, before adding an approval action, determine who may approve and what state changes. Styling details can usually follow the existing interface. A request to fix a clear validation error can proceed using the reproduction and existing contract.

Keep dependent work pending when an essential decision is unanswered. Continue independent inspection or implementation within the authorized scope. For reversible choices, state the assumption and proceed; do not treat silence as approval or invent external business rules.

## Record enough to implement and verify

Scale the result to the task:

| Task | Useful result |
|---|---|
| Clear small fix | Brief scope and observable completion criterion, then implementation |
| Feature with a few decisions | Confirmed behavior, relevant constraints, acceptance examples, and remaining blockers |
| Requested specification or sustained project work | Update the existing specification or Plan with the settled contract and open decisions |

Follow the project's document locations, language, and ownership rules. Keep detailed specifications and current state in their existing source of truth. A Handoff should point to the Plan when the Plan owns those details; do not create a separate PRD or Handoff merely because this skill was invoked.

When a detailed specification is useful, include only relevant material:

- Problem, intended users, scope, and explicit exclusions.
- Inputs, outputs, state changes, permissions, and integration boundaries.
- Failure or recovery behavior that affects acceptance.
- Observable acceptance examples, including meaningful boundary cases.
- Unresolved decisions, their owner, and which work they block.

Distinguish confirmed requirements from assumptions and proposals. Do not fill a template with invented versions, estimates, metrics, architecture choices, or deployment phases. Use the tools available in the current environment.

## Proceed when the task is actionable

Continue once the goal, affected behavior, applicable constraints, and completion criteria are clear enough for the next authorized step. Open decisions may remain if their dependent work is identified and kept pending.

Do not gate progress on a numeric clarity score, a number of clarification rounds, a complete PRD template, or repeated confirmation of decisions already settled. Report what was resolved, material assumptions, and any remaining blocker in the user's requested language.
