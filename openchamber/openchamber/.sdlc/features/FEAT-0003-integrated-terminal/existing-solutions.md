---
issue: ""
title: "Integrated Terminal"
status: draft
---

# Existing Solutions: Integrated Terminal

## Overview

OpenChamber's integrated terminal is already fully implemented using `ghostty-web` (WASM-compiled Ghostty terminal emulation) for the browser renderer and `bun-pty`/`node-pty` for server-side PTY management, with a custom WebSocket protocol (`TERMINAL_WS_PROTOCOL.md`) for input/output relay. The recommendation is to continue with this stack, which is modern, well-architected, and already covers all functional requirements. The main area of improvement is potential migration from the coder/ghostty-web fork to an official Ghostty WASM distribution once available.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/terminal/` (runtime.js, terminal-ws-protocol.js, output-replay-buffer.js, DOCUMENTATION.md, TERMINAL_WS_PROTOCOL.md), `packages/ui/src/components/terminal/TerminalViewport.tsx` (ghostty-web integration), `packages/ui/src/components/views/TerminalView.tsx` (full terminal view with tabs), `packages/ui/src/stores/useTerminalStore.ts`, `packages/ui/src/lib/terminalTheme.ts`, `packages/ui/src/lib/terminal/SerializeAddon.ts`, `package.json` (ghostty-web ^0.4.0) |
| Open-source | Yes | ghostty-web (coder/ghostty-web), ghostty-web (remorses/ghostty-web), @wterm/ghostty, xterm.js, hterm, ttyd, wetty |
| Commercial / SaaS | Yes | VS Code integrated terminal, Hyper terminal, Warp terminal, iTerm2 web integration |
| Standards / protocols | Yes | WebSocket (RFC 6455), PTY (POSIX), VT100/xterm escape sequences, ANSI escape codes, UTF-8 (RFC 3629) |
| Reference material | Yes | ghostty-web README and API docs, xterm.js API docs, bun-pty docs, node-pty docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| ghostty-web (coder/ghostty-web, current) | Library | MIT | Active (2.5K stars) | FR-01, FR-02, FR-03, FR-04, NFR-01, NFR-02, NFR-03 | FR-07 (mobile keyboard), NFR-04 (capacity limit) |
| xterm.js | Library | MIT | Mature (27K stars) | FR-01 through FR-04 | No WASM parser, complex script issues, may need migration from current implementation |
| internal runtime (`packages/web/server/lib/terminal/runtime.js`) | Internal | MIT | Ship-ready | FR-01, FR-02, FR-03, NFR-01, NFR-02, NFR-04 (429 enforcement) | FR-04 (control keys relayed by client, server passes through) |
| @wterm/ghostty | Library | MIT | Active | Same as ghostty-web, different build approach | Smaller community, depends on upstream ghostty |

## Evaluation

### ghostty-web (coder/ghostty-web, current)

- **Strengths:** WASM-compiled Ghostty parser — battle-tested VT100 implementation used in the native Ghostty app. xterm.js-compatible API (drop-in replacement). Zero runtime dependencies beyond the ~400KB WASM bundle. Proper Unicode grapheme handling (Devanagari, Arabic). Full SGR attribute support. Canvas-based rendering at 60 FPS. Actively maintained (20 contributors, latest release v0.4.0).
- **Weaknesses:** Relatively new (first published Nov 2025). ~400KB WASM bundle added to page weight. Some API differences from xterm.js. Open issues: 48.
- **Integration effort:** Already integrated. TerminalViewport.tsx has full integration with Ghostty load, FitAddon, theme conversion, font preferences.
- **Cost:** MIT (free).
- **Risks:** Low. Ghostty is a well-respected terminal emulator. The WASM approach is architecturally sound. The coder/ghostty-web project is actively maintained.

### xterm.js

- **Strengths:** The most widely used web terminal library (VS Code, Hyper, many others). Massive community and ecosystem of addons (fit, search, serialize, etc.). Battle-tested across millions of users. 27K GitHub stars.
- **Weaknesses:** Reimplements terminal emulation in JavaScript — all escape sequences manually coded. Known issues with complex scripts (Devanagari, Arabic). No WASM parser. Would require migrating away from ghostty-web, which is already integrated and working well.
- **Integration effort:** Medium. Different API, different addon system, would need to rewrite TerminalViewport.tsx.
- **Cost:** MIT (free).
- **Risks:** Architectural — JS emulation is fundamentally more error-prone than WASM-compiled native code. Ghostty-web provides better correctness by design.

## Recommendation

**Direction:** Adopt

Continue with the current ghostty-web + bun-pty stack. It is modern, correct (WASM-compiled native parser), and already fully integrated. Monitor the Ghostty team's progress on an official WASM distribution (`libghostty` WASM target) — when available, migrate to ensure upstream maintenance and reduce reliance on the coder/ghostty-web fork.

## Sources of Information

- ghostty-web (coder): `github.com/coder/ghostty-web` — WASM-compiled Ghostty terminal for web with xterm.js API compatibility
- ghostty-web (remorses): `github.com/remorses/ghostty-web` — original ghostty-web project
- xterm.js: `github.com/xtermjs/xterm.js` — the original browser terminal emulator
- @wterm/ghostty: `npmjs.com/package/@wterm/ghostty` — alternative libghostty WASM build
- Existing `packages/web/server/lib/terminal/DOCUMENTATION.md` — terminal module architecture
- Existing `packages/web/server/TERMINAL_WS_PROTOCOL.md` — WebSocket protocol specification
- bun-pty: `github.com/oven-sh/bun-pty` — Bun-native PTY library (preferred over node-pty)

## Open Questions

1. When will the Ghostty team release an official WASM distribution, and should migration be planned now or when it stabilizes?
2. Should mobile keyboard handling (FR-07) reuse the existing virtual keys in TerminalView.tsx or use a different approach for tablet-sized screens?
