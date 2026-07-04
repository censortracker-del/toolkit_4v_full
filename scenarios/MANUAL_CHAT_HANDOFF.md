# MANUAL_CHAT_HANDOFF.md

Use this when the user works in separate Claude/Codex/OpenCode chats and shares
one project folder.

## When To Use

- No API orchestrator is available or desired.
- The user manually transfers short references between chats.
- A common local/Git folder stores `Agent_Wiki/`.
- The goal is low-token cross-chat coordination.

## Flow

1. User creates or opens the project folder.
2. Agent_Wiki exists or is bootstrapped through `core/LITE.md` or
   `core/PRINCIPLES_MAX.md`.
3. Claude reads `00_START_HERE.md` plus cursor and writes
   `Claude_Inbox/feedback_N.md`.
4. User gives Codex only the relevant path, `entry_id`, or feedback file.
5. Codex reads feedback, implements accepted changes, and appends
   `Project/Change_Log.md`.
6. OpenCode, if needed, writes `OPEN_Inbox/review_N.md` or `deal_N.md`.
7. User passes short references between chats, not full history.

## Rules

- Chat is transport; files are memory.
- Use paths and `entry_id`.
- Highest `N` is newest.
- Never overwrite feedback/review/deal files.
- Destructive actions still require dry-run plus explicit confirmation.

## Example

```text
User to Codex:
Please handle Claude_Inbox/feedback_7.md for entry_id e0042.

Codex:
Reads 00_START_HERE.md, Project/Change_Log.md, the scoped files, and
Claude_Inbox/feedback_7.md. Applies accepted changes, logs e0043, and reports
the changed paths.
```
