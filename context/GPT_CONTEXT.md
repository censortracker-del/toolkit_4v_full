# GPT_CONTEXT.md - Agent Wiki Toolkit Context

This is an adaptive prompt toolkit, not one giant prompt.

## Purpose

The toolkit helps an agent or orchestrator choose the smallest sufficient Agent
Wiki workflow:

```text
project input
-> questionnaire or file-driven intake
-> selected files from GitHub
-> bootstrap_tier or daily loop
-> role_mode
-> Agent_Wiki as durable memory
```

## Core Decisions

- `core/PRINCIPLES_MAX.md` is protocol v3 for bootstrap, recovery, and high-risk
  work.
- `core/PRINCIPLES_MINI.md` is only the daily loop for an already deployed
  Agent_Wiki.
- `core/LITE.md` is a low-risk starter with stable IDs, provenance, and upgrade
  path.
- `USER_PROFILE.md` stores durable intake defaults; if absent, ask all questions.
- Machine logic uses `bootstrap_tier: LITE | MAX` and
  `daily_loop_file: core/PRINCIPLES_MINI.md`.
- `role_mode` is runtime config: `SOLO`, `DUAL`, or `FULL`.

## Supported Modes

- Questionnaire routing through `intake/ROUTER.md`.
- File-driven adaptive intake through `intake/ADAPTIVE_INTAKE.md`.
- Manual chat handoff through shared Agent_Wiki files.
- Simple API use.
- Orchestrated multi-agent API use.

## Optional Layers

- MCP is optional tool access, not core protocol.
- RAG/indexed retrieval is optional evidence retrieval, not project memory.
- Agent_Wiki remains the control plane and durable decision log.

## Non-Goals

- Do not fetch all prompts just in case.
- Do not create API/manual/MCP prompt variants.
- Do not make MCP or RAG mandatory.
- Do not put secrets in prompts, repo files, logs, screenshots, or Agent_Wiki.
- Do not reopen MAX architecture without a real protocol-level gap.
