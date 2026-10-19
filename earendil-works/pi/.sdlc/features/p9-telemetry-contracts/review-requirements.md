---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

`packages/telemetry` implements three capability areas that the requirement set does not state at all: cross-process propagation, span links, and metrics. It also ships a public conformance suite that no requirement covers. The existing FR-1..FR-9 and NFR-1..NFR-4 all match the code.

## Sync drift: 2026-10-19

### Cross-process propagation is not a requirement
- **Evidence:** `packages/telemetry/src/index.ts:10` (`TelemetryCarrier`), `packages/telemetry/src/index.ts:13-16` (`TelemetryPropagation.inject`/`extract`), `packages/telemetry/src/noop.ts:24-27` (`NOOP_TELEMETRY_PROPAGATION`), `packages/telemetry/src/memory.ts:358-391` (in-memory `inject`/`extract` with root fallback for absent, invalid, and unknown carriers).
- **Artifact says:** the Overview and FR-1..FR-9 cover spans, events, attributes, status, the no-op context, the in-memory context, and typed schemas. No requirement mentions injection, extraction, carriers, or remote parents.
- **Required change:** add a Must FR for the `TelemetryPropagation` capability: an opaque string-map `TelemetryCarrier`, `inject(context)` returning a detached carrier or `undefined`, `extract(carrier)` returning a receiver-owned parent, passive root fallback for absent/invalid/unknown carriers, and a shared `NOOP_TELEMETRY_PROPAGATION` that never inspects its arguments.

### Span links are not a requirement
- **Evidence:** `packages/telemetry/src/index.ts:18-21` (`SpanLink`), `packages/telemetry/src/index.ts:26` (`SpanOptions.links`), `packages/telemetry/src/index.ts:39` (`TelemetrySpan.addLink`), `packages/telemetry/CHANGELOG.md:7` (Breaking Change: "Adapters must implement `TelemetrySpan.addLink()`").
- **Artifact says:** no requirement mentions links, even though `addLink()` is an adapter-breaking change in the package's `[Unreleased]` changelog.
- **Required change:** add a Must FR for links: `SpanOptions.links` at creation plus `TelemetrySpan.addLink()` after start, ordered and copied attributes, a settled target stays linkable, a settled source ignores calls, and failed link calls are atomic and never throw.

### Metrics are not a requirement
- **Evidence:** `packages/telemetry/src/metrics.ts:19-36` (`TelemetryCounter`, `TelemetryUpDownCounter`, `TelemetryHistogram`, `TelemetryMetrics` factories), `packages/telemetry/src/metrics.ts:38` (`TelemetryMetricAttributeDefinition` rejects `cardinality: "high"`), `packages/telemetry/src/metrics.ts:124-140` (`createTypedMetrics`), `packages/telemetry/src/noop.ts:17-21` (`NOOP_TELEMETRY_METRICS`), `packages/telemetry/src/memory.ts:406-413` (`getMetrics()`).
- **Artifact says:** no requirement mentions counters, up-down counters, histograms, histogram exemplar contexts, or typed metric schemas.
- **Required change:** add a Must FR for the metrics capability: `counter`/`upDownCounter`/`histogram` factories, the optional exemplar `context` argument on histogram `record`, non-negative finite counter increments, and `createTypedMetrics` binding exact instrument names, kinds, metadata, and low-cardinality attributes.

### The adapter conformance suite is not a requirement
- **Evidence:** `packages/telemetry/package.json:13-16` (public `./testing` subpath), `packages/telemetry/src/testing/conformance.ts:70-517` (`createTelemetryAdapterConformance`, 17 cases in 9 groups), `packages/telemetry/src/testing/types.ts:5-21` (`TelemetryAdapterFixture`, `TelemetryAdapterFixtureFactory`, `TelemetryAdapterConformanceCase`).
- **Artifact says:** the stakeholder table names "Backend adapter author | Needs a stable contract with observable conformance semantics", but no requirement states the suite as a deliverable, and FR-7 covers only the in-memory adapter.
- **Required change:** add a Must FR for the `./testing` subpath: a runner-independent conformance suite driven by a fixture contract that supplies a fresh context and a normalized `RecordedTelemetrySpan` reader, covering the ten adapter obligations the package README lists.

### Advisory: context capability members are not stated
- **Evidence:** `packages/telemetry/src/index.ts:32-34` (`readonly metrics?` and `readonly propagation?` on `TelemetryContext`), `packages/telemetry/CHANGELOG.md:8` (Breaking Change: adapters must carry them through roots, spans, and extracted parents).
- **Artifact says:** no requirement states that contexts and spans expose optional `metrics` and `propagation` capabilities, nor that child spans and extracted parents carry the same capability objects.
- **Required change:** state the capability members and the propagation rule, or fold them into the propagation and metrics requirements above.

### Advisory: runtime neutrality needs a scope caveat
- **Evidence:** `packages/telemetry/src/testing/conformance.ts:1` (`import { deepStrictEqual, doesNotThrow, fail, ok, strictEqual } from "node:assert/strict"`), `packages/telemetry/package.json:13-16`, `packages/telemetry/README.md:316` ("The testing subpath uses Node's assertion APIs; the root telemetry package remains runtime-neutral.").
- **Artifact says:** NFR-2 states the system shall remain runtime-neutral without ambient context APIs, with no scope caveat, while the package root has zero runtime dependencies and the only Node import in the whole package sits in the Node-only `./testing` subpath.
- **Required change:** scope NFR-2 to the root entrypoint and state that the `./testing` subpath is Node-only.

## Open questions

- None. The code fully determines the missing requirements.
