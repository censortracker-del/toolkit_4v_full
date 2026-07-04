# TASK.md — no-wiki execution shell (tier TASK)

For one-shot, low-risk work. No Agent_Wiki is created; the deliverable is the
memory. Selected by ROUTER when strictness < 15 and no hard override fires.

`task_shell_version: 1` · `protocol_version: 4`

## Loop

1. Restate the `clarified_task` spec to the user in 2–3 lines (user language).
   A misread idea must die cheaply, before work starts.
2. Follow the selected playbook's `method`.
3. Verify the result against `done_criteria` and the playbook `qa checklist`.
4. Deliver per `format`: exact file path or the answer itself — never
   "should work" without the artifact.
5. If an `Agent_Wiki/` already exists in the project and the result is
   reusable synthesis, OFFER to file it back (one question, user decides).
   Do not create a wiki for a TASK-tier run.

## Discipline (condensed; superseded by blocks/ when present)

- Provenance: keep `source_evidence` / `agent_inference` / `external_evidence`
  / `user_override` separate; never present inference as source fact; mark
  derived judgements with confidence.
- No invention: a value absent from the inputs is `unknown`, not a guess.
- Read-only by default: TASK tier never moves / renames / deletes / mutates
  sources or writes to DBs. Creating NEW deliverable files in the agreed
  output location is allowed and is not a destructive operation. If that need appears mid-task — stop, report, and
  re-route upward (this is a tier violation, not a judgement call).
- No secrets anywhere. No unconfirmed paid/large LLM runs.

## Escalation triggers (stop and re-route)

- Destructive operation or DB/API write turns out to be required → MAX.
- The "one-shot" reveals itself as multi-session → LITE (create wiki then).
- Legal / financial / submission stakes surface → MAX.
- The user starts a second related task in the same area → suggest LITE so the
  work compounds instead of evaporating.

## Done

Done = spec restated and confirmed cheap-to-fix; playbook method followed;
`done_criteria` checked; artifact delivered with exact path or inline; open
assumptions listed. NOT done: silent assumptions, unverified "should work",
scope creep past the clarified spec without asking.
