---
artifact: requirements.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: requirements.md

## Sync drift: 2026-11-16

- FR-7 ("The desktop app shall communicate with a headless hermes serve backend over WebSocket/JSON-RPC", requirements.md:30) names `hermes serve` as the desktop backend. The local desktop does not start or use a `hermes serve` process: Electron runs `hermes gateway ensure` (`apps/desktop/electron/local-gateway.ts:17,156`) and the renderer dials the profile gateway over `/api/ws` with one-use tickets (same file, around line 354). The user docs state the desktop app "needs no separate `hermes serve` process and never opens the web dashboard" (`website/docs/user-guide/desktop.md:634`). `hermes serve` remains only the remote-backend option (desktop.md:644, 666). The WebSocket/JSON-RPC part of FR-7 still holds; only the named backend is contradicted.
