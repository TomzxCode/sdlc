---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### FR-14 names the wrong terminal mechanism for color scheme detection
- **Evidence:** `packages/tui/src/terminal-colors.ts:42` — `COLOR_SCHEME_REPORT_PATTERN = /^(?:\x1b\[\?997;(1|2)n)+$/`; `parseTerminalColorSchemeReport` at `packages/tui/src/terminal-colors.ts:85-91` returns `"dark"` for `CSI ? 997;1n` and `"light"` for `CSI ? 997;2n`. OSC 11 is a different feature: it is the *background color query* answered as RGB (`packages/tui/src/terminal-colors.ts:41` `OSC_COLOR_RESPONSE_PATTERN`, consumed by `TuiBase.queryTerminalColors` at `packages/tui/src/tui.ts:1494-1516`, which reads OSC 10/11/4 colors, not a light/dark scheme).
- **Artifact says:** FR-14 (Should): "The system shall detect terminal color scheme (light/dark) via OSC 11."
- **Required change:** FR-14 must name the color-scheme report sequence (`CSI ? 997;1n` dark / `CSI ? 997;2n` light), and separately state that OSC 10/11/4 are queried to read terminal theme RGB colors. Blocking.

### FR-06 omits built-in components the package ships
- **Evidence:** `packages/tui/src/components/v-stack.ts:3` (`VStack`), `packages/tui/src/components/h-stack.ts:4` (`HStack`), `packages/tui/src/components/scroll-view.ts:22` (`ScrollView`), `packages/tui/src/components/mouse-region.ts:15` (`MouseRegion`), `packages/tui/src/tui.ts:358` (`Container`). All are exported from the package root (`packages/tui/src/index.ts:40-78,184`) and are listed as built-in components in `packages/tui/README.md:14`.
- **Artifact says:** FR-06 (Must) lists only `Editor`, `Text`, `TruncatedText`, `Input`, `Box`, `Markdown`, `SelectList`, `SettingsList`, `Loader`, `CancellableLoader`, `Image`, `Spacer`.
- **Required change:** Add `VStack`, `HStack`, `ScrollView`, `MouseRegion`, and `Container` to FR-06. Blocking.

### No requirement covers the alternate-screen renderer or the layout engine
- **Evidence:** `packages/tui/src/tui-alt-screen.ts:202` (`TuiAltScreen`, `mode = "fullscreen"`), `packages/tui/src/tui-main-screen.ts:124` (`TuiMainScreen`, `mode = "regular"`), `packages/tui/src/tui.ts:497-503` (`ViewportTUI`, `isViewportTUI`), `packages/tui/src/tui-alt-screen.ts:327` (`setLayoutRoot`), `packages/tui/src/layout.ts:379` (`renderLayoutFrame`), `packages/tui/src/components/stack.ts:4-22` and `:135` (`basis`/`grow`/`shrink`/`minSize`/`maxSize`/`gap`/`align`, `allocateStackSizes`).
- **Artifact says:** FR-02 (Must) describes a single `TUI` manager composing a linear document. `TuiMainScreen`, `TuiAltScreen`, `setLayoutRoot`, and the flexbox-like stack layout never appear in the artifact.
- **Required change:** Add a requirement for the two interchangeable renderers (main screen keeps terminal scrollback; alt screen owns a fixed-height, application-scrolled viewport) and one for the layout engine (`VStack`/`HStack` entry sizing and `ScrollView` region ownership), with the `ViewportTUI`/`setLayoutRoot` opt-in. Blocking.

### No requirement covers mouse input
- **Evidence:** `packages/tui/src/tui.ts:129` (`Component.handleMouse`), `packages/tui/src/tui.ts:25-58` (`TuiMouseEvent`, `TuiMouseEventResult`), `packages/tui/src/tui-alt-screen.ts:375-384` (SGR mouse tracking enabled on alt-screen start), plus wheel scrolling, scrollbar dragging, drag text selection with OSC 52 auto-copy, and OSC 8 link activation in `packages/tui/src/tui-alt-screen.ts`.
- **Artifact says:** FR-01 mentions only `render` and optional `handleInput`; no requirement mentions mouse input at any priority.
- **Required change:** Add a requirement for normalized mouse input (event types `press|release|move|drag|click|wheel`, hit-testing against the layout frame, wheel-to-`ScrollView` chaining, text selection) and note that the main screen does not enable mouse tracking so the terminal keeps scrollback. Blocking.

### NFR-01 and its acceptance criterion only hold for the main-screen renderer
- **Evidence:** `packages/tui/src/tui-main-screen.ts:518-545` — an over-wide line writes `pi-tui-crash.log` and throws. `packages/tui/src/tui-alt-screen.ts:414` and `:1699-1700` — the alt screen silently truncates the line with `sliceByColumn(line, 0, width, true)` and never errors.
- **Artifact says:** NFR-01 (Must): "Components shall return lines that do not exceed the provided width; the framework shall error otherwise." Acceptance criterion: "**Then** the framework raises an error rather than overflowing the terminal."
- **Required change:** Scope the error to `TuiMainScreen` and state that `TuiAltScreen` truncates over-wide lines to the viewport width instead of failing. Blocking.

### FR-11 does not state the alt-screen iTerm2 limitation
- **Evidence:** `packages/tui/src/tui-alt-screen.ts:356-359` — on alt-screen start, `capabilities.images === "iterm2"` forces `setCapabilities({ ...capabilities, images: null })`, so the `Image` component (`packages/tui/src/components/image.ts:106-160`) emits its text fallback rather than an iTerm2 inline image. Kitty images are still rendered in alt mode.
- **Artifact says:** FR-11 (Should): "The system shall support terminal image protocols (Kitty and iTerm2 inline images) with capability detection."
- **Required change:** State that iTerm2 inline images are main-screen only; the alt screen falls back to a text placeholder for iTerm2 while keeping Kitty support. Advisory.

### FR-01 describes an incomplete `Component` contract
- **Evidence:** `packages/tui/src/tui.ts:117-142` — the interface is `render(width): string[]`, `handleInput?(data: string): void`, `handleMouse?(event) => TuiMouseEventResult | undefined`, `wantsKeyRelease?: boolean`, and the **required** `invalidate(): void`.
- **Artifact says:** FR-01 (Must): "components implement `render(width): string[]` and optional `handleInput`." `invalidate()` is not mentioned and is not optional.
- **Required change:** Name `invalidate()` as required and list `handleMouse` and `wantsKeyRelease` as optional members. Advisory.

### FR-16 omits the shipped Linux native addon
- **Evidence:** `packages/tui/native/linux/` ships prebuilds for `linux-arm64` and `linux-x64`; `packages/tui/src/native-platform.ts:61-64` loads the `linux-x11` helper when `DISPLAY` is set; `packages/tui/native/linux/README.md` documents X11 text and image reads only. `packages/tui/src/native-platform.ts:56-59` returns `undefined` on Linux, so modifier-key state remains darwin/win32 only (`packages/tui/src/native-modifiers.ts:6-12`).
- **Artifact says:** FR-16 (May): "The system shall ship native addons for win32 and darwin to report modifier-key state."
- **Required change:** Add the Linux X11 clipboard helper to FR-16, and answer Open Question 1: the Linux addon exists but is clipboard-only; no Linux modifier-key path is implemented. Advisory.

### Constraints omit the package's import surface
- **Evidence:** `packages/tui/package.json:6,53` — `"main": "dist/index.js"`, `"types": "./dist/index.d.ts"`, and no `exports` map and no `bin`. Only the root entry is importable; subpath imports are not supported.
- **Artifact says:** Constraints lists only "No React, no Ink, no virtual DOM", "Dependencies kept minimal (`get-east-asian-width`, `marked`)", and "Erasable TypeScript syntax only; ESM only".
- **Required change:** Add the packaging constraint (root-only entry point, no `exports` map, no `bin`). Advisory.

## Open questions
- FR-16's Linux clipboard addon is now implemented, so Open Question 1 is answered by the code. Open Question 2 ("policy for adding new built-in components") is not answered by the code; it remains a product decision.
