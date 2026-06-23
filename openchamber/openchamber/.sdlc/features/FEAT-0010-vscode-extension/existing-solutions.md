---
issue: ""
title: "VS Code Extension"
status: draft
---

# Existing Solutions: VS Code Extension

## Overview

OpenChamber already ships a full VS Code extension in `packages/vscode/`. It provides a sidebar chat webview (`ChatViewProvider`), agent manager panel (`AgentManagerPanelProvider`), session editor panel (`SessionEditorPanelProvider`), right-click context menu actions (Explain, Improve Code, Add to Context), VS Code theme-to-OpenChamber theme mapping, SSE proxy with reconnection, bridge runtime for filesystem/git/settings operations, and settings sync. The extension is published under publisher ID `fedaykindev` on the VS Code Marketplace. It uses the shared `@openchamber/ui` workspace package for the webview React UI. Several community VS Code extensions for OpenCode exist (opencode_sidebar, Varro, VSCode ACP Chat, opencode-web-for-vscode) providing reference patterns for features like inline diff preview, session persistence, and ACP multi-agent support.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/vscode/` (src/, webview/, package.json, extension.ts, ChatViewProvider.ts, AgentManagerPanelProvider.ts, SessionEditorPanelProvider.ts, bridge-*.ts, sseProxy.ts, theme.ts, shikiThemes.ts) |
| Open-source | Yes | opencode_sidebar (emngny), Varro (koltyakov), VSCode ACP Chat (pengjiantao), opencode-web-for-vscode (cpkt9762), claude-code-chat (andrepimenta) |
| Commercial / SaaS | No | GitHub Copilot, Cursor, Continue.dev (open-source) |
| Standards / protocols | Yes | VS Code Extension API, Webview API, ThemeColor API, MessagePassing API |
| Reference material | Yes | VS Code extension guides, WebviewViewProvider docs, ColorTheme API |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber VS Code extension | Internal | MIT | Mature | FR-01 to FR-08, NFR-01 to NFR-03 | None significant |
| opencode_sidebar (community) | External | NOASSERTION | Active | Chat sidebar, file change cards, permissions, session management | No agent manager, no editor panel, no theme mapping |
| Varro (community) | External | MIT | Active | Native sidebar, live workspace context, inline permissions, plan/ralph loops | No shared UI reuse, different architecture |
| VSCode ACP Chat | External | MIT | Active | Multi-agent ACP support, rich markdown, session management | ACP protocol focused, not OpenCode-specific |
| opencode-web-for-vscode | External | MIT | Active | Full OpenCode web UI proxied into webview, stable port persistence | Embedded iframe approach, no native integration |
| Continue.dev | External | Apache-2.0 | Mature | Full-featured AI coding assistant, multi-model, context providers | Much broader scope, different stack (Node.js backend) |

## Evaluation

### OpenChamber VS Code extension

- **Strengths:** Complete extension with sidebar webview, agent manager, session editor panel, right-click actions (Explain, Improve Code, Add to Context), VS Code theme mapping via `shikiThemes.ts` and `theme.ts`, SSE proxy with reconnection and stall detection, comprehensive bridge runtime for filesystem (read/write/diff), git operations, settings sync, system operations, and secret storage. Uses shared `@openchamber/ui` workspace package for UI consistency across runtimes. Published on VS Code Marketplace. Handles delayed API readiness with retries (NFR-02) via `opencode-ready.ts`.
- **Weaknesses:** Theme mapping (FR-06) from VS Code themes to OpenChamber theme tokens could be more complete. Settings sync (FR-07) currently handles API URL and binary path but could cover more settings. The extension architecture is complex with multiple bridge modules.
- **Integration effort:** Low (already built and published).
- **Cost:** None (MIT).
- **Risks:** None.

### Community extensions (opencode_sidebar, Varro, opencode-web-for-vscode)

- **Strengths:** Demonstrate various approaches: proxied iframe embedding, native ACP protocol support, workspace context integration, plan/ralph loops.
- **Weaknesses:** Different architectures that are not directly compatible with OpenChamber's shared UI approach. None have the same feature scope. Some are not actively maintained.
- **Integration effort:** Not applicable (reference only).
- **Cost:** Not applicable.
- **Risks:** Not applicable.

### Continue.dev

- **Strengths:** Mature, Apache-2.0, multi-model support, extensive context provider system, model selection, slash commands, inline editing.
- **Weaknesses:** Entirely different architecture (Python + Node.js backend), does not use OpenCode at all. Replacing the extension with Continue would mean abandoning the OpenCode ecosystem.
- **Integration effort:** Prohibitively high.
- **Cost:** Free (Apache-2.0).
- **Risks:** Not a direct alternative.

## Recommendation

**Direction: Adopt and extend**

The existing VS Code extension is feature-complete and published. Extend with:
- More comprehensive VS Code theme-to-OpenChamber theme token mapping (FR-06) by expanding the `shikiThemes.ts` and `theme.ts` adapters.
- Expanded settings sync (FR-07) to cover more OpenChamber settings like provider keys, agent config, and MCP server settings.
- Responsive layout improvements (FR-08) to handle very narrow sidebar widths gracefully.
- Study Varro's workspace context integration and opencode_sidebar's file change cards for inspiration, but the existing architecture is sound.

## Sources of Information

- `extension.ts` at `packages/vscode/src/extension.ts` - extension activation and registration
- `ChatViewProvider.ts` at `packages/vscode/src/ChatViewProvider.ts` - sidebar webview provider
- `AgentManagerPanelProvider.ts` at `packages/vscode/src/AgentManagerPanelProvider.ts` - agent manager panel
- `SessionEditorPanelProvider.ts` at `packages/vscode/src/SessionEditorPanelProvider.ts` - session editor panel
- `bridge-proxy-runtime.ts` at `packages/vscode/src/bridge-proxy-runtime.ts` - API proxy bridge
- `bridge-settings-runtime.ts` at `packages/vscode/src/bridge-settings-runtime.ts` - VS Code settings sync
- `sseProxy.ts` at `packages/vscode/src/sseProxy.ts` - SSE event proxy with reconnection
- `theme.ts` at `packages/vscode/src/theme.ts` - VS Code theme mapping
- `shikiThemes.ts` at `packages/vscode/src/shikiThemes.ts` - Shiki syntax theme mapping
- `opencode_sidebar` at `github.com/emngny/opencode_sidebar` - community reference
- `Varro` at `github.com/koltyakov/varro` - community reference
- VS Code Extension API docs at `code.visualstudio.com/api`

## Open Questions

1. Should theme mapping (FR-06) support VS Code's semantic token colors in addition to TextMate scopes?
2. How should settings sync handle conflicts between VS Code settings and OpenChamber's local settings.json?
3. Should the extension support ACP (Agent Client Protocol) for multi-agent compatibility like VSCode ACP Chat?
