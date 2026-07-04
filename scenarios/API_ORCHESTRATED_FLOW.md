# API_ORCHESTRATED_FLOW.md

Use this for multi-agent/API coordination.

## When To Use

- Multiple agents/runs are needed.
- One agent implements.
- A second reviews semantics.
- A third audits code, safety, or data integrity.
- State is coordinated through Agent_Wiki files.

## Flow

1. Orchestrator creates task.
2. Fetches `MANIFEST.json`.
3. Runs `intake/ROUTER.md` or `intake/ADAPTIVE_INTAKE.md`.
4. Validates routing/intake JSON.
5. Enables only required tools/MCP servers.
6. Fetches selected files.
7. Creates or updates Agent_Wiki.
8. Codex/implementer performs work.
9. Change_Log entry is created.
10. Review flags decide whether Claude/OpenCode runs are needed.
11. Claude writes `Claude_Inbox/feedback_N.md`.
12. OpenCode writes `OPEN_Inbox/review_N.md` or `deal_N.md`.
13. Codex applies accepted fixes.
14. Final Change_Log entry and completion criteria.

## Rules

- Do not rely on chat history as memory.
- Use `entry_id`, cursors, and exact review scopes.
- Do not fetch MAX unless selected.
- Do not run mutating tools without confirmation gates.
