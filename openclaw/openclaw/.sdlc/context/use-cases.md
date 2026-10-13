<!-- session_link: reconciled by /sync-sdlc context pass on 2026-10-13 -->
# Use Cases

<!--
This file records what people and systems do with the project, so requirements,
specifications, and prioritization can reason about the actors and goals behind
a change. Each entry names the actor, the goal, and how the project serves it
today. Keep IDs stable: reuse an existing UC-N for the same use case, and only
add a new one for a genuinely new use case. Put not-yet-built use cases under
"Wanted", each with a signal (an issue, feature, or roadmap reference). Record
deliberate non-goals under "Out of scope".
-->

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Chat on messaging channels | Operator | The operator converses with the assistant on Discord, Telegram, Slack, Teams, WhatsApp, iMessage, and 20+ more channels via channel plugins that normalize messages into a shared envelope. |
| UC-2 | Voice conversations | Operator | The operator speaks and listens through full-duplex voice sessions (Talk) on supported platforms such as macOS, iOS, and Android. |
| UC-3 | Rich interaction in Control UI and Canvas | Operator | The operator chats, manages the Gateway, and views agent-driven visual workspaces through the web-based Control UI and Canvas. |
| UC-4 | Gateway operations via CLI | Operator | The operator configures, onboards, diagnoses (`openclaw doctor`), updates, and inspects the Gateway through the `openclaw` CLI and TUI. |
| UC-5 | Shared team deployment | Team members | A team shares one Gateway (workspace chat bot, shared sessions, named roles) as configuration of the same product, within a single trust domain. |
| UC-6 | Companion apps on devices | Operator | The operator uses native macOS, iOS, Android, Windows, and Linux apps and device nodes for voice, Canvas, camera, screen, and device-local actions. |
| UC-7 | Plugin installation and extension | Operator, plugin developer | The operator installs capabilities from ClawHub or the registry, and the developer builds and distributes them through the plugin SDK. |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| — | None identified | — | No wanted use case with a concrete issue, roadmap, or VISION.md signal was identified during the 2026-10-13 context pass; VISION.md lists directional themes only. | Context pass 2026-10-13 |

## Out of scope

- Multi-tenant SaaS hosting for mutually untrusted parties (run one Gateway per tenant instead).
- Centralized cloud-hosted OpenClaw fleet, paid tier, or token.
- Formal enterprise SSO or RBAC.
