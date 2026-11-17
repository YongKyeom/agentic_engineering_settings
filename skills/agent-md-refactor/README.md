# Agent MD Refactor

Reorganize agent instructions so essential rules remain available and detailed guidance is easy to discover. The operating instructions are in [SKILL.md](SKILL.md).

Use this skill for restructuring or deduplicating `AGENTS.md`, `CLAUDE.md`, and similar instruction files. Handle a narrow correction directly. Root length alone does not determine whether a refactor is useful.

The workflow checks the requested scope, instruction precedence, document ownership, and the consuming agents' loading behavior. It resolves conflicts from existing authority before asking the user about any remaining material ambiguity.

The root retains project context, authority boundaries, required execution summaries, and triggers for reading detailed rules. Detail can move into existing documents or correctly scoped instruction files. A Markdown link provides a route to a document; its presence does not prove that the agent loads it automatically.

Preserve substantive rules by tracking their destination and treatment. Merge duplication only after comparing scope, conditions, exceptions, and strength. Remove a rule only with evidence and within the authorized scope; familiar wording or normal model behavior does not make a user requirement disposable.

Examples:

- **A project requires Python, Git, verification, and delegation summaries in its root.** Preserve those summaries and move only the supporting detail.
- **A parent rule and a scoped rule differ.** Apply the established precedence and retain the relevant scope; ask only if an unresolved choice affects behavior.
- **Several agents share the repository.** Check their actual instruction discovery before choosing links, imports, or scoped files.

Completion means the semantic obligations are preserved, required rules are encountered before the actions they govern, and affected links work for their intended readers. Validate tracked references against a fresh checkout's available files. Report justified removals and remaining uncertainty alongside the changed paths.

The refactor stays within the requested repository files. Editing installed or global agent configuration requires separate authorization.

## Attribution and license

Inspired by [Matt Pocock's prompt idea](https://x.com/mattpocockuk/status/2012906065856270504). License: MIT.
