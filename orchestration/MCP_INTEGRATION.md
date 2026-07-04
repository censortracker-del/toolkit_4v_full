# MCP_INTEGRATION.md - Optional Tool Access

MCP is an optional runtime/tooling layer. It is not the Agent Wiki memory
protocol and must not be required for manual use.

## Use MCP When

- GitHub fetch needs a standardized tool layer.
- File-driven intake needs filesystem inventory.
- A project explicitly needs database inspection.
- Browser/search is required for fresh or external evidence.
- A team workflow needs issue tracker or document store access.

## Do Not Use MCP When

- Manual chat handoff is enough.
- The project is small and files can be provided directly.
- A tool would add more context/schema overhead than value.

## Minimal Tool Sets

- GitHub only: fetch manifest and selected prompt files.
- Filesystem: inventory, sample, detect Agent_Wiki, write allowed outputs.
- Database: read-only by default; writes require explicit confirmation.
- Browser/search: record source URL, title, date, checked_at, support status.

## Safety

- Load only the servers needed for the current task.
- Read-only by default.
- Mutating actions require dry-run plus explicit user confirmation unless a
  project is explicitly configured for trusted automation.
- Log mutations in `Agent_Wiki/Project/Change_Log.md`.
- Never store credentials in markdown, prompts, logs, screenshots, or reports.

## Schema Hint

`SOURCE_INVENTORY_SCHEMA.json` carries `tooling_recommendation`:

```json
{
  "mcp_needed": false,
  "recommended_servers": ["none"],
  "reasoning": "",
  "mutation_allowed": false,
  "requires_user_confirmation": true
}
```
