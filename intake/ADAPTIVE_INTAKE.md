# ADAPTIVE_INTAKE.md - File-Driven Intake

Use this when project files, a folder, repository, archive, uploaded documents,
datasets, scripts, reports, or an existing `Agent_Wiki/` are available.

Keep this short. This file diagnoses the project shape; it is not a second MAX.

Read `USER_PROFILE.md` first when available; skip any question it answers; apply
its overrides. If it is absent, continue and ask all needed questions.

## Goal

Inspect minimally, form explicit hypotheses, ask only blocking questions, and
select the smallest sufficient files.

## Inspection Order

1. File tree, names, extensions, sizes.
2. README, manifest, package/config files, obvious entry files.
3. Detect `Agent_Wiki/` and inspect only `00_START_HERE.md` headers if present.
4. Headings, metadata, and small samples.
5. Relevant files only.
6. Never full-scan huge files or corpora unless the user explicitly confirms a
   bounded plan.

## Required Output

Produce JSON that conforms to `schemas/SOURCE_INVENTORY_SCHEMA.json`, then a
short human explanation.

The JSON must include:

- `bootstrap_mode`
- `bootstrap_tier`
- `daily_loop_file`
- `role_mode`
- `corpus_profile`
- `retrieval_strategy`
- `large_corpus_controls`
- `tooling_recommendation`
- `adapter_draft`
- `questions_for_user`
- `files_to_fetch`

## Decision Rules

To set bootstrap_tier and role_mode, apply the same Strictness/Risk and Agent
Independence scoring rubric defined in intake/ROUTER.md (the file-driven door
reuses that rubric; it is not redefined here).

- Existing healthy `Agent_Wiki/` -> fetch `core/PRINCIPLES_MINI.md`.
- New small/low-risk project -> fetch `core/LITE.md`.
- New high-risk/heavy/destructive project -> fetch `core/PRINCIPLES_MAX.md`.
- Recovery, corrupt context, missing adapter, or old schema -> fetch
  `core/PRINCIPLES_MAX.md`.
- Book legacy project -> add `project_notes/BOOK_PROJECT_NOTES.md` only when the
  project is the book project.

## Corpus Size Rules

- Small/medium human-readable corpus -> Agent_Wiki only is usually enough.
- Large/search-heavy corpus -> recommend RAG/index or hybrid mode.
- Huge corpus, hundreds of GB, or around 1 TB -> do not analyze directly.
  First output a project-local `CORPUS_INTAKE_PLAN.md` proposal and ask for
  confirmation before indexing or heavy processing.

## No Invention

If files do not reveal a value, mark it unknown and ask.

Do not invent:

- source of truth path;
- item definition;
- stable ID strategy;
- safety rules;
- output types;
- review triggers;
- legal/business meaning;
- which source is authoritative.

## Token Rule

Minimal diagnosis first. Minimal file fetch second. Minimal tools third. Heavy
protocol only when justified.
