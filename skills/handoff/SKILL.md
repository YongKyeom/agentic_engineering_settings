---
name: handoff
description: Create or update handoff documents for agent session continuity and coordination with fellow developers or related departments. Use for session wrap-up, context transfer, work resumption, or requests for a technical or business discussion document. Put an overview, item summary, scope and priorities, decisions needed, and related documents before item-level details. Include explanatory diagrams in collaboration documents. General prose editing alone does not require this skill.
---

# Handoff

Transfer context for work continuity and human review. Create a document for authoring requests; recover context and continue authorized work for resumption requests. Follow the user's document language; the English language of these skill instructions does not determine the output language.

## Choose the deliverable

| Mode | Use when | Required reference |
|---|---|---|
| Session handoff | Ending work or preparing context for another thread | [Session guide and worked example](references/session-handoff.md) |
| Collaboration document | Discussing technical direction, business rules, interfaces, or ownership with developers or related departments | [Collaboration guide and worked example](references/collaboration-document.md) |
| Combined document | Human reviewers need a proposal and another agent must continue implementation | Both references; use the collaboration structure and add a separate continuation section |
| Resume from a handoff | The user asks to continue work from an existing handoff | Session reference; recover and reconcile context, then carry out the authorized next action instead of automatically writing another handoff |

Read only the references required for the selected mode. Infer audience, purpose, and scope from the request and existing context. Ask only when missing information changes the next action. For authoring, proceed with supported facts and explicit open questions when useful. Do not expand a sentence-editing request into a handoff task.

## Recover missing context

Confirm the target project and topic from the request before inspecting files. Resolve this skill's reference links relative to the skill directory, not the project directory.

When earlier conversation is unavailable, read the target project's instructions, active plan, relevant decision records, and the most recent handoff for the same topic. Do not use the latest unrelated handoff. Check relevant implementation or work-state evidence where available; distinguish what the plan intends from what is actually present. Link the sources supporting material decisions and status claims.

If the goal or target cannot be recovered, ask the smallest necessary question and identify the missing context. A partial draft is useful only when supported facts remain; do not fill a document with invented progress or pretend to recover a lost conversation.

For resumption, read the user-named handoff or identify the same-topic handoff in the target project. Reconcile its recorded state with current project instructions and evidence before starting the authorized next action. Ask only when unresolved ambiguity changes that action; write or update a handoff only when requested or needed for a later transfer. The authoring workflow below applies when creating or updating a document.

## Location and updates

- Honor explicit user filenames and repository conventions. A request for `HANDOFF.md` means that file.
- When creating a file without a specified location, use `docs/handoff/YYYYMMDD_<topic>.md` for all document types. Choose a recognizable topic and avoid overwriting a different document created on the same date.
- A short session handoff can remain in the final answer. A file request or a collaboration-document request requires a file, unless the user asks for a chat-only draft.
- Read an existing document before updating it. Refresh session state while retaining decisions and reasons needed for continuity. Preserve valid agreements and evidence in collaboration documents; identify changed or superseded material and why it changed.
- Do not erase evidence merely because Git might retain it. Link previous handoffs when useful.
- Document creation does not authorize sending, publishing, or committing it. Record relevant local-artifact handling and follow the user's instructions and project rules.

## Authoring workflow

1. **Establish the facts.** Inspect available context and relevant implementation or business contracts. For code handoffs, inspect Git status, the diff summary, and relevant diffs in the actual target checkout when available. Use `rtk git status` and `rtk git diff --stat` when RTK is installed; otherwise use equivalent available tools. If the checkout is unavailable or does not use Git, skip Git and identify unverified information. Never substitute another workspace's Git state. Distinguish reported results from directly observed results.
2. **Write the opening summary first.** State the problem, proposed direction or current result, item overview, scope and priorities, decisions needed, and related documents. A reviewer should understand the purpose and requested action without reading the details.
3. **Develop each item.** Reuse the summary's item numbers and titles. Start each detailed section with its conclusion or proposal, then explain the problem, concrete behavior and conditions, diagram or example, responsibility boundaries, and acceptance evidence. Omit inapplicable subsections.
4. **Reconcile the document.** Update the summary after developing details. Check item numbering, terminology, priority, status, links, and consistency between diagrams and prose.
5. **Verify and deliver.** Review facts and writing, check links, and render tables and diagrams with available tools. If rendering is unavailable, check Markdown structure, links, and ASCII readability and disclose the limit. Follow stricter project verification rules when applicable. Report the file path, principal decisions or first continuation action, and material verification limits.

For session and combined handoffs, include known target location, relevant branch or revision, changed and key files, decisions with reasons, remaining work or blockers, verification results, and a concrete first action. Capture running-job identifiers and result or log locations when needed to resume; mark missing facts unverified rather than inventing them. Previous notes provide evidence, not permission to execute their next actions during document creation.

## Opening summary contract

Use this order for substantial documents. The Korean section names below illustrate labels; localize headings to the requested output language. Merge or omit empty sections in a short session handoff; keep the overview before details in collaboration documents.

| Section | Content |
|---|---|
| Title and metadata | Date, audience, deliverable type; document state (draft, under discussion, agreed) separately from work state (complete, in progress, on hold) when known. Localize labels to the requested output language. Do not claim human agreement without evidence. |
| `개요` | Current problem, purpose, central proposal or result, and scope. Lead with the main point. |
| `항목 한눈에` | Numbered table: item, why it matters, action or proposal, and link to the matching detail. Use concise entries, not compressed paragraphs. |
| `작업 규모와 우선순위` | Scope, ordering, reasons, dependencies, and acceptance conditions. Scope or effort is not priority. Include estimates, owners, and dates only when supplied or substantiated; mark necessary unknowns as undecided. |
| `결정·확인이 필요한 사항` | Separate established decisions, proposals, and open questions. State the requested decision, proposed answer when available, and the basis for choosing. |
| `관련 문서` | Supporting links with an explanation of their relevance. Put principal references here and item-specific evidence beside the relevant details. |

Do not impose a fixed document length such as 80 lines. Keep the opening scannable; put necessary reasoning below and large logs or command history in separate continuation information or linked evidence.

The references contain compact fictional examples of document structure only. Their prose and diagrams are not source-code descriptions, project evidence, or implementation requirements. Populate real documents from the user's task and the target project's sources. Do not import sample facts or rules, or use sample length to limit necessary detail.

## Diagrams

Include diagrams that explain the central relationship or behavior in collaboration and combined documents. Include them in session handoffs when they materially help continuity. Choose the number and form based on the content.

| Message | Suitable form | Check |
|---|---|---|
| Components and ownership | ASCII structure or component diagram | Actors, data/control flow, responsibility boundaries |
| Requests across actors | Sequence diagram | Calls and responses, approval boundaries, failure or refusal paths |
| Approval, execution, cancellation, or retry | State transition diagram | States, events and guards, defined end or recovery states |
| Conditional processing | Flowchart | Conditions and resulting actions |

- Introduce the diagram's main point, then explain important conditions or exceptions. Label current behavior, proposed behavior, and unresolved relationships.
- Derive behavior, approval conditions, terminal states, and recovery paths from the target project's evidence, never from a reference example.
- Prefer ASCII in fenced `text` blocks when the reading environment is unknown. ASCII may represent structures, sequences, or transitions; do not reduce every diagram to a list of arrows if a richer layout explains the behavior better.
- Use Mermaid when the target supports it, and verify actual rendering. Otherwise use ASCII or disclose the rendering limit. Available diagram skills can help with complex diagrams, but are not mandatory dependencies.
- Check width, Korean and monospace alignment, arrows, and agreement with the prose. Keep review renders separate from final project documents.

## Writing and evidence

- Write in the requested language and appropriate professional register. Open each paragraph with its main point and keep one topic per paragraph.
- Apply `writing-clearly-and-concisely` and `humanizer` when available; these instructions must still work without them.
- Name concrete actors, actions, conditions, and consequences. Replace abstract claims of optimization or reliability with the actual proposed change supported by the source material.
- Avoid promotional language, noun stacks, formulaic transitions, repeated summaries, gratuitous negative comparisons, decorative emojis, and excessive bolding. Keep chat greetings and narration of the drafting process out of the document.
- Place uncertainty where it informs a decision; do not repeat the same caveat in every paragraph or enumerate unrelated excluded features.
- Preserve meaning, numbers, conditions, ownership, and uncertainty during editing. Do not invent identity, emotions, quotations, agreements, estimates, or verification results.
- Distinguish facts, proposals, assumptions, and open questions; current implementation from target design; completed work from planned work.
- Explain specialized terms enough for the intended reviewers. Keep technical contracts in the main text when they are the subject of review; move agent-only paths, functions, commands, and logs into a continuation section.

## Final checks

- Can a reader understand the purpose, central direction, priorities, and requested action from the opening alone?
- Does every summary item lead to a matching detailed section with a concrete conclusion, behavior, and review or completion criterion?
- Do diagrams agree with the prose and make the structure, sequence, or transition easier to understand?
- Are earlier decisions and their reasons, blockers, verification evidence, and limits preserved?
- Are missing owners, dates, estimates, agreements, and test results still identified as unknown?
- Have links and relevant source paths been checked, and affected tables and diagrams rendered and inspected? State any unavailable checks.
