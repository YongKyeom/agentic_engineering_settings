---
name: karpathy-guidelines
description: Coding judgment for implementation, debugging, refactoring, and review. Use to trace affected behavior, reuse existing solutions, keep changes complete and focused, and verify the requested outcome.
license: MIT
---

# Karpathy + Ponytail Coding Guidelines

**Complete the requested behavior; minimize the complexity needed to deliver it.** Never use simplicity, a small diff, or token savings to justify missing requirements, skipped investigation, or inadequate verification. User instructions and project contracts set the quality bar. Scale the work to its impact.
For reviews, apply these criteria within the requested read/write scope.

## 1. Understand the Outcome and Scope

- Read the relevant project instructions, contracts, and implementation before choosing a solution. Define an observable success criterion.
- For multi-step work, give a short plan that pairs each outcome with its check. Keep trivial tasks lightweight.
- Trace the paths the change affects: callers, tests, fixtures, configuration, and exports as relevant. Include compatibility and data effects in the scope.
- Resolve uncertainty from evidence first. State consequential, reversible assumptions and proceed when safe. Ask when unresolved ambiguity changes required behavior or makes proceeding unsafe.
- When evidence contradicts an assumption, recheck it and adjust the solution before adding workarounds.
- For vague requests, establish the core outcome without silently dropping requested capabilities. Explain tradeoffs when a simpler approach changes the outcome.

## 2. Choose the Simplest Complete Solution

First check whether the requested outcome already works without a code change. If it does, show the evidence. Otherwise, take the first option that meets the requirements and project contracts:

1. Reuse an existing helper, component, service, or pattern in the codebase.
2. Use a standard library or platform feature when the project has no established equivalent.
3. Use a suitable dependency already installed in the project.
4. Write the smallest clear implementation needed to close the remaining gap.

- Add abstractions, wrappers, options, or configuration only when current requirements or project contracts justify them.
- Avoid redundant conversions and boilerplate. Keep values in the form expected by the platform or project boundary unless conversion serves a concrete requirement.
- Before adding a dependency, weigh its reliability and maintenance benefits against its cost, especially for a small amount of code.
- Prefer code a reader understands directly. Line count and diff size do not justify obscure expressions or incomplete behavior.
- Among similarly simple solutions, prefer the one correct for relevant boundary cases. Do not invent unsupported scenarios to justify extra machinery.

## 3. Make a Focused, Complete Change

- Complete the affected paths identified during scoping. A small patch that leaves a broken integration is incomplete.
- For bug fixes, inspect affected callers and address the cause at the appropriate boundary; verify that callers sharing that code still behave correctly.
- Preserve the project's layers, interfaces, typing, documentation, and formatting conventions. Avoid unrelated cleanup, renaming, reformatting, or speculative features.
- Remove imports, variables, and helpers made unused by your change. Leave unrelated pre-existing dead code alone; report it only when consequential.
- Before finalizing, inspect your diff: every changed line must serve the requested outcome or its required verification. Simplify avoidable complexity introduced by your change without weakening behavior.
- Preserve validation at trust boundaries, data-loss safeguards, security, accessibility, and required error handling when simplifying or moving code.
- Handle realistic failure modes; add defensive code only for conditions supported by the contract or evidence.
- For a deliberate shortcut within the agreed requirements, record its limit and concrete revisit trigger near the implementation or in the project's designated record. Do not disguise an unmet requirement as a shortcut.

## 4. Verify the Requested Outcome

- Choose the narrowest meaningful checks for the success criterion and affected behavior. Follow required project gates.
- Reuse suitable tests. Add or update focused tests when existing coverage does not establish the changed behavior or reproduce the bug.
- For reproducible bugs, confirm a regression check fails for the expected reason before editing and passes after the fix. If reproduction is blocked, state the evidence and validation limits. For refactoring, compare relevant behavior before and after, reusing valid baseline evidence.
- Match verification to the artifact: trivial text or formatting changes usually need inspection rather than new code tests. A successful build alone may not establish a behavioral contract.
- Confirm the requested outcome as well as passing checks. Report blocked or unrun checks accurately; do not imply they passed.
- If checks fail, investigate the failure and revisit assumptions. Do not weaken assertions or remove required validation merely to obtain a passing result.
- Broaden or repeat checks when failures, further changes, or unresolved impact justify it. Reuse still-valid evidence.

## 5. Communicate Decisions and Evidence

- Share consequential assumptions, tradeoffs, and blockers while work can still be adjusted.
- Report what changed and how the outcome was verified. Mention material limitations or unchecked behavior when they affect confidence or next steps.

Adapted from [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md), inspired by [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876), and [Ponytail](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md).
