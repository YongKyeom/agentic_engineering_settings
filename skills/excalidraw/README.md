# Excalidraw

Create, inspect, compare, and edit Excalidraw scenes while keeping the source editable. The skill supports rough sketches and existing `.excalidraw` or `.excalidraw.json` artifacts.

Examples:

- “Explain the components and arrows in this Excalidraw file.”
- “Add a cache next to the API and connect them without changing the other groups.”
- “Compare these two scenes and summarize the changed relationships.”
- “Create an editable sketch of this workflow.”

[SKILL.md](SKILL.md) describes focused scene inspection, preservation of IDs and bindings, and structural and visual checks. Small tasks can be handled directly. For large or noisy work, the lead may delegate within project rules; delegation is a context-management option, not a prerequisite for editing.

The editable scene is the source artifact. Image exports help with review but do not replace it. Validation should include a compatible renderer when available; report visual checks that could not be performed.

## License

Part of the Softaworks Agent Skills collection.
