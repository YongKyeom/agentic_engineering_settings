---
name: agent-md-refactor
description: Reorganize AGENTS.md, CLAUDE.md, or similar agent instructions for progressive disclosure while preserving authority, essential root rules, and task discovery. Use when instruction files need restructuring or deduplication; handle narrow wording edits directly.
license: MIT
---

# Agent MD Refactor

Make instructions easier to find and apply without changing their meaning or the user's conventions. Keep executable baseline summaries in the root and move detail only when agents can reliably discover it.

## Establish scope and authority

Inspect the requested files, their callers and links, applicable parent and scoped instruction files, and the project's document rules. Preserve unrelated working-tree changes. Reorganizing repository files does not authorize edits to installed or global agent configuration.

Determine which agents consume the files and how they load instructions in this environment. Distinguish automatic root or ancestor loading, scoped `AGENTS.md` rules, linked Markdown references, and agent-specific imports. Do not assume that a link automatically loads its target or that different agents share discovery behavior. Verify uncertain behavior from available authoritative documentation when it affects the proposed move.

Resolve apparent conflicts using applicable instruction precedence and existing sources of truth. Preserve intentional conditions and exceptions. Ask the user only when a material ambiguity remains after that analysis; continue independent restructuring when possible.

## Decide what stays at the root

Keep enough information in the root for an agent to obey essential rules before opening another file:

- Project purpose, source-of-truth order, and relevant work areas.
- Required authority, safety, user conventions, and execution boundaries.
- Essential coding, verification, Git, and delegation summaries when the project requires them.
- Clear routing to detailed rules, stating when they must be read.

Preserve any baseline sections the project requires unchanged. A rule need not apply to every task to warrant a root summary: it may govern the next tool call or tell the agent which detail to read. Do not optimize for a fixed line count.

Project instructions may deliberately repeat global guidance or skill essentials. Preserve the required operational rules and apply the relevant skills to carry them out; do not replace the actual obligations with skill names or personal paths merely to reduce duplication. This differs from duplicating the changing status of a task in several documents.

Move lengthy procedures, examples, and topic-specific detail to existing appropriate documents where possible. Use a scoped `AGENTS.md` only when its scope matches the rule and the intended agent will load it for the relevant work. For cross-cutting rules, retain a root summary and reading trigger instead of relying on subtree discovery.

Choose file boundaries from actual responsibilities and lookup needs. Preserve the established directory layout and language; do not create a sample hierarchy or translate instructions just to match this skill.

## Preserve coverage during restructuring

Track each substantive instruction or coherent rule group through the change. A compact mapping can use:

| Original rule or section | Destination | Treatment and reason |
|---|---|---|
| Existing section identifier | Root summary plus detailed section | Preserved, moved, merged, or removed with evidence |

Keep this mapping in the task's existing working record when needed; a small edit can report it in the response. Do not create a separate report by default.

Merge duplicates only after comparing their conditions, exceptions, force, and scope. Preserve the strongest applicable obligation without broadening it. A familiar or “obvious” rule may encode a deliberate user requirement, authority boundary, or safety constraint; that is not a deletion reason.

Remove instructions only when the requested scope permits it and evidence establishes that they are obsolete, fully duplicated, or intentionally superseded. Preserve ambiguous rules and flag the issue rather than silently deleting them. Do not remove safety rules merely because the model usually follows them.

Update affected links and callers with each move. Tracked documents must refer to destinations available to a fresh checkout; keep local Plan or Handoff references within their permitted local context. Preserve existing Plan, Handoff, and ADR ownership instead of copying their changing state into the root.

## Verify the resulting instructions

Compare the semantic before and after content, including conditions, exceptions, authority, and language. Confirm that every preserved obligation has a usable destination and that intended removals have a reason. Check local links, anchors, and tracked-file availability where applicable.

Walk through representative tasks against the new structure: a small fix, a feature requiring detailed rules, and a task near an authority or scope boundary. Verify that the agent encounters each required rule before the action it governs. Inspect affected Markdown rendering when tables or diagrams change.

Report the changed files, preserved root responsibilities, justified removals, verification performed, and any uncertain loading behavior. A shorter root alone is not evidence of a successful refactor.
