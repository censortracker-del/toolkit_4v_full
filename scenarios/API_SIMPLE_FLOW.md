# API_SIMPLE_FLOW.md

Use this for a one-agent or simple API run.

## When To Use

- Single agent.
- Low or medium risk.
- No complex independent review.
- API should fetch selected prompts from GitHub and work with Agent_Wiki.

## Flow

1. API receives user request plus project description or files.
2. API fetches `MANIFEST.json`.
3. If files exist, fetch `intake/ADAPTIVE_INTAKE.md` and
   `schemas/SOURCE_INVENTORY_SCHEMA.json`.
4. If no files exist, fetch `intake/ROUTER.md` and
   `schemas/ROUTER_OUTPUT_SCHEMA.json`.
5. Agent produces routing/intake JSON.
6. User confirms blocking assumptions if needed.
7. API fetches only selected files.
8. Agent creates or continues Agent_Wiki.
9. Outputs go to Agent_Wiki, not long chat history.

## Safety

- No secrets in prompts or repo files.
- Mutating actions require dry-run plus explicit confirmation.
- Large/huge corpus requires corpus intake plan before heavy processing.
