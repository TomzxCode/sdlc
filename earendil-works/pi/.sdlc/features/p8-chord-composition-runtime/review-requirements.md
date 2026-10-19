---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25896ffeQpp5pBlvJ7Lg1u
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### NFR-1 is wrong: the package does depend on a Pi workspace package
- **Evidence:** `packages/chord/package.json:82-85` declares `"@earendil-works/pi-telemetry": "1.3.0"` as a runtime dependency; `packages/chord/src/context/index.ts:1` imports `NOOP_TELEMETRY_CONTEXT`, `SpanOptions` and `TelemetrySpan` from it; `packages/chord/test/boundary.test.ts:11-12` allows exactly that one package (`const ALLOWED = new Set(["@earendil-works/pi-telemetry"])`) and rejects every other `@earendil-works/pi-*` dependency.
- **Artifact says:** NFR-1: "The system shall ship as a standalone package with no dependency on any other Pi workspace package." The acceptance criterion says "Then no import reaches any other Pi workspace package or file outside Chord".
- **Required change:** NFR-1 must state that the only Pi workspace dependency is `@earendil-works/pi-telemetry` (needed for `Context.telemetry`, `src/context/index.ts:13`), and that the boundary test asserts no *other* Pi package is imported and no file outside `packages/chord/src` is referenced. The "zero Pi dependencies" wording is not satisfiable as written.
- **Severity:** blocking

### FR-1 to FR-5 describe a facet-kernel service graph that the code does not implement
- **Evidence:** `packages/chord/src/host.ts:96-99` (`defineFacet(setup, { uses })`) and `packages/chord/src/host.ts:84-88` (`FacetDefinition.uses` is "Contract tokens this facet consumes; checked against providers at reload"). There is no `provide` declaration. `packages/chord/src/object.ts:76` is the only lifecycle mode: `export type Lifetime = "referenced" | "host"`. A search of `packages/chord/src` finds no "singleton" or "keyed" service mode (only the SQLite metadata table in `src/sqlite/migrations.ts:27` and an internal delta helper in `src/delta/tracker.ts:1464`). Objects are addressed by contract input and principal, not by a service id: `packages/chord/src/host.ts:519-528`. The only graph check at load time is `packages/chord/src/reload.ts:321-345` (`checkProviders`: a coverage check of changed contracts and a `bind` of each facet's `uses` token), and there is no duplicate-provider or cycle detection over facets. The synchronous-factory rule exists (`packages/chord/src/object.ts:1184`, "factories must be synchronous"), but it is not a dependency-graph validation.
- **Artifact says:** FR-1 "facets as synchronous setup units that state the services they provide and require"; FR-2 "validate the complete facet dependency graph and reject missing dependencies, duplicate providers, cycles, and asynchronous setup"; FR-3 "singleton services with one provider behind a stable consumer-facing handle"; FR-4 "keyed services with dynamically spawned and retired per-key instances"; FR-5 "bind services after graph validation, activate providers before consumers, and dispose resources in reverse dependency order".
- **Required change:** Restate FR-1 to FR-5 against the shipped model: a facet declares `setup(api)` plus an optional `uses` list of contract tokens; `host.serve(contract, factory, options)` registers a factory for a contract type; objects are addressed by `(contract, normalized input, principal key)` and live for `lifetime: "referenced"` or `lifetime: "host"`; contracts are `remote` (with a `host` placement) or `local`. Remove the singleton/keyed modes, the provide/require graph, and the duplicate-provider/cycle validation, or state them as requirements the code does not meet.
- **Severity:** blocking

### FR-9 describes a reload the code does not implement
- **Evidence:** `packages/chord/src/reload.ts:23-52` (`ReloadOptions`, `ReloadReport` with `codeVersion`, `previous`, `changed`, `removed`, `prepared`, `gated`, `children`); `packages/chord/src/reload.ts:351-370` (`prepareAll` prepares every live object of a changed type); `packages/chord/src/reload.ts:321-345` (`checkProviders`); the prepare/gate/commit/retire sequence is specified in `packages/chord/docs/spec.md:201-219`. There is no singleton to replace and no keyed generation: a reload swaps the code version, keeps cells and their values, migrates a cell whose version was raised, and rejects late old-code roots with `upgrade_conflict`.
- **Artifact says:** FR-9: "The system shall reload facets by replacing singletons without an unavailable interval and giving keyed replacements fresh generations." The acceptance criterion expects "singleton handles stay connected while keyed replacements get fresh generations".
- **Required change:** Restate FR-9 as a hot-reload of facets that swaps the code version while objects, cells, resources and listeners survive where compatible, that gates only objects whose cell version was raised or whose exclusive resource was replaced, that migrates raised cell versions through `migrate`, and that reports `upgrade_conflict` to late old-code roots.
- **Severity:** blocking

### The constraint "Chord prescribes no transport, framing, routing, or application wire envelope" is contradicted by the code, and FR-7 builds on it
- **Evidence:** `packages/chord/src/wire.ts:24` (`export const PROTOCOL_VERSION = 4`) and `packages/chord/src/wire.ts:60-165` define Chord's own JSON frame grammar (`hello`, `ack`, `hold`, `release`, `shape`, `gone`, `call`, `result`, `cancel`, `sub`, `unsub`, `resync`, `state`, `ping`, `pong`, `bye`, `root_end`, `invalidate`, `prepare`, `vote`, `commit`, `retire`, `abort`). Routing is a Chord surface: `packages/chord/src/host.ts:160-167` (`Route` with `authorize`, `resolve`, `principal`) and `packages/chord/src/host.ts:232` (`host.route(prefix, route)`). Chord ships link adapters: `packages/chord/src/link.ts:272` (`memoryLinkPair`), `packages/chord/src/link.ts:339` (`ipcLink`), `packages/chord/src/link.ts:414` (`webSocketLink`), `packages/chord/src/websocket.ts:18` (`acceptWebSockets`).
- **Artifact says:** Constraint: "Chord prescribes no transport, framing, routing, or application wire envelope." FR-7: "expose remotely consumable services through an application-supplied transport carrying strict-JSON calls and subscriptions."
- **Required change:** Remove the constraint and restate it: Chord defines its own link frame protocol and `PROTOCOL_VERSION`, defines the routing surface (`host.route`), and ships memory, Node IPC and WebSocket link adapters; an application supplies only the `Link` transport underneath those adapters. Restate FR-7 against the `hold`/`shape`/`call`/`state` frame model rather than "an application-supplied transport".
- **Severity:** blocking

### The requirements omit the SQLite facade, the output module, the child-host manager, cluster reload, and the telemetry context
- **Evidence:** `packages/chord/src/sqlite/index.ts` exports `SqliteDatabase`, `SqliteExecutor`, `SqliteValue`, `applySqliteMigrations` and `validateSqliteSchemaPrefix`; `packages/chord/src/sqlite/migrations.ts:12` (atomic migration runner, contiguous versions from 1, refuses a newer stored version); `packages/chord/src/sqlite/schema.ts:2-8` (prefix must match `^[A-Za-z_][A-Za-z0-9_]*$` and must not start with `sqlite_`); `packages/chord/src/sqlite/node.ts:179` (`openNodeSqliteDatabase`); `packages/chord/src/sqlite/cloudflare.ts:138` (`DurableObjectSqliteDatabase`); `packages/chord/src/output.ts:40,49,127,276,325` (`sanitizeOutput`, `boundOutput`, `OutputBuffer`, `utf8ByteLength`, `Progress`); `packages/chord/src/manager.ts:82,164,256,394` (`processLock`, `forkDriver`, `createHostManager`, `childControl`); `packages/chord/src/cluster.ts:39,123,173` (`runClusterReload`, `reconcileChild`, `ChildReloads`); `packages/chord/src/context/index.ts:13,91,99` (`Context.telemetry` is a required `TelemetrySpan`; `withTelemetry`, `traceIn`).
- **Artifact says:** The functional requirements and constraints cover only facets, services, replicated state, the remote boundary, delta tracking, reload, module loading and context. No requirement mentions SQLite, bounded output, child host processes, cross-host reload, or telemetry.
- **Required change:** Add requirements for the shipped subsystems: the portable SQLite facade and migration runner (Chord defines no tables of its own; it only provides the facade, the runner and the prefix validator), the bounded output surface, the child host manager and cluster reload, and the explicit telemetry-carrying `Context`.
- **Severity:** blocking

### The `$chord.*` service namespace does not exist
- **Evidence:** A search of `packages/chord/src`, `packages/chord/docs` and `packages/chord/README.md` finds no occurrence of `$chord`. The reservation the code enforces is on contract *member* names: `packages/chord/src/contract.ts:179-190` (`RESERVED_MEMBERS`: `variant`, `status`, `ready`, `shape`, `error`, `onShape`, `onStatus`, `release`, `then`, `contract`).
- **Artifact says:** Open question 2: "Should the reserved `$chord.*` service namespace become a permanent part of the Chord contract?"
- **Required change:** Drop the `$chord.*` namespace question and ask the real one (whether the reserved contract member names stay stable), or remove the question.
- **Severity:** advisory

### FR-11 calls the context "Go-like" and does not distinguish the two context types
- **Evidence:** `packages/chord/src/types.ts:22-35` defines `Ctx`, the call context operations take (`signal`, `rootId`, `codeVersion`, `principal`, `get`). `packages/chord/src/context/index.ts:11-16` defines `Context`, a separate carrier with `abortSignal`, a required `telemetry: TelemetrySpan` and `value(key)`. The two are unrelated types.
- **Artifact says:** FR-11: "The system shall provide a Go-like context carrying cancellation and invocation-scoped values through operations." The acceptance criterion expects "an operation invoked with a cancellable context carrying a typed value".
- **Required change:** Name both: `Ctx` is the explicit per-root call context passed to methods and listeners; `Context` (entry point `@earendil-works/chord/context`) is the immutable values-and-telemetry carrier with `withContextValue`, `withCancel`, `withTelemetry` and `traceIn`. Drop "Go-like" and state that `Context.telemetry` is a required `TelemetrySpan`.
- **Severity:** advisory

### NFR-4 describes a "path-codec" the code does not have
- **Evidence:** Each member stream owns a delta `Encoder`, not a path codec: `packages/chord/src/connection.ts:996` (`const feed: Feed = { ..., encoder: encoder(), buffer: [] }`) and `packages/chord/src/connection.ts:1035` (`feed.encoder = encoder()` resets it on a reset). A publication produces one `state` frame with `as: "ops"` per member stream (`packages/chord/src/connection.ts:1029-1032`); the ops are encoded by `encoder()` in `packages/chord/src/delta/index.ts:566`.
- **Artifact says:** NFR-4: "The system shall flush at most one decoded operation batch per publication with independent path-codec state per client stream."
- **Required change:** Say "per-stream delta encoder state" rather than "path-codec state", and name the frame (`state` with `as: "ops"`).
- **Severity:** advisory

## Open questions
- The requirements do not state which parts of Chord are meant to be consumed by `packages/durable` (which depends on Chord and stores document revisions as Chord delta operations). The code shows the coupling but the artifact does not, so the intended division of responsibility cannot be recovered from it.
- The requirements never state whether the SQLite facade is expected to remain table-free in Chord. `packages/chord/src/sqlite/` only provides the portable facade, the migration runner and the prefix validator; the tables live in `packages/durable/src/storage/sqlite/`. The code answers that, but the artifact leaves it open.
