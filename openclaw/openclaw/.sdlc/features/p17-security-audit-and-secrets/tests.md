---
title: "Security, Audit, and Secrets"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Security, Audit, and Secrets

## Scope

This plan covers the test suites that prove the three trust surfaces of the feature: the local static security audit in `src/security/`, the durable content-free activity ledger in `src/audit/`, the secret indirection layer in `src/secrets/`, the channel pairing store in `src/pairing/`, and the operator command surfaces in `src/cli/`. The debug proxy suites in `src/proxy-capture/` are listed because they exercise the separate local capture tool, not the secrets egress proxy. The end-to-end suites of the OpenClaw release validation (a Gateway with a real agent and model, the channel end-to-end suites, and the Control UI end-to-end suite) are out of scope here and are owned by the release validation workflow.

## Unit Tests

| ID | Description | Source | Input | Expected Output |
|---|---|---|---|---|
| TC-1 | Credential masking strips control characters and keeps UTF-16 surrogate pairs intact at the mask boundary | `src/security/secret-mask.test.ts` | A credential value with control characters and a surrogate pair | A masked value shows the head and tail, never a broken surrogate pair |
| TC-2 | Permission fix collects targets for the credentials directory, the agent auth and session stores, and the config include files, and tightens the live legacy main auth store | `src/security/fix.test.ts` | A state directory and a config path | The expected permission targets are collected and the legacy auth store mode is tightened |
| TC-3 | Config include files that are group or world readable raise a finding | `src/security/audit-config-include-perms.test.ts` | An include file with wide permissions | Findings with the `fs.config_include` check ids are emitted |
| TC-4 | Windows ACL-derived filesystem findings are produced from ACL state rather than POSIX mode bits | `src/security/audit-filesystem-windows.test.ts` | A Windows ACL state | The Windows specific filesystem findings are evaluated |
| TC-5 | SecretRef id validation accepts and rejects file and exec ids | `src/secrets/ref-contract.test.ts` | Valid ids, invalid ids, and traversal segments | Valid ids are accepted, invalid ids are rejected |
| TC-6 | The resolver enforces the per-provider reference limit and rejects invalid refs before provider resolution | `src/secrets/resolve.test.ts` | Invalid env, file, exec, and provider refs | Each invalid ref is rejected before any provider call |
| TC-7 | The secrets plan validator rejects a target path that does not match the registered shape, requires an agent id for auth-profile targets, and accepts plugin-managed exec provider upserts | `src/secrets/plan.test.ts` | A plan with a malformed target path | Each malformed plan is rejected before any config write |
| TC-8 | The capture store keeps byte-limited UTF-8 previews on a complete character boundary and stores sessions with payload deduplication | `src/proxy-capture/store.sqlite.test.ts` | A session with a large body | The preview is bounded and complete payloads are deduplicated |

## Integration Tests

| ID | Description | Source | Preconditions | Expected Outcome |
|---|---|---|---|---|
| TC-9 | The security audit reports attack-surface and summary findings | `src/security/audit-summary.test.ts` | A config with an agent opted into sandboxed GitHub identity execution | A summary with critical, warn, and info counts and the matching info findings |
| TC-10 | The security audit reports Gateway exposure findings, including the MCP Apps bridge, insecure or dangerous flags, the host-header origin fallback, and trusted-proxy guardrails | `src/security/audit-gateway-exposure.test.ts` | A config with the corresponding exposure settings | Each exposure finding is emitted with a stable check id |
| TC-11 | The security audit reports trust-model exposure findings | `src/security/audit-trust-model.test.ts` | A config that exposes the Gateway on a non-loopback bind | The trust-model findings are evaluated and emitted |
| TC-12 | The security audit reports install metadata findings, keeps install metadata precedence, reads hooks after plugin versions, reports phantom allowlist findings, and ignores install backup and debris directories | `src/security/audit-plugins-trust.test.ts` | An installed plugin root with metadata and backup directories | The findings are emitted and the backup directories are excluded from the audited roots |
| TC-13 | The security audit reports channel DM policy findings without losing sibling findings, keeps producer-owned severity through the summary, and warns when custom finite routing omits an unknown-principal policy | `src/security/audit-channel-dm-policy.test.ts` | A config with DM routes for several channels | The DM policy findings appear alongside the other findings in the summary |
| TC-14 | The security audit selects Gateway auth across local and remote modes and warns when the probe auth SecretRef is unavailable | `src/security/audit-gateway-auth-selection.test.ts` | A config with several auth modes | The selected mode is the expected one and the warning finding is emitted |
| TC-15 | Ledger persistence keeps stable ordering, filters, and cursor pagination across a reopen | `src/audit/audit-events.test.ts` | A ledger with more than one page of records | A reopened ledger returns the same order, honours the filters, and pages by cursor |
| TC-16 | Ledger retention prunes records outside the fixed retention window and prunes overflow in one statement while keeping the retained sequence window | `src/audit/audit-events.test.ts` | A ledger with expired and overflow rows | The expired and overflow rows are removed and the retained window is preserved |
| TC-17 | The ledger rehydrates its sequence after an enclosing transaction rolls back | `src/audit/audit-events.test.ts` | A write inside a transaction that is rolled back | The next write does not collide with a reused sequence number |
| TC-18 | The audit writer keeps schema and insert failures, and malformed, serialization, and key failures, off the admission path | `src/audit/audit-event-writer.test.ts` | A store that rejects writes | The audited operation still completes and the failure is observable |
| TC-19 | The audit writer rejects one uncloneable event without disabling later audit records, and persists owned unknown state without inheriting evidence | `src/audit/audit-event-writer.test.ts` | An event that cannot be cloned | The bad event is dropped and later records are still written |
| TC-20 | The shared audit worker drops a repeatedly crashing batch, persists work queued after the first failure, and keeps earlier family commits when a prune transaction fails | `src/audit/audit-event-writer.worker.test.ts` | A worker whose batch crashes repeatedly | The failing batch is dropped, later work is persisted, and earlier commits survive |
| TC-21 | Message audit persistence stores domain-separated pseudonyms without raw transport identities, fails closed on corrupt identity key material, and forgets a transaction-local key after a rolled-back insert | `src/audit/audit-event-store.message.test.ts` | A message record and a damaged key row | Pseudonyms are stable, the corrupt key raises an error, and the rolled-back key is not reused |
| TC-22 | The message audit recorder keeps message events off by default, records only known direct conversations in direct mode, and records group metadata only in all mode | `src/audit/audit-recorder.test.ts` | Each recorder policy | Only the records the policy allows are written |
| TC-23 | The trusted message audit event bus isolates a throwing listener and continues notifying later listeners, and forwards producer metadata without durable identity work | `src/audit/message-audit-events.test.ts` | A listener that throws | The later listeners still receive the event |
| TC-24 | The execution identity context replays a byte-identical canonical context idempotently across a restart, keeps distinct turns sharing a run correlation inspectable, and confirms durable retries without manufacturing lost evidence | `src/audit/execution-identity-context.test.ts` | A persisted context | A replay produces no duplicate, and the retained evidence matches what was written |
| TC-25 | The execution identity context records attribution only when an invoker fact is present, keeps maintenance read-only until the first capture, and enforces the row cap across independent database connections | `src/audit/execution-identity-context.test.ts` | A config with execution identity collection disabled and then enabled | The coverage state reflects the evidence present and the row cap holds |
| TC-26 | The execution identity child lineage projects copied spawn facts without retaining raw owner refs, and deduplicates sorted missing invoker evidence | `src/audit/execution-identity-context.spawn-lineage.test.ts` | A run spawned from another run | The child context holds only the derived facts |
| TC-27 | The execution identity admission envelope is deterministic, deeply frozen, and redacted, and rejects inherited, malformed, ambiguous, oversized, noncanonical, and lossy clone data | `src/audit/execution-identity-admission.test.ts` | A set of malformed admission envelopes | Each malformed envelope is rejected before allocation and enqueue |
| TC-28 | Generic decision facts persist repeated same-reason broadcast denials with distinct opaque ids, project exact-bound cron owner rows without generic facts, and do not assign run-only delivery evidence to either exact execution sharing a run id | `src/audit/execution-decision-facts.test.ts` | A run with several decisions | Each decision keeps its own receipt and no evidence is attributed to the wrong execution |
| TC-29 | Generic decision facts page equal-time facts by a bounded portable cursor, require an exact retained context for every append, and project a fact as unknown when the requested tuple does not match | `src/audit/execution-decision-facts.test.ts` | Facts written at the same timestamp | Paging is stable and a mismatched tuple yields unknown rather than a wrong fact |
| TC-30 | The inspection decision cursor rejection matrix rejects every malformed cursor shape | `src/audit/execution-decision-cursors.test.ts` | A set of malformed cursors | Each malformed cursor is rejected before the receipt query runs |
| TC-31 | Owner-native execution lifecycle receipts use admitted absence without catalog probes, read an unbound released cron receipt, and reject a reused owner cursor whose binding belongs to another execution | `src/audit/execution-owner-lifecycle-receipts.test.ts` | A cron run with a released receipt | The receipt is projected from the owner row and a mismatched cursor is rejected |
| TC-32 | The execution owner binding settles an owner row against the exact execution that owns it | `src/audit/execution-owner-binding.test.ts` | A binding for one execution | The binding settles against that execution only |
| TC-33 | The outbound message progress companion ensures idempotently, deduplicates replay, stores no raw message material, pages large offsets across bounded chunks, and bounds expired maintenance | `src/audit/message-delivery-progress-store.test.ts` | A set of progress rows for one owner | The rows are deduplicated, bounded, and free of message material |
| TC-34 | The secrets audit reports plaintext and shadowing findings, reports plaintext that duplicates the store while resolving store refs, and reports unresolved SecretRef objects in provider headers | `src/secrets/audit.test.ts` | A config with a plaintext key, a shadowed ref, and an unresolved header | The `PLAINTEXT_FOUND`, `REF_SHADOWED`, and `REF_UNRESOLVED` findings are emitted |
| TC-35 | The secrets audit does not inspect or mutate the legacy auth file, reports Doctor-created auth archives without reading their contents, and skips exec ref resolution unless it is explicitly allowed | `src/secrets/audit.test.ts` | A legacy auth file and an auth archive present | Neither file is read, and exec resolution is skipped by default |
| TC-36 | The secrets audit batches ref resolution per provider when exec resolution is allowed and short-circuits the per-ref fallback for a provider-wide batch failure | `src/secrets/audit.test.ts` | A provider whose exec resolution fails | The failure is reported once for the provider rather than once per reference |
| TC-37 | The secrets store round-trips env and secret values without disclosing them in listings or exec projection, keeps hidden GitHub records out of listings, and purges transient records on their own deadlines | `src/secrets/store/secret-store.test.ts` | A store with env, secret, and transient entries | Values never appear in a listing, hidden records stay hidden, and transient records are purged |
| TC-38 | The secret store redaction refuses a padded display marker without overwriting the credential, quarantines a corrupted row from exec and egress, and reports a resolvable redaction marker as an audit error | `src/secrets/store/secret-store.redaction.test.ts` | A store row whose redaction marker is damaged | The credential is preserved, the corrupted row is quarantined, and the error names the exact reference |
| TC-39 | The secrets apply preflights and applies a one-way scrub without plaintext backups, rolls back committed auth rows when runtime publication fails, and atomically deletes a newly created auth store when a later auth write fails | `src/secrets/apply.test.ts` | A plan with config and auth-profile targets | The scrub leaves no plaintext backup, and a failed publication rolls the auth rows back |
| TC-40 | The secrets apply rejects write mode for exec plans unless exec resolution is explicitly allowed, and preserves an auth-profile token reference during a provider scrub | `src/secrets/apply.test.ts` | A plan that includes an exec provider | The write is refused with an explanation, and the token reference survives the scrub |
| TC-41 | The interactive secrets configure warns when the shared auth-profile store carries plaintext credentials, does not warn when the store carries only SecretRef values, and does not warn when the store is missing | `src/secrets/configure.test.ts` | A shared auth-profile store in each of the three states | The warning appears only in the plaintext case |
| TC-42 | The secret egress proxy substitutes multiple sentinels in a Basic credential without decoding other base64, and does not follow redirects and reauthorizes credentials on a redirected destination | `src/secrets/egress-proxy/proxy-server.test.ts` | A request with a sentinel-bearing Authorization header | Only the sentinel is replaced, and a redirect does not carry the credential to a new host |
| TC-43 | The secret egress proxy rejects conflicting content-length and chunked request framing and preserves fixed-length binary upload bytes | `src/secrets/egress-proxy/proxy-server.test.ts` | A request with conflicting framing and a binary body upload | The conflicting request is rejected and the binary body is forwarded unchanged |
| TC-44 | The debug proxy caps UTF-8 previews on character boundaries while forwarding full bodies, pauses the upstream response while downstream forwarding is backpressured, and returns 504 when a CONNECT opening attempt times out | `src/proxy-capture/proxy-server.test.ts` | A debug proxy session | The preview is bounded, the backpressure is honoured, and the connect timeout returns 504 |
| TC-45 | The capture store keeps a cached store open until the last lease releases, rebinds after the state database closes underneath it, fences a store opened before external ownership was claimed, and uses rollback journaling for captures on NFS-backed volumes | `src/proxy-capture/store.sqlite.test.ts` | A shared capture store under lease changes | The store closes only when the last lease is released and stays fenced once ownership moves |
| TC-46 | The capture runtime isolates same-session databases through independent finalization, preserves fresh ambient lazy sessions, and releases retired settings, store, and runtime closures | `src/proxy-capture/runtime.lifecycle.test.ts` | A retired capture admission generation | Retired resources are released and same-session databases stay isolated |
| TC-47 | The pairing store skips malformed persisted requests while approving valid codes, handles pending request reuse, expiry, and per-account limits, and approves and dismisses account-scoped requests by opaque id | `src/pairing/pairing-store.test.ts` | A store with a malformed row and a full pending set | The malformed row is skipped, the oldest pending request is pruned, and approval by opaque id works |
| TC-48 | The pairing store regenerates colliding codes and reports exhaustion without leaking codes, and keeps the allow list and pending requests isolated by account | `src/pairing/pairing-store.test.ts` | A code generator that collides | A new code is generated, exhaustion is reported, and no code leaks into the error |
| TC-49 | The pairing allowlist lifecycle retains a typed worker refusal through cleanup, refuses replacement of the captured store before queued dispatch, and propagates a lost worker result without replay | `src/pairing/pairing-allowlist.lifecycle.test.ts` | A worker that refuses or loses a result | The refusal and the loss are surfaced rather than replayed |
| TC-50 | The device pairing setup code round-trips while canonicalizing the TLS fingerprint, rejects an invalid fingerprint, rejects garbage and expired payload shapes, and accepts older payloads without a fingerprint or expiry | `src/pairing/setup-code.test.ts` | A set of setup code payloads | Valid payloads round-trip and invalid ones are rejected |
| TC-51 | The security CLI runs the audit with read-only SecretRef resolution and prints JSON diagnostics, and reports an unexpected fixer failure instead of emitting a successful JSON audit | `src/cli/security-cli.test.ts` | A CLI invocation with and without the fix flag | The JSON report is printed, and a fixer failure is surfaced rather than masked |
| TC-52 | The secrets CLI calls secrets.reload and prints human and JSON output, explains a Gateway reload failure without duplicate doctor noise, and writes one audit report before exiting with the check code | `src/cli/secrets-cli.test.ts` | A CLI invocation against a mock Gateway | The output and the exit code match the contract |
| TC-53 | The secrets CLI forwards the exec opt-in to the secrets audit, shows the irreversibility warning before applying configured targets, cancels the apply when the warning is declined, and writes generated plan files at the apply limit | `src/cli/secrets-cli.test.ts` | A CLI invocation with and without the opt-in | The flags reach the command, the warning gates the apply, and the plan file is written |
| TC-54 | The proxy CLI registers the debug proxy subcommands and normalizes signed decimal numeric options through the shared parser | `src/cli/proxy-cli.test.ts` | A CLI invocation | The subcommands are registered and the numeric options are normalized |

## End-to-End Tests

| ID | Description | Source | Steps | Expected Outcome |
|---|---|---|---|---|
| TC-55 | The operator runs the full audit and read path against a live Gateway | `src/cli/security-cli.test.ts`, `src/audit/audit-events.test.ts` | Start a Gateway with a real agent, run `openclaw security audit --deep --json`, then run `openclaw audit --agent AGENT_ID --explain --json` | The deep probe succeeds, the report is emitted as JSON, and the audit command returns the run identity and decision receipts for the real run |
| TC-56 | The operator stores a credential and routes a call through the secrets egress proxy | `src/secrets/egress-proxy/proxy-server.test.ts`, `src/secrets/store/secret-store.test.ts` | Create a store entry bound to a host, configure the egress proxy allowlist, then make a call to that host | The secret is injected at request time and the value never appears in the proxy log or the client request |
| TC-57 | A DM sender requests pairing and the operator approves it | `src/pairing/pairing-store.test.ts`, `src/cli/pairing-cli.test.ts` | Have a sender message a pairing-policy channel, then run `openclaw pairing list` and `openclaw pairing approve PAIRING_CODE` | The pending request appears with an opaque request id, approval adds the sender to the allow list, and the sender can then message the agent directly |

## Edge Cases and Failure Scenarios

| ID | Scenario | Source | Expected Behavior |
|---|---|---|---|
| TC-58 | The audit identity key row is corrupt or has the wrong key length | `src/audit/audit-event-store.message.test.ts` | The pseudonym derivation fails with a corrupt identity key error, and no unkeyed digest is substituted |
| TC-59 | A retained message reference loses its identity key | `src/audit/audit-event-store.message.test.ts` | The read fails closed rather than returning a record with a broken reference |
| TC-60 | The store schema predates the lazily created hidden GitHub table | `src/secrets/store/secret-store.test.ts` | The missing table is treated as empty and the schema version is preserved |
| TC-61 | The store redaction marker is corrupted in an existing row | `src/secrets/store/secret-store.redaction.test.ts` | The row is quarantined from exec and egress, healthy siblings stay visible, and the error names the exact reference and the repair command |
| TC-62 | An exec provider fails for every reference of that provider | `src/secrets/audit.test.ts` | The failure is reported once for the provider rather than once per reference |
| TC-63 | A pending pairing request is older than the 1 hour TTL | `src/pairing/pairing-store.test.ts` | The request is treated as expired and pruned rather than approvable |
| TC-64 | A channel account already holds 3 pending pairing requests | `src/pairing/pairing-store.test.ts` | The oldest pending request is pruned so the cap holds |
| TC-65 | The pairing code generator cannot find a free code | `src/pairing/pairing-store.test.ts` | The exhaustion is reported with the existing code count and no code is leaked |
| TC-66 | A permission fix target is a symbolic link, or is not the expected file or directory type | `src/security/fix.test.ts` | The action is skipped with a reason and the target is not modified |
| TC-67 | The ledger is queried with a filter combination that is not supported | `src/audit/audit-events.test.ts` | The request is rejected with the conflicting field named, and no partial result is returned |
| TC-68 | The legacy `audit.list` projection is asked for a message record | `src/audit/audit-events.test.ts` | The call fails rather than silently dropping the message record |

## Test Infrastructure

- The audit, secret store, pairing, and capture suites run against temporary SQLite state databases created by the shared OpenClaw state database helpers, so each suite owns an isolated database and an isolated state directory.
- The security audit suites build synthetic config objects and temporary config, state, and credentials directories rather than reading a real installation.
- The CLI suites stub the Gateway transport and assert on the emitted output and the exit code, so no Gateway process is required.
- The egress proxy suites run a real local HTTP server so that header substitution, redirect handling, and framing conflicts are proven against a real socket.
- The capture suites use loopback servers and a temporary capture store, with filesystem lease behaviour asserted through the store's own reference counting.
- The pairing suites use the SQLite-backed pairing store worker so that the pending limits, the code collision path, and the account isolation are proven against the real persistence layer.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-9, TC-10, TC-11, TC-12, TC-13, TC-14, TC-51 |
| FR-2 | TC-14, TC-55 |
| FR-3 | TC-2, TC-66 |
| FR-4 | TC-15, TC-16, TC-21, TC-33, TC-67, TC-68 |
| FR-5 | TC-15, TC-19, TC-21, TC-22, TC-23 |
| FR-6 | TC-21, TC-58, TC-59 |
| FR-7 | TC-24, TC-25, TC-26, TC-27, TC-28, TC-29, TC-30, TC-31, TC-32, TC-55 |
| FR-8 | TC-16, TC-17, TC-33 |
| FR-9 | TC-15, TC-51, TC-55, TC-67 |
| FR-10 | TC-5, TC-6, TC-34 |
| FR-11 | TC-37, TC-38, TC-52, TC-60, TC-61 |
| FR-12 | TC-42, TC-43, TC-56 |
| FR-13 | TC-34, TC-35, TC-36, TC-52, TC-62 |
| FR-14 | TC-7, TC-39, TC-40, TC-41, TC-53 |
| FR-15 | TC-47, TC-48, TC-49, TC-50, TC-57, TC-63, TC-64, TC-65 |
| NFR-1 | TC-15, TC-21, TC-33, TC-58, TC-59 |
| NFR-2 | TC-1, TC-37, TC-38, TC-53 |
| NFR-3 | TC-15, TC-29, TC-30, TC-67 |
| NFR-4 | TC-2, TC-4, TC-66 |
| NFR-5 | TC-18, TC-19, TC-20, TC-67 |
| NFR-6 | TC-9, TC-10, TC-11, TC-12, TC-13, TC-14 |
