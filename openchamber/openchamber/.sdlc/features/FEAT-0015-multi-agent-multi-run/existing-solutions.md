---
issue: ""
title: "Multi-Agent / Multi-Run Sessions"
status: draft
---

# Existing Solutions: Multi-Agent / Multi-Run Sessions

## Overview

The codebase already has a comprehensive multi-agent/multi-run implementation with worktree isolation, parallel session creation, independent streaming per agent, and a fusion comparison view. The architecture uses the OpenCode SDK for session management, `simple-git` for worktree operations, and Zustand for UI state of parallel agents. The recommendation is to adopt the existing implementation and look to comparable open-source tools (Emdash, Workstreams) for UI pattern inspiration, not for replacement.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useMultiRunStore.ts`, `packages/ui/src/components/multirun/`, `packages/ui/src/types/multirun.ts`, `packages/web/server/lib/git/service.js` |
| Open-source | Yes | Emdash (generalaction/emdash), Workstreams (workstream-labs/workstreams), wt CLI (EmilRex/wt) |
| Commercial / SaaS | Yes | Claude Code `--worktree`, OpenClaw agents |
| Standards / protocols | Yes | Git worktree protocol, OpenCode SDK session management |
| Reference material | Yes | Git worktree documentation, GitHub blog on parallel AI agents |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing useMultiRunStore + components | Internal | MIT | Mature | FR-01 through FR-07, NFR-01, NFR-02, NFR-03 | None significant |
| Emdash (generalaction/emdash) | Desktop app | MIT | Mature | FR-01, FR-02, FR-03 | External desktop app; not embeddable |
| Workstreams (workstream-labs/workstreams) | Desktop app | Proprietary | Active | FR-01, FR-02 | External desktop app; not embeddable |
| Claude Code --worktree | CLI | Proprietary | Mature | FR-01, FR-04 | CLI-only; Claude Code specific |
| wt CLI (EmilRex/wt) | CLI | MIT | Active | FR-01 | CLI-only; no UI |

## Evaluation

### Existing Multi-Run Implementation

- **Strengths:** Full integration with OpenCode SDK for creating parallel sessions. Git worktree isolation via `simple-git` with worktree creation, validation, removal, bootstrap status, and type detection. Worktree directory candidate generation with conflicts resolution. Per-agent slug generation from provider+model IDs. Multi-run launcher with ModelMultiSelect, AgentSelector, BranchSelector. Fusion dialog for comparing results. Non-Git isolation (directory-level) fallback. At-most-5-models-per-group enforcement. Per-model setup commands support. Session registration into sync stores for live streaming. Test suite for useMultiRunStore. Bus-based state dispatch for multi-run events. Cross-runtime support (VS Code bridge).
- **Weaknesses:** Fusion comparison view (`MultiRunFusionDialog.tsx`) is functional but could be enhanced with side-by-side diff comparison. No explicit cost capping per multi-run (FR-07).
- **Integration effort:** Low. Already shipping in production.
- **Cost:** Free (MIT).
- **Risks:** Low. Worktree-heavy operations could leave orphaned worktrees on crash, but cleanup paths exist.

### Emdash

- **Strengths:** Open-source agentic development environment. Runs multiple coding agents in parallel in isolated Git worktrees. Provider-agnostic (25+ CLIs including Claude Code, Codex, Gemini, OpenCode). Diff view for side-by-side comparisons. Issue integration (Linear, Asana, Jira, GitHub). Worktree pre-warming for fast task startup (500-1000ms). Remote SSH support. CI/CD check monitoring. Diff comments. Y Combinator W26 backed. 840K+ downloads.
- **Weaknesses:** External desktop app (macOS, Linux, Windows). Not embeddable in OpenChamber. Different architecture (CLI subprocess vs SDK). No OpenCode-native session streaming.
- **Integration effort:** Not applicable (external app).
- **Cost:** Free (MIT).
- **Risks:** None for OpenChamber — Emdash is a complementary tool, not a replacement.

### Workstreams

- **Strengths:** IDE for parallel AI coding agents. Worktree sidebar with live diff stats. Inline review comments with agent-aware prompt injection. Agent session state tracking. Provider-agnostic (Claude, Codex, Aider).
- **Weaknesses:** macOS desktop app only. Proprietary license. Not embeddable.
- **Integration effort:** Not applicable.
- **Cost:** Free (proprietary).
- **Risks:** None for OpenChamber.

### Claude Code --worktree

- **Strengths:** Native worktree support in Claude Code CLI. Named and auto-named worktrees. Mid-session worktree creation. Works with other Claude Code features.
- **Weaknesses:** Claude Code specific. CLI-only. No parallel session management UI. No comparison view.
- **Integration effort:** Already integrated (OpenCode SDK).
- **Cost:** Free (subject to Anthropic's terms).
- **Risks:** Low.

## Recommendation

**Direction:** Adopt

The existing multi-agent/multi-run implementation is feature-complete and production-tested. No external tool adoption is warranted. Emdash and Workstreams provide useful UI pattern references for the fusion/comparison view and diff review UX, but OpenChamber's architecture (SDK-based session creation, OpenCode-native messaging, Zustand streaming) is fundamentally different from these CLI-subprocess-based tools.

## Sources of Information

- `packages/ui/src/stores/useMultiRunStore.ts` and `packages/ui/src/stores/useMultiRunStore.test.ts`: Core multi-run store with worktree creation, session management, and tests.
- `packages/ui/src/components/multirun/`: All multi-run components (launcher, fusion dialog, model multi-select, agent selector, branch selector).
- `packages/ui/src/types/multirun.ts`: Type definitions for multi-run params, groups, and results.
- `packages/web/server/lib/git/service.js:919-1349`: Git worktree operations (create, remove, list, validate, bootstrap, branch management).
- `packages/web/server/lib/git/routes.js:848-1025`: Git worktree API routes.
- `packages/web/server/lib/git/DOCUMENTATION.md`: Git module documentation.
- `packages/ui/src/sync/session-ui-store.ts:61`: Multi-run sending routing.
- Emdash: `github.com/generalaction/emdash` — open-source ADE reference for UI patterns.
- Workstreams: `github.com/workstream-labs/workstreams` — IDE reference for diff review patterns.

## Open Questions

1. Should the fusion comparison view show diffs side-by-side (like Emdash) or in a stacked/tabbed view?
2. Should non-Git multi-run (FR-05) use temporary directory copies or symlink-based isolation?
3. Should cost capping (FR-07) warn before starting or enforce a hard stop mid-run?
