---
title: "Internal Event Hooks"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Internal Event Hooks

## Scope

This plan covers the internal event hook subsystem: descriptor discovery, the `HOOK.md` metadata contract, handler loading, enablement and eligibility policy, internal event dispatch, the bundled hook pack set, hook pack install and update, the `openclaw hooks` CLI, the `hooks.status` Gateway RPC method, the native harness relay CLI verb, and the built-in Gmail watcher.

Out of scope: the HTTP webhook ingress surface configured by `hooks.enabled`, `hooks.path`, `hooks.token`, and `hooks.mappings`; cron automations; typed plugin hooks; standing orders; and the IMAP reader plugin.

## Unit Tests

| ID | File | Description | Input | Expected Output |
|---|---|---|---|---|
| TC-1 | `src/hooks/config.test.ts` | Hook environment requirement satisfaction and the legacy config path defaults | A hook requiring an environment variable plus a config path | The hook is included once the binary is present on an unchanged `PATH`; the environment requirement is reported satisfied only with a nonblank process or per-hook value |
| TC-2 | `src/hooks/configured.test.ts` | Selection allowlist resolution from config entries and tracked installs | Named config entries, install records with hook names, and an install record with no hook names | Named entries stay closed when the master flag is on; install hook names act as an allowlist; an install without a hook list keeps discovery open-ended |
| TC-3 | `src/hooks/frontmatter.test.ts` | `metadata.openclaw` resolution | Frontmatter with events, export, hookKey, os, requires, and install specs, plus a missing metadata block | The metadata record is resolved; a missing block returns undefined; a real `session-memory` `HOOK.md` parses |
| TC-4 | `src/hooks/policy.test.ts` | Source precedence and enablement resolution | A managed, plugin, bundled, and workspace hook sharing one name | Managed wins over bundled and plugin; a workspace hook cannot override a non-workspace hook |
| TC-5 | `src/hooks/internal-hook-types.test.ts` | Known internal event key catalog | Every emitted `type:action` key, bare family keys, and a typo | Emitted keys and families are accepted; typos, bare actions, and unknown families are rejected |
| TC-6 | `src/hooks/internal-hooks.test.ts` | Dispatch error isolation and event type guards | A handler that throws, and agent and Gateway bootstrap events | The error is caught and logged, later handlers still run, and the type guards accept only well-formed bootstrap and startup events |
| TC-7 | `src/hooks/fire-and-forget.test.ts` | Bounded non-blocking dispatch | Rejected tasks, resolved tasks, and an oversized timeout | Rejections are logged as sanitized single lines, resolved tasks log nothing, and the timeout timer is capped |
| TC-8 | `src/hooks/module-loader.test.ts` | Handler export resolution | A module with an explicit export, with named exports, and with a non-callable export | The explicit export wins, the named export is the fallback, and a non-callable export resolves to undefined |
| TC-9 | `src/hooks/import-url.test.ts` | Import URL cache busting for mutable hook modules | A workspace hook edited to the same size with a restored mtime | The import URL changes so the edited handler is reloaded; a missing file falls back to `Date.now()` |
| TC-10 | `src/hooks/hooks-status.test.ts` | Hook status report construction | An eventless managed hook, an always-on hook on an incompatible OS, and hooks with requirements | An eventless winner is not loadable; OS incompatibility stays visible; missing requirements are listed per group |
| TC-11 | `src/hooks/message-hooks.test.ts` | Message family event dispatch | Action-specific and family subscribers, plus an async handler that throws | Action-specific handlers do not fire for other actions, async errors are isolated, and the mutable message buffer and session key are preserved |
| TC-12 | `src/hooks/message-hook-mappers.test.ts` | Message context projection for hook and plugin consumers | Inbound reply metadata, blank command bodies, and pending remote media | Metadata maps into the canonical payload, a blank command body falls back to the raw body, and pending remote media is withheld from every inbound hook event |
| TC-13 | `src/hooks/workspace.test.ts` | Discovery roots, path containment, and metadata size limits | A package manifest with traversal, an oversized descriptor, and a symlink escape | Traversal and symlink escapes are rejected without scanning unlisted children, oversized metadata is skipped with a warning, and other hooks keep loading |
| TC-14 | `src/hooks/loader.test.ts` | Hook generation prepare and commit | Unconfigured hooks, an unknown event key, a failing import, and a shadowed collision loser | Discovery is skipped until internal hooks are configured, unknown keys warn but load, the committed generation survives a failed import, and a shadowed hook does not activate |
| TC-15 | `src/hooks/gmail.test.ts` | Gmail runtime config resolution and argument redaction | A config with and without a hook token, a custom serve path, and the built serve arguments | A missing token fails resolution, the custom public path is preserved, and the logged serve arguments omit the token flags and values |
| TC-16 | `src/hooks/gmail.windows.test.ts` | Windows `gog` invocation | A spaced `gog` `.cmd` path and caret arguments | The command is wrapped in an outer `cmd.exe` command line and caret arguments are quoted |
| TC-17 | `src/hooks/gmail-setup-utils.test.ts` | `gcloud` and Tailscale setup helpers | An abort signal, invalid JSON output, and a successful exit | The abort signal reaches the Tailscale commands, invalid JSON diagnostics are bounded while the parser cause and exit metadata are retained |
| TC-18 | `src/hooks/gmail-watcher.test.ts` | Watcher process supervision | Cancelled startups, repeated starts, a late child close, a bind conflict, and stream errors | A stale cancel does not clear newer config, renewals coalesce, stale timeouts are cancelled, bind retries are bounded, and stream errors do not crash the process |
| TC-19 | `src/hooks/gmail-watcher-lifecycle.test.ts` | Watcher startup logging and skip behavior | A successful start, a disabled watcher, and a startup error | The signal and schedule ownership are passed through, success and failure are logged, and the skip callback runs when the watcher is skipped |
| TC-20 | `src/hooks/gmail-ops.test.ts` | Watcher service renewal and bind error handling | A single-flight renewal and split bind errors | Renewal stays single-flight and is cancelled on shutdown, and bind retries stay bounded while watch renewal continues |
| TC-21 | `src/hooks/llm-slug-generator.test.ts` | Model-generated memory filename slug | A conversation excerpt and a slow local provider | Slugs are generated without exposing tools, the agent timeout is honored, error payloads are rejected, and the prompt stays free of lone surrogates |
| TC-22 | `src/hooks/installs.test.ts` | Hook install record read and compensation | A record written by a worker and a replaced lifecycle lease | A newly recorded pack is visible after a worker read, and compensation is refused once the lease is replaced |
| TC-23 | `src/hooks/install.test.ts` | Hook pack install validation | Traversal-like pack ids, an oversized `HOOK.md`, out-of-package hook entries, and policy failures | Unsafe ids and oversized descriptors are rejected, out-of-package entries are refused, and policy evaluation fails closed |
| TC-24 | `src/hooks/install-policy-warning.test.ts` | Install policy warning acknowledgement | An acknowledged and an unacknowledged policy warning | The acknowledgement reaches both scan stages |
| TC-25 | `src/hooks/update.test.ts` | npm hook pack update | A retained lease, an integrity drift, and a caller rollback | Mutation without the lease and compensation sink is refused, integrity drift aborts by default, and rollback restores the payload and the record |
| TC-26 | `src/hooks/install.work-deadline.test.ts` | Hook install and update work deadlines | An npm hook pack install and an npm hook pack update | The pack step and the dependency install step both receive the configured work timeout |
| TC-27 | `src/hooks/plugin-hooks.test.ts` | Plugin hook discovery and policy | A plugin metadata snapshot and a Claude `hooks.json` bundle | Published plugin metadata is reused, plugin hook policy is committed from the Gateway inventory, and a Claude `hooks.json` bundle is not treated as an OpenClaw hook pack |
| TC-28 | `src/hooks/autoreset-regression.test.ts` | Session auto-reset dispatch | A closed requester and a failing hook | Delayed hook work is released and dispatch continues after the requester closes and a hook errors |
| TC-29 | `src/hooks/bundled/boot-md/handler.test.ts` | `boot-md` startup handler | Non-gateway events, non-startup actions, an event without config, and two agents sharing a workspace | The non-matching events are skipped, and agents sharing a workspace run the checklist once |
| TC-30 | `src/hooks/bundled/bootstrap-extra-files/handler.test.ts` | `bootstrap-extra-files` handler | Configured path patterns, nested memory files, and a subagent context | Extra bootstrap files are appended from the configured patterns, nested memory is appended without applying session policy, and subagent allowlist enforcement is left to the final resolver |
| TC-31 | `src/hooks/bundled/compaction-notifier/handler.test.ts` | `compaction-notifier` handler | A compaction start, a skipped compaction outcome, and a successful compaction | The start notice carries an optional message count, a skipped compaction reports a truthful skip, and a successful compaction reports an optional token delta |
| TC-32 | `src/hooks/bundled/session-memory/handler.test.ts` | `session-memory` handler | A reset command, an ineligible tail, a failing transcript load, and configured timezone and slug options | The excerpt is written with the configured message window, a transcript failure is recorded and warned, and the filename uses the configured timezone and slug behavior |
| TC-33 | `src/hooks/bundled/session-memory/handler-admission.test.ts` | `session-memory` admission rules | A detached manual-reset slug generation after the request returns | The detached slug generation stays admitted after the request returns |
| TC-34 | `src/hooks/bundled/session-memory/handler-auto-reset.test.ts` | `session-memory` automatic reset path | A `session:auto-reset` event with reason `daily` and with reason `idle` | One memory artifact is created from the ended session and records the reset reason |
| TC-35 | `src/hooks/bundled/session-memory/capture.test.ts` | `session-memory` transcript capture | A transcript spanning compaction, discarded reset-tail tool rows, oversized rows, and a message cap | The capture selects the explicit branch across compaction, does not charge discarded tool rows against the budget, skips oversized rows, and does not scan beyond the message cap |
| TC-36 | `src/hooks/bundled/session-memory/transcript.test.ts` | `session-memory` memory text shaping | A zero recent-message limit, model and runtime artifacts, silence markers, and an omitted slash-command turn | The memory text is empty at a zero limit, artifacts are sanitized, silence markers and visible assistant rows are preserved, and the retained tail is filtered before slicing |
| TC-37 | `src/cli/native-hook-relay-cli.test.ts` | Native harness relay CLI | A cold-path argument vector, Codex hook JSON on stdin, a legacy relay command, and oversized input | The relay forwards stdin JSON to the gateway relay, a legacy command renders unavailable output, and oversized input fails without touching the gateway |

## Integration Tests

| ID | File | Description | Preconditions | Expected Outcome |
|---|---|---|---|---|
| TC-38 | `src/hooks/hooks-install.test.ts` | Install, discover, and trigger an installed hook pack | A local hook pack with a manifest declaring one hook, installed in copied and linked layouts | Only the installed hook is discovered, the config entry and the install record are written, and the hook fires on `command:new` |
| TC-39 | `src/hooks/gmail-watcher.integration.test.ts` | Watcher shutdown against a real child process | A running `gog` process with a credential-helper descendant | `stopGmailWatcher` removes the `gog` process and its descendant |
| TC-40 | `src/hooks/gmail-setup.integration.test.ts` | Gmail setup diagnostics through real command execution | Fixture `gcloud` and `gog` executables on `PATH` that fail at login or at watch start | The bounded failure is propagated and no config is written |
| TC-41 | `src/hooks/bundled/boot-md/handler.gateway-startup.integration.test.ts` | `boot-md` through the internal hook registry | Two configured agents with distinct workspaces and a registered `gateway:startup` hook | The `gateway:startup` event dispatches through the internal hooks and BOOT runs once per configured agent scope |
| TC-42 | `src/cli/hooks-cli.test.ts` | Hook report CLI formatting and JSON output | A report containing an eventless hook and a pending config write lock | The JSON check output classifies the eventless hook as not eligible, and a disable waits for the write lock |
| TC-43 | `src/cli/hooks-cli.toggle.test.ts` | Enable and disable semantics | A Gateway that owns state, an ambiguous selector, an unknown hook, an ineligible hook, a plugin-managed hook, and a remote Gateway | Each case fails with the correct message, no config is written on failure, and `hooks.status` is used for the read commands |
| TC-44 | `src/cli/hooks-cli.process.test.ts` | CLI process lifecycle | A plugin-owned handle open during `hooks list` | The handle is joined after the list output completes |
| TC-45 | `src/cli/native-hook-relay-cli.import-boundary.test.ts` | Native relay import boundary | A Gateway fallback path | Only the client relay owner is loaded before the Gateway fallback, and the hidden relay dispatches before the general CLI loads |
| TC-46 | `src/cli/native-hook-relay-cli.locator-worker.test.ts` | Native relay locator admission | A newer locator schema | The locator refuses the newer schema without migrating it |
| TC-47 | `src/gateway/server-methods/hooks-status.test.ts` | `hooks.status` RPC method | An ownerless explicit agent fleet, a live plugin hook registry, and a client without the `operator.read` scope | The method returns a typed selection-required error for an ownerless fleet, includes live plugin hooks in the report, and rejects a client that lacks the scope or sends unexpected params |

## End-to-End Tests

| ID | File | Description | Steps | Expected Outcome |
|---|---|---|---|---|
| TC-48 | `src/hooks/hooks-lifecycle.e2e.test.ts` | Full hook pack lifecycle | Author a hook pack, install it, list it, enable it, disable it, and dispatch an event | The pack is discovered, the toggle writes the config entry, and the handler runs with the expected side effect |
| TC-49 | `src/hooks/plugin-hooks.e2e.test.ts` | Plugin hook lifecycle contracts | Load a plugin and run message, session, and cron lifecycle hooks, then a `before_tool_call` policy | The plugin hooks execute and the tool-call policy routes through the embedded approval boundary |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-50 | A pack manifest declares a hook path outside the package root | The path is ignored with a warning and unlisted children are not scanned |
| TC-51 | A `HOOK.md` descriptor exceeds the 1 MiB metadata cap | The descriptor is skipped with a warning and other hooks keep loading |
| TC-52 | A handler path symlinks outside the hook directory | The path fails the boundary check and is not loaded |
| TC-53 | A hook declares no events | The hook is not loadable and the blocked reason is `no events defined` |
| TC-54 | A hook's required binary, environment variable, or config path is missing | The hook is not loadable, the missing group is named, and the install route is shown |
| TC-55 | A plugin-managed hook is enabled or disabled through the hooks CLI | The command is refused and the config is unchanged |
| TC-56 | A hook key matches more than one hook | The command fails and lists the candidates without writing config |
| TC-57 | An unknown hook name is supplied | The command exits with code 1 and prints the `hooks list` recovery command |
| TC-58 | `--agent` is blank | The command is rejected before a subcommand dispatches |
| TC-59 | A configured remote Gateway does not support the report method | The command fails instead of showing client-local hooks |
| TC-60 | The declared export exists but is not a function | The handler load fails and the hook is not registered |
| TC-61 | A hook subscribes to an event key core does not emit | The handler still loads and a warning names the key as a likely typo |
| TC-62 | A replacement generation fails to import | The previously committed generation keeps serving events |
| TC-63 | The fire-and-forget queue is at its bound | The new job is dropped and the drop is logged |
| TC-64 | A hook throws a multi-line error | The log entry is a single line of at most 500 characters |
| TC-65 | The Gmail watcher starts while hooks are disabled, the account is missing, or `gog` is absent | The watcher does not start and reports the reason |
| TC-66 | The Gmail serve process cannot bind its port | Retries are bounded at 3 attempts with backoff and the watcher then stops restarting |
| TC-67 | The Gmail watcher is stopped while the serve process is running | The process tree is terminated and the renewal schedule is cancelled |
| TC-68 | The native relay receives more than 1 MiB on stdin | The relay fails without contacting the Gateway |
| TC-69 | The Gateway relay is unavailable for a `permission_request` event | The relay fails closed rather than allowing the action |
| TC-70 | An install policy warning is not acknowledged | The install stops and the warning is surfaced |
| TC-71 | The lifecycle lease is replaced before a failed install is compensated | The compensation is refused and the newer record is retained |
| TC-72 | The stored integrity hash differs from the downloaded artifact | The update aborts by default and the drift is reported |

## Test Infrastructure

- Hook fixtures are written to temporary directories with a `HOOK.md` descriptor and a handler module, using helpers such as `src/hooks/hook-fixture.test-support.ts` and `src/hooks/install-archive.test-support.ts`.
- `src/hooks/gmail.test-support.ts` supplies the Gmail fixture helpers used by the watcher and setup suites.
- State isolation uses `createOpenClawTestState` from `src/test-utils/openclaw-test-state.ts` together with `pinConfigDir` from `src/utils.ts`, so each suite owns its state directory and cleans it up afterwards.
- The internal hook registry is a process-wide singleton, so suites call `clearInternalHooks()` and `setInternalHooksEnabled(true)` between cases.
- The native relay suites use `src/cli/native-hook-relay-cli.test-support.ts` to drive the CLI with a fake stdin and stdout.
- The Gmail setup suite installs a fixture `gcloud` executable on `PATH` so the setup path runs without Google Cloud credentials.
- The gateway RPC suite builds a method registry from `createCoreGatewayMethodDescriptors` and dispatches raw request frames through `handleGatewayRequest`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-13, TC-27, TC-38 |
| FR-2 | TC-4, TC-13, TC-14 |
| FR-3 | TC-3, TC-10, TC-50, TC-53, TC-61 |
| FR-4 | TC-8, TC-60, TC-9 |
| FR-5 | TC-2, TC-4, TC-10, TC-43, TC-55 |
| FR-6 | TC-1, TC-10, TC-54 |
| FR-7 | TC-6, TC-11, TC-28 |
| FR-8 | TC-5, TC-6, TC-14, TC-61 |
| FR-9 | TC-14, TC-62 |
| FR-10 | TC-42, TC-43, TC-47, TC-48 |
| FR-11 | TC-43, TC-55, TC-56, TC-57 |
| FR-12 | TC-29, TC-30, TC-31, TC-32, TC-41 |
| FR-13 | TC-22, TC-23, TC-24, TC-25, TC-26, TC-38, TC-70, TC-71, TC-72 |
| FR-14 | TC-15, TC-16, TC-17, TC-18, TC-19, TC-20, TC-39, TC-40, TC-65, TC-66, TC-67 |
| FR-15 | TC-37, TC-45, TC-46, TC-68, TC-69 |
| NFR-1 | TC-13, TC-23, TC-50, TC-51, TC-52 |
| NFR-2 | TC-7, TC-63, TC-64 |
| NFR-3 | TC-18, TC-20, TC-39, TC-66, TC-67 |
| NFR-4 | TC-42, TC-47 |
| NFR-5 | TC-15 |
| NFR-6 | TC-6, TC-7, TC-64 |
