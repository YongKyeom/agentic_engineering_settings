---
name: humanizer
description: Edit existing prose to remove formulaic, inflated, or translation-like AI-style phrasing while preserving meaning and the author's voice. Use when the user asks to humanize text, remove AI tone, or make Korean or English writing sound natural. For general drafting or document structure, use writing-clearly-and-concisely instead; this skill does not determine whether an author used AI.
---

# Humanizer

Edit the phrasing that makes the supplied text sound formulaic. Keep the author's point, evidence, and voice; natural writing need not be casual, opinionated, or personal.

## Preserve before polishing

- Preserve every necessary claim, condition, exception, negation, number, unit, name, citation, attribution, time boundary, and degree of certainty or obligation.
- Do not invent facts, sources, causes, features, feedback, experiences, feelings, opinions, or first-person narration. Replace vague phrasing with specifics only when those specifics are in the supplied context. Otherwise keep the uncertainty or narrow the edit to wording.
- Match the existing authorial voice, genre, language, and intended audience. Neutral scientific reporting, legal precision, and a reserved personal voice can all sound natural.
- Preserve quotations and required terminology. Keep meaningful contrast and qualifications even when they resemble a listed pattern. “입증되지 않았다” does not mean “없다”; “원칙적으로 금지하되 사전 동의 시 허용한다” must retain its exception.

## What to change

Look for empty importance claims, promotional adjectives, unsupported commentary, vague authority, repetitive sentence templates, filler, forced contrasts, and mechanical formatting. Change them when they obscure the point or mismatch the intended tone.

Treat patterns as clues for editorial judgment, not word bans or evidence of AI authorship. A real three-item list, an em dash, a heading, or a technical word can be the clearest choice. Remove empty hedging while retaining uncertainty supported by the source. Keep useful structure and the destination's typography conventions.

For Korean, preserve 높임말 and sentence endings. Reduce translationese, heavy nominalizations, repeated “~에 대한,” and empty phrases such as “중요한 역할을 수행합니다” only where a direct expression preserves the substance. Do not force slang, 반말, humor, or an invented personal reaction.

| Input | Revision |
| --- | --- |
| 이 설정은 알림을 끄는 역할을 수행합니다. | 이 설정은 알림을 끕니다. |
| 이번 결과는 일부 조건에서 성능이 개선될 가능성이 있을 수 있음을 시사합니다. | 이번 결과는 일부 조건에서 성능이 개선될 가능성을 시사합니다. |
| 솔직히 이번 결과는 좀 아쉽다. 그렇다고 실험이 의미 없었다는 건 아니다. | 솔직히 이번 결과는 좀 아쉽다. 그렇다고 실험에 의미가 없었다는 뜻은 아니다. |
| The update provides the ability to work offline. | The update enables offline work. |

The personal example preserves a feeling already present in the input; it is not permission to add one to neutral prose.

## Working scope and output

For an ordinary edit, revise directly and compare the result with the input for lost or strengthened meaning. If a supposed improvement changes the claim or erases intentional voice, keep the original phrasing. Ask only when missing context materially affects the result and cannot reasonably be inferred; do not add a questionnaire, delegation, or research to a simple edit.

Return the revised text in the requested format. For a short edit, the text alone is usually sufficient. Include a brief explanation or alternatives when requested or when a consequential ambiguity needs to be surfaced. Do not automatically append a change log or offer more work.

For longer or stubbornly formulaic drafts, consult the relevant section of [Pattern decisions](references/pattern-decisions.md): [inflation and attribution](references/pattern-decisions.md#inflation-and-attribution), [wording and rhythm](references/pattern-decisions.md#wording-and-rhythm), or [formatting and chatbot artifacts](references/pattern-decisions.md#formatting-and-chatbot-artifacts). Short edits need no reference loading.

General document structure and new drafting belong to `writing-clearly-and-concisely`; use it only if that broader task is also requested or needed. Neither skill requires loading the other.

## Source and credit

Adapted from @blader's [humanizer](https://github.com/blader/humanizer) (MIT), informed by [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). That guide describes observations in Wikipedia content, not universal style rules or a reliable authorship test. Its indicators are used here only where they improve the supplied prose.
