# Mermaid Diagrams

Create and edit text-based diagrams for software and process documentation. The skill selects a view for the user's question, preserves existing diagrams during focused edits, and checks the actual rendering when tools are available.

Examples:

- “Show this retry flow as a Mermaid sequence diagram.”
- “Add the timeout branch to this flowchart and keep its styling.”
- “Create an ERD from these tables; leave unknown cardinalities marked.”
- “Export this Mermaid diagram as SVG for the architecture document.”

[SKILL.md](SKILL.md) contains the workflow and routes to focused syntax references. References cover flowcharts, sequences, classes, ERDs, C4, infrastructure architecture, configuration, and export. They are loaded as needed rather than as a single tutorial.

Rendering support depends on the destination's Mermaid version and configuration. Keep editable source with any requested exports and distinguish syntax checks from visual inspection. The skill does not require a full architecture hierarchy or additional diagrams for every documentation task.

See the [Mermaid documentation](https://mermaid.js.org/) for version-specific features and the [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) for local rendering.
