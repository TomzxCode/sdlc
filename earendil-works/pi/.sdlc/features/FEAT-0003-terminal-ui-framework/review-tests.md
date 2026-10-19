---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The plan never states the test runner, and this package is not on Vitest
- **Evidence:** `packages/tui/package.json:13` — `"test": "node --test --test-reporter=dot --test-reporter-destination=stdout test/*.test.ts"`. `packages/tui` has no `vitest.config.ts` (every other test-bearing package does), and `packages/tui/test/*.test.ts` files import from `node:test` (`packages/tui/test/terminal-colors.test.ts:2`). The root `test.sh` reaches it through `npm run test --workspaces --if-present` (`package.json:40`).
- **Artifact says:** The plan never names a runner; it only says "Test files under `packages/tui/test/` cover: ...".
- **Required change:** State that this package runs on Node's built-in test runner (`node --test`), not Vitest, and that the glob is `test/*.test.ts`. A reader following the rest of the monorepo's Vitest convention would silently skip this package. Blocking.

### Scope and coverage matrix omit the alt-screen renderer, layout engine, mouse input, and search
- **Evidence:** `packages/tui/test/tui-alt-screen.test.ts` (~90 cases: viewport rendering, wheel routing and chaining, scrollbar drag, transcript search, OSC 133 prompt jumps, Kitty image placement and caching, text selection and OSC 52 copy, flash messages, CJK/emoji selection snapping), `packages/tui/test/layout.test.ts` (stack sizing, gaps, min sizes, scrollbar geometry, Kitty cropping), `packages/tui/test/mouse-components.test.ts` (nested mouse regions), `packages/tui/test/wheel-scroll.test.ts`.
- **Artifact says:** Scope: "Covers `pi-tui` rendering pipeline, components, key handling, terminal abstraction, overlays, and differential rendering." The Coverage Matrix has no row for layout, viewport rendering, mouse input, text selection, or transcript search, and the Unit Tests list mentions `tui-alt-screen.test.ts` and `layout.test.ts` only in the trailing "Additional coverage" sentence with no described coverage.
- **Required change:** Extend the Scope and add coverage rows for the alternate-screen viewport, the layout engine, mouse input, and transcript search, naming the cases each file covers. Blocking.

### Test Infrastructure names the wrong sequence for the color-scheme mock
- **Evidence:** `packages/tui/test/terminal-colors.test.ts:96-106` parses `CSI ? 997;1n` (dark) and `CSI ? 997;2n` (light) via `parseTerminalColorSchemeReport`; the OSC 11 replies in the same file (`:108-121`, `:138-161`) are RGB background-color replies consumed by `TuiBase.queryTerminalColors` (`packages/tui/src/tui.ts:1494-1516`).
- **Artifact says:** Test Infrastructure: "- Mock terminal color scheme (OSC 11)".
- **Required change:** Replace with the color-scheme report sequence (`CSI ? 997;1n` / `CSI ? 997;2n`) and list OSC 10/11/4 separately as the terminal color query. Blocking.

### The FR-12 coverage row cites no test file
- **Evidence:** `packages/tui/test/tui-render.test.ts:957-1020` ("TUI fake cursor") asserts the `CURSOR_MARKER` handling and the hardware-cursor column for both `showHardwareCursor` modes; `packages/tui/test/tui-render.test.ts:17` imports `CURSOR_MARKER` and `renderFakeCursor`.
- **Artifact says:** "| FR-12 (IME support) | (covered by tui-render cursor positioning) |".
- **Required change:** Cite the file and the case names, as every other matrix row does. Advisory.

### Test Infrastructure omits the non-test support and manual scripts in `test/`
- **Evidence:** `packages/tui/test/` also contains `key-tester.ts`, `test-themes.ts`, `chat-simple.ts` (demo app), `alt-screen-large-transcript-bench.ts` and `render-churn-bench.ts` (benchmarks), `viewport-overwrite-repro.ts` (repro script), `image-test.ts` (manual script, not matched by the `test/*.test.ts` glob), and `fixtures/`.
- **Artifact says:** Test Infrastructure lists only "- `VirtualTerminal` for headless render assertions".
- **Required change:** List the support files and manual scripts so readers know which files the runner glob picks up and which are run by hand. Advisory.

### The FR-16 coverage row does not flag that the Linux clipboard test is environment-gated
- **Evidence:** `packages/tui/test/native-clipboard-linux.test.ts:71` — `describe("native Linux clipboard", { skip: !dependenciesAvailable, timeout: 60000 }, ...)`; `packages/tui/native/linux/README.md` states the tests skip when Xvfb/xclip/pkg-config are missing.
- **Artifact says:** "| FR-16 (Native addons) | native-platform.test.ts, native-module-path.test.ts, native-clipboard-linux.test.ts |".
- **Required change:** Note that `native-clipboard-linux.test.ts` is skipped when the X11 build dependencies are absent, so its coverage is conditional. Advisory.

## Coverage reconciliation

Every one of the 43 `packages/tui/test/*.test.ts` files is named in the artifact, and no file named in the artifact is missing from the repository. The drift is in what the plan claims the files cover, not in which files it lists.

## Open questions
- None.
