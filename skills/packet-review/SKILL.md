---
name: packet-review
description: Review current work packet against the active plan document for direction drift, gaps, and must-close items before the next packet. Use when you want to verify ongoing implementation aligns with the plan before proceeding.
---

# Packet Review

Review the current implementation against the active plan document in this session.

## Steps

1. **Identify the active plan document** from the current conversation context. This is the plan file that has been referenced or is currently being worked on. Do not read all files in `docs/plan/` — read only the relevant plan document(s). If the active plan is ambiguous, ask the user before proceeding.

2. **Delegate to a read-only sub-agent** with the following contract:

   - **Objective**: Compare the current implementation against the active plan and surface issues to resolve before the next packet starts.
   - **Files to read**: The active plan document + relevant source files + `git log --oneline -30` + `git diff HEAD`
   - **No edits allowed**

3. **What the sub-agent analyzes**:
   - **Direction alignment** — Is the implementation consistent with the plan's direction? Flag architectural, design, or scope drift.
   - **Packet completeness** — For the current packet: planned vs. implemented. List gaps and partial work.
   - **Must-close items** — What must be resolved before the next packet starts?

4. **Output format**:

```
## Packet Review — <packet name>

### Direction Alignment [PASS / WARN / FAIL]
- ...

### Packet Completeness
| Planned | Status | Gap |
|---------|--------|-----|
| ...     | ✅/⚠️/❌ | ... |

### Gaps & Deficiencies
- ...

### Must-Close Before Next Packet
- [ ] ...

### Risk Level [LOW / MEDIUM / HIGH]
- ...
```

5. Present the sub-agent's findings as-is without modification.

If `$ARGUMENTS` is provided, treat it as the current packet name or number.
