<!-- session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA -->
# Use Cases

<!--
This file records why actors use the project, so requirements, specifications,
and prioritization can reason about the goals behind a change. An entry is a
reason an actor has for reaching for the project, not an operation the project
exposes: "read a conversation offline" is a use case, "run the cache status
command" is not. Each entry names the actor, the goal, and how the project
serves that goal today. Keep IDs stable: reuse an existing UC-N for the same
goal, and only add a new one for a genuinely new goal. Put not-yet-built goals
under "Wanted", each with a signal (an issue, feature, or roadmap item). Record
deliberate non-goals under "Out of scope".
-->

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Stay in touch with the assistant on the channels they already use | Operator | The operator converses with the assistant on Discord, Telegram, Slack, Teams, WhatsApp, iMessage, and many more channels, and binds those accounts and conversations to the agent that should answer them. |
| UC-2 | Have spoken conversations with the assistant | Operator | The operator speaks and listens through full-duplex voice sessions (Talk) on supported platforms such as macOS, iOS, and Android, including voice calls with briefs, reports, and live steering. |
| UC-3 | See and steer rich, visual workspaces | Operator | The operator chats, manages the Gateway, and views agent-driven visual workspaces through the web-based Control UI, session boards, and Canvas. |
| UC-4 | Run and maintain the installation from a terminal | Operator | The operator configures, onboards, diagnoses (`openclaw doctor`), updates, backs up, and inspects the Gateway through the `openclaw` CLI, the setup wizard, and the terminal UI. |
| UC-5 | Work as a team on one shared assistant | Team members | A team shares one Gateway (workspace chat bot, shared sessions, named roles, shared boards and reports) as configuration of the same product, within a single trust domain. |
| UC-6 | Use the assistant from the device in their pocket | Operator | The operator uses native macOS, iOS, Android, Windows, and Linux apps and device nodes for voice, Canvas, camera, screen, and device-local actions. |
| UC-7 | Extend the assistant with plugins and skills | Operator, plugin developer | The operator installs capabilities from ClawHub or the registry, and the developer builds and distributes them through the plugin SDK and skill bundles. |
| UC-8 | Have the assistant remember past conversations | Operator | The operator relies on curated memory files, episodic notes, standing intents, hybrid search over past sessions, and deep recall when a question needs history. |
| UC-9 | Run long or heavy work away from the Gateway host | Operator | The operator hands a session to a paired device or a leased cloud machine while the Gateway keeps the transcript, the workspace, and the credentials, and brings back accepted changes. |
| UC-10 | Know what the assistant did and keep credentials out of plaintext | Operator | The operator audits the installation for unsafe settings, reads a durable content-free activity ledger of what ran, and keeps credentials behind SecretRefs and a shared secret store. |
| UC-11 | Track work across sessions and agents on a shared board | Operator, Team members | The operator sees a per-session dashboard of tabs and widgets, keeps a project registry of repositories and checkouts, and moves work through a shared board. |
| UC-12 | Drive the assistant from an external agent client | Developer, Operator | The operator or a developer connects an IDE or another agent client to an OpenClaw session over the Agent Client Protocol and steers the turn. |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| — | None identified | — | No wanted use case with a concrete issue, roadmap, or VISION.md signal was identified during the 2026-10-19 context pass; VISION.md lists directional themes only. | Context pass 2026-10-19 |

## Out of scope

- Multi-tenant SaaS hosting for mutually untrusted parties (run one Gateway per tenant instead).
- Centralized cloud-hosted OpenClaw fleet, paid tier, or token.
- Formal enterprise SSO or RBAC.
