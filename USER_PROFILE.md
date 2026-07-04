# USER_PROFILE.md — durable defaults for the intake router

Agent-facing (EN). The bot reads this BEFORE asking router questions and skips any
question this profile already answers. Per-project questions are NOT here — they
are asked fresh every project. These are defaults; project risk OVERRIDES them.

## Identity / conventions (always apply)
- user-facing notes: RU. agent-facing files (protocols, profiles, briefs): EN.
- secrets: never in any file/log/prompt/screenshot/export. Hard rule.
- style: direct, concise, no hedging/preamble; minimal formatting.

## Router defaults — Agent Independence axis only
(Strictness axis is ALWAYS per-project. Do not pre-answer strictness here.)

- engines available: three-role workflow available (implement lane + review lane +
  audit lane, agents available). → independence Q4 = 15 (stable; skip the question).
- token/cost sensitivity: extreme token saving preferred. → independence Q6 = -15
  by DEFAULT. **OVERRIDE to +10 when the project has data-loss / legal / financial
  / government-submission risk** — accuracy and audit beat tokens there. Do not let
  the -15 default pull a high-stakes project down a role_mode tier.
- manual verification: user is a deep technical expert (Oracle/SQL/data). Often
  "partly" (5). Still per-project — volume decides; do not hardcode.

## Agent-lane map (role_mode is about LANES, not vendor names)
The toolkit's role_mode (SOLO/DUAL/FULL) means lane coverage, not specific products.
Map lanes to whatever agents are actually used on the project:
- implement lane: Codex, OR a local model (e.g. Assembler), OR Claude Code.
- review/semantic lane: Claude, OR a local Reviewer.
- audit/safety lane: OpenCode, OR a second independent local pass.
- For a local-model pipeline (Ollama/LM Studio), FULL may = User + Parser +
  Assembler + Reviewer, not User+Claude+Codex+OpenCode. Same lanes, different agents.

## Manual vs API preference
- Default workflow: manual chat handoff (path / entry_id / feedback_N, never full
  history) unless the project explicitly needs API/orchestration.

## Typical project shape (hint, NOT a score)
User's projects skew toward data/pipeline/Oracle/government work, which TENDS to
score high on strictness. This is a hint to expect MAX-tier often — it is NOT a
pre-filled score. Always run the strictness questions; never assume the tier.
