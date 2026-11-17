---
name: lesson-learned
description: Extract practical engineering lessons from actual code changes, debugging events, or supplied evidence. Use for requests to reflect on recent work, identify a recurring mistake, or explain what to carry forward. Ground each lesson in the event; routine small fixes do not require a retrospective.
---

# Lesson Learned

Explain what a specific piece of work teaches, the evidence behind it, and when the lesson applies again. Recognize useful decisions as well as mistakes. Keep the reflection proportional to the event; a typo or straightforward config fix may have no broader lesson.

## Bound the evidence

Use the user's requested commit, range, working changes, debugging event, or supplied notes first. Infer a useful scope from the active task when it is clear; state the selected boundary. Ask only when choosing between unrelated events would change the answer.

When Git is relevant, inspect the repository's actual state and integration branch. Do not assume the default branch is `main`, use a fixed history depth, or analyze every change on a feature branch when the request concerns one fix. Git is unnecessary when the supplied diff, logs, or conversation already establish the event.

Examples below use RTK when available; use the project's available Git runner otherwise:

| Evidence needed | Example |
|---|---|
| Working changes | `rtk git status --short`, `rtk git diff`, `rtk git diff --cached` |
| Named commit | `rtk git show <revision>` |
| Explicit range | `rtk git log <from>..<to> --oneline`, `rtk git diff <from>..<to>` |
| Feature relative to its verified base | `rtk git log <base>..HEAD --oneline`, `rtk git diff <base>...HEAD` |

Read relevant messages for intent and the diff or event evidence for what changed. Messages alone do not prove the cause, successful behavior, or benefit. For a large scope, start with a summary such as `rtk git diff --stat <from>..<to>` and inspect the files tied to the event, rather than selecting only the largest files. Follow a caller, contract, or test outside the diff when it is necessary to establish the claim; avoid an unrelated repository audit.

## Derive the lesson

- Establish the concrete sequence: observed problem or decision → supported cause or constraint → change → observed result. Mark unknown steps instead of filling them in.
- Distinguish an observed result from a plausible interpretation or a proposed improvement. A changed assertion, a green test report, or a new abstraction is not by itself proof that the underlying problem was solved.
- Choose the most useful lesson supported by the evidence. Add others only when they explain distinct, consequential observations. Do not meet a lesson quota or force a named principle onto an ordinary change.
- State the conditions under which the takeaway applies, including a meaningful tradeoff or exception. A local incident should not become a universal ban or mandatory process.
- Attach each substantive claim to a file and relevant lines, commit, log excerpt, or supplied event. If the evidence cannot support a broader lesson, say what can be concluded and what remains unknown.

References are optional lookup aids:

- Use [se-principles.md](references/se-principles.md) when a named engineering principle clarifies an observed pattern.
- Use [anti-patterns.md](references/anti-patterns.md) when explaining a concrete design problem. Its signals are hypotheses to check, not diagnoses based on line counts, file counts, or class shape.

## Present and preserve scope

Lead with the useful takeaway, then connect the specific event, its evidence, and its consequence. A compact structure can be:

> **Lesson:** Keep validation at the boundary shared by all supported callers.
>
> **Evidence:** `<file:line or event>` shows `<observed change/result>`.
>
> **Why:** `<supported mechanism and relevant limit>`.
>
> **Next time:** `<one action for a similar condition>`.

Adapt the structure to the user's requested format and language. Avoid blame, forced praise, and advice disconnected from the work. Do not claim a performance, security, or reliability improvement without evidence for that claim.

Default to an answer in the conversation. Reflection does not authorize code edits, a new ADR/Plan/Handoff, unrelated instruction changes, commits, or external sharing. Save a lesson to a requested destination or update an existing authorized project record when asked. Persistent memory updates require an explicit user request and must follow the environment's memory rules; never update them automatically after a fix. Do not start another interview or repeat a retrospective simply because a small follow-up edit was made.
