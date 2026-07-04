# LITE.md — Agent Wiki Lite

Karpathy-weight entry protocol for small projects, but compatible upward with Agent Wiki v4.

`lite_version: 2`
`compatible_protocol_version: 4`

Use this when the router selects `tier: LITE`.

## What this is

A light wiki workflow for one agent and one user. It keeps the useful part of the Karpathy-style idea — durable local memory instead of chat history — but adds three guardrails missing from a naive loose wiki:

1. stable IDs, not file paths as identity;
2. minimal provenance: source facts vs agent inferences;
3. upgrade path to MAX without starting over.

## When to use

Use LITE for:

- small research notes;
- reading/learning projects;
- early idea exploration;
- personal knowledge bases;
- small document summaries;
- low-risk projects with no destructive source operations.

Do NOT use LITE for:

- file moves/renames/deletes;
- DB/API writes;
- expensive batch LLM runs;
- legal/financial/high-stakes evidence packages;
- projects that already require independent audit.

If those appear, upgrade to `PRINCIPLES_MAX.md`.

## Core rule

The chat is not memory. The wiki files are memory.

## Minimal folder structure

```text
<PROJECT_ROOT>/Agent_Wiki/
  00_START_HERE.md
  Project/
    _index.tsv
    Change_Log.md
  Notes/      (optional)
  Reports/    (optional)
  Sources/    (optional pointers, not source copies unless user wants)
```

No cursors, no inboxes, no separate audit lane. Those are added only when upgrading to MAX.

## Start checklist

1. Read `Agent_Wiki/00_START_HERE.md`.
2. Read `Agent_Wiki/Project/_index.tsv`.
3. Read the exact relevant note/source page only.
4. Do the task.
5. If the answer creates reusable synthesis, file it back into `Notes/` or `Reports/`.
6. Append one entry to `Project/Change_Log.md` if a file was created/changed.

## Minimal project interview

Before creating the LITE wiki, ask only these questions:

1. Where are the raw sources?
2. What counts as one item?
3. What stable ID should identify an item? Do not use path as identity if the item can move.
4. What output do you want: notes, reports, table, checklist, summary?
5. Is anything forbidden to edit/move/delete?

If the user does not answer, keep the project read-only and do not mutate sources.

## Evidence rules

Keep these separate:

- `source_evidence`: fact directly present in a source;
- `agent_inference`: classification, summary, recommendation, risk judgement, synthesis;
- `external_evidence`: web/API/source outside the local project;
- `user_override`: user correction or decision.

No invention: never present `agent_inference` as `source_evidence`.

If the task is classification or recommendation, it is allowed, but mark it as `agent_inference` and include confidence when useful.

## Minimal starter files

### `Agent_Wiki/00_START_HERE.md`

```md
# Agent Wiki Lite

lite_version: 2
compatible_protocol_version: 4
updated: <ISO timestamp>
project_name: <name>
source_of_truth: <path or description>
item_definition: <what counts as one item>
stable_id_rule: <how ids are assigned>
status: active

## Current focus
<short note>

## Read first
- Project/_index.tsv
- Project/Change_Log.md
```

### `Agent_Wiki/Project/_index.tsv`

```tsv
id	title	status	needs_manual_review	last_note
```

Allowed status values: `raw`, `noted`, `synthesized`, `review_needed`, `done`, `archive_candidate`.

### `Agent_Wiki/Project/Change_Log.md`

```md
# Change Log — Lite

## entry_id: l0001
created: <ISO timestamp>
changed_files: [00_START_HERE.md, Project/_index.tsv, Project/Change_Log.md]
summary: created Lite wiki skeleton
```

## Query behavior

When the user asks a question:

1. answer from the wiki and scoped sources;
2. separate fact from inference;
3. if the answer is reusable, save it as `Notes/<stable_id>_<short_title>.md` or `Reports/<short_title>.md`;
4. update `_index.tsv` only if it helps routing;
5. log the change.

## Lite lint

On request, check:

- orphan notes;
- duplicate notes;
- missing source pointers;
- claims without provenance;
- unresolved `needs_manual_review`;
- contradictions between notes.

Do not run lint automatically.

## Destructive actions

LITE is read-only by default. If the user asks to move/rename/delete files:

1. stop;
2. create a dry-run list in chat or `Reports/dry_run_manifest.md`;
3. ask for explicit confirmation;
4. if the operation is large or risky, upgrade to MAX before execution.

## Upgrade path to MAX

A LITE project upgrades cleanly because it already uses:

- `Agent_Wiki/`;
- `_index.tsv`;
- `Change_Log.md`;
- stable IDs;
- provenance language.

To upgrade:

1. fetch `PRINCIPLES_MAX.md`;
2. create missing MAX files from Appendix A: cursors, `Agent_Protocol.md`, inbox READMEs;
3. convert the LITE starter metadata into the MAX domain adapter;
4. preserve old notes and log entries;
5. do not rewrite sources.

## Token economy

Read `00_START_HERE.md` and `_index.tsv` first. Do not scan all notes unless asked. Do not fetch MAX unless LITE is no longer enough.
