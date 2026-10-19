<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Observability

<!--
This file inventories the project's observability surface: metrics, logging, tracing, and alerting.
The project ships no observability backend.
packages/telemetry is a contract that a host application can bind to a backend, not a running collector.
Service-level targets do not exist because .sdlc/context/service-levels.md is absent.
Update this file when the monitoring stack changes.
-->

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | None | Not configured (contract only) |
| Logging | Local files under ~/.pi/agent | In use (local files only) |
| Tracing | packages/telemetry contracts only | Not configured (contract only) |
| Profiling | npm run profile:tui, npm run profile:rpc | Not configured (ad-hoc profilers only) |

No package in the workspace declares an observability backend.
There is no OpenTelemetry SDK, Prometheus client, Datadog, Sentry, Jaeger, Zipkin, Loki, ELK, or Grafana dependency, configuration, or endpoint in the repository.
The only HTTP servers in the repo are OAuth callback servers (packages/ai/src/auth/oauth/callback-server.ts, packages/mcp/src/oauth/callback.ts) and a chord socket manager.
There is no metrics scrape endpoint and no /health or /ready endpoint.

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| @earendil-works/pi-telemetry (packages/telemetry) | Tracing and metrics contracts | Contract only, no exporter and no backend binding |

### Telemetry contract (packages/telemetry)

packages/telemetry is the only telemetry library in the repository.
It has zero runtime dependencies and ships no exporter, sampler, or backend SDK.

| Export | Purpose |
|---|---|
| TelemetryContext | Adapter seam. startSpan(options, callback) returns a promise and owns span settlement. |
| TelemetrySpan | addEvent, setAttributes, setStatus, addLink. Also acts as the child-span parent context. |
| TelemetryMetrics | counter, upDownCounter, and histogram factories. |
| TelemetryPropagation | inject(context) and extract(carrier) over an opaque TelemetryCarrier (Record<string, string>). |
| defineTelemetrySchema | Typed identity function over serializable schema data. Performs no runtime validation. |
| createTypedSpanStarter | Binds one context to the span vocabulary of one or more schemas. |
| createTypedMetrics | Binds instrument names, kinds, and attributes to one or more schemas. |
| InMemoryTelemetryContext | Reference adapter. Process-local, unbounded, records no timestamps. |
| NOOP_TELEMETRY_CONTEXT, NOOP_TELEMETRY_METRICS, NOOP_TELEMETRY_PROPAGATION | Shared inert fallbacks that never inspect their arguments. |
| @earendil-works/pi-telemetry/testing, createTelemetryAdapterConformance | Runner-independent adapter conformance suite, 17 cases in 8 groups (capabilities, metrics, links, propagation, status, recording, parentage, passivity). |

The Adapter Contract section of packages/telemetry/README.md lists 10 explicit adapter obligations.
Adapter authors are expected to pass the ./testing conformance suite.
The in-memory adapter records spans, events, links, and measurements with no timestamps, and its storage is unbounded and process-local.

### Instrumented schemas

| Schema | Location | Contract version |
|---|---|---|
| AI_TELEMETRY_SCHEMA | packages/ai/src/telemetry.ts | 1 |
| DURABLE_TELEMETRY_SCHEMA | packages/durable/src/harness/telemetry.ts | 1 |

AI_TELEMETRY_SCHEMA vocabulary:

| Kind | Name | Attributes |
|---|---|---|
| span | pi.ai.request | start: provider, api, model (all required), reasoning (optional). end: stop, usage.input, usage.output, usage.cache_read, usage.cache_write, cost.total, response.id. |
| span | pi.ai.poll | Same shape as pi.ai.request, for one deferred-response poll. |
| event | pi.ai.first_chunk | None. |
| event | pi.ai.block | type (text, thinking, or tool_call), index, chars, tool (optional, tool-call blocks only). |
| metric | pi.ai.request.duration | Histogram, unit ms. Attributes: provider, model, stop. |
| metric | pi.ai.first_chunk.duration | Histogram, unit ms. Attributes: provider, model. |
| metric | pi.ai.tokens | Counter, unit token. Attributes: provider, model, kind (input, output, cache_read, or cache_write). |
| metric | pi.ai.cost | Counter, unit USD. Attributes: provider, model. |

Instrumentation is attached at the Models layer through observeModelRequest (packages/ai/src/models.ts calls packages/ai/src/telemetry.ts).
Direct provider and API calls are not instrumented.
The parent span arrives through StreamOptions.telemetry (packages/ai/src/types.ts).
No prompt, completion, reasoning, or tool-argument content is recorded.

DURABLE_TELEMETRY_SCHEMA vocabulary:

| Kind | Name | Attributes |
|---|---|---|
| span | pi.durable.submit | start: submission.type, conversation.id. end: submission.id, result. |
| span | pi.durable.phase | start: task.id, task.name, phase, kind (run or abort), attempt, resumed. end: outcome, tool.name, tool.call_id. |
| event | pi.durable.entry | entry.id, entry.kind. |
| event | pi.durable.submission | submission.id, status, answer.entry_id. |
| event | pi.durable.report | type, reason, extension, task.id. |
| event | pi.durable.checkpoint | phase. |
| event | pi.durable.replay | tool.name. |
| metric | pi.durable.reports | Counter. Attribute: type. |
| metric | pi.durable.phase.duration | Histogram, unit ms. Attributes: task, phase, outcome. |
| metric | pi.durable.tasks.active | Up-down counter. Attribute: task. |

Durable attributes hold record identifiers and control metadata, never messages, arguments, or results, and diagnostics are capped at 500 characters.
Wiring: packages/durable/src/harness/scheduler.ts starts phase spans and metrics, packages/durable/src/harness/submissions.ts starts submit spans, packages/durable/src/harness/harness.ts counts reports, and packages/durable/src/session/session.ts emits entry and submission events.
The host supplies the adapter through HarnessOptions.telemetry (packages/durable/src/harness/types.ts).

### Packages with no instrumentation

| Package | Spans, events, and metrics |
|---|---|
| packages/agent (@earendil-works/pi-agent-core) | None. The package has no telemetry code and does not depend on pi-telemetry. |
| packages/coding-agent | None. The only telemetry-shaped behavior is the install ping described below. |
| packages/mcp | None. |
| packages/codemode | None. |
| packages/env | None. |
| packages/chord (@earendil-works/chord) | Carries a TelemetrySpan on its Context (withTelemetry, traceIn; BACKGROUND_CONTEXT and TODO_CONTEXT use NOOP_TELEMETRY_CONTEXT). It does not instrument hosts, methods, or network frames, and packages/chord/README.md says so. |

## Log aggregation

- No log aggregation destination is configured.
- No structured logging library is used, and no package contains a logger.
- No retention, sampling, or filtering policy exists outside the crash log's own bounds.

### Local log files

| Path | Source | Content |
|---|---|---|
| ~/.pi/agent/crashes.json | packages/coding-agent/src/core/crash-log.ts | JSON array of records with timestamp, version, kind (uncaught_exception or fatal_error), message, stack, sessionFile, and cwd. At most 5 records, 7-day expiry. Extension stack-trace attribution through findExtensionStackMatches. |
| ~/.pi/agent/pi-debug.log | packages/coding-agent/src/config.ts, getDebugLogPath | Debug log for the coding agent. |
| ~/.pi/agent/pi-tui-debug.log | packages/tui/src/tui-main-screen.ts | Redraw log, enabled by PI_TUI_DEBUG_REDRAW=1. |
| ~/.pi/agent/pi-tui-crash.log | packages/tui/src/tui-main-screen.ts | Rendered lines captured when a line overflows the terminal width. |
| /tmp/tui | packages/tui/src/tui-main-screen.ts | Frame dumps, enabled by PI_TUI_DEBUG=1. |
| Path in PI_TUI_WRITE_LOG | packages/tui/src/terminal.ts | Raw ANSI stream capture. The value is a file path, or a directory, in which case the file is named tui-<timestamp>-<pid>.log. |

packages/coding-agent/src/core/timings.ts records startup phase timings only when PI_TIMING=1 and prints them to stderr.
packages/coding-agent/src/main.ts calls printTimings() in print, rpc, and interactive modes, and PI_STARTUP_BENCHMARK (interactive mode only) runs the startup path and then prints them.
packages/env exposes ConnectionOptions.onLog (packages/env/src/connection.ts), which receives the daemon's stderr stream and the ssh transport's warnings (packages/env/src/ssh.ts).

### Outbound network diagnostics

| Signal | Endpoint | Gate |
|---|---|---|
| Install ping | GET https://pi.dev/api/report-install?version=<v> | PI_TELEMETRY env var when set, otherwise the enableInstallTelemetry setting (default true). Suppressed when PI_OFFLINE is set. 5 s timeout, fire-and-forget, User-Agent pi/<version> (platform; node/x.y.z; arch). |
| Version check | GET https://pi.dev/api/latest-version | 10 s timeout, PI_SKIP_VERSION_CHECK opt-out, skipped when PI_OFFLINE is set. |
| Provider attribution headers | OpenRouter HTTP-Referer, X-OpenRouter-Title, and X-OpenRouter-Categories; NVIDIA X-BILLING-INVOKE-ORIGIN; Cloudflare User-Agent; OpenCode x-opencode-session and x-opencode-client | The same install telemetry switch (packages/coding-agent/src/core/provider-attribution.ts). |

The enableAnalytics setting (default false) generates deviceId and trackingId UUIDs in settings.json, but no analytics sink in this repository consumes them.
packages/coding-agent/src/core/bug-report.ts strips both identifiers from bug reports.

## Tracing

- No trace backend is configured.
- No sampling strategy is defined.
- No exporter ships with the contract, so spans go nowhere unless a host application supplies an adapter.
- There is no W3C Trace Context or B3 support in the repository. The carrier format is adapter-owned.
- There is no ambient current span and no AsyncLocalStorage. Parents are passed explicitly through TelemetryContext arguments.

Cross-process propagation uses the opaque TelemetryCarrier.
The in-memory adapter's carrier codec is pi-memory-scope (a UUID) plus pi-memory-span (a numeric span id).
That carrier survives a JSON round trip and a process boundary, and packages/telemetry/test/propagation.test.ts with packages/telemetry/test/propagation-worker.ts prove cross-process continuation.

Durable stores opaque carriers on tasks and submissions (TaskRecord.trace, TaskRecord.links, and SubmissionRecord.trace in packages/durable/src/types.ts).
packages/durable/src/harness/scheduler.ts calls propagation.extract on task.trace to continue the parent trace, so a task resumes its trace after a restart.
packages/ai takes the parent span through StreamOptions.telemetry and starts pi.ai.request or pi.ai.poll from it.

## Alerting

No alert rules are defined.
No alert routing, on-call schedule, or paging target exists.

The only gate signals are CI workflows.

| Signal | Source | Trigger | Severity |
|---|---|---|---|
| CI | .github/workflows/ci.yml | Push and pull request against main | Blocking |
| npm audit | .github/workflows/npm-audit.yml | Daily at 07:37 UTC, plus manual dispatch | Advisory |
| Nix flake check | .github/workflows/nix.yml | Version tag push, and pull requests that touch the flake or the model catalog pin | Blocking |
| Issue analysis | .github/workflows/issue-analysis.yml | The pi-analyze label, or an @issuron analyze comment | Advisory |

## Dashboards

No dashboards exist, and no dashboard source files or Grafana definitions are in the repository.

## SLO reference

No service-level objectives, indicators, or error budgets exist.
.sdlc/context/service-levels.md is absent.
That file is where service-level targets would live, next to this one.
Feature-level observability plans have no SLO targets to reference.

## Known gaps

- No exporter or backend ships with packages/telemetry, so instrumented spans and metrics are discarded unless a host application supplies an adapter.
- There is no .sdlc/context/service-levels.md, so no SLO, SLI, or error budget can be referenced.
- There is no metrics scraping endpoint. The instrumented metrics are only ever recorded by a supplied adapter.
- packages/telemetry/README.md is stale. It imports AGENT_TELEMETRY_SCHEMAS from @earendil-works/pi-agent-core (lines 433 and 437) and states that pi-agent-core retains its agent-loop and session instrumentation and schemas (line 479). packages/agent exports no such symbol and contains no telemetry code.
