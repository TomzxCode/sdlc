---
title: "Harness API and SDKs"
status: done
---

# Specification: Harness API and SDKs

## Overview

The harness API is defined in `crates/jcode-harness-api` (client API, requests, events, capability coverage, schema snapshots) and served by `crates/jcode-harness-api-server` (the `jcode api-bridge` binary). The Rust SDK (`crates/jcode-sdk`) and the TypeScript SDK (`sdk/typescript`, published as `@1jehuang/jcode-sdk`) consume the bridge; platform launcher packages live under `sdk/npm/`. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
SDK clients (Rust: jcode-sdk, TypeScript: @1jehuang/jcode-sdk)
        │
        ▼
jcode api-bridge (jcode-harness-api-server, Unix socket)
        │  framing + translation
        ▼
jcode internal protocol (jcode-protocol)
        │
        ▼
jcode server (agent runtime, sessions, events)
```

## Data Models

### Harness API client crate

- `requests.rs` — versioned request types.
- `events.rs` — streamed event types.
- `capability_coverage.rs` — capability negotiation.
- `schema_snapshot.rs` — schema snapshots for parity.

## API Contracts

### CLI: `jcode api-bridge` (alias `jcode api`, Unix only)

Serves the versioned harness API on a Unix socket for SDK clients.

### SDK launch

SDK clients can launch jcode directly; platform launcher packages in `sdk/npm/` provide the executable per platform (darwin-arm64, darwin-x64, linux-arm64, linux-x64, win32-arm64, win32-x64).

## Sequences

### Drive a session from an SDK

```
SDK → api-bridge (connect, negotiate version) → open session
SDK → send message → server turn loop → events stream back to SDK
SDK → cancel/close session
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Versioned client crate | `jcode-harness-api` | Stable surface independent of internal protocol evolution. |
| Bridge in released binary | `jcode api-bridge` | SDK users need no Rust toolchain (NFR-2). |
| Unix socket bridge | `jcode-harness-api-server` | Low-overhead local IPC, versioned framing. |
| Schema parity testing | `schema-parity.test.ts`, `capability_coverage.rs` | Keeps Rust and TS SDKs consistent (FR-6). |
| Platform launcher packages | `sdk/npm/*` | One install story per platform. |

## Risks and Unknowns

1. The bridge is Unix-only by design; Windows support relies on the named-pipe transport behind the same API.
2. Capability negotiation and version deprecation policy are only partially documented.

## Out of Scope

- A network-exposed API (bridge is local IPC only).
- Full parity for every internal protocol feature; the API surface is intentionally smaller.
