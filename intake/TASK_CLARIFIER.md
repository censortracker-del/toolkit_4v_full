# TASK_CLARIFIER.md — universal task specification (v4)

Purpose: turn a raw project idea into an explicit task spec BEFORE routing and
execution. This is about the task itself; risk/independence scoring lives in
`intake/ROUTER.md`.

`clarifier_version: 1` · `protocol_version: 4`

## Six slots

Every task must have all six slots filled (by inference or by asking):

1. `goal` — what the user wants and why / for whom.
2. `inputs` — what is given: files, links, data, access, prior work, examples.
3. `outputs` — what must exist at the end: artifact(s), decision, answer.
4. `format` — shape of the output: file type, structure, language, где отдать
   (chat / file / repo / wiki).
5. `constraints` — forbidden things, required stack/tools, environment limits
   (offline contour, no external APIs), deadlines, budget/token limits.
6. `done_criteria` — how the user will judge "готово": checks, acceptance
   examples, who reviews.

## Rules

- **Infer first.** Extract every slot you can from the user's message and
  USER_PROFILE. Mark each slot: `stated` | `inferred` | `missing`.
- **Ask only `missing` slots**, plus `inferred` slots whose wrong guess would
  waste significant work. One batched message, numbered, in the user's
  language (default RU). Maximum ~5 questions; merge related ones.
- **Derive 2–4 domain questions from the idea itself.** The toolkit cannot
  pre-list questions for every domain; a good agent generates them. Example:
  idea "сайт с котятами" → галерея или магазин? откуда контент? стек или мне
  решить? где хостить?
- If the user answers "сам реши" / "на твоё усмотрение" → decide, and record
  the decision in `assumptions[]`, not silently.
- Slot answers feed ROUTER scoring: e.g. `outputs` mentioning DB writes or file
  reorganization triggers the destructive-operations criterion; `constraints`
  mentioning submission/legal raises stakes.
- Do not re-ask anything USER_PROFILE or the message already answers.

## Output

A `clarified_task` object embedded in the ROUTER output JSON:

```json
{
  "goal": "...",
  "inputs": "...",
  "outputs": "...",
  "format": "...",
  "constraints": "...",
  "done_criteria": "...",
  "slot_sources": {
    "goal": "stated", "inputs": "inferred", "outputs": "stated",
    "format": "asked", "constraints": "asked", "done_criteria": "asked"
  }
}
```

Before heavy execution, restate the spec to the user in 2–3 lines (user
language) so a misread idea dies cheaply.
