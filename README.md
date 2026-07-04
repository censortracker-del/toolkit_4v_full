# Agent Wiki Toolkit (v4)

> **AI agent reading this?** Do not parse this README. Fetch `MANIFEST.json`
> and follow `START.md` → `intake/ROUTER.md`. This page is for humans.

A GitHub-hosted skeleton for running ANY project with an AI agent. The user
supplies only the idea; the agent clarifies the task, routes it, fetches the
smallest sufficient prompt files, and executes — with durable file-based memory
(`Agent_Wiki/`) when the project deserves one.

```text
idea ("хочу сайт с котятами")
-> START.md (pasted into any agent)
-> MANIFEST.json + USER_PROFILE.md
-> task_type -> playbook          (Axis 0: WHAT kind of work)
-> clarifying questions (batched, user language)
-> strictness -> tier TASK|LITE|MAX  (Axis 1: HOW strictly)
-> independence -> SOLO|DUAL|FULL    (Axis 2: HOW many lanes)
-> assembled runtime prompt -> execution
```

## Core rules

- **Core purity.** `core/`, `intake/`, `blocks/`, `schemas/`, `START.md`,
  `MANIFEST.json` are domain-agnostic forever. Domain knowledge lives ONLY in
  `playbooks/` and `adapters/`, added only as proposals the user approves.
- **Lane-neutral naming.** Roles are Implementer / Reviewer / Auditor; project
  files use `Review_Inbox/`, `Audit_Inbox/`, `_review_cursor.txt`,
  `_audit_cursor.txt`, `AGENT_CONTEXT`. Concrete agents (Claude, Codex, local
  models…) are bound per project via `lane_binding` in `Agent_Protocol.md`.
- **Smallest sufficient fetch.** Never fetch everything; never fetch
  `core/PRINCIPLES_MAX.md` unless selected. One-shot tasks run tier `TASK`
  with no wiki at all.
- **Inference-first clarification.** The agent scores risk from the
  description and asks only questions that are missing or can change the
  route. Risk questions are never silently assumed "no".
- The wiki files are memory; chat is transport. No secrets anywhere, ever.

## Tiers

| tier | when | core file |
|---|---|---|
| `TASK` | one-shot, low risk | `core/TASK.md` — no wiki |
| `LITE` | small multi-session project | `core/LITE.md` |
| `MAX` | high-risk / destructive / heavy | `core/PRINCIPLES_MAX.md` |
| daily | already-deployed wiki | `core/PRINCIPLES_MINI.md` |

## File map

```text
START.md            single paste-in entry point (raw URL baked in)
MANIFEST.json       file map + task_type→playbook + rename_map
USER_PROFILE.md     durable user defaults
intake/             ROUTER.md (3-axis routing) · TASK_CLARIFIER.md · ADAPTIVE_INTAKE.md
core/               TASK.md · LITE.md · PRINCIPLES_MINI.md · PRINCIPLES_MAX.md
playbooks/          methods per task family (PLAYBOOK_generic.md = default)
blocks/             shared discipline blocks (planned)
adapters/           filled domain adapters, grow per project (planned)
schemas/            JSON validation for router/intake output
scenarios/          manual handoff · simple API · orchestrated API
orchestration/      loader prompt · API spec · optional MCP/RAG layers
```

## History

v3 (vendor role names, book-project legacy) is frozen at git tag `v3.2`.
v4 = lane-neutral naming, task_type axis, TASK tier, playbooks/adapters layer,
core purity rule. Files marked `pending_v4_rewrite` in `MANIFEST.json` still
follow v3 mechanics; agents apply `rename_map` when creating new project files.
