---
title: "Canvas Dynamic UI"
status: done
---

# Test Plan: Canvas Dynamic UI

## Scope

This plan covers the Canvas plugin's agent tool, node eligibility, CLI, widget presenter, A2UI validation and board-widget composition, hosted renderer routes, config and doctor migration, and asset build scripts.
The Control UI iframe hosting surface is covered under FEAT-p8; only the plugin-owned contracts are tested here.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tool preserves present placement and hosted target parameters | present with target, x, y, width, height | node.invoke canvas.present with url and placement |
| TC-2 | Tool accepts target as the navigate URL alias | navigate with target instead of url | node.invoke canvas.navigate with the alias as url |
| TC-3 | Tool forwards gateway and node selection options | gatewayUrl, gatewayToken, timeoutMs, node query | Same options reach listNodes and callGatewayTool |
| TC-4 | Tool rejects an explicit legacy non-macOS Canvas node | node query matching a Linux node | Error naming the canvas.present eligibility requirement |
| TC-5 | Tool rejects malformed presenter arguments before invoking a node | Invalid action or params | Validation error with no node call |
| TC-6 | Validator accepts the v0.9 create, component, data, and delete message set | JSONL with createSurface, updateComponents, updateDataModel, deleteSurface | Version v0.9 with the message count |
| TC-7 | CLI preserves present target and placement fields | canvas present with target and placement flags | node.invoke params carry url and placement |
| TC-8 | CLI prints the full Gateway response in JSON mode | --json flag | Full response JSON on stdout |
| TC-9 | CLI keeps the Gateway deadline longer than an explicit node deadline | --invoke-timeout with --timeout | Transport timeout exceeds the node deadline by the grace margin |
| TC-10 | CLI resolves and invokes a paired node when an older Gateway lacks node.list | Gateway without node.list | Falls back to node.pair.list and invokes |
| TC-11 | Board kind exposes only its two registered renderer bundles as public static resources | Arbitrary resource path | Non-bundle paths return undefined |
| TC-12 | Board kind rejects a document when its renderer resource was not provisioned | Valid source with missing bundle URL | Error naming the unavailable renderer resource |
| TC-13 | Migration keeps only enabled from the legacy root host config | Config with host root, port, liveReload | Only host.enabled survives |
| TC-14 | Migration removes an empty retired host object without creating replacement config | Empty retired host object | No replacement config written |
| TC-15 | Migration is idempotent for canonical or absent config | Canonical or missing config | No changes reported |
| TC-16 | Migration moves an unresolved older root into the pending plugin setting | Older canvasHost.root value | Value preserved under the plugin setting |
| TC-17 | Config parses and resolves only host.enabled | Plugin config record | host.enabled or empty host |
| TC-18 | Config honors the internal skip-host test switch | Truthy skip switch | Host reported disabled |
| TC-19 | Presenter shows the hosted URL on a versioned macOS node | Hosted document and eligible node | node.invoke canvas.present, kind node result |
| TC-20 | Presenter reports offline nodes as unavailable | No connected eligible node | no_eligible_node error |
| TC-21 | Presenter leaves no stale visible content when atomic presentation fails | Failing node invoke | node_error with no partial panel state |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-22 | Plugin entry registers the macOS-only presenter surface and command policy | Plugin registration | Presenter, node policy, tool, and CLI feature registered |
| TC-23 | Plugin entry uses host.enabled as the single presenter and hosted-resource gate | host.enabled false | Presenter and routes skipped, tool and CLI kept |
| TC-24 | Plugin entry defers A2UI asset implementation until the route is used | Fresh startup | Renderer module loads only on first route hit |
| TC-25 | Plugin entry defers Canvas CLI and tool implementations until use | Fresh startup | CLI and tool modules load only on first use |
| TC-26 | Doctor flags and removes retired file-host settings | Retired canvasHost settings present | Settings removed with reported changes |
| TC-27 | Doctor ignores the default core document root | Root already at the default | No migration proposed |
| TC-28 | Doctor moves custom-root documents into the stable core layout | Documents under a custom root | Documents atomically copied to core storage |
| TC-29 | Doctor leaves a conflicting legacy document in place | Core target already exists | Warning kept, source retained for retry |
| TC-30 | Doctor cleans partial copies and retries the migration | Interrupted prior copy | Partial state removed, migration completes |
| TC-31 | Hosted route rejects Linux nodes that cannot resolve hosted document paths | Unresolvable hosted path | Unavailable response, no file read |
| TC-32 | Hosted route retries renderer root resolution after a transient filesystem failure | Transient failure then recovery | Bundle served after retry |
| TC-33 | Hosted route rejects missing, malformed, and traversal paths | Escaping or malformed path | Rejection without reading outside the root |
| TC-34 | Hosted route returns unavailable when renderer assets cannot be resolved | No bundle root found | Unavailable instead of an error page |
| TC-35 | File resolver opens directory index files through the fs-safe root | Directory path under root | Index file contents returned |
| TC-36 | File resolver rejects traversal paths | Path with parent segments | Rejection with no filesystem access outside root |
| TC-37 | Bundle script requires both prebuilt dialects when A2UI build dependencies are absent | Missing build deps | Error demanding both v0.8 and v0.9 bundles |
| TC-38 | Bundle script sorts hash inputs without locale-dependent collation | Tracked inputs | Stable hash across locales |
| TC-39 | Bundle script bounds tracked-input discovery and treats a timeout as a fallback | Slow discovery | Bounded wait, fallback build proceeds |
| TC-40 | Copy script throws a helpful error when assets are missing | Missing source assets | Actionable error message |
| TC-41 | Copy script skips missing assets when OPENCLAW_A2UI_SKIP_MISSING=1 | Missing assets, flag set | Skip with notice instead of failure |
| TC-42 | Copy script skips missing assets when OPENCLAW_SPARSE_PROFILE is set | Missing assets, sparse profile | Skip with notice instead of failure |
| TC-43 | Copy script copies nested bundled assets and removes stale output | Changed asset tree | Fresh nested copy, stale files removed |
| TC-44 | Copy script rejects overlapping source and output directories before cleaning output | Overlapping dirs | Refusal before any deletion |
| TC-45 | Runner executes native pnpm from npm_execpath directly | Native npm_execpath binary | Direct exec without a shell |
| TC-46 | Runner falls back to bare pnpm when native npm_execpath is not executable | Non-executable npm_execpath | Bare pnpm fallback |

## End-to-End Tests

No dedicated end-to-end tests exist for this feature.
Panel behavior is proven through node.invoke integration coverage and the macOS app surface.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-29 | Core target already exists during document migration | Source retained, warning names the conflict and the retry path |
| TC-33 | Traversal path against the renderer root | Rejected before any filesystem read |
| TC-4 | Explicit non-macOS node selected for presentation | Actionable eligibility error before any invoke |
| TC-20 | Panel requested with no connected Mac | no_eligible_node, chat widget still renders inline |

## Test Infrastructure

- Vitest suites colocated with sources (`extensions/canvas/**/*.test.ts`).
- Temporary directories for migration, resolver, and runner fixtures, cleaned per test.
- Gateway and node runtimes mocked at the plugin SDK boundary; no live node required.
- Prebuilt A2UI bundles stubbed or resolved from the source asset tree.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-3, TC-5, TC-7, TC-8, TC-9, TC-10 |
| FR-2 | TC-4, TC-31 |
| FR-3 | TC-7, TC-8, TC-9, TC-10 |
| FR-4 | TC-19, TC-20, TC-21, TC-22 |
| FR-5 | TC-6 |
| FR-6 | TC-11, TC-12 |
| FR-7 | TC-23, TC-24, TC-31, TC-32, TC-33, TC-34, TC-35, TC-36 |
| FR-8 | TC-17, TC-18, TC-22, TC-23 |
| FR-9 | TC-13, TC-14, TC-15, TC-16, TC-26, TC-27, TC-28, TC-29, TC-30 |
| FR-10 | Covered under FEAT-p8 hosting surface, no plugin-owned cases |
| NFR-1 | TC-33, TC-35, TC-36 |
| NFR-2 | TC-21, TC-29, TC-30, TC-44 |
| NFR-3 | TC-24, TC-25 |
| Build scripts | TC-37, TC-38, TC-39, TC-40, TC-41, TC-42, TC-43, TC-44, TC-45, TC-46 |
