---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Test Plan for Node Host and Device Execution

## Sync drift: 2026-11-16

### Most current node-host test files are not documented in the plan (non-blocking)

- Evidence: `src/node-host/` contains 96 `*.test.ts` files and tests.md names 12 of them, leaving 84 undocumented suites.
- Artifact says: tests.md:15 states that every test file listed below was confirmed to exist, which is still true, but the plan does not claim to be exhaustive.
- Code: undocumented suites add coverage for OpenClaw ID enrollment and transport (`openclaw-id-*.test.ts`), config (`config.test.ts`), connection (`connection.test.ts`, `gateway-candidate-connection.test.ts`), exec policy (`exec-policy.test.ts`, `plugin-exec-policy.test.ts`), host stats, MCP (`invoke.mcp.test.ts`, `mcp-elicitation*.test.ts`, `mcp.cancellation.integration.test.ts`, `node-worker-mcp.authority.integration.test.ts`), plugin hosting (`plugin-node-host*.test.ts`), CLI agent runs (`invoke-agent-cli-claude.test.ts`, `claude-skill-session.test.ts`), runner inventory (`runner.inventory.test.ts`), runner shutdown and auto-update (`runner.shutdown.test.ts`, `runner.auto-update.test.ts`), supervisor lifecycle variants (`node-worker-supervisor.lifetime|reboot|recovery|settlement|startup|idle|container|device-folder.test.ts`), workspace variants (`node-worker-workspace-*.test.ts`), prepared workspaces (`node-worker-prepared-workspace*.test.ts`), transfers (`node-worker-transfer-client*.test.ts`), device folders, native inference, container engine, publication, and several system-run plan and environment variants.
- Impact: the coverage matrix at tests.md:86-107 does not reflect the current test suite and does not show which requirements the newer suites protect.
- Action: decide whether to extend tests.md with the new suites or record them as out of scope for this feature.

### No documented test file is missing (no drift)

- Evidence: all 12 node-host test files named in tests.md exist, along with all 5 Gateway node suites and the referenced helpers.
- Artifact says: tests.md:15 claims every listed file exists.
- Code: every listed path was confirmed present in the repository.
