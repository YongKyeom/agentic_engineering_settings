---
name: structured-prompt-template
description: Design, generate, refactor, or audit provider-neutral system prompts with XML-inspired section tags and Jinja2 templates. Use for agent role prompts, Skill and Tool catalogs, priority rules, numbered workflows, output contracts, prompt template files such as prompt.md or *.j2, and runtimes using native tool calling, OpenAI-compatible APIs, vLLM, or text-only tool protocols.
---

# Structured Prompt Template

Build readable prompt packets whose structure remains visible in source and whose runtime data has one owner.

## Workflow

1. Inspect the runtime before designing the template.
   - Identify the system/user message boundary.
   - Determine whether Tool schemas and structured-output schemas are injected natively.
   - Identify the authoritative Skill and Tool manifests.
   - List trusted template variables and untrusted request data separately.
2. Select the provider mode.
   - For native Tool schemas, render Tool purpose and usage guidance only. Never duplicate the JSON schema.
   - For an OpenAI-compatible or vLLM endpoint, confirm the served chat template supports native tool calling. If it does, use the native mode.
   - For text-only tool calling, generate the compact Tool contract from the same runtime manifest. Never maintain a second hand-written schema.
3. Copy `assets/system-prompt.md.j2` into the project and replace only the context data, not the section hierarchy, unless the task requires a different contract.
4. Keep the rendered top-level order:
   `ROLE -> PRIORITIES -> BOUNDARIES -> SKILLS -> TOOLS -> WORKFLOW -> OUTPUT_CONTRACT`.
5. Render with `StrictUndefined`, a closed context object, deterministic list order, and escaping for values inserted into tag bodies or attributes.
6. Run `scripts/validate_prompt.py` against the template and context with the runtime's local prompt-byte budget. Inspect the rendered prompt before wiring it into the runtime.
7. Test one normal request and negative cases for missing variables, malformed tags, forged STEP tags, unknown context fields, over-budget rendered prompts, and delimiter-like context text.

## Design Rules

- Use XML-inspired tags as section boundaries, not as a claim that the whole prompt is valid XML.
- Use numbered tags only for ordered execution: `<STEP_1>` through `<STEP_N>`. Keep numbers contiguous.
- Put priorities in explicit `<P0>`, `<P1>`, and lower levels. State conflict resolution in P0.
- Give every Skill a name, description, and activation condition.
- Keep each Skill's recommended Tool names in its trusted manifest or body. Render them only when the initial catalog needs that routing hint.
- Give every Tool a name, purpose, and usage guidance. Keep native argument schemas in the runtime Tool definition.
- Treat Skill instructions and Tool capabilities as different concepts. A Skill teaches procedure; a Tool performs an action.
- Treat Skill-to-Tool references as advisory. The role Tool manifest controls availability; the broker and current-turn lifecycle control authorization.
- Keep untrusted user text, retrieved documents, and Tool results out of the system-template context. Pass them through their runtime message channels.
- Preserve one source of truth for each dynamic field and bind the rendered prompt to the manifest or context digest when reproducibility matters.
- Keep the base template provider-neutral. Put provider-specific serialization in an adapter, not in prompt prose.
- When the host runtime already supplies a system-message envelope, keep the tagged sections as top-level siblings. Add one root tag only when a downstream XML parser requires a well-formed document.

## Anti-Patterns

- Never target a model name in the reusable template. Capabilities change independently of names and deployments.
- Never paste a native Tool or output JSON schema into the prompt. Two copies drift and waste context.
- Never let a Skill manifest grant Tool authority. Reject recommended Tool names that are absent from the role Tool manifest.
- Never use Jinja2 `safe`, `include`, `import`, `extends`, macros, calls, assignments, item access, or arbitrary filters in a prompt template.
- Never render secrets, provider metadata, hidden reasoning, raw Tool arguments, or untrusted retrieved text into the system prompt.
- Never silently ignore an undefined variable or malformed tag. Fail before opening the model provider.
- Never make prose order carry a hard priority or workflow dependency that a smaller model must infer.

## Resource Loading

- For any implementation or audit, read `references/provider-modes.md` completely before editing the target prompt.
- Use `assets/system-prompt.md.j2` and `assets/context.example.json` when creating a new template.
- Do not load or copy the assets when only reviewing an existing prompt; validate the existing files directly.

## Validation Command

```bash
uv run --with jinja2 python -B scripts/validate_prompt.py \
  --template assets/system-prompt.md.j2 \
  --context assets/context.example.json \
  --max-bytes 32768 \
  --output /tmp/rendered-system-prompt.md

uv run --with jinja2 python -B scripts/test_validate_prompt.py
```

Set `--max-bytes` to the runtime's local budget. The validator checks the closed context shape, restricted Jinja2 surface, deterministic section hierarchy, contiguous priority and STEP tags, Skill and Tool uniqueness, native-schema non-duplication, and rendered UTF-8 byte size.
