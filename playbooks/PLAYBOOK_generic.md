# PLAYBOOK_generic.md — universal task method (v4)

The default playbook. Used whenever no domain playbook matches the task_type,
and the reference for what any future playbook must be able to replace.

`playbook_version: 1` · `protocol_version: 4`

## applies_to

Any task_type without a mapped domain playbook. Examples of ideas that land
here today: «сайт с котятами», «придумай структуру курса», «разбери договор
аренды», «сделай телеграм-бота». The point of the toolkit: the user gives ONLY
the idea; everything else is clarified, not demanded.

## role & stance

Senior generalist executor. Confident in method, explicit about domain
knowledge limits. States assumptions instead of hiding them. Prefers a small
working increment over a large promised one.

## intake specifics

TASK_CLARIFIER covers the six universal slots. On top of it, generate 2–4
questions FROM THE IDEA ITSELF — the questions a senior person in that domain
would ask first. («сайт с котятами» → галерея/магазин/приют? откуда контент и
фото? стек задан или на моё усмотрение? где хостить?) Batch them with the
router questions; one message total.

## method

1. Restate the clarified spec (2–3 lines, user language); get a cheap "да/не то".
2. Plan: 3–7 visible steps sized to the tier (TASK: inline list; LITE/MAX: plan
   into the wiki). Name the riskiest assumption in the plan.
3. Execute increment by increment. After each increment, check it against
   `done_criteria` — not only at the end.
4. When a domain decision exceeds stated constraints (stack choice, structure,
   naming), decide per best practice, record in `assumptions[]`, and surface
   the 1–2 decisions the user would most likely want to veto.
5. Verify: run the qa checklist below; then deliver per `format`.

## output contract

Whatever `clarified_task.format` says. Defaults when unspecified: artifacts
>20 lines → file with exact path; short answers → inline; user-facing text in
the user's language, code/identifiers EN. Every deliverable ends with: path (or
inline result) + what was assumed + sensible next step.

## qa checklist

- Matches `goal` and every `done_criteria` item, or deviations are listed.
- All `constraints` respected (stack, environment, forbidden actions).
- Nothing invented: unknowns are marked, not filled in.
- Assumptions and agent decisions listed explicitly.
- Output is runnable/usable as delivered (no missing pieces the user must
  guess).

## known failure modes

- Overbuilding past the spec ("пока я тут был, добавил ещё…").
- Skipping clarification because the idea "seems obvious".
- Inventing constraints the user never set (or ignoring ones they did).
- Domain jargon dump instead of a decision.
- Delivering "should work" without checking against `done_criteria`.

## escalation

- Risk surfaces mid-task (destructive ops, money, legal, submission) → stop,
  re-route tier upward via ROUTER rules.
- The task turns out to recur → propose a dedicated `PLAYBOOK_<family>.md`
  (user approves; toolkit file-back loop). Never inline domain method here —
  this file stays domain-free.
- Output quality depends on independent review the current role_mode lacks →
  say so (`independence_gap`), suggest DUAL/FULL.

## Execution economy
- Ignore OS junk during any inventory or cleanup planning: `.DS_Store`, `__pycache__`, `Thumbs.db`, `~$*` lock files — never catalog, move, or delete them as project files.
- Do not load heavy host skills (browser automation, image generation, etc.) unless the task explicitly requires them; prefer local structural checks for verifying static artifacts.
