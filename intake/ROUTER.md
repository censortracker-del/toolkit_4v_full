# ROUTER.md — Agent Wiki Router (v3)

Purpose: from a task described in words, decide WHAT KIND of work it is
(→ playbook), HOW STRICTLY to run it (→ tier), and HOW MANY agent lanes it
needs (→ role_mode). Select the smallest sufficient toolkit files.

`router_version: 3` · `protocol_version: 4` · `protocol_family: Agent Wiki`

Read `USER_PROFILE.md` first when available; skip any question it answers;
apply its overrides. Run `intake/TASK_CLARIFIER.md` as part of step 2 below.
For file-driven entry (files/repo/archive present) use `intake/ADAPTIVE_INTAKE.md`
for inspection, then return here for the same three-axis decision.

Ask all user-facing questions in the user's language (USER_PROFILE; default RU).
Do not fetch `core/PRINCIPLES_MAX.md` by default.

## Routing model — three axes

- **Axis 0 — task_type** → which playbook (the method).
- **Axis 1 — strictness/risk** → `bootstrap_tier`: `TASK`, `LITE`, or `MAX`.
- **Axis 2 — independence** → `role_mode`: `SOLO`, `DUAL`, or `FULL`.

Plus `bootstrap_mode`: `new_project` | `existing_agent_wiki` | `recovery_needed`.
`core/PRINCIPLES_MINI.md` is not a tier; it is the daily loop for an already
deployed Agent_Wiki.

## Axis 0 — task_type

Classify the PRIMARY verb of the task. Domain-free by design.

| task_type | meaning | examples |
|---|---|---|
| `build` | create software / site / tool / agent / system | сайт с котятами, C# утилита, jira-агент |
| `analyze` | extract / transform / analyze data; SQL; dashboards | выгрузка по схеме, скрипт SELECT, Excel-трекер |
| `research` | collect + synthesize external information | брифинг, обзор рынка, OSINT, сравнение моделей |
| `write` | produce documents / content for humans | отчёт руководству, резюме, статья, письмо |
| `review` | evaluate an EXISTING artifact | код-ревью, аудит репо, оценка кандидата |
| `operate` | run / maintain / automate a recurring process | еженедельный радар, мониторинг, регламентная задача |
| `plan` | architecture / strategy / decision support, no build yet | выбрать стек, спроектировать пайплайн, ADR |
| `other` | none of the above | — |

Rules:

- Pick ONE primary type + optional `task_type_secondary[]` (e.g. analyze +
  write for "выгрузи и оформи отчёт"). Secondary types pull extra blocks or a
  second playbook's `output contract` section — never two full playbooks.
- State `task_type_confidence`: `high` | `medium` | `low`. If `low`, ask the
  user ONE classification question before proceeding.
- Resolve playbook via MANIFEST `task_type_map`. No specific playbook →
  `playbooks/PLAYBOOK_generic.md`. If the same unmatched task family recurs,
  propose creating a new playbook (toolkit file-back loop) — as a proposal to
  the user, never by silently editing core.

## Step order (inference-first)

1. Read USER_PROFILE; note which router inputs it fixes.
2. Classify task_type (Axis 0). Run TASK_CLARIFIER: fill six slots; collect
   `missing` questions.
3. **Score both axes from the description + clarified slots.** For every
   criterion record: score + basis = `stated` | `inferred` | `asked` | `assumed` | `profile`
   (profile = fixed by USER_PROFILE). Recorded per criterion in the required
   `strictness_breakdown` / `independence_breakdown` output fields.
4. **Safety floor:** criteria S4 (destructive operations) and S5 (data-loss /
   money / legal / submission) may NEVER be `assumed` at 0. If not explicit,
   they join the question batch; the schema rejects S4/S5 with basis `assumed`.
   Independence I3 (audit needed) follows S4/S5.
5. Build ONE batched question message (user language): TASK_CLARIFIER missing
   slots + safety-floor questions + any question whose answer can flip a
   tier/role boundary (within ±5 points of a cut). Nothing else. If nothing
   qualifies — ask nothing.
6. Recompute scores from answers. Emit output JSON + a 3–5 line human summary
   (user language) with key assumptions.
7. Fetch `files_to_fetch`; assemble runtime prompt; hand off to execution.

## Axis 1 — Strictness / Risk score (theoretical max 160; tier cuts below)

1. Project duration: one-off = 0 · days/weeks = 5 · months/long-running = 10
2. Source volume/complexity: <20 items simple = 0 · 20–500 or mixed formats = 8 · 500+/DB/API/pipeline = 15
3. Corpus size: <100 MB = 0 · 100 MB–5 GB = 5 · 5–100 GB = 12 · >100 GB = 20
4. Destructive operations: none / read-only / NEW deliverable files in the agreed output location = 0 · overwrite or reorganize EXISTING user files = 10 · move/rename/delete sources, DB/API writes = 25
5. Data loss / money / legal / business risk: none = 0 · inconvenient = 10 · serious/legal/financial/reputational = 25
6. Provenance / citations / audit need: casual = 0 · useful = 10 · mandatory evidence + review trail = 20
7. Automation / API / repeated pipeline: manual chat = 0 · repeated/simple scripts = 10 · API/DB/expensive LLM/idempotency = 20
8. Contradictions / freshness / research uncertainty: stable = 0 · some = 8 · research/OSINT/legal/conflicting = 15
9. Stakeholders / external use: private = 0 · shared/reused = 5 · submitted/published/decision-driving = 10

## Axis 2 — Agent Independence score (theoretical max 120; role cuts below)

1. Implementation needed: none = 0 · files/reports = 10 · scripts/DB/API/destructive manifests = 25
2. Semantic judgement: mechanical = 0 · classification/recommendation = 15 · architecture/legal/research meaning = 25
3. Independent audit: no = 0 · useful = 15 · required (destructive/high-risk) = 35
4. Engines available: one = 0 · two = 10 · three-lane workflow = 15
5. User can manually verify: easily = 0 · partly = 5 · no = 10
6. Token/cost sensitivity: extreme saving = -15 · normal = 0 · accuracy over tokens = +10

USER_PROFILE token override stands: default -15, forced to +10 when the project
carries data-loss / legal / financial / government-submission risk. Token
preference must never silently drop a high-stakes project down a role_mode tier.

## Decision rules

`bootstrap_mode`:

- `existing_agent_wiki` (healthy) → fetch `core/PRINCIPLES_MINI.md` only, plus
  the playbook if the day's task benefits from one.
- `recovery_needed` (corrupt context / missing adapter / old schema) → fetch
  `core/PRINCIPLES_MAX.md`; set `bootstrap_tier: MAX`.
- User implies continuation ("продолжаем", "continue this project") but no
  `Agent_Wiki/` exists at the confirmed root → do NOT improvise continuity and
  do NOT scan parent/sibling directories; ask the user for the correct path,
  or confirm starting as `new_project`.

`bootstrap_tier` for `new_project`:

- strictness `0–14` → `TASK` — no Agent_Wiki; execute under
  `core/TASK.md` + playbook. One-shot work must not pay wiki overhead.
- strictness `15–39` → `LITE`
- strictness `>= 40` → `MAX`

Hard overrides to `MAX` regardless of score:

- destructive source operations planned;
- legal / financial / government-submission stakes;
- DB/API writes or expensive LLM batches;
- huge corpus needing a corpus intake plan first;
- user explicitly requests strict audit.

Every triggered override MUST also be declared in the `hard_overrides[]`
output field (`destructive_ops` | `high_stakes` | `db_api_writes_or_expensive`
| `huge_corpus` | `user_strict_audit`). The validator forces MAX whenever the
list is non-empty and cross-checks the four machine-derivable kinds against
the breakdown; `user_strict_audit` is the structured channel for the
user-requested case — do not leave it only as free text in `reason[]`.

A `TASK`-tier result with duration = months (criterion 1 = 10) is suspicious:
recheck — long-running work almost always deserves at least LITE memory.

`role_mode`: independence `0–24` → `SOLO` · `25–59` → `DUAL` · `60–100` → `FULL`.
Override to `FULL` when destructive operations + user cannot manually inspect
outputs. Only one engine available → `SOLO`; if the score or an override demanded more,
set `independence_gap: true`.

## Output format

Always produce the full JSON — it is the validator's input and the audit
trail. User-facing display depends on tier: for `TASK` with empty
`hard_overrides` show ONLY a 2–3 line summary in the user language (type,
tier/role, risk level, what happens next) and keep the JSON internal unless
the user asks; for `LITE`/`MAX`/recovery show JSON first, then the short
human summary (user language). Orchestrated flows
MUST fetch `tools/validate_router_output.py` + `schemas/ROUTER_OUTPUT_SCHEMA.json`
(MANIFEST `entry_rules.orchestrated_flows_add`) alongside this router and run the validator on this JSON (structural checks,
sums, tier/role cuts, hard overrides, safety floor) — fail closed. In manual
chat the agent self-applies the same checks before fetching — EXCEPT agents
with shell access (CLI agents, Claude Code, Codex): they MUST fetch and run
`tools/validate_router_output.py` on their JSON instead of self-applying;
live testing showed self-checks miss rubric violations.

```json
{
  "router_version": 3,
  "protocol_version": 4,
  "entry_mode": "questionnaire",
  "task_type": "build",
  "task_type_secondary": [],
  "task_type_confidence": "high",
  "playbook": "playbooks/PLAYBOOK_generic.md",
  "blocks": [],
  "bootstrap_mode": "new_project",
  "bootstrap_tier": "LITE",
  "daily_loop_file": null,
  "role_mode": "SOLO",
  "strictness_score": 18,
  "independence_score": 10,
  "hard_overrides": [],
  "clarified_task": {
    "goal": "public kitten gallery site for a shelter",
    "inputs": "photos + texts in content/, no code yet",
    "outputs": "static site, one page per kitten + gallery index",
    "format": "static HTML/CSS, RU content, deploy-ready folder",
    "constraints": "no paid services; stack at agent's discretion",
    "done_criteria": "opens locally, all kittens listed, owner approves look",
    "slot_sources": {
      "goal": "stated",
      "inputs": "asked",
      "outputs": "inferred",
      "format": "asked",
      "constraints": "asked",
      "done_criteria": "asked"
    }
  },
  "assumptions": [
    "S4=0 — user confirmed no source photo mutation",
    "stack: static site generator chosen by agent",
    "I4=0 — single engine in this run (stated)"
  ],
  "corpus_size_hint": "small",
  "files_to_fetch": [
    "playbooks/PLAYBOOK_generic.md",
    "core/LITE.md"
  ],
  "do_not_fetch": [
    "core/PRINCIPLES_MAX.md"
  ],
  "reason": [
    "multi-session build, low risk, no destructive ops"
  ],
  "independence_gap": false,
  "next_action": "fetch selected files, assemble runtime prompt, begin execution",
  "strictness_breakdown": {
    "S1": {
      "score": 5,
      "basis": "inferred"
    },
    "S2": {
      "score": 8,
      "basis": "asked"
    },
    "S3": {
      "score": 0,
      "basis": "inferred"
    },
    "S4": {
      "score": 0,
      "basis": "asked"
    },
    "S5": {
      "score": 0,
      "basis": "asked"
    },
    "S6": {
      "score": 0,
      "basis": "inferred"
    },
    "S7": {
      "score": 0,
      "basis": "inferred"
    },
    "S8": {
      "score": 0,
      "basis": "inferred"
    },
    "S9": {
      "score": 5,
      "basis": "stated"
    }
  },
  "independence_breakdown": {
    "I1": {
      "score": 10,
      "basis": "inferred"
    },
    "I2": {
      "score": 0,
      "basis": "inferred"
    },
    "I3": {
      "score": 0,
      "basis": "inferred"
    },
    "I4": {
      "score": 0,
      "basis": "profile"
    },
    "I5": {
      "score": 0,
      "basis": "inferred"
    },
    "I6": {
      "score": 0,
      "basis": "profile"
    }
  }
}
```

## Runtime header (prepend to assembled prompt)

```text
ROUTER_SELECTION:
task_type: <build|analyze|research|write|review|operate|plan|other>
playbook: <path>
blocks: <list|none>
bootstrap_mode: <new_project|existing_agent_wiki|recovery_needed>
bootstrap_tier: <TASK|LITE|MAX|null>
daily_loop_file: <core/PRINCIPLES_MINI.md|null>
role_mode: <SOLO|DUAL|FULL>
clarified_task: <one-line digest of the six slots>
files_loaded: <list>
Do not assume unavailable lanes exist.
SOLO: one agent covers all lanes; mark any independence gap.
DUAL: implementer + one reviewer (review + audit folded).
FULL: separate implement / review / audit lanes.
```

## Hard routing rules

- Never fetch all files "just in case"; never fetch MAX when LITE is enough;
  never fetch LITE when TASK is enough.
- Questions to the user: one batch, user language, only routing-relevant or
  missing-slot questions.
- Safety-floor criteria are never assumed downward.
- If GitHub is unavailable, ask the user for the exact selected files only.
- Core purity: routing may propose new playbooks/adapters; it never writes
  domain content into core files.
