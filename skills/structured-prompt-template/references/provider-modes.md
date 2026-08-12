# Provider Modes

## Choose by capability

Do not infer prompt structure from a provider or model name. Inspect the runtime request surface.

When a framework such as LangChain already places the rendered template in a system-message role, the message boundary is the outer envelope. Do not add a `<SYSTEM_PROMPT>` wrapper unless a downstream XML parser requires a single document root.

| Runtime capability | Prompt content | Runtime content |
|---|---|---|
| Native Tool calling | Tool purpose, activation guidance, sequencing, failure behavior | Exact Tool name, description, and argument schema |
| Native structured output | Semantic output rules and authority requirements | Exact output JSON schema |
| OpenAI-compatible native Tools | Same as native Tool calling after a request-capture or smoke check | Exact Tool schema in the compatible request field |
| Text-only tool protocol | Compact generated contract from the Tool manifest | Parser, validator, and dispatcher for that generated contract |
| Plain text output | Explicit tagged output contract | Parser and fail-closed validation when structure is required |

For vLLM, check the served chat template and tool parser configuration. An OpenAI-compatible endpoint does not guarantee that every served model or chat template supports the same Tool surface.

## Keep one authority

The runtime Tool manifest owns:

- canonical Tool name;
- human-readable description;
- typed argument contract;
- ordering when ordering is meaningful;
- availability by role or phase.

A Skill manifest may own `recommended_tools` so an agent can select the minimum Tool sequence for that procedure. The Skill body may refine those recommendations by branch, order, cardinality, or stop condition. These names are advisory and must be a subset of the role-visible Tool manifest. The broker still decides whether the current principal, phase, loaded Skill body, and typed input authorize a call.

The system prompt may explain when and why to use a Tool. It must not become another schema registry. If text-only tool calling is required, generate its compact schema projection from the runtime manifest during assembly.

The same rule applies to output schemas: explain semantics in the prompt, but keep the machine schema in one runtime authority.

## Separate data by trust

The system prompt may contain trusted, bounded configuration such as role policy, Skill catalog entries, Tool usage guidance, and workflow rules. Put user text, retrieved documents, Tool results, and other variable evidence in their proper runtime messages.

If trusted descriptions can contain delimiter-like text, escape them before rendering. Do not use Jinja2 `safe`. Do not rely on a provider to repair malformed prompt boundaries.

## Capability checks

Before accepting a new adapter, capture or inspect one final outbound request without sending secrets. Verify:

1. system and user messages remain separate;
2. Tool schemas appear exactly once;
3. structured-output schemas appear exactly once;
4. Tool choice and output mode match the runtime contract;
5. rendered prompt bytes stay within the local budget;
6. missing context or invalid templates fail before provider access.

Keep this check provider-specific. Keep the prompt template provider-neutral.
