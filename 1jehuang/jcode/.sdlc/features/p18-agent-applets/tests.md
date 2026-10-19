---
title: "Agent Applets"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Agent Applets

## Scope

Covers the applet wire types and their validation, the per-session persistence layer, the `applet` tool, the MCP resource bridge, and the harness API translation of the applet requests and events.

Out of scope: the Desktop renderer that draws the node tree, which lives outside this repository, and any provider-side implementation that consumes `ProviderMessage` and `HostMessage`.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Instance id generation in `crates/jcode-app-core/src/tool/applet_tests.rs` (`ids_are_slugs_with_hex`) | Titles `"Sales Chart!"` and `"!!"` | A slug of the title plus four hex digits, with `applet-` as the fallback slug for a title with no alphanumeric characters |
| TC-2 | Desktop capability gating in `crates/jcode-app-core/src/tool/applet_tests.rs` (`applet_requires_desktop_capability`) | A `Registry` with desktop UI enabled and disabled | The `applet` tool appears in the definitions only when enabled, is absent from the base tool map, and execution fails when disabled |
| TC-3 | Action message formatting in `crates/jcode-app-core/src/tool/applet_tests.rs` (`action_message_is_compact`) | An action `select` with args `{"id":2}`, state `{"q":"x"}` | The exact message `[applet action] instance \`chart-3f2a\` ("Title"): \`select\` args {"id":2}\nstate: {"q":"x"}` |
| TC-4 | Documented node shapes validate in `crates/jcode-app-core/src/tool/applet_tests.rs` (`documented_shapes_validate`) | A view using select, tabs, key_value, button, toggle, input, list_item, progress and text, built exactly as the tool description spells them | The description contains the documented field names, and the document deserializes and validates against the agent manifest |
| TC-5 | Session persistence lifecycle in `crates/jcode-base/src/applets.rs` (`tests::lifecycle`) | Mount, remount, patch, state write, move and close on a session | Remount keeps the position and bumps the revision, a patch bumps it again, a stale base revision fails, a state write keeps the revision, a move bumps it, an invalid id and an invalid state fail, and close removes the instance |
| TC-6 | MCP resource to document mapping in `crates/jcode-base/src/applets.rs` (`mcp_tests::mcp_resources_map_to_documents`) | A `ui://` resource with `text/html`, a `ui://` resource with `text/uri-list`, a resource with the native applet mime type, and a non-matching resource | HTML becomes an `html` view, a URI list becomes a card with a `host.open_url` action, the native resource becomes its document, and the non-matching resource returns nothing |
| TC-7 | Agent manifest and snapshot in `crates/jcode-applet-types/src/agent.rs` (`tests::manifest_is_valid_and_allows_html`, `tests::snapshot_round_trips_and_defaults_empty`) | The agent manifest and a snapshot with one instance | The manifest validates and allows `html` but not `read_files`; an empty snapshot defaults to no instances; a populated snapshot round-trips unchanged and its document validates |
| TC-8 | Agent tool surface follows the desktop capability in `crates/jcode-app-core/src/agent_tests.rs` (`user_response_capability_updates_locked_tool_surface`) | An agent with the desktop response capability toggled on and off | The `applet` tool is present only while the capability is on, and an unchanged capability keeps the locked tool cache |
| TC-9 | Tool description and schema budgets in `crates/jcode-app-core/src/tool/tests.rs` (`tool_descriptions_stay_under_token_cap`, `tool_parameter_descriptions_stay_under_token_cap`, `only_the_known_open_world_tools_are_ineligible_for_openai_strict_mode`) | The registry tool definitions | The `applet` description and its `placement` parameter description stay exempt and within the caps, and the `applet` schema stays on the list of tools that cannot use strict mode because its view tree is open-world |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | Wire round trip of a rich document in `crates/jcode-applet-types/tests/applet_types.rs` (`round_trips_a_rich_document_with_images_and_placements`) | A mount message with an overlay placement, a persistent lifetime, a declared asset and a stack of input, grid, image and list nodes | The message survives a serialize and deserialize round trip, the placement is an overlay, and the document validates |
| TC-11 | Placement independence from tool calls in `crates/jcode-applet-types/tests/applet_types.rs` (`placements_are_independent_of_tool_calls`) | The panel, sidebar, composer, background and three inline placements | Every placement parses and re-serializes to the same `kind`, and inline placements carry the tool call, message and end anchors |
| TC-12 | Unknown node degradation in `crates/jcode-applet-types/tests/applet_types.rs` (`unknown_nodes_degrade_to_fallback_and_survive_round_trip`) | A stack whose child is a `map_view` node with fallback text and an extra field | The child becomes an unknown node keeping its type name, its fallback and its raw fields, the document still validates, and re-serialization restores the original object |
| TC-13 | Malformed known nodes fail in `crates/jcode-applet-types/tests/applet_types.rs` (`malformed_known_nodes_are_errors`) | A `button` node with no `on_press` | Deserialization fails with an `invalid \`button\` node` error rather than degrading to an unknown node |
| TC-14 | Capability gating of host actions and image sources in `crates/jcode-applet-types/tests/applet_types.rs` (`capabilities_gate_host_actions_and_image_sources`) | Documents using `host.open_url`, a `javascript:` URL, a remote image over https and http, a relative image path, an `html` node and an unknown host action | Each is refused with the matching error, and the same documents pass once the matching capability is declared |
| TC-15 | Limits and references in `crates/jcode-applet-types/tests/applet_types.rs` (`enforces_limits_and_references`) | An unknown asset reference, a duplicated node key, a tree deeper than the limit, an oversized inline image, a ragged table and an unsupported asset mime type | Each is refused with the matching validation error |
| TC-16 | Patch revisioning, atomicity and path restriction in `crates/jcode-applet-types/tests/applet_types.rs` (`patches_are_revisioned_atomic_and_path_restricted`) | A patch that replaces a nested view field, appends a child and writes a state key, plus a stale base revision, a forbidden path, a missing path and a patch that breaks a known node | The valid patch produces revision 2 with the new view and state, and each invalid patch is refused without changing the document |
| TC-17 | Manifest schema, launchers and tool card claims in `crates/jcode-applet-types/tests/applet_types.rs` (`manifest_schema_and_tool_card_claims`) | A manifest with sidebar, shortcut and startup launchers and a tool card claim, and a copy with schema `jcode.applet/2` | The manifest validates, singleton defaults hold, the tool card matches on tool and action but not on an unlisted action or a missing action, and a future major schema is rejected |
| TC-18 | Harness API translation in `crates/jcode-harness-api-server/src/translate_tests.rs` (`applet_requests_and_state_translate`) | An `applet_action` request and a `close_applet` request, and an `applet_state` event | The requests forward to the daemon with their instance, action, state and source key, and the event reaches clients as a full snapshot, including an empty one |
| TC-19 | Applet state during attachment hydration in `crates/jcode-harness-api-server/src/translate_tests.rs` (`attachment_recovery_preserves_directive_in_both_history_state_orders`, `attachment_recovery_suppresses_empty_active_completed_and_blank_directives_once`) | A bridge that attaches a client to a session | The bridge emits an `AppletState` frame during attachment, next to the side panel state, in both history and state orderings |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-20 | The full agent-facing applet loop in `crates/jcode-app-core/src/tool/applet_tests.rs` (`mount_patch_wait_and_close`) | Mount an applet in a session with an isolated `JCODE_HOME`, read the stored snapshot, attempt an update with an invalid view, patch the title, run an update with `wait` and deliver an action to the waiting call, then close the instance | The mount stores an inline placement anchored at the calling tool call, the invalid update is rejected without changing the stored instance, the patch changes the title, the waiting call returns the delivered action, and the close empties the session |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-21 | Patch applied at a stale base revision | Refused with a revision mismatch, and the stored document is unchanged |
| TC-22 | Patch targeting a path outside `/view`, `/state` and `/title` | Refused with a forbidden path error |
| TC-23 | Patch targeting a path that does not exist | Refused with a path not found error |
| TC-24 | Patch whose result is not a valid document | Refused as a whole with an invalid document error, so no half-updated document survives |
| TC-25 | Image node referencing an asset that was never declared | Validation fails with an unknown asset error |
| TC-26 | Two nodes sharing the same `key` | Validation fails with a duplicate key error |
| TC-27 | View tree deeper than the depth limit | Validation fails with a too deep error |
| TC-28 | Inline base64 image above the inline image size limit | Validation fails with an inline image too large error |
| TC-29 | Table whose row width differs from the column count | Validation fails with a ragged table error |
| TC-30 | Asset declared with a mime type that is not a supported image type | Validation fails with an unsupported mime error |
| TC-31 | Known node type with a missing required field | Deserialization fails instead of degrading to an unknown node |
| TC-32 | Host action with an unknown `host.` prefix | Validation fails with an invalid value error |
| TC-33 | `host.open_url` with a `javascript:` URL | Validation fails, because only `http`, `https` and `mailto` are accepted |
| TC-34 | Remote image over plain http | Validation fails, because remote images must use https |
| TC-35 | Image path that is not absolute | Validation fails, because image paths must be absolute |
| TC-36 | Instance id containing characters outside `[A-Za-z0-9-_.]`, or longer than 64 characters | The mount is refused with an id validation error |
| TC-37 | User state written as a non-object | The state write is refused and the stored document is unchanged |
| TC-38 | `applet` tool called on a client that does not advertise the desktop capability | The tool is not advertised and execution fails |
| TC-39 | MCP resource whose uri is not a `ui://` uri and whose mime type is not the native applet type | The resource is not mounted and is passed through as text |
| TC-40 | More than 64 instances in one session | The mount is refused with a message naming the maximum |

## Test Infrastructure

- Every test that touches the store sets `JCODE_HOME` to a temporary directory and holds `crate::storage::lock_test_env()` so parallel tests do not share state.
- `crates/jcode-app-core/src/tool/applet_tests.rs` uses a `Home` guard that restores the previous `JCODE_HOME` on drop.
- The `applet` tool is exercised directly through `AppletTool::new()` and through an empty `Registry` for the capability checks.
- A waiting tool call is released by calling `deliver_to_waiter` from the test, which exercises the real oneshot path rather than a mock.
- The harness API tests use the bridge translation layer directly, with no socket and no running server.
- No provider, network access or Desktop renderer is required by any test in this plan.
- Useful commands: `cargo test -p jcode-applet-types`, `cargo test -p jcode-base applets`, `cargo test -p jcode-app-core applet`, `cargo test -p jcode-harness-api-server translate`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-10, TC-12, TC-4 |
| FR-2 | TC-14, TC-15, TC-5, TC-4 |
| FR-3 | TC-2, TC-20 |
| FR-4 | TC-1, TC-20 |
| FR-5 | TC-5, TC-20 |
| FR-6 | TC-16, TC-20, TC-21, TC-22, TC-23, TC-24 |
| FR-7 | TC-5, TC-11 |
| FR-8 | TC-5, TC-20 |
| FR-9 | TC-18, TC-19, TC-20 |
| FR-10 | TC-3, TC-18, TC-20 |
| FR-11 | TC-20 |
| FR-12 | TC-5, TC-18, TC-37 |
| FR-13 | TC-11, TC-5, TC-20 |
| FR-14 | TC-6, TC-39 |
| FR-15 | TC-14, TC-6 |
| NFR-1 | TC-10, TC-4 |
| NFR-2 | TC-12, TC-13 |
| NFR-3 | TC-15, TC-27, TC-28, TC-29, TC-30 |
| NFR-4 | TC-14, TC-32, TC-33, TC-34, TC-35 |
| NFR-5 | TC-5, TC-16, TC-24, TC-37 |
| NFR-6 | TC-18, TC-19 |
| NFR-7 | TC-2, TC-8, TC-38 |

## Known gaps

- The 64-instance cap has no dedicated automated test. TC-40 records the expected behavior, but no test mounts 65 instances to prove it.
- No test covers the Desktop renderer. The fallback rendering of an unknown node, the placement geometry, and the host action execution are asserted by the wire contract and the client protocol, not by a test in this repository.
- The MCP mount path (`mount_mcp_resource`) is covered for document mapping, but the anchored placement, the generated instance id and the rendered-UI tool output are not asserted by a test.
- The `wait` timeout and the graceful shutdown interruption are not covered; only the successful delivery path is tested.
