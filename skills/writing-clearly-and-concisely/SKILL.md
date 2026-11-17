---
name: writing-clearly-and-concisely
description: Draft or edit documentation, explanations, reports, commit messages, and UI text for clarity and concision. Use when wording, structure, or readability needs attention while preserving the full meaning and intended register. For a focused request to remove formulaic AI-style phrasing, use humanizer instead.
---

# Writing Clearly and Concisely

Make the reader's task easier while preserving what the author means. Clarity can require an extra sentence; brevity is useful only when it preserves necessary information.

## Editing decisions

- Lead with the point the reader needs, then supply its reasons, evidence, or next action. Keep related claims, conditions, and qualifications together.
- Remove repetition and empty framing. Keep details that explain a decision, define scope, distinguish alternatives, or support a claim.
- Prefer familiar, concrete language and consistent terms. Use technical vocabulary when it carries needed precision; explain it for the intended audience rather than replacing it with a looser synonym.
- Prefer an explicit actor when known and useful. Passive voice is appropriate when the actor is unknown, irrelevant, or deliberately outside the sentence's focus.
- Use paragraphs for connected reasoning, lists for parallel or sequential items, and tables for comparisons. Follow the requested format and the destination's conventions.

When editing, preserve facts, numbers, units, names, citations, attribution, conditions, exceptions, negation, obligation, uncertainty, and time boundaries. Do not invent a cause or example to make a vague sentence sound specific. Keep “may,” “must,” and “has not been shown” distinct from stronger claims. Preserve quotations unless the user asks to edit them.

Match the author's language, register, and voice. In Korean, preserve 높임말, sentence endings, and established technical terms; reduce translationese such as unnecessary nominalizations or repeated “~에 대한.” Do not impose English article, comma, or word-order rules on Korean.

For example:

| Input | Clearer wording |
| --- | --- |
| 이 기능의 사용을 위해서는 먼저 로그인을 진행해 주셔야 합니다. | 이 기능을 사용하려면 먼저 로그인하셔야 합니다. |
| 일부 환경에서는 오류가 발생할 가능성이 있을 수 있습니다. | 일부 환경에서는 오류가 발생할 수 있습니다. |
| The API might potentially return an error in certain situations. | The API may return an error in some situations. |

“효과가 입증되지 않았다” must retain the lack of evidence; “효과가 없다” asserts something different. A concise edit must preserve that difference.

## Scope and output

Handle an ordinary edit directly using the supplied context. Ask only when an unresolved ambiguity materially changes the result; otherwise retain the ambiguity or original wording. A short edit normally needs only the revised text. Add explanations or alternatives when requested or when a consequential ambiguity needs to be visible.

For drafting, distinguish supplied facts from proposed content and keep unsupported details out of factual prose. A request to polish language does not require research, delegation, or a broader rewrite. Keep any file changes within the requested target.

`humanizer` can complement this skill when formulaic phrasing is also a concrete problem; neither skill requires loading the other.

## Optional references

Ordinary drafting and copyediting need no reference loading. These files preserve historical English guidance from William Strunk Jr.'s *The Elements of Style* (1918), rather than a current universal style standard. Consult only the relevant passage when the user asks about these principles or a specific English usage question; current audience, publication conventions, and meaning preservation take priority.

- Historical overview: [Introduction](elements-of-style/01-introductory.md).
- English grammar and punctuation: [Rules of usage](elements-of-style/02-elementary-rules-of-usage.md).
- Paragraphs, voice, modifiers, and concision: [Composition principles](elements-of-style/03-elementary-principles-of-composition.md).
- Historical quotation, reference, and title conventions: [Matters of form](elements-of-style/04-a-few-matters-of-form.md).
- Historical English word choices: [Words and expressions](elements-of-style/05-words-and-expressions-commonly-misused.md). Several prescriptions are dated; read the editorial notes before applying them.

For a request specifically about Wikipedia's AI-writing indicators, [Signs of AI writing](signs-of-ai-writing.md) is an archived descriptive field guide. Its Wikipedia-specific observations are not editing rules or proof of authorship. It is unnecessary for ordinary prose editing.

## Credits

Adapted from @joshuadavidthomas's [agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT) and [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style). Historical writing principles: William Strunk Jr. (1918). AI-writing source: Wikipedia's field guide, retained with its source links.
