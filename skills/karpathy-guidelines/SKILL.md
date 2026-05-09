---
name: karpathy-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.

## 3. Surgical Changes

**Modify only what needs to change. Leave the rest alone.**

- Change one thing at a time. If multiple changes are needed, do them sequentially and separately.
- Don't refactor "while you're at it."
- Don't rename variables unless the change requires it.
- Don't reformat code unless fixing bugs or required by linting.

## 4. Surface Assumptions

**Make what you're assuming explicit.**

- "I'm assuming X" before diving into implementation.
- If assumptions break, update understanding and adjust.
- When something unexpected happens, look at your assumptions first.

## 5. Define Success Criteria

**Before coding: What does done look like? How will we verify?**

- "Done" is not: "It compiles" or "It runs."
- "Done" is: A passing test. A metric improving. A user need satisfied.
- Specify criteria upfront. Check them before claiming victory.

## 6. Test Before Declaring Done

**If it passes its tests, it's done. Not before.**

- Write or update tests that directly validate success criteria.
- Don't skip testing because "it looks right."
- Don't claim done until tests pass.

## 7. Ask for Feedback Early

**Show work in progress. Get unstuck faster.**

- Share assumptions, approach, intermediate results.
- If stuck, raise the problem immediately.
- Don't silently struggle or overengineer.
