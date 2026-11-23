---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-23
---

# Review: specification.md

## Sync drift: 2026-11-16

- TUI transport is documented as stdio JSON-RPC in three places: the architecture tree ("Ink frontend (ui-tui/src/) ← stdio JSON-RPC → tui_gateway (Python backend)", lines 15-16; "Transport (stdio)", line 19) and Technical Decisions ("TUI transport | stdio JSON-RPC", line 63). The current TUI connects to the profile's ordinary gateway over authenticated WebSocket, not stdio and not by launching `tui_gateway.entry`: `ui-tui/src/gatewayClient.ts` extends `GatewayClient` from `@hermes/shared/gateway-client` with an Undici `WebSocket` and `attachUrl`/`sidecarUrl`, and `ui-tui/src/localGatewayBootstrap.ts` only runs `gateway_bootstrap.py` to obtain a private control ticket. `ui-tui/CANONICAL_GATEWAY.md` states outright that "Ink no longer starts `tui_gateway.entry` or owns an agent loop" and that it "connects over authenticated WebSocket." The `tui_gateway/` Python package still exists, but as the gateway/server implementation, not a stdio child the Ink frontend spawns.
- The desktop backend is documented as `hermes serve --headless` (architecture "Desktop (hermes serve --headless): Electron app ← WebSocket/JSON-RPC → AIAgent + gateway", lines 26-27; Technical Decisions "Desktop backend | hermes serve (headless)", line 64). Local Desktop instead attaches to the shared gateway: `apps/desktop/electron/local-gateway.ts` runs `hermes gateway ensure` and reserves tickets on `/api/ws` with one-use grants. `hermes serve` is used only for remote backends (`website/docs/user-guide/desktop.md:634,644,666`).
- The architecture tree names desktop source paths that no longer exist: `apps/desktop/src/app/composer/hooks/use-slash-completions.ts` (line 30) moved to `apps/desktop/src/app/chat/composer/hooks/use-slash-completions.ts`, and `apps/desktop/src/app/session/hooks/use-prompt-actions.ts (runSlash)` (line 31) is now the directory `apps/desktop/src/app/session/hooks/use-prompt-actions/slash.ts`. `apps/desktop/src/lib/desktop-slash-commands.ts` (line 29) still exists.

## Sync drift: 2026-11-23

- The TUI component tree in the architecture section (specification.md:18-24) lists five files as `ui-tui/src/<name>` that are no longer there.
  - `messageLine.tsx`, `thinking.tsx`, `prompts.tsx`, and `branding.tsx` now live under `ui-tui/src/components/`.
  - `sessionPicker.tsx` has been replaced by `ui-tui/src/components/activeSessionSwitcher.tsx`, used at `ui-tui/src/components/appOverlays.tsx:11,323` and covered by `ui-tui/src/__tests__/canonicalSessionPicker.test.tsx:7`.
  - `app.tsx` and `theme.ts` still exist at `ui-tui/src/`.
