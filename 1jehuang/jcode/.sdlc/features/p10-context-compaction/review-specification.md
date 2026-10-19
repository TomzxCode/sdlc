---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Data Models | the `[compaction]` table with the rows `reactive`, `proactive`, `semantic` | `[compaction]` has one `mode` key plus ten tuning keys: `mode`, `lookahead_turns`, `ewma_alpha`, `proactive_floor`, `min_samples`, `stall_window`, `min_turns_between_compactions`, `topic_shift_threshold`, `relevance_keep_threshold`, `goal_window_turns`, `max_context_tokens` (`crates/jcode-config-types/src/lib.rs:363-403`). The `CompactionMode` values are `reactive` (default), `proactive`, `semantic` (`:20-47`). | Replace the table with the real keys, types, and defaults. |
| Data Models | "`OpenAICompaction` \| ContentBlock" and "`stable_message_hash` \| string", "`cache_relevant_message_hashes` \| list" | `stable_message_hash` returns `u64` and `cache_relevant_message_hashes` returns `Vec<u64>` (`crates/jcode-message-types/src/lib.rs:409,471`). `OpenAICompaction` carries `encrypted_content: String` (`:208-210`). | Correct the types and the `OpenAICompaction` payload. |
| Architecture | the diagram shows only the app-core path | The map omits the TUI-local path (`crates/jcode-tui/src/tui/app/model_context.rs:1341,1367,1503,1520,1864,1892`; `conversation_state.rs:244-320`), the provider-native path (`crates/jcode-app-core/src/agent.rs:911-980`, `turn_streaming_mpsc.rs:409,1022,1366-1368`, `turn_loops.rs:295,722,968-969`; `crates/jcode-provider-openai/src/request.rs:718`), the emergency recovery paths (`crates/jcode-app-core/src/agent/compaction.rs:130-350`; `crates/jcode-base/src/compaction.rs:951-1090,1621-1700`), and the KV-cache invalidation on compaction (`crates/jcode-app-core/src/agent/compaction.rs:25-31`). | Extend the diagram with the TUI-local path and name the other paths in the overview. |
| Sequences | one sequence, "Reactive compaction on a turn" | There are at least five distinct sequences: reactive, proactive, and semantic background compaction; the hard compact at the critical threshold; the context-limit error recovery; the HTTP 413 and image-rejection recovery; and provider-native compaction. | Add the missing sequences. |
| Out of Scope | "Provider-specific compaction APIs that are not already integrated." | OpenAI provider-native compaction is integrated and configurable through `[provider] openai_native_compaction_mode` (`crates/jcode-provider-openai/src/request.rs:238,718`; `crates/jcode-app-core/src/agent.rs:911-980`; `crates/jcode-base/src/compaction.rs:418-455`; `crates/jcode-config-types/src/lib.rs:1263-1264`). | Reword to: "Provider-specific compaction APIs other than OpenAI native compaction, which is integrated and configured through [provider] openai_native_compaction_mode." |

## Missing Information

- The emergency truncation and image-stripping helpers are not described: `crates/jcode-compaction-core/src/lib.rs:608-760` (`emergency_truncate_large_payloads`, `emergency_strip_large_images`, `strip_large_images_in_contents`, `decay_old_tool_images_in_contents`).
- The manual compaction request path is not described (`crates/jcode-app-core/src/agent/compaction.rs:55-114`, the server handler at `crates/jcode-app-core/src/server/client_actions.rs:1231`).
- The interaction with hibernation is not described: hibernation is skipped while a compaction is in flight (`crates/jcode-app-core/src/agent/idle_hibernation.rs:352-353`; `crates/jcode-app-core/src/server/idle_hibernation.rs:128`).

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.
