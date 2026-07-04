# API_ORCHESTRATION_SPEC.md - minimal-token orchestration

## Goal

An API/coworking layer should diagnose the project, fetch the smallest sufficient
toolkit files from GitHub, and create or continue Agent_Wiki memory without
resending full chat history.

## Universal Flow

```text
User request
-> fetch MANIFEST.json
-> choose entry mode
-> run ROUTER or ADAPTIVE_INTAKE
-> validate JSON
-> ask only blocking questions
-> fetch files_to_fetch
-> run selected workflow with runtime header
-> write outputs/state to Agent_Wiki
```

## Entry Mode Decision

- Description only -> `intake/ROUTER.md` + `schemas/ROUTER_OUTPUT_SCHEMA.json`
- Files/repo/archive/uploads -> `intake/ADAPTIVE_INTAKE.md` +
  `schemas/SOURCE_INVENTORY_SCHEMA.json`

## Simple API Flow

Use for one agent, low/medium risk, no complex independent review.

1. Fetch `MANIFEST.json`.
2. Run the chosen entry mode.
3. Validate router/intake JSON.
4. Fetch only selected files.
5. Create or continue Agent_Wiki.
6. Save reusable findings to wiki files.
7. Return paths and next action, not a long copied chat history.

## Orchestrated API Flow

Use when multiple agents/runs coordinate through files.

1. Fetch `MANIFEST.json`.
2. Run `ROUTER` or `ADAPTIVE_INTAKE`.
3. Enable only required tools/MCP servers.
4. Fetch selected core/scenario/orchestration files.
5. Codex/implementer performs work.
6. Codex appends `Project/Change_Log.md`.
7. Review flags decide whether Claude/OpenCode runs are needed.
8. Claude writes `Claude_Inbox/feedback_N.md`.
9. OpenCode writes `OPEN_Inbox/review_N.md` or `deal_N.md`.
10. Codex applies accepted fixes.
11. Final change log entry and completion criteria.

## Manual Handoff Is Supported

Manual chat handoff is not API, but the toolkit supports it through
`scenarios/MANUAL_CHAT_HANDOFF.md`. The API spec must not imply that API is the
only supported mode.

## Large Corpus Gate

Before analysis, classify size/count/type distribution.

If the corpus is huge, do not ingest everything. Produce a project-local
`CORPUS_INTAKE_PLAN.md`, ask for confirmation, and only then proceed with
indexing/RAG/heavy processing.

## Security

Private GitHub repositories require credentials outside prompts and repo files.

Example environment variables:

```bash
AGENT_WIKI_REPO="owner/repo"
AGENT_WIKI_BRANCH="main"
GITHUB_TOKEN="..."
```

No token or secret may be written into markdown, logs, screenshots, or Agent_Wiki
outputs.

## Validation

- `MANIFEST.json` is valid JSON.
- Every referenced file exists.
- `sha256` and `bytes` match fetched content.
- Router/intake output validates against its schema.
- `files_to_fetch` contains only known paths.
- `core/PRINCIPLES_MAX.md` is not fetched by default.
- Mutating actions require dry-run plus explicit confirmation.
