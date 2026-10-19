---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf25896ffeQpp5pBlvJ7Lg1u
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The "Package coupling" decision is wrong: Chord depends on `@earendil-works/pi-telemetry`
- **Evidence:** `packages/chord/package.json:82-85`; `packages/chord/src/context/index.ts:1`; `packages/chord/test/boundary.test.ts:11-12`.
- **Artifact says:** "| Package coupling | Standalone with zero Pi workspace dependencies | Lets unrelated applications adopt Chord without the Pi monorepo |"
- **Required change:** State that Chord's only Pi workspace dependency is `@earendil-works/pi-telemetry` (a leaf package with no dependencies of its own, used for `Context.telemetry`), and that the boundary test enforces exactly that.
- **Severity:** blocking

### The "Remote boundary" decision and the "Out of Scope" list contradict the code: Chord defines framing, routing, and ships link adapters
- **Evidence:** `packages/chord/src/wire.ts:24` (`PROTOCOL_VERSION = 4`) and `packages/chord/src/wire.ts:60-165` (Chord's own frame grammar); `packages/chord/src/host.ts:160-167` and `packages/chord/src/host.ts:232` (`Route`, `host.route(prefix, route)`); `packages/chord/src/link.ts:272` (`memoryLinkPair`), `packages/chord/src/link.ts:339` (`ipcLink`), `packages/chord/src/link.ts:414` (`webSocketLink`), `packages/chord/src/websocket.ts:18` (`acceptWebSockets`).
- **Artifact says:** "| Remote boundary | Transport-independent wire grammar with application-supplied adapters | Keeps Chord neutral on framing, routing, and envelopes while enforcing strict JSON |", "Out of Scope: Any concrete transport, framing, routing, or envelope implementation.", and Risk 1 "Symmetric RPC peers are planned but not yet specified as the reference transport implementation."
- **Required change:** State that the link frame grammar and `PROTOCOL_VERSION` are Chord's own, that routing is a Chord surface (`host.route` with `authorize`/`resolve`/`principal`), and that Chord ships memory, Node IPC and WebSocket adapters while the application supplies only the `Link` transport underneath them. Keep only the symmetric peer role open.
- **Severity:** blocking

### The Facet and Service data models do not match the code
- **Evidence:** `packages/chord/src/host.ts:84-99`: `FacetDefinition<P>` is `{ uses?: readonly AnyContract[]; setup(api: FacetApi<P>): void }` and `Facet<P>` adds `name` (the module URL). `FacetApi<P>` (`packages/chord/src/host.ts:67-81`) is `{ serve, name, root, registry, signal }`; it does not carry "provided and required services". `packages/chord/src/object.ts:86-91`: `Service` is `{ contract, factory, options, facet }`. `packages/chord/src/contract.ts:166-176`: a contract is `RemoteContract` or `LocalContract` with `scope: "remote" | "local"`, `name`, `version`, `input` (a TypeBox schema), and for remote types a `host` placement (`hostNamed`/`hostFamily`, `packages/chord/src/contract.ts:64-77`) and `variants` of `state` and `methods` members. The only mode is `Lifetime = "referenced" | "host"` (`packages/chord/src/object.ts:76`).
- **Artifact says:** "### Facet | id | string | PK, not null | Stable identity of one facet within its plugin | setup | function | synchronous, not null | Declares provided and required services against the facet environment" and "### Service | id | string | PK, not null, `$chord.*` reserved | local | boolean | not null, defaults false | mode | singleton or keyed | not null | Selects one provider versus dynamic per-key instances".
- **Required change:** Replace both tables with the real models: Facet = `{ name, uses?, setup(api) }`; Contract = `{ name, version, input, scope, host? (placement), variants }`; Service = `{ contract, factory, options, facet }`; and the lifetime modes `referenced` / `host`. Remove the `$chord.*` reservation and the singleton/keyed mode.
- **Severity:** blocking

### The "Service Subscription Snapshot" data model does not exist
- **Evidence:** The wire carries a `shape` frame (`packages/chord/src/wire.ts:99-105`: `t: "shape"`, `variant`, `members`, `contract`, `state`) followed by one `state` frame per listed member (`packages/chord/src/wire.ts:131-143`: `t: "state"`, `hold`, `m`, `as: "snap" | "reset" | "ops" | "error"`, `value`, `ops`). Later updates are `ops` frames on the same hold and member. `packages/chord/docs/spec.md:240` describes the same unit model. There is no `serviceId` / `mode` / `instances` structure anywhere.
- **Artifact says:** "### Service Subscription Snapshot | serviceId | string | not null | Service the snapshot describes | mode | singleton or keyed | not null | Provider mode the snapshot was taken under | instances | array | possibly empty | Per-instance member lists with state sequences and operation batches".
- **Required change:** Replace the table with the hold/member model: a `shape` frame names the variant, the members and the contract fingerprint and lists the members whose snapshots follow; each listed member is delivered as a `state` frame with `as: "snap"`; later frames are `as: "ops"` (per-stream encoded), `as: "reset"` or `as: "error"`.
- **Severity:** blocking

### The architecture and sequence diagrams use a "Facet Kernel" and a provide/require flow that do not exist
- **Evidence:** `packages/chord/src/host.ts:192-236` is the real `Host` surface: `serve`, `install`, `load`, `ready`, `get`, `hold`, `root`, `registry`, `invalidatePrincipal`, `accept`, `connect`, `route`, `reload`, `close`. `packages/chord/src/host.ts:47-58` (`Serve`) registers a factory for a *contract type*, not a service in a graph. Objects live at an address built from the contract, the normalized input and the principal key (`packages/chord/src/host.ts:519-528`, `packages/chord/src/host.ts:539-542`).
- **Artifact says:** The flowchart has a "Facet Kernel" node between the plugin and the "Service Provider"; the sequence diagram has "F->>K: setup(env): provide and require services" and "K->>K: validate dependency graph".
- **Required change:** Redraw the flow as: facet `setup(api)` → `api.serve(contract, factory)` → host registers the service → `ctx.get(contract, input)` resolves the placement, creates or locates the object, and returns a reference → the object publishes cells → the connection encodes state per member stream and the link carries it. Remove the dependency-graph step and the "Facet Kernel" node.
- **Severity:** blocking

### The "API Contracts" section omits three entry points and two shipped subsystems
- **Evidence:** `packages/chord/package.json:8-50` exports `.`, `./context`, `./output`, `./delta`, `./node`, `./sqlite`, `./sqlite/node` and `./sqlite/cloudflare`. The `output` entry point carries `OutputBuffer`, `boundOutput`, `sanitizeOutput`, `utf8ByteLength` and `Progress` (`packages/chord/src/output.ts:40,49,127,276,325`); the `sqlite` entry points carry the portable facade, the migration runner and the prefix validator (`packages/chord/src/sqlite/index.ts:1-3`).
- **Artifact says:** "The normative contract is the TypeScript surface exported from the package root plus the context, delta, and node entry points."
- **Required change:** List all eight entry points, and add the output and SQLite surfaces to the data models and API contracts.
- **Severity:** blocking

### Risk 3 claims the code enforces a `$chord.*` reservation that does not exist
- **Evidence:** No occurrence of `$chord` in `packages/chord/src`, `packages/chord/docs` or `packages/chord/README.md`. The enforced reservation is on contract member names: `packages/chord/src/contract.ts:179-190` (`RESERVED_MEMBERS`).
- **Artifact says:** "3. The `$chord.*` service-ID reservation is enforced in code but its long-term namespace policy is undecided."
- **Required change:** Replace the risk with the real one (the reserved member-name list and the contract fingerprint compatibility rule, `packages/chord/src/contract.ts:210-212` and `packages/chord/src/contract.ts:326-351`).
- **Severity:** blocking

### The "Replicated State" data model describes a mutation surface the public API does not have
- **Evidence:** `packages/chord/src/state.ts:30-42`: `MutableReplicatedState<T>` exposes `change(context, mutate: (draft: Draft<T>) => void)` and `replace(context, value)`. The producer never mutates a tracked proxy directly; the draft is a `Draft` overlay (`packages/chord/src/delta/draft.ts`) valid only inside the callback. The sequence number lives on the delivery, not on the state: `packages/chord/src/state.ts:9-12` (`ReplicatedStateDelivery { kind: "hydrate" | "update", sequence }`).
- **Artifact says:** "state | tracked proxy | producer-only writes | Mutable view that records operations for the next publication" and "sequence | number | monotonically increasing | Orders hydrate and update deliveries per subscription".
- **Required change:** State that writes go through `change(context, (draft) => …)` (one atomic publication per successful call) or `replace(context, value)` (ownership transfer), that the value is contract-immutable but not frozen, and that the sequence is carried by the delivery passed to the subscriber.
- **Severity:** advisory

### The "Context model" decision names one context where the code has two
- **Evidence:** `packages/chord/src/types.ts:22-35` (`Ctx`: `signal`, `rootId`, `codeVersion`, `principal`, `get`) is what methods, listeners and tasks receive. `packages/chord/src/context/index.ts:11-16` (`Context`: `abortSignal`, `telemetry`, `value(key)`) is a separate values-and-telemetry carrier.
- **Artifact says:** "| Context model | Explicit Go-like context parameter on operations | Carries cancellation and scoped values without Chord depending on either domain |"
- **Required change:** Name both contexts and their roles, and say that `Context.telemetry` is a required `TelemetrySpan` from `@earendil-works/pi-telemetry` (`packages/chord/src/context/index.ts:13`, `packages/chord/src/context/index.ts:34-36`).
- **Severity:** advisory

### The "Module loading" decision omits a known limitation the code documents
- **Evidence:** `packages/chord/src/loader.ts:1-5` (`TODO(loader): replace with an isolating, evicting loader ... old copies are never evicted (they leak until the process exits). TUI plugins need isolation, which this loader does not provide.`); `packages/chord/docs/spec.md:264` ("The Node loader leaks.").
- **Artifact says:** The decision records the mechanism but Risks and Unknowns lists only three risks, none of them the loader leak or the missing isolation.
- **Required change:** Add the loader leak and the missing plugin isolation to Risks and Unknowns.
- **Severity:** advisory

## Open questions
- The specification does not say how Chord's delta operations are persisted. The code is agnostic here: `packages/durable` stores document revisions as Chord operation batches, but nothing in `packages/chord` mentions a storage backend, so the intended boundary cannot be recovered from the artifact.
- The specification does not state whether the SQLite facade is meant to be the only SQL surface in the monorepo. The code answers it (Chord defines no tables; `packages/durable/src/storage/sqlite/` owns the schema), but the artifact leaves the data model section silent on SQL entirely.
