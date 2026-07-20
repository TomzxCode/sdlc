# Goals and Objectives

## Purpose

OpenChamber provides multi-runtime GUI surfaces (web, Electron, VS Code, mobile) for OpenCode, an AI-powered coding assistant CLI. The project solves the problem of OpenCode being terminal-only by adding rich visual workflows: branchable chat timelines, diff viewers, Git integration, integrated terminals, voice mode, multi-agent runs, and remote access.

## Vision

Be the universal frontend for AI-assisted coding that works seamlessly across every device a developer uses, from desktop to mobile to IDE.

## Time Horizon

- **Current period:** 2026 H2
- **Period type:** half

## Objectives

### Expand runtime coverage and stability

**Owner:** OpenChamber maintainers
**Statement:** Make OpenChamber reliable and feature-complete across all target runtimes

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Electron desktop reaches feature parity with web | 100% | Feature comparison checklist | ~80% | On track |
| VS Code extension passes all integration tests | 100% pass rate | CI test results | ~90% | On track |
| iOS and Android mobile builds pass CI | Green CI | Mobile CI workflow | Green | On track |

### Improve developer experience and AI capabilities

**Owner:** OpenChamber maintainers
**Statement:** Deliver advanced AI workflows beyond basic chat

| Key Result | Target | Measurement Method | Current | Status |
|---|---|---|---|---|
| Session goals feature ships | GA | Release notes | Implemented | Done |
| Support multi-agent multi-run | GA | Feature available | Implemented | Done |
| Private relay for remote access | GA | Feature available | Implemented | Done |

## Strategic Pillars

- Multi-runtime support (web, desktop, VS Code, mobile) with shared UI
- Rich AI interaction beyond basic chat (goals, multi-run, auto-review)
- Self-hosted first with optional cloud relay
- Developer experience and workflow automation

## Non-Goals

- Replacing OpenCode itself as the AI engine
- Building a full IDE (complements VS Code instead)
- Competing with cloud-only AI coding tools (self-hosted focus)

## Alignment

| Feature / Initiative | Objective | Notes |
|---|---|---|
| FEAT-0043-electron-desktop | Expand runtime coverage | Forward desktop shell |
| FEAT-0010-vscode-extension | Expand runtime coverage | In-editor integration |
| FEAT-0024-mobile-ui-touch-gestures | Expand runtime coverage | Mobile PWA and Capacitor |
| FEAT-0035-project-management | Improve AI capabilities | Plan view, goals, tasks |
| FEAT-0015-multi-agent-multi-run | Improve AI capabilities | Parallel agent execution |
| FEAT-0014-tunnel-remote-access | Improve AI capabilities | Remote access and relay |

## Review Cadence

- **Review frequency:** quarterly
- **Last reviewed:** 2026-07-13
- **Next review:** 2026-10-01

## Open Questions

1. What are the formal adoption metrics and target numbers?
2. Which runtimes should be prioritized for new feature development?
