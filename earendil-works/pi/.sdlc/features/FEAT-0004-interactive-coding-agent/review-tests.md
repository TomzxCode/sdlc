---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### A listed test file does not exist
- **Evidence:** `packages/coding-agent/test/` contains `clipboard.test.ts`, `clipboard-command.test.ts`, `clipboard-image.test.ts`, `clipboard-image-bmp-conversion.test.ts`, `clipboard-image-native-errors.test.ts`, and `clipboard-paste-file-paths.test.ts`. There is no `clipboard-native.test.ts`.
- **Artifact says:** "Clipboard handling (clipboard.test.ts, clipboard-native.test.ts, clipboard-image.test.ts, clipboard-image-bmp-conversion.test.ts)".
- **Required change:** Replace `clipboard-native.test.ts` with the files that exist (`clipboard-command.test.ts`, `clipboard-image-native-errors.test.ts`, `clipboard-paste-file-paths.test.ts`). Blocking.

### The `test/session-manager/` suite is not referenced
- **Evidence:** `packages/coding-agent/test/session-manager/` holds 8 test files: `build-context.test.ts`, `custom-session-id.test.ts`, `file-operations.test.ts`, `labels.test.ts`, `load-entries.test.ts`, `migration.test.ts`, `save-entry.test.ts`, `tree-traversal.test.ts`. They cover the session file header, entry read/write, label entries, and the v1 to v2 and v2 to v3 entry migrations (`packages/coding-agent/src/core/session-manager.ts:286-352`).
- **Artifact says:** The Unit Tests section lists only files directly under `packages/coding-agent/test/` and `test/suite/`. The `test/session-manager/` directory is never mentioned.
- **Required change:** Add a bullet for the `test/session-manager/` suite. Blocking.

### The MCP conformance suite is not referenced
- **Evidence:** `packages/coding-agent/test/mcp-conformance/` holds `client.ts` (pi as an MCP client), `run.ts` (runs `@modelcontextprotocol/conformance@0.2.0-alpha.11` over protocol versions `2025-03-26`, `2025-06-18`, `2025-11-25`), `baseline.json` (the committed pass/fail baseline), and `README.md`. It is a separate CI job invoked by `npm run test:mcp-conformance` and documented in `packages/coding-agent/test/mcp-conformance/README.md:9`.
- **Artifact says:** The Integration Tests section lists only the `test/suite/` harness tests and the `test/suite/regressions/` files. The conformance suite is not mentioned.
- **Required change:** Add the MCP conformance suite as a separate integration-test group, noting that it needs network access on the first run and is compared against `baseline.json`. Blocking.

### The Coverage Matrix has no rows for FR-13, FR-14, or NFR-01, NFR-03, NFR-04, NFR-05
- **Evidence:** FR-13 is covered by `packages/coding-agent/test/first-time-setup.test.ts` and `packages/coding-agent/test/first-time-setup-fork.test.ts` (the flow at `packages/coding-agent/src/cli/startup-ui.ts:132-201`, gated by `PI_EXPERIMENTAL=1`). FR-14 is covered by `packages/coding-agent/test/package-manager.test.ts`, `packages/coding-agent/test/package-command-paths.test.ts`, `packages/coding-agent/test/package-distribution.test.ts`, and `packages/coding-agent/test/package-manager-ssh.test.ts`. NFR-04 (offline startup) is covered by `packages/coding-agent/test/stdout-cleanliness.test.ts` and the `PI_OFFLINE` handling in `packages/coding-agent/src/main.ts:578-580`.
- **Artifact says:** The Coverage Matrix has rows for FR-01 through FR-12 and NFR-02 only.
- **Required change:** Add rows for FR-13, FR-14, and NFR-01 through NFR-05, pointing at the files above, or state that the matrix is partial. Blocking.

### The `test/suite/` description misses two integration tests
- **Evidence:** `packages/coding-agent/test/suite/` contains 15 integration test files plus the `harness.ts` and `mcp-oauth-server.ts` support files. Two of them do not match the `suite/agent-session-*.test.ts` glob used by the artifact: `packages/coding-agent/test/suite/lax-message-content.test.ts` and `packages/coding-agent/test/suite/virtual-models.test.ts`.
- **Artifact says:** "Suite tests (suite/agent-session-*.test.ts) using the harness + faux provider" and "Suite tests under `test/suite/` use the coding-agent test harness with a faux provider for full prompt-loop testing without real API calls".
- **Required change:** Name the two extra suite tests, or say "the 15 integration tests under `test/suite/`". Advisory.

### The `test/fixtures/` directory is not referenced
- **Evidence:** `packages/coding-agent/test/fixtures/` holds `before-compaction.jsonl` (2.3 MB), `large-session.jsonl` (974 KB), `assistant-message-with-thinking-code.json`, `fake-external-editor.mjs`, `empty-agent/`, `empty-cwd/`, `skills/` (12 skill fixtures), and `skills-collision/`.
- **Artifact says:** The "Test Infrastructure" section lists the harness, the in-memory session manager, and the controlled bash process lifecycle. Fixtures are not mentioned.
- **Required change:** Add the fixtures directory to Test Infrastructure. Advisory.

### The JSON run mode has no dedicated test file
- **Evidence:** `--mode json` is only exercised indirectly: `packages/coding-agent/test/args.test.ts:159-191` (argument parsing) and `packages/coding-agent/test/stdout-cleanliness.test.ts:101` (`--mode json --help`). The streaming behaviour is covered by the regressions `packages/coding-agent/test/suite/regressions/7911-json-stream-usage.test.ts` and `packages/coding-agent/test/suite/regressions/7290-json-stream-linear.test.ts`.
- **Artifact says:** Coverage Matrix row "FR-06 (Run modes) | print-mode.test.ts, rpc.test.ts".
- **Required change:** Add the JSON-mode coverage that exists (the two regression files and `args.test.ts`), or add a dedicated `json-mode` test file to close the gap. Advisory.

### The artifact does not state the size of the suite
- **Evidence:** `packages/coding-agent/test/` is flat with 196 top-level `*.test.ts` files, plus `test/session-manager/` (8), `test/suite/` (15 integration + 2 support), `test/suite/regressions/` (81), and `test/mcp-conformance/` (2 sources plus a baseline). The runner is Vitest (`packages/coding-agent/vitest.config.ts`); the root `./test.sh` runs the monorepo suite under an isolated `HOME` with no API keys.
- **Artifact says:** "Test files under `packages/coding-agent/test/` cover:" followed by a selected list, with no count and no statement that the list is partial.
- **Required change:** State the layout and counts so the list is read as a selection, and name the runner. Advisory.

## Open questions
- The artifact's 2026-10-13 drift section says `test/suite/regressions/` holds "~80 regression files". The current count is 81, and the naming convention (`<issue>-<slug>.test.ts`) still holds.
- The MCP conformance baseline (`packages/coding-agent/test/mcp-conformance/baseline.json`) records scenarios that are expected to fail, such as `auth/scope-retry-limit`. Whether those should stay baselined is a product decision the code cannot answer.
