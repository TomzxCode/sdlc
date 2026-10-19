---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The architecture describes one renderer; the code has two behind a shared interface
- **Evidence:** `packages/tui/src/tui.ts:464-493` defines the `TUI` interface; `packages/tui/src/tui.ts:506` defines the shared `TuiBase`; `packages/tui/src/tui-main-screen.ts:124` implements `TuiMainScreen` (`mode = "regular"`, linear document, terminal keeps scrollback); `packages/tui/src/tui-alt-screen.ts:202-204` implements `TuiAltScreen` (`mode = "fullscreen"`, `readonly [VIEWPORT_TUI] = true`, fixed-height viewport with application-owned scrolling). `packages/tui/README.md:7,59-62` documents them as interchangeable renderers.
- **Artifact says:** The architecture diagram has a single "TUI (manager)" box feeding a single "differential write" box; neither `TuiMainScreen` nor `TuiAltScreen` is named anywhere in the artifact.
- **Required change:** Show the `TUI` interface with the two concrete renderers, and state the difference in document model (linear scrollback document vs. fixed viewport) and in full-redraw behaviour. Blocking.

### The "Key" data model does not exist in the code
- **Evidence:** `packages/tui/src/keys.ts:152` — `export type KeyId = BaseKey | ModifiedKeyId<BaseKey>`; a key id is a **string** such as `"ctrl+c"` or `"shift+tab"`. `packages/tui/src/keys.ts:163` — `Key` is a constant helper namespace of string literals (`Key.enter`, `Key.ctrl("c")`), not a data object. `packages/tui/src/keys.ts:520` — `export type KeyEventType = "press" | "repeat" | "release"`. `packages/tui/src/keys.ts:1292` — `parseKey(data: string): string | undefined` returns a key-id string, not an object. No key model anywhere carries boolean modifier flags or a `paste` flag; bracketed paste is a terminal mode marker (`\x1b[200~`) handled by `StdinBuffer` and the `Editor`, and only special-cased in `isKeyRelease`/`isKeyRepeat` (`packages/tui/src/keys.ts:542-549, 572-577`).
- **Artifact says:** A "Key" data model with `key: string`, `ctrl/alt/shift: boolean`, and `paste: boolean`.
- **Required change:** Replace the table with the real model: `KeyId` string union, the `Key` helper namespace, `KeyEventType` (`press|repeat|release`), and `parseKey`/`matchesKey` returning key-id strings. Blocking.

### The Component data model has the wrong `handleInput` signature and omits mouse handling
- **Evidence:** `packages/tui/src/tui.ts:126` — `handleInput?(data: string): void;` (returns `void`, it does not report consumption). `packages/tui/src/tui.ts:129` — `handleMouse?(event: TuiMouseEvent): TuiMouseEventResult | undefined;`. `packages/tui/src/tui.ts:135` — `wantsKeyRelease?: boolean;`. `packages/tui/src/tui.ts:141` — `invalidate(): void;` (required).
- **Artifact says:** `handleInput | (data) => boolean | optional | Returns true if input consumed`; the table has no `handleMouse` row.
- **Required change:** Correct the `handleInput` signature to `void`, add the `handleMouse` row, and keep `wantsKeyRelease` and `invalidate` as declared. Blocking.

### The OverlayOptions data model is wrong and incomplete
- **Evidence:** `packages/tui/src/tui.ts:254-290` — `width?: SizeValue` and `maxHeight?: SizeValue` where `SizeValue = number | \`${number}%\`` (`packages/tui/src/tui.ts:236`); `minWidth?: number`; `anchor?: OverlayAnchor`, a union of 9 named positions (`packages/tui/src/tui.ts:214-223`); `offsetX?: number`, `offsetY?: number`; `row?: SizeValue`, `col?: SizeValue`; `margin?: OverlayMargin | number` with per-side `top/right/bottom/left` (`packages/tui/src/tui.ts:228-234, 279`); `visible?: (termWidth: number, termHeight: number) => boolean` (`packages/tui/src/tui.ts:287`); `nonCapturing?: boolean`.
- **Artifact says:** `anchor | object`, `margins | object`, `visible | () => boolean`; it lists no `width`, `minWidth`, `maxHeight`, `offsetX`, `offsetY`, `row`, or `col`.
- **Required change:** Replace the table with the real `OverlayOptions` shape, including `SizeValue` percentages, the `OverlayAnchor` union, `margin` as number-or-per-side, and `visible(termWidth, termHeight)`. Blocking.

### The differential-render sequence omits the full-redraw triggers and the alt-screen path
- **Evidence:** `packages/tui/src/tui-main-screen.ts:339-361` — width change and height change (skipped under Termux, `isTermuxSession()` at `:109-111`) force a full redraw; `:357` — `clearOnShrink` with content below `maxLinesRendered` and no overlays forces one. `packages/tui/src/tui-main-screen.ts:401-423` — deletions that move the viewport above the content start, or `extraLines > height`, force one. `:452-456` — a first changed line above the previous viewport top forces one. `:496-504` — a Kitty image pre-clear that would scroll forces one. The alt screen builds each frame through `renderLayoutFrame` (`packages/tui/src/layout.ts:379`) and rewrites only changed rows, with a full redraw on width/height change.
- **Artifact says:** The sequence lists "if first render", "elif full re-render", and "else (differential)" with no trigger conditions, and no alt-screen path at all.
- **Required change:** List the full-redraw trigger conditions and add the alt-screen (viewport/layout) render path. Blocking.

### `matchesKey` is described as a configurable-binding lookup
- **Evidence:** `packages/tui/src/keys.ts:859` — `export function matchesKey(data: string, keyId: KeyId): boolean` compares raw terminal input against a single key id. Configurable bindings are resolved by `KeybindingsManager.matches(data, keybinding)` (`packages/tui/src/keybindings.ts:270-276`) over `TUI_KEYBINDINGS` (`packages/tui/src/keybindings.ts:71-210`).
- **Artifact says:** "`matchesKey(keyData, binding)` compares parsed keys against configurable bindings."
- **Required change:** State that `matchesKey(data, keyId)` is a single-id comparison and that the configurable-binding lookup is `KeybindingsManager.matches` / `getKeybindings()`. Advisory.

### The throttling decision omits the immediate-render path
- **Evidence:** `packages/tui/src/tui.ts:518` — `MIN_RENDER_INTERVAL_MS = 16`; `scheduleRender` at `:1035-1053` enforces it. But keyboard input takes the immediate path: `requestImmediateRender()` (`:1012-1027`) is called from `handleTerminalInput` (`:1129`) and deliberately bypasses the 16 ms tick.
- **Artifact says:** "Throttling | ~60fps with nextTick coalescing", and the sequence's "TUI (next tick, if >= MIN_RENDER_INTERVAL_MS)".
- **Required change:** Note that input-driven renders bypass the throttle for latency, and that `requestRender(force = true)` renders immediately. Advisory.

### The architecture diagram places `VirtualTerminal` in the production data flow
- **Evidence:** `VirtualTerminal` is a test-only double at `packages/tui/test/virtual-terminal.ts`, built on `@xterm/headless` (`packages/tui/package.json:59`); it is not exported from `packages/tui/src/index.ts` and does not exist in `src/`.
- **Artifact says:** The diagram's "Terminal interface" box reads "(ProcessTerminal / VirtualTerminal)".
- **Required change:** Mark `VirtualTerminal` as a test double, or drop it from the production diagram. Advisory.

### The Data Models section omits the public render-state API
- **Evidence:** `packages/tui/src/tui-main-screen.ts:113-121` — `export interface TuiMainScreenRenderState`; `:135` `captureRenderState()`; `:147` `restoreRenderState(state)`. It is exported from the package root (`packages/tui/src/index.ts:185`).
- **Artifact says:** The Data Models section covers only `Component`, `OverlayOptions`, and `Key`.
- **Required change:** Add `TuiMainScreenRenderState` to the data models. Advisory.

## Open questions
- None. Every claim checked against the code was resolvable; the remaining gaps are missing coverage rather than ambiguity.
