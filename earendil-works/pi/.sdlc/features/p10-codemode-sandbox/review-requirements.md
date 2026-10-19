---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The coding-agent script surface is not stated in any requirement
- **Evidence:** `packages/coding-agent/src/extensions/codemode/execute.ts:600` (`searchTools`), `:622` (`describeTool`), `:634` (`describeNamespace`), `:735-765` (`models.getModelsOfType`, `models.getAvailableOfType`, `models.getModelOfType`, `models.classify`, `models.generateImages`); enabled by `packages/coding-agent/src/extensions/codemode/index.ts:19-20` (`CodemodeExtensionOptions.models`).
- **Artifact says:** FR-2 lists the script surface as `tools`, `ALL_TOOLS`, `text`, `image`, `exit`, `console.*`, `store`/`load` and host `globals`; FR-10 mentions only that the coding agent wraps `execute()`.
- **Required change:** add a requirement for the coding agent's script globals (`searchTools`, `describeTool`, `describeNamespace`, and the `models` namespace with its five functions) and say they are coding-agent globals, not part of the package's script environment.

### The coding agent makes the session the owner of `store()` writes
- **Evidence:** `packages/coding-agent/src/extensions/codemode/tool.ts:42` (`CODEMODE_STORE_ENTRY_TYPE = "codemode-store"`), `packages/coding-agent/src/extensions/codemode/execute.ts:240-251` (`readCodemodeStore` folds the branch's `codemode-store` entries into the snapshot), `packages/coding-agent/src/extensions/codemode/execute.ts:541-544` (a successful script appends its writes as a custom entry).
- **Artifact says:** FR-6 says the store is a caller-owned snapshot and the sandbox itself keeps nothing; nothing says the coding agent persists the writes to the session, per branch.
- **Required change:** state that the coding agent reads `load()` from the branch's `codemode-store` entries and appends a `codemode-store` entry with the writes of a successful script, so values persist across codemode calls on the same path.

### The coding agent's own tool behaviour is not stated
- **Evidence:** `packages/coding-agent/src/extensions/codemode/index.ts:44` (`defaultActive: false`), `packages/coding-agent/src/extensions/codemode/tool.ts:383` (`exposure: "model-only"`), `packages/coding-agent/src/extensions/codemode/tool.ts:320-356` (`codemode.mode` `on`/`only` decides which tools the description lists, `codemode.inlineBudget` caps the description), `packages/coding-agent/src/core/settings-defaults.ts:57-60` (`mode: "on"`, `inlineBudget: 3000`), `packages/coding-agent/src/extensions/codemode/tool.ts:387` (`constrainedSampling` with `CODEMODE_SOURCE_GRAMMAR`), `packages/coding-agent/src/extensions/codemode/execute.ts:510` (the coding agent sets the sandbox deadline to `Infinity`, so only `timeout_ms` bounds a script), `packages/coding-agent/src/extensions/codemode/execute.ts:557-563` (`max_output_tokens` truncates the output and spills the full text to a file).
- **Artifact says:** FR-4 says the system accepts a `// @options:` line; FR-10 says the coding agent wraps `execute()`. Neither says the coding agent is the party that enforces the options, that the tool ships inactive and model-only, or that the mode and budget settings shape the description.
- **Required change:** extend FR-10 (or add requirements) to state that the coding agent enforces `timeout_ms` and `max_output_tokens`, registers the tool inactive and model-only, and that `codemode.mode` and `codemode.inlineBudget` decide which tools the model is shown.

### The sandbox's mutable tool table is not stated
- **Evidence:** `packages/codemode/src/runtime/execution.ts:479-486` (`registerTool` throws on a duplicate name, `unregisterTool` removes one); `packages/codemode/test/sandbox.test.ts:400` ("supports register and unregister between executions").
- **Artifact says:** FR-1 and FR-2 describe a fixed set of injected tools; no requirement says a host can change the tool table between executions.
- **Required change:** add a requirement that the tool table is mutable between executions (registering a duplicate name throws) and that call records of earlier executions are unaffected.

### Advisory: NFR-6's 20 ms figure has no measurement in the repo
- **Evidence:** `packages/codemode/README.md:362` is the only source for "about 20 ms including VM creation"; no test or benchmark under `packages/codemode/test/` measures worker startup, and `packages/durable/test/codemode-bench.ts` measures code mode overhead, not startup.
- **Artifact says:** NFR-6 requires worker-thread startup including VM creation to stay around 20 ms.
- **Required change:** present the figure as a documented target from the README rather than a measured guarantee, or add a benchmark.

## Open questions
- Is the second consumer of the sandbox, `packages/durable/src/codemode/` (`CODEMODE_MODULE_VERSION = 2`, `packages/durable/src/codemode/codemode.ts:86`), part of this feature? These requirements describe the package and the coding-agent extension only, while the deterministic-run requirement exists for a durable host.
