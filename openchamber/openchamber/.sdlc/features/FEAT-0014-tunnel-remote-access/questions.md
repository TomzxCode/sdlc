# Open Questions: Tunnel & Remote Access

Questions captured during review phases.
High-risk questions should be promoted to a formal assumption via `/create-assumption`.

1. [sync-2025-06-24] **Sync drift: ngrok provider not documented**
   The codebase now includes an ngrok tunnel provider (`packages/web/server/lib/tunnels/providers/ngrok.js`) alongside Cloudflare.
   - requirements.md only mentions Cloudflare tunnels (FR-01)
   - specification.md only describes `cloudflared` as the tunnel subprocess (Technical Decisions)
   - specification.md states "Multi-provider active tunnels simultaneously" as out of scope, which is still correct
   Review and update requirements/specification to cover ngrok support.
