---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Control UI test plan

## Sync drift: 2026-10-19

### Three of the ten listed test files no longer exist (blocking)

- Evidence: `ui/src/app/router-outlet.test.ts` is absent, `ui/src/app/gateway-store.test.ts` is absent, `ui/src/components/app-sidebar.test.ts` is absent, `ui/src/app/app-host.test.ts` exists, `ui/src/app/theme.test.ts` exists, `ui/src/app/custom-theme.test.ts` exists, `ui/src/app/control-ui-chunking.test.ts` exists, `ui/src/app/agent-selection.test.ts` exists, `ui/src/app/native-bridge.test.ts` exists, `ui/src/components/markdown.test.ts` exists
- Artifact says: the unit test table lists `ui/src/app/router-outlet.test.ts`, `ui/src/app/gateway-store.test.ts`, and `ui/src/components/app-sidebar.test.ts` (tests.md:17, tests.md:21, tests.md:24).
- Code: the three files were split or removed. The gateway store now has focused suites under `ui/src/app/`, including `ui/src/app/gateway-store.auth.test.ts`, `ui/src/app/gateway-store.availability.ts` and `ui/src/app/gateway-store.credentials.ts`, `ui/src/app/gateway-store.device-credential.test.ts`, `ui/src/app/gateway-store.observers.test.ts`, `ui/src/app/gateway-store.plugins.test.ts`, `ui/src/app/gateway-store.presence.test.ts`, `ui/src/app/gateway-store.retention.test.ts`, and `ui/src/app/gateway-store.self-profile.test.ts`. The sidebar has fifty suites under `ui/src/components/app-sidebar*.test.*`. Routing is covered by `ui/src/app-routes.test.ts`, `ui/src/app-route-paths.test.ts`, `ui/src/app/route-transition.test.ts`, and `ui/src/app/app-host.deleted-session-routing.test.ts`.
- Blocking: the plan points a reviewer at three files that cannot be opened, and the coverage matrix below names two of them.

### The coverage matrix names two deleted files (blocking)

- Evidence: `tests.md:47-48`, `tests.md:51`, `ui/src/app/gateway-store.test.ts` is absent, `ui/src/app/app-host.test.ts` exists
- Artifact says: "| FR-1 (Chat interface) | `gateway-store.test.ts`, `app-host.test.ts` |" and "| FR-2 (Streaming) | `gateway-store.test.ts` |" and "| FR-4 (Session management) | `gateway-store.test.ts` |" and "| FR-5 (Gateway status) | `gateway-store.test.ts` |" (tests.md:47-51).
- Code: `gateway-store.test.ts` does not exist, so four of the six mapped requirements point at a file that cannot be opened. The coverage now lives in the split gateway-store suites listed above and in the browser and e2e lanes under `ui/src/e2e/`.
- Blocking: the matrix is the plan's main index, and most of its entries are dangling.

### The test infrastructure still names Lit testing utilities (blocking)

- Evidence: `ui/package.json:58` (`@solidjs/testing-library` `1.0.0-beta.3`), `ui/package.json:61` (`@vitest/browser` `5.0.3`), `ui/package.json:62` (`@vitest/browser-playwright` `5.0.3`), `ui/vitest.config.ts:1-40` (`playwright` and `chromium` browser project), `grep -rl "@solidjs/testing-library" ui/src` returns 38 files
- Artifact says: "## Test Infrastructure" lists "- Vitest unit test runner", "- Lit testing utilities", "- Mock WebSocket for gateway store tests", "- Component fixtures for rendering tests" (tests.md:38-41).
- Code: the runner is still Vitest, but rendering tests use `@solidjs/testing-library`, and the suite runs in a real Playwright Chromium browser project through `@vitest/browser-playwright`. There is no Lit test utility anywhere in the tree.
- Blocking: the plan instructs a contributor to set up a test stack the repository has replaced.

### The scope statement understates the suite by two orders of magnitude (blocking)

- Evidence: `tests.md:10`, `find ui/src -name "*.test.ts" -o -name "*.test.tsx"` returns 2753 files, `find ui/src -name "*.browser.test.ts" -o -name "*.browser.test.tsx"` returns 200 files, `find ui/src/e2e -name "*.test.ts"` returns 812 files, `ls ui/src/e2e/` lists 918 entries
- Artifact says: "Tests cover UI components, routing, theming, gateway store interaction, agent selection, markdown rendering, and native bridge functionality. Does not cover gateway server behavior or browser compatibility." (tests.md:10)
- Code: the Control UI has roughly 2,753 unit and component test files, 200 Playwright browser tests, and 812 e2e tests. The plan describes a suite of about ten files. The claim that browser compatibility is not covered is also wrong, because the browser project runs those 200 browser tests.
- Blocking: the scope statement is a material misdescription of the suite.

### The edge case table does not mention the failure modes the code now handles (advisory)

- Evidence: `tests.md:29-34`, `ui/src/app/browser-auth-recovery.tsx`, `ui/src/app/bootstrap-location.ts`, `ui/src/app/boot-record.ts`, `ui/src/app/session-route-recovery.test.ts`, `ui/src/app/bootstrap.warm-boot.test.ts`
- Artifact says: the edge case table covers gateway disconnected, empty session list, large response streaming, and invalid theme config (tests.md:29-34).
- Code: the UI also handles stale-build recovery, warm boot and cross-tab boot coordination, browser auth recovery, route recovery after a deleted session, and a boot record.
- Advisory: the table is not wrong, only incomplete.

### The terminal, desktop, editor, and plugin view surfaces have no test entry (advisory)

- Evidence: `ui/src/components/terminal/`, `ui/src/components/desktop/desktop-client.test.ts`, `ui/src/pages/chat/components/file-editor-view.ts`, `ui/src/plugins/control-ui-view.test.tsx`, `ui/src/plugins/control-ui-contributions.test.ts`, `ui/src/plugins/control-ui-dashboard.test.ts`
- Artifact says: none of these areas appear in the plan (tests.md:12-35).
- Code: each shipped subsystem has its own test suites, including a terminal panel suite, a desktop client suite, plugin view and contribution suites, and a plugin dashboard suite.
- Advisory: a reader of the plan would not know the new surfaces are tested.
