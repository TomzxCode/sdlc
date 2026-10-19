---
title: "Hosted Account and Plans"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Hosted Account and Plans

## Scope

Covers the hosted account and plan surface: the device-authorization and email-code sign-in, the account API client, the account credential store, the curated hosted model catalog and its route, the spending balance and daily allowances, the plan-limit notice, the TUI account commands and the hosted account status surface, and the CLI `jcode account` subcommands.

Out of scope: the account service itself, the Jcode router that enforces the spending limit server-side, the Stripe billing portal and checkout flows beyond the client-side URL checks, the Jcode Cloud control plane, and the Desktop rendering of the account surfaces.

Every test listed below exists in the repository today.
The table names the file and the test function for each case, so a reader can run one directly.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Curated model alias resolution in `crates/jcode-base/src/subscription_catalog.rs` (`curated_model_aliases_resolve_to_canonical_ids`) | `"opus 5.5"`, `"Claude Opus 5.5"`, `"sonnet 5.5"`, `"haiku 5.5"`, `"sol"`, `"GPT 6.1 Sol"`, `"unknown-model"` | Each known alias resolves to its canonical id, and an unknown model resolves to nothing |
| TC-2 | Retired and unsupported model rejection in `crates/jcode-base/src/subscription_catalog.rs` (`retired_models_and_unsupported_generations_are_not_curated`) | A list of 30 retired Claude, GPT and open-weight model ids, each also with an `@provider` suffix | None of them is curated and none is allowed for the current tier |
| TC-3 | Provider pin suffix handling in `crates/jcode-base/src/subscription_catalog.rs` (`curated_model_lookup_ignores_provider_pin_suffix`) | `"claude-opus-5-5@anthropic"`, `"gpt-6.1-sol@openai"` | Both resolve to their canonical curated ids |
| TC-4 | Default hosted model selection in `crates/jcode-base/src/subscription_catalog.rs` (`default_model_is_newest_curated_flagship`) | The curated catalog | The default model is the ranked Claude flagship, `claude-opus-5-5` |
| TC-5 | Exact hosted catalog shape in `crates/jcode-base/src/subscription_catalog.rs` (`curated_catalog_has_exact_hosted_set_without_legacy_model_gates`) | The curated catalog | Exactly four models are gated at `Plus`, none at `Ultra`, none at `Flagship`, and unknown models such as `magistral-small-1.2` are absent |
| TC-6 | Tier pricing table in `crates/jcode-base/src/subscription_catalog.rs` (`tier_pricing_matches_launched_plans`) | The five tiers | Each tier keeps its wire id, display name, retail price, usable budget, included inference and overage multiplier; `Flagship` displays as `Solo` |
| TC-7 | Tier parsing in `crates/jcode-base/src/subscription_catalog.rs` (`tier_parse_round_trips`) | Every tier id in mixed case and with surrounding spaces, plus `"solo"` and `"starter"` | Every tier id round-trips, `solo` maps to `Flagship`, and an unknown tier parses to nothing |
| TC-8 | Tier ordering in `crates/jcode-base/src/subscription_catalog.rs` (`tier_gating_follows_catalog_order`) | Every pair of tiers | A tier allows exactly the tiers at or below it in the ladder |
| TC-9 | Base-plan availability in `crates/jcode-base/src/subscription_catalog.rs` (`every_hosted_model_is_available_from_the_base_subscription`) | Every curated model and every tier | Every curated model is gated at `Plus` and is allowed from every tier |
| TC-10 | Cached tier independence in `crates/jcode-base/src/subscription_catalog.rs` (`hosted_catalog_access_does_not_depend_on_legacy_cached_tier`) | No cached tier, an unreadable cached tier, `Pro`, `Max`, `Ultra`, then a persisted `Flagship` | The available hosted models never change, and the cached tier is cleared and restored cleanly |
| TC-11 | Runtime mode flag in `crates/jcode-base/src/subscription_catalog.rs` (`runtime_mode_flag_tracks_subscription_activation`) | Runtime env cleared, then applied, then cleared | The hosted runtime mode is inactive, then active, then inactive again |
| TC-12 | Upgrade card validity in `crates/jcode-base/src/subscription_notice.rs` (`upgrade_card_is_a_valid_applet_with_upgrade_button`) | A browser-allowance notice on the Plus plan with a Pro upgrade target | The card validates against the agent manifest, names the feature and the plan, carries an `Upgrade to Pro` button that opens the pricing URL, and is mounted inline at the end of the session |
| TC-13 | Top-tier card in `crates/jcode-base/src/subscription_notice.rs` (`top_tier_card_has_no_upgrade_button`) | The same notice without an upgrade target | The card still validates, carries no open-url button, and offers a dismiss button instead |
| TC-14 | Notice wording in `crates/jcode-base/src/subscription_notice.rs` (`upgrade_prompt_names_plan_feature_and_link`) | A notice with an upgrade target | The rendered text names the browser automation feature, the Plus plan, the Pro upgrade, the pricing link and the 24 hour reset |
| TC-15 | Top-tier wording in `crates/jcode-base/src/subscription_notice.rs` (`top_tier_gets_reset_message_without_upsell`) | A notice without an upgrade target | The text mentions the reset and contains no upgrade upsell |
| TC-16 | Notice lifetime in `crates/jcode-base/src/subscription_notice.rs` (`notice_is_recoverable_from_anyhow_chain_and_taken_once`) | A notice wrapped in an `anyhow` error chain, then recorded | The notice is found in the chain, is taken once, and is gone on the second take |
| TC-17 | Hosted provider runtime mode in `crates/jcode-base/src/provider/jcode.rs` (`jcode_provider_enables_subscription_runtime_mode`) | A new `JcodeProvider` | The hosted runtime mode becomes active and every offered model is a curated model |
| TC-18 | Hosted provider identity in `crates/jcode-base/src/provider/jcode.rs` (`jcode_provider_name_and_default_model_are_curated`) | A new `JcodeProvider` | The provider is named `Jcode Subscription` and its default model is curated |
| TC-19 | Managed transport pinning in `crates/jcode-base/src/provider/jcode.rs` (`jcode_models_are_pinned_to_the_managed_transport`) | `claude-opus-5-5`, `claude-haiku-5-5`, `gpt-6.1-sol` | Each becomes `openrouter:<model>`, so the id never reaches a direct provider credential |
| TC-20 | Hosted route table in `crates/jcode-base/src/provider/jcode.rs` (`jcode_provider_exposes_only_explicit_subscription_routes`) | Routes for the `Plus` and `Flagship` tiers | Exactly four routes are exposed, all with provider `Jcode Subscription`, api method `jcode-subscription` and `available` set, and the two tiers produce identical routes |
| TC-21 | Curated model guard in `crates/jcode-base/src/provider/tests/catalog_subscription.rs` (`test_subscription_model_guard_allows_only_curated_models_when_enabled`) | The curated ids and aliases, then 30 retired ids, with the runtime mode active | Every curated id and alias is allowed and every retired id is refused |
| TC-22 | Tier-independent hosted guard in `crates/jcode-base/src/provider/tests/catalog_subscription.rs` (`test_hosted_model_guard_does_not_gate_models_by_legacy_tier`) | A stale cached tier of `ultra` with the runtime mode active | The curated models stay available, so a stale tier cannot change client-side availability |
| TC-23 | Display model filtering in `crates/jcode-base/src/provider/tests/catalog_subscription.rs` (`test_filtered_display_models_respects_curated_subscription_catalog`) | A list mixing curated and unknown model ids | The display list holds only the curated models, before and after a stale tier is set |
| TC-24 | Remote route fallback in `crates/jcode-base/src/provider/tests/catalog_subscription.rs` (`test_remote_jcode_subscription_fallback_keeps_managed_route_identity`) | A remote route fallback built for the hosted provider | The four curated models are returned, each with the hosted provider display name, the `jcode-subscription` api method and `available` set |
| TC-25 | Saved credential does not activate the filter in `crates/jcode-base/src/provider/tests/catalog_subscription.rs` (`test_subscription_filters_do_not_activate_from_saved_credentials_alone`) | A saved account key with the runtime mode cleared | The model filters stay inactive, so a saved credential alone does not switch routing |
| TC-26 | Inference balance rendering in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_shows_monthly_inference_spending_and_remaining`) | An account with $12.50 used of a $50.00 limit and a reset time | The report has an `Inference spending limit (monthly)` row at 25 percent with the reset time, shows $37.50 remaining and `$12.50 / $50.00` spent, and does not mark the limit reached |
| TC-27 | Limit exhaustion in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_monthly_limit_exhaustion_clamps_remaining`) | $50.00 and $60.00 spent against a $50.00 limit | The hard limit is marked reached and the remaining amount is clamped to `$0.00` |
| TC-28 | Unknown limit in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_unknown_monthly_budget_is_not_exhausted`) | A limit of 0, -1, NaN and infinity | The hard limit is never marked reached and the remaining amount row is omitted, while a daily allowance overrun still marks it reached |
| TC-29 | Daily allowances without upsell in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_shows_daily_allowances_without_upsell_when_low`) | A memory allowance at 100 of 1000 with an upgrade target available | The report is named `Jcode subscription`, lists the daily allowance at 10 percent, and carries no upgrade row while the allowance is low |
| TC-30 | Upgrade hint near the allowance limit in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_suggests_upgrade_near_and_at_the_limit`) | A memory allowance at 850 of 1000, then at 1000, then at 1000 on the top plan | The near-limit case carries an upgrade row with the pricing link and is not exhausted, the at-limit case is exhausted, and the top plan carries no upgrade row |
| TC-31 | Older gateway tolerance in `crates/jcode-base/src/usage/tests.rs` (`jcode_usage_tolerates_older_gateways_without_jev_usage`) | An account payload with no `jev_usage` | The report has no limit rows and still reports the plan name |
| TC-32 | Management URL allowlist in `src/cli/account.rs` (`manage_url_accepts_only_public_allowlisted_https_origins`) | `https://jcode.sh/account`, a foreign origin carrying a key, and a URL with embedded credentials | The allowlisted URL is kept and the other two fall back to the public account page |
| TC-33 | Credential file lifecycle in `src/cli/login/jcode_device/tests.rs` (`approved_key_persistence_is_owner_only_and_clear_is_deterministic`) | An approved key persisted into an isolated `JCODE_HOME`, then cleared | The file holds the key with mode `0600`, and after clearing it holds neither the key, the account id nor the email |
| TC-34 | Revoked key messaging in `crates/jcode-tui/src/tui/app/auth_subscription_status_tests.rs` (`revoked_account_reports_successful_cleanup`) | A successful local cleanup | The message says the credentials were cleared and points at `/account jcode login` |
| TC-35 | Failed cleanup messaging in `crates/jcode-tui/src/tui/app/auth_subscription_status_tests.rs` (`revoked_account_does_not_claim_failed_cleanup_succeeded`) | A cleanup that fails with a permission error | The message reports the error, points at `/account jcode logout`, and does not claim the credentials were cleared |
| TC-36 | Hosted account command parsing in `crates/jcode-tui/src/tui/app/auth_account_commands.rs` (`parse_native_jcode_account_actions`) | `/account jcode login`, `/account jcode status`, `/account jcode manage`, `/account jcode logout` | Each parses to the matching hosted account action |
| TC-37 | Nudge weekly gate in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`weekly_gate_blocks_within_a_week_and_allows_after`) | A never-shown state, a state shown a week ago, one shown just under a week ago, and a clock that went backwards | The gate allows the first two, blocks the third, and saturates rather than wrapping on the backwards clock |
| TC-38 | Long-task qualification in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`long_task_qualification_requires_all_completed_and_gated_confidence`) | An empty list, an in-progress item, a low completion confidence, a missing confidence, and a fully completed list | Only the fully completed list with a passing confidence qualifies |
| TC-39 | Long-task message wording in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`long_task_message_reads_support_wording_with_elapsed`) | 83 minutes and 1 hour | The message reads `jcode just worked 1h 23m for you. Try Jcode hosted models: /hosted` and the shorter durations format as `59m` and `1h` |
| TC-40 | Rate-limit nudge copy in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`rate_limit_copy_leads_with_the_hosted_model_value_prop`) | The shared nudge line | The line leads with the hosted-model value proposition and names `/hosted` |
| TC-41 | Hosted pitch content in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`pitch_explains_limits_warnings_tranches_and_next_step`) | The rendered pitch | The pitch states that there is no subscription, names the monthly spending limit, the warnings, the $20 start, the progressively larger tranches, the month-end collection, that the software stays open source, and points at `/login jcode` and `/usage`, and lists every curated model |
| TC-42 | Elapsed formatting in `crates/jcode-tui/src/tui/app/subscribe_nudge.rs` (`elapsed_formatting_covers_minute_and_hour_shapes`) | 61 minutes, 2 hours, 45 minutes | They format as `1h 1m`, `2h` and `45m` |
| TC-43 | TUI logout credential clearing in `crates/jcode-tui/src/tui/app/auth_tests.rs` (`tui_jcode_subscription_logout_clears_credentials_and_preserves_api_base`) | A saved key, account id, email and API base | The key, account id and email are cleared, the API base is retained, and no credential is left in the environment or in the env file |
| TC-44 | Browser URL validation in `crates/jcode-base/src/account_login/tests.rs` (`rejects_unsafe_browser_urls`) | Eleven URLs: plain http, a foreign host, a userinfo host, embedded credentials, an explicit port, a non-account path, an extra query parameter, a fragment, a percent-encoded newline, a one-character flow value and a missing flow value | Every one of them is refused as an invalid response |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-45 | Device request contract in `crates/jcode-base/src/subscription_api.rs` (`device_request_uses_new_contract_and_parses_public_urls`) | A scripted server that answers the device request | The device code, flow id, verification URI and interval are parsed, and the verification URL does not contain the device secret |
| TC-46 | No tier selection on the device request in `crates/jcode-base/src/subscription_api.rs` (`metered_device_request_does_not_select_a_subscription_tier`) | A server that captures the request body | The body is exactly `{"client_name":"jcode-cli"}` and carries no `requested_tier` |
| TC-47 | Legacy backend detection in `crates/jcode-base/src/subscription_api.rs` (`legacy_device_response_is_explained_without_echoing_body`) | A server that answers with the old `verify_url` shape | The client reports the legacy login contract and does not echo the device code from the body |
| TC-48 | Token poll outcomes in `crates/jcode-base/src/subscription_api.rs` (`token_poll_handles_pending_slow_down_success_denied_and_replay`) | A server that answers with 428, 429 with `Retry-After: 9`, an approval, a denial and an expiry | Each status maps to its own outcome: pending, slow down with the header delay, approved, denied and expired |
| TC-49 | Revoked key classification in `crates/jcode-base/src/subscription_api.rs` (`me_and_revoke_classify_revoked_keys_without_leaking_them`) | A server that answers 401 with a body naming the key | Both the account read and the revocation report an unauthorized key, and neither message contains the key |
| TC-50 | Billing and portal handling in `crates/jcode-base/src/subscription_api.rs` (`billing_cap_and_portal_parse_and_reject_unsafe_urls`) | A server that answers the billing read, the hard-cap write, an https portal URL, a non-https portal URL and a 409 | The cap converts to dollars, the period spend and the promotional credit convert correctly, the cap write returns the new value, the https portal URL is accepted, and the non-https URL and the 409 are refused with their code |
| TC-51 | Checkout and plan change in `crates/jcode-base/src/subscription_api.rs` (`checkout_and_plan_change_only_accept_safe_replies`) | A server that answers with a Stripe Checkout URL, a non-Stripe URL, a plan change and a 409 | The Stripe URL is accepted, the non-Stripe URL is refused as an invalid response, the plan change returns the plan, the limit and the effective moment, and the 409 is surfaced with its code |
| TC-52 | Account payload shape in `crates/jcode-base/src/subscription_api.rs` (`subscription_me_parses_expected_shape`) | A `/v1/me` payload with a tier, a status, a usage block and a management URL | The tier parses, the capabilities default to false, the account counts as an active paid plan, and the management URL is read |
| TC-53 | Metered payload shape in `crates/jcode-base/src/subscription_api.rs` (`metered_account_parses_spending_limit_and_tranche_state_without_a_tier`) | A payload with `tier: "none"`, `spend_limit_usd`, `billed_usd` and `next_charge_at_usd` | The limit is read through the `spend_limit_usd` alias, the billed and next-charge amounts are read, no tier is parsed, and the account still counts as an active paid plan |
| TC-54 | Polling backoff in `crates/jcode-base/src/subscription_api.rs` (`polling_backoff_is_deterministic_and_bounded`) | A backoff with a 3 second base | The delay goes from 3 to 8 to 12 seconds, then to 24 and 30 seconds on offline errors, and back to 3 seconds after a pending answer |
| TC-55 | Device flow wire contract in `crates/jcode-base/src/account_login/tests.rs` (`account_only_start_and_approval_use_expected_wire_contract`) | A scripted server that answers the device request and the token exchange | The flow exposes the public approval URL, the interval and the expiry, the device request body is exactly `{"client_name":"jcode-cli"}`, the token body carries the device code, the device secret and the account key never appear in the debug rendering, and exactly two requests are made with no account read, provider selection or checkout |
| TC-56 | Poll result separation in `crates/jcode-base/src/account_login/tests.rs` (`pending_slowdown_denial_and_expiry_are_separate_results`) | A scripted server that answers pending, a `Retry-After: 12` slow down, a slow down with no header, a denial and an expiry | Each answer maps to its own result, the slow down uses the header delay and otherwise falls back to the interval plus 5 seconds, and a locally expired flow makes no HTTP request |
| TC-57 | Redaction of hostile bodies in `crates/jcode-base/src/account_login/tests.rs` (`malicious_error_bodies_and_malformed_responses_are_redacted`) | A server that answers with a 500 whose body embeds the secret, a bare secret body, and a device response pointing at a foreign host | Every error rendering is free of the secret, and an offline error carrying a secret-bearing URL is redacted and reported as temporary |
| TC-58 | Save and account read in an isolated home in `crates/jcode-base/src/account_login/tests.rs` (`explicit_save_and_current_account_are_sandboxed_without_paid_plan`) | An isolated `JCODE_HOME`, a cleared environment, and a scripted account API | No credential exists before the approval, the credential exists after the save, the hosted runtime mode stays off, the credential survives the removal of the process variables, the file sits under the isolated home with mode `0600`, the account read returns the account and reports no active paid plan, and an unauthorized answer leaves the credential in place |
| TC-59 | Cancellation of an in-flight poll in `crates/jcode-base/src/account_login/tests.rs` (`in_flight_poll_is_cancellable_without_a_detached_worker`) | A server that accepts the token request and never answers | The poll task is aborted without waiting for the request timeout, and no detached worker is left behind |
| TC-60 | Live deployed device flow in `crates/jcode-base/src/account_login/tests.rs` (`deployed_account_start_and_pending_are_compatible`) | The `JCODE_ACCOUNT_TEST_API_BASE` environment variable, `#[ignore]`d by default | The live flow starts with an https approval URL and the first poll is pending |
| TC-61 | Email code sign-in contract in `crates/jcode-base/src/account_login/tests.rs` (`email_code_sign_in_uses_expected_wire_contract`) | A scripted server that answers the code request, a wrong code, an approval and an expiry | The address is normalized, the code length is read, the login token never appears in the debug rendering, the request bodies carry the client name, the email, the code and the token, a wrong code reports the remaining attempts, a code with separators is accepted, and a used code reports an expiry |
| TC-62 | Gmail search link in `crates/jcode-base/src/account_login/tests.rs` (`gmail_link_searches_for_our_sender_including_spam`) | An address with surrounding spaces and mixed case | The link targets the normalized address, the `login@solosystems.dev` sender, `in:anywhere` and a one-day window |
| TC-63 | Device poll approval in `src/cli/login/jcode_device/tests.rs` (`polling_pending_slow_down_then_approval`) | A scripted server that answers pending, a slow down with `Retry-After: 1`, then an approval | The poll returns the approved account id, email and tier |
| TC-64 | Denial redaction in `src/cli/login/jcode_device/tests.rs` (`polling_denied_has_clear_redacted_error`) | A scripted server that answers a denial whose body carries the device secret | The error says the login was canceled or denied and does not contain the device secret |
| TC-65 | Deterministic timeout in `src/cli/login/jcode_device/tests.rs` (`polling_timeout_is_deterministic_before_first_request`) | An unreachable endpoint with a 1 second expiry and a 2 second interval | The poll fails with a timeout message before making a request |
| TC-66 | Cancellation during a consumed exchange in `src/cli/login/jcode_device/tests.rs` (`cancellation_during_consumed_exchange_finishes_and_returns_the_key`) | A server that answers the token request after 300 ms while the cancel fires after 1100 ms | The exchange still finishes and the approved key is returned, so the single-use device code is not stranded |
| TC-67 | Plan quota upgrade prompt in `crates/jcode-base/src/jev/transport_tests.rs` (`gateway_plan_quota_is_not_retried_and_becomes_upgrade_prompt`) | A mock gateway that answers 429 with a plan quota and an upgrade target | The error carries a typed notice naming the feature, the current tier and the upgrade tier with the pricing link, and the gateway is called once for the preflight and once for the decision, so plan quotas are never retried |
| TC-68 | Upgrade link origin check in `crates/jcode-base/src/jev/transport_tests.rs` (`gateway_quota_rejects_non_jcode_upgrade_links`) | A mock gateway whose quota carries an upgrade URL on a foreign host | The notice drops the upgrade link and the error text does not contain the foreign host |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-69 | The hosted account status surface in `crates/jcode-tui/src/tui/app/tests/commands_accounts_01/part_02.rs` (`test_subscription_command_shows_jcode_status_scaffold`) | With the runtime mode cleared and no credential or API base configured, type `/subscription` and submit | A system message is shown that names the hosted model status, states the pay-as-you-go model with no subscription fee, names the monthly spending limit and the progressively larger tranches, points at `/login jcode`, lists all four curated models, and mentions none of the retired models, the old monthly price wording or the old budget wording |
| TC-70 | The hosted model pitch in `crates/jcode-tui/src/tui/app/tests/commands_accounts_01/part_02.rs` (`test_subscribe_command_shows_hosted_pitch_and_next_step`) | Type `/subscribe` and submit | A system message is shown that names the hosted models, states there is no subscription, names the monthly spending limit, the open-source statement, the $20 start and the progressively larger tranches, and points at `/login jcode` and `/usage` |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-71 | The approval URL is over plain http, on a foreign host, with a userinfo host, with embedded credentials, with an explicit port, on a non-account path, with an extra query parameter, with a fragment, with a percent-encoded newline in the flow value, with a one-character flow value, or with no flow value at all | Every one of them is refused as an invalid response, so no browser ever opens an untrusted URL (TC-44) |
| TC-72 | The device code expires, the user denies the request, the server asks the client to slow down, or the flow expires locally | Each case maps to its own distinct result, and a locally expired flow makes no HTTP request (TC-48, TC-56) |
| TC-73 | The account API answers with a body that embeds the device secret, the account key or a secret-bearing URL | The secret never appears in the error rendering, and the error is classified as temporary when it is an offline error (TC-47, TC-49, TC-57) |
| TC-74 | The user cancels the login while the token exchange is already in flight | The exchange is allowed to finish and the approved key is returned, because the device code is single use (TC-59, TC-66) |
| TC-75 | The account API cannot be reached during the device poll | The poll retries with a bounded backoff, and the flow fails with a timeout message rather than an unhandled network error (TC-54, TC-65) |
| TC-76 | The account key was revoked or expired | The local credentials are cleared, the user is told to sign in again, and a failed local cleanup is reported as a failure rather than a success (TC-34, TC-35, TC-49) |
| TC-77 | The account API is unreachable during the logout | The local credential, account id, email and tier are still cleared, and the API base is retained (TC-33, TC-43) |
| TC-78 | The monthly limit is zero, negative, NaN or infinite | The hard limit is never marked reached and the remaining amount row is omitted, so an unknown limit never reads as an exhausted one (TC-28) |
| TC-79 | The account payload carries a management URL on a foreign origin or with embedded credentials | The client falls back to the public Jcode account page (TC-32) |
| TC-80 | The account API returns a billing portal URL that is not https, or a checkout URL that is not a Stripe Checkout URL | The reply is refused as an invalid response, so the client never opens a non-Stripe or non-https payment URL (TC-50, TC-51) |
| TC-81 | The configured account API still offers the old email-based login contract | The client reports a specific compatibility error naming the current endpoint, and does not echo the response body (TC-47) |
| TC-82 | The account API is unreachable for the whole activation window | The key stays saved and the recovery commands are printed, so a slow checkout never destroys a valid credential (not covered by a test, see gap G-3) |
| TC-83 | A stale cached tier of `ultra` or `flagship` is on the machine | The available hosted models do not change, because the router owns the model policy (TC-10, TC-22, TC-23) |
| TC-84 | The user already holds account credentials when a hosted-model nudge would fire | The nudge is suppressed, and the weekly gate blocks a second nudge inside the same week (TC-37) |

## Test Infrastructure

- Scripted HTTP servers back every network test.
  `crates/jcode-base/src/account_login/tests.rs` has a `server` helper that binds a loopback listener and answers a scripted list of statuses, headers and bodies, capturing each request for assertions.
  `crates/jcode-base/src/subscription_api.rs` has a `spawn_server` helper with the same shape.
  `src/cli/login/jcode_device/tests.rs` has a `spawn_scripted_http_server` helper.
  `crates/jcode-base/src/jev/transport_tests.rs` has a `mock_server` helper for the plan-quota cases.
- Every client in these tests is built with `reqwest::Client::builder().no_proxy()`, so a proxy in the environment cannot intercept the loopback server.
- Environment isolation uses `crate::storage::lock_test_env()`, an isolated `JCODE_HOME` pointing at a `tempfile::tempdir()`, and an `EnvGuard` that saves and restores `JCODE_API_KEY`, `JCODE_API_BASE`, `JCODE_ACCOUNT_ID`, `JCODE_ACCOUNT_EMAIL`, `JCODE_TIER` and `JCODE_SUBSCRIPTION_ACTIVE` around the test.
- Credential permission assertions run only on Unix, where the file mode is compared against `0o600`.
- The one live test against the deployed account service, `deployed_account_start_and_pending_are_compatible`, is `#[ignore]`d and only runs when `JCODE_ACCOUNT_TEST_API_BASE` is set explicitly.
- The TUI tests build the app with the shared `create_test_app()` helper from the TUI test support and drive it by setting the input and calling `submit_input()`.
- The hosted-model nudge code path is disabled in test builds on purpose, so its tests assert the copy and the gate rather than the rendered message.

## Coverage Gaps

- The CLI entry points `jcode account status`, `jcode account manage` and `jcode account logout` have no test of their own.
  Only their helpers are covered: the management URL allowlist in `src/cli/account.rs` and the credential clearing in `src/cli/login/jcode_device/tests.rs` and `crates/jcode-tui/src/tui/app/auth_tests.rs`.
  The text and JSON rendering of `jcode account status` is untested.
- `subscription_api::poll_for_paid_activation` has no test.
  Its inputs and outcomes are covered only indirectly, through `has_active_paid_plan` and the `/v1/me` fetch, and `checkout_was_canceled` is not asserted anywhere.
- The CLI device login orchestration in `src/cli/login/jcode_device.rs` is covered at the polling level, but the four activation outcomes of `login_jcode_device_flow` are not.
- The TUI background read of `/v1/me` and the `UiActivity` publication in `crates/jcode-tui/src/tui/app/auth_subscription_status.rs` is not tested, only the revoked-key message helper next to it.
- `usage::provider_fetch::fetch_jcode_usage_report` has no test of its network path, only the pure `jcode_usage_report` mapping.
- The email-code sign-in is tested in the shared library but is not reachable from any CLI or TUI command, and it has no test at that level.
- There is no test that a hosted request is refused once the spending limit is reached, because the limit is enforced server-side and the client never sees that decision.
- There is no end-to-end test that drives the browser approval or the spending-limit page, because both live outside the client.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-44, TC-45, TC-46, TC-47, TC-48, TC-55, TC-56, TC-63, TC-64, TC-65, TC-71, TC-72 |
| FR-2 | TC-52, TC-53, TC-54 (partial, see gap G-3) |
| FR-3 | TC-33, TC-43, TC-55, TC-58 |
| FR-4 | TC-33, TC-49, TC-58 (partial, see gap G-3) |
| FR-5 | TC-52, TC-53 (partial, the CLI rendering is untested, see gap G-1) |
| FR-6 | TC-49, TC-58, TC-69 (partial, see gap G-1) |
| FR-7 | TC-32, TC-79 (partial, the browser launch is untested, see gap G-1) |
| FR-8 | TC-33, TC-43, TC-58 |
| FR-9 | TC-43, TC-77 (partial, the CLI message wording is untested, see gap G-1) |
| FR-10 | TC-33, TC-43, TC-58 |
| FR-11 | TC-1, TC-2, TC-3, TC-5, TC-19, TC-20, TC-21, TC-22, TC-23, TC-24, TC-25, TC-83 |
| FR-12 | TC-36, TC-69, TC-70 |
| FR-13 | TC-11, TC-17, TC-41, TC-69 (partial, the background read is untested, see gap G-4) |
| FR-14 | TC-34, TC-35, TC-76 |
| FR-15 | TC-26, TC-27, TC-28, TC-29, TC-30, TC-31, TC-78 |
| FR-16 | TC-12, TC-13, TC-14, TC-15, TC-16, TC-67, TC-68 |
| FR-17 | TC-36, TC-69 |
| FR-18 | TC-11, TC-17, TC-25, TC-83 |
| FR-19 | TC-61, TC-62 |
| FR-20 | TC-37, TC-38, TC-39, TC-40, TC-41, TC-42, TC-84 |
| FR-21 | TC-50, TC-51, TC-80 |
| NFR-1 | TC-47, TC-49, TC-55, TC-57, TC-64, TC-73 |
| NFR-2 | TC-32, TC-44, TC-71, TC-79 |
| NFR-3 | TC-10, TC-22, TC-23, TC-83 |
| NFR-4 | TC-33, TC-43, TC-77 |
| NFR-5 | No test. The only telemetry emitted for this feature is the coarse authentication success event, and no test asserts its shape. |
| NFR-6 | TC-54, TC-56, TC-58, TC-75 |
| NFR-7 | TC-54 |
| NFR-8 | TC-59, TC-66, TC-74 |
| NFR-9 | TC-41, TC-69, TC-70 |
| NFR-10 | TC-32, TC-44, TC-79 |
| NFR-11 | TC-47, TC-81 |
