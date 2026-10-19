---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

The specification describes the span, event, status, no-op, in-memory, and typed-schema surfaces accurately, but its data models and API contract table predate the propagation, links, and metrics capabilities. It also omits three recorded snapshot types and the optional capability members on `TelemetryContext`.

## Sync drift: 2026-10-19

### SpanOptions data model omits links
- **Evidence:** `packages/telemetry/src/index.ts:23-27` — `SpanOptions` is `{ name: string; attributes?: SpanAttributes; links?: readonly SpanLink[] }`.
- **Artifact says:** the SpanOptions table lists only `name` and `attributes`.
- **Required change:** add the `links?: readonly SpanLink[]` row, with `SpanLink` = `{ context: TelemetryContext; attributes?: SpanAttributes }` (`packages/telemetry/src/index.ts:18-21`).

### RecordedTelemetrySpan data model omits context, parentContext, and links
- **Evidence:** `packages/telemetry/src/memory.ts:32-45` — `RecordedTelemetrySpan` also carries `context: Readonly<TelemetryCarrier>`, `parentContext: Readonly<TelemetryCarrier> | null`, and `links: readonly RecordedTelemetryLink[]`.
- **Artifact says:** the table lists `id`, `parentId`, `name`, `attributes`, `events`, `status`, `settled`, `endSequence`.
- **Required change:** add the three missing rows and state the semantics the code implements: a root has `parentId: null` and `parentContext: null`, a remote parent has `parentId: null` with a non-null `parentContext` (`packages/telemetry/src/memory.ts:34-35`, `packages/telemetry/src/memory.ts:177-179`).

### TelemetrySchemaDefinition data model omits metrics
- **Evidence:** `packages/telemetry/src/index.ts:101-105` — `TelemetrySchemaDefinition` is `{ version: number; spans: Record<string, TelemetrySpanDefinition>; metrics?: Record<string, TelemetryMetricDefinition> }`.
- **Artifact says:** the table lists `version` and `spans` only.
- **Required change:** add the optional `metrics` row, and state that `version` is the contract version used to type spans and metrics (the number is part of the schema data and is not checked at runtime).

### API contract table omits the propagation and metrics capabilities
- **Evidence:** `packages/telemetry/src/index.ts:10` (`TelemetryCarrier`), `packages/telemetry/src/index.ts:13-16` (`TelemetryPropagation`), `packages/telemetry/src/metrics.ts:10-36` (`InstrumentOptions`, `HistogramOptions`, `TelemetryCounter`, `TelemetryUpDownCounter`, `TelemetryHistogram`, `TelemetryMetrics`), `packages/telemetry/src/metrics.ts:124-140` (`createTypedMetrics`), `packages/telemetry/src/noop.ts:17-27` (`NOOP_TELEMETRY_METRICS`, `NOOP_TELEMETRY_PROPAGATION`).
- **Artifact says:** the table lists `TelemetryContext`, `TelemetrySpan`, `NOOP_TELEMETRY_CONTEXT`, `InMemoryTelemetryContext`, `defineTelemetrySchema`, `createTypedSpanStarter`.
- **Required change:** add rows for `TelemetryPropagation`, `TelemetryCarrier`, `TelemetryMetrics` and its instrument types, `NOOP_TELEMETRY_METRICS`, `NOOP_TELEMETRY_PROPAGATION`, `createTypedMetrics`, and the metric schema types `TelemetryMetricDefinition` and `TelemetryMetricAttributeDefinition`.

### Data model omits the RecordedTelemetryLink and RecordedTelemetryMeasurement snapshots
- **Evidence:** `packages/telemetry/src/memory.ts:27-30` (`RecordedTelemetryLink`), `packages/telemetry/src/memory.ts:47-56` (`RecordedTelemetryMeasurement`).
- **Artifact says:** only `RecordedTelemetrySpan` and `RecordedTelemetryEvent` are modelled.
- **Required change:** add both types with their fields, and note that `getMetrics()` returns detached measurement snapshots in recording order, with a carrier-shaped exemplar `context` or `null` (`packages/telemetry/src/memory.ts:405-413`).

### TelemetryContext and TelemetrySpan rows omit the optional capability members
- **Evidence:** `packages/telemetry/src/index.ts:31-43` — `TelemetryContext` declares `readonly metrics?: TelemetryMetrics` and `readonly propagation?: TelemetryPropagation`; `packages/telemetry/CHANGELOG.md:8` makes carrying them through roots, spans, and extracted parents an adapter breaking change.
- **Artifact says:** the two rows describe only `startSpan` and the recording methods.
- **Required change:** state that contexts and spans expose optional `metrics` and `propagation` capabilities, and that child spans and extracted parents carry the same capability objects (`packages/telemetry/src/memory.ts:224-236`, `packages/telemetry/src/memory.ts:380-385`).

### Advisory: architecture and decisions omit the capability axes
- **Evidence:** the mermaid diagram and the Technical Decisions table cover spans, no-op, in-memory, adapters, and typed schemas, but not propagation, links, or metrics. `packages/telemetry/src/memory.ts:190-206` (`startInertSpan`) shows that the in-memory adapter falls back to no-op semantics for child spans of a settled parent, which is a settlement rule the specification does not state.
- **Artifact says:** the diagram shows only the span axis.
- **Required change:** add the propagation, links, and metrics axes to the diagram and a settlement-fallback row to the decisions table.

### Advisory: SpanStatus error payload wording
- **Evidence:** `packages/telemetry/src/index.ts:29` — `{ status: "error"; error?: { name: string; message: string } }`.
- **Artifact says:** the table row reads "error | optional name and message".
- **Required change:** clarify that the `error` object is optional as a whole, while `name` and `message` are both required inside it.

### Advisory: the package README makes a false claim about pi-agent-core
- **Evidence:** `packages/telemetry/README.md:433` imports `AGENT_TELEMETRY_SCHEMAS` from `@earendil-works/pi-agent-core`, and `packages/telemetry/README.md:479` states that pi-agent-core "retains its existing agent-loop and session instrumentation and schemas". No such export exists: `packages/agent/src` contains no telemetry code, `packages/agent/test` contains none either, and `packages/agent/package.json` declares no `@earendil-works/pi-telemetry` dependency.
- **Artifact says:** the SDLC artifacts do not repeat the claim, so the specification itself is not wrong; the defect is in the package README, which is the authoritative contract document for this feature.
- **Required change:** fix `packages/telemetry/README.md:433` and `packages/telemetry/README.md:479` (outside the scope of this feature directory), and record the package ownership list as pi-telemetry, pi-ai, and pi-durable only.

## Open questions

- None. Every claim above is decided by the code, the package README, and the package changelog.
