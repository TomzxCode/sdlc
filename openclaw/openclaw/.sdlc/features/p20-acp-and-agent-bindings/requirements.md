---
title: "ACP and Agent Bindings"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: ACP and Agent Bindings

## Overview

An external agent client such as an IDE needs a way to drive an OpenClaw session, and an operator needs a way to send a given conversation to the right agent.
The ACP half of this feature speaks the Agent Client Protocol in both directions.
`openclaw acp` runs a stdio bridge that speaks ACP over NDJSON and forwards prompts into a Gateway session over WebSocket, `src/acp/translator.ts` and its `translator.*.ts` family translate ACP session updates into Gateway events, `src/acp/client.ts` spawns an external ACP server and relays the permission requests that come back, and `src/acp/control-plane/` holds the process-wide session manager that owns ACP session identity, runtime handles, cancellation, turn delivery, backend failover, and actor-epoch fencing.
The shared, transport-free logic lives in `packages/acp-core/`, so the Gateway and the bridge agree on session identity, interaction mode, lineage metadata, error formatting, and structured auth redaction.
The bindings half of this feature decides which agent answers an inbound message.
`src/routing/resolve-route.ts` evaluates the configured route bindings against the channel, the account, the peer, the parent peer, the guild, the team, and the Discord member roles, `src/routing/session-key.ts` owns the `agent:<id>:<peer>` session key family, and `src/config/bindings.ts` is the config source of truth.
A binding only chooses the agent.
It does not create a channel account, and it does not grant access, because a binding is consulted only after the channel has already accepted the message through its own pairing, allowlist, and account rules.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| IDE and editor users | Drive an OpenClaw session from an ACP client and see the turn progress in the editor |
| Channel operators | Route each conversation to the right agent, with a predictable match order |
| Agent authors | Spawn, steer, cancel, and configure an ACP session from chat |
| Gateway operators | Keep ACP behind an explicit feature gate and an agent allowlist |
| Security reviewers | Confirm that a binding never widens channel access and that ACP credentials never reach a log |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide an `openclaw acp` command that runs an ACP bridge over NDJSON on stdio and forwards prompts into a Gateway session over WebSocket, accepting the options `--url`, `--token`, `--token-file`, `--password`, `--password-file`, `--session`, `--session-label`, `--require-existing`, `--reset-session`, `--no-prefix-cwd`, `--provenance`, and `-v` |
| FR-2 | Must | The system shall translate ACP session updates into Gateway events and Gateway events back into ACP session updates, and shall relay a permission request raised by an ACP tool call into the Gateway approval path |
| FR-3 | Must | The system shall own ACP session identity, runtime handles, cancellation, turn delivery, backend failover, and actor-epoch fencing in one process-wide session manager, so two callers cannot drive the same ACP session concurrently |
| FR-4 | Must | The system shall refuse to create or run an ACP session when `acp.enabled` is `false`, and shall report the refusal with a typed `ACP_DISPATCH_DISABLED` error |
| FR-5 | Must | The system shall enforce `acp.dispatch.enabled` independently of `acp.enabled`, so that the ACP commands stay available while ACP turn execution is blocked |
| FR-6 | Must | The system shall treat `acp.allowedAgents` as an allowlist of ACP target agent ids, and shall refuse a target outside the list with a typed `ACP_SESSION_INIT_FAILED` error |
| FR-7 | Must | The system shall register ACP runtime backends by id in a process-wide registry, probe their health, and shall fail over to a configured fallback backend only when the primary attempt failed before the prompt started, produced no output, and reported a transient availability error |
| FR-8 | Must | The system shall record ACP prompts and session updates in a replay ledger bounded by a maximum number of sessions, a maximum number of events per session, and a maximum total serialized size |
| FR-9 | Must | The system shall bind a channel conversation to a persistent ACP session, either with `/acp spawn --bind here` or with a configured binding of type `acp`, and shall derive a stable session key from the channel, the account, and the conversation id |
| FR-10 | Must | The system shall resolve the agent for an inbound message by evaluating the configured route bindings against the peer, the parent peer, the peer wildcard, the guild with roles, the guild, the team, the account, and the channel, in that order, and shall report which rule matched |
| FR-11 | Must | The system shall use a binding only to select the agent, and shall neither create a channel account nor grant access, because a binding is consulted only after the channel has accepted the message through its own pairing, allowlist, and account rules |
| FR-12 | Must | The system shall derive the session key of a routed conversation in the `agent:<agentId>:<peer>` family, using `agent:<agentId>:main` for the agent main session, `agent:<agentId>:direct:<peerId>` for a per-peer direct chat, `agent:<agentId>:<channel>:direct:<peerId>` for a per-channel direct chat, and `agent:<agentId>:<channel>:<peerKind>:<peerId>` for a group conversation |
| FR-13 | Should | The system shall expose the chat command `/acp` with the actions `spawn`, `cancel`, `steer`, `close`, `sessions`, `status`, `set-mode`, `set`, `cwd`, `permissions`, `timeout`, and `model`, and shall resolve each action against a session key, a session id, or a session label |
| FR-14 | Should | The system shall expose `openclaw agents list`, `openclaw agents bindings`, `openclaw agents bind`, and `openclaw agents unbind` so an operator can inspect and edit the route bindings that decide which agent answers |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall read Gateway credentials for the bridge from an explicit token, a password, or a file, shall keep them out of stdout, and shall redact them from every error the bridge reports |
| NFR-2 | Must | Security | The system shall classify every ACP tool approval request and shall auto-approve only a read-only tool that the classifier recognizes, so an unknown or mutating tool still requires a decision |
| NFR-3 | Must | Reliability | The system shall fence an ACP turn by actor epoch, so a superseded actor cannot publish into a session it no longer owns, and shall scope a cancellation to the invocation it captured |
| NFR-4 | Should | Performance | The system shall maintain a running byte estimate for the replay ledger so a budget check never scans the event table, and shall evict the oldest idle ACP session rather than an active one when the session store reaches its cap |
| NFR-5 | Should | Portability | The system shall keep the session identity, interaction mode, lineage metadata, error formatting, and structured auth redaction in the transport-free `@openclaw/acp-core` package, so the Gateway and the stdio bridge share one implementation |

## Constraints

- The Agent Client Protocol SDK is pinned at version 1.8.0.
- The bridge runs over stdio, so stdout carries protocol bytes and all logging goes to stderr.
- The ACP bridge needs a Gateway connection, so it cannot run against a Gateway that has no reachable URL and no credentials.
- `acp.enabled` gates the whole ACP surface; `acp.dispatch.enabled` gates only turn execution.
- `acp.allowedAgents` is empty by default, and an empty allowlist permits every agent.
- A configured ACP binding is reconciled against the live session: a session whose agent, mode, backend, or working directory no longer matches the binding is closed and recreated.
- A route binding is a config entry under `bindings`, and a binding without an explicit `type` is a route binding.
- The `agent:<agentId>:<peer>` session key is a public contract that clients depend on, so its shape cannot change without a migration.
- The `/acp` command surface is shared by every channel, and each channel adapter decides whether it can host a thread-bound ACP session.
- A route binding match is scoped to one channel and one account, so a binding never reaches across accounts.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Start the ACP bridge against a remote Gateway
      Given a running Gateway reachable over WebSocket
      When "openclaw acp --url wss://gateway.example/ws --token-file /tmp/token" is started
      Then the bridge speaks ACP over NDJSON on stdio
      And the first prompt is forwarded into the Gateway session
    ```

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Refuse to attach to a session that does not exist
      Given a session key that is not present on the Gateway
      When "openclaw acp --session agent:main:missing --require-existing" is started
      Then the bridge exits with a failure
      And the failure names the missing session
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Forward an agent message chunk back to the ACP client
      Given an ACP client attached to a session
      When the Gateway emits an agent message chunk for that session
      Then the client receives the matching ACP session update
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Relay a permission request into the Gateway approval path
      Given an ACP tool call that needs a permission decision
      When the ACP client receives the permission request
      Then the request is offered to the Gateway approval path
      And the decision is sent back to the ACP client
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Reject a second concurrent turn on the same ACP session
      Given an ACP session with a turn in flight
      When a second turn is submitted for the same session key
      Then the second turn is refused rather than interleaved with the first
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Cancel only the invocation that was captured
      Given an ACP session whose current turn was already cancelled and replaced
      When a late cancel arrives for the previous run
      Then the replacement run is not aborted
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Refuse an ACP session when the feature gate is closed
      Given the configuration acp.enabled set to false
      When an ACP session is created
      Then the call fails with the error code ACP_DISPATCH_DISABLED
      And the message names acp.enabled=false
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Keep the commands available while blocking turn execution
      Given the configuration acp.dispatch.enabled set to false and acp.enabled left on
      When the ACP status command runs
      Then the command answers
      And a turn dispatch fails with the error code ACP_DISPATCH_DISABLED
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Refuse an ACP target outside the allowlist
      Given the configuration acp.allowedAgents set to only "ops"
      When an ACP session is created for the agent "main"
      Then the call fails with the error code ACP_SESSION_INIT_FAILED
      And the message names the agent and the policy
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Allow every agent when the allowlist is empty
      Given the configuration acp.allowedAgents left unset
      When an ACP session is created for the agent "main"
      Then the session is admitted
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Fail over when the primary backend is unavailable before the prompt starts
      Given a primary ACP backend that reports the quota exhausted before any prompt output
      And a configured fallback backend
      When a turn is submitted
      Then the fallback backend runs the turn
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Keep the primary backend after it produced output
      Given a primary ACP backend that failed after it produced output
      And a configured fallback backend
      When a turn is submitted
      Then the turn fails on the primary backend
      And the fallback backend is not started
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Read a replay of the recorded session updates
      Given an ACP session whose prompt and updates were recorded
      When the replay is read for that session
      Then the recorded updates are returned in sequence order
      And the replay reports whether the session is complete
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Trim the ledger when the serialized size budget is exceeded
      Given a replay session whose recorded events exceed the total byte budget
      When another event is recorded
      Then the oldest events are trimmed
      And the session stays within the byte budget
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Bind the current conversation to a persistent ACP session
      Given a chat conversation on a channel that supports thread binding
      When "/acp spawn codex --bind here" runs
      Then the conversation is bound to a persistent ACP session
      And later messages in that conversation reach that session
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Derive the same session key for the same configured binding
      Given a configured binding of type acp for one channel, account, and conversation
      When the binding is reconciled twice
      Then both runs resolve to the same ACP session key
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Recreate a session that no longer matches its configured binding
      Given a configured binding whose agent differs from the live ACP session
      When the binding is reconciled
      Then the mismatched session is closed
      And a new session is created for the configured agent
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Prefer a peer binding over an account binding
      Given a peer binding and an account binding for the same channel
      When a message arrives from that peer
      Then the peer binding wins
      And the route reports that it matched on the peer
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Fall back to the channel binding when nothing more specific matches
      Given a channel-wide binding and a message from an unbound account
      When the message is routed
      Then the channel binding is used
      And the route reports that it matched on the channel
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Keep a binding from widening channel access
      Given a binding that names an account the channel never accepts
      When a message arrives on a different, unaccepted account
      Then the binding does not route that message
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Report that agent selection is required when nothing matches
      Given a multi-agent setup with no matching binding and no resolvable default owner
      When a message is routed
      Then routing reports AGENT_SELECTION_REQUIRED
      And the error names the channel and the account
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Build the session key of a direct conversation
      Given the agent "ops" and the DM scope set to per-peer
      When the session key is built for a direct peer
      Then the key is agent:ops:direct:<peerId>
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Keep a separate key for the agent main session
      Given the agent "ops"
      When the main session key is built
      Then the key is agent:ops:main
      And a direct conversation key differs from it
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: List the ACP sessions from chat
      Given a chat conversation with an ACP session bound to it
      When "/acp sessions" runs
      Then the reply lists the ACP sessions with their backend and mode
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Resolve an ACP action by session label
      Given two ACP sessions with distinct labels
      When "/acp status my-label" runs
      Then the reply reports the status of the session labelled "my-label"
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: List the route bindings
      Given a configuration with two route bindings
      When "openclaw agents bindings" runs
      Then both bindings are listed with their channel, account, and agent
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Remove a route binding
      Given a configuration with a route binding for one channel and account
      When "openclaw agents unbind --agent ops --bind discord:support" runs
      Then the binding is removed from the configuration
      And the reply reports the removed binding
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Keep the Gateway token out of stdout and out of errors
      Given a Gateway token supplied on the command line
      When the bridge fails to connect
      Then the failure message does not contain the token
      And stdout carries no token bytes
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Redact a credential from a structured auth failure
      Given a backend that returns an authentication error carrying a secret
      When the failure is reported
      Then the secret is replaced by a redaction marker
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Require a decision for an unrecognized tool
      Given an ACP tool call for a tool the classifier does not know
      When the permission request is raised
      Then the request is not auto-approved
      And it is offered for a decision
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Auto-approve a recognized read-only tool
      Given an ACP tool call for a recognized read-only search tool
      When the permission request is raised
      Then the request is auto-approved
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Refuse a publish from a superseded actor
      Given an ACP session whose owner was replaced by a newer actor
      When the superseded actor tries to publish a turn result
      Then the publish is refused
      And the newer actor keeps the session
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Refuse a stale discard token
      Given an ACP session replaced by a newer runtime
      When a stale discard token is presented
      Then the successor runtime is not removed
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Check the ledger budget without scanning the event table
      Given a replay session with a running byte estimate
      When the budget is checked
      Then the estimate is used
      And the event table is not read
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Evict the oldest idle session rather than an active one
      Given an in-memory ACP session store at its session cap
      And one session with an active run
      When a new session is created
      Then the oldest idle session is evicted
      And the session with the active run is kept
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Share the session identity rules between the bridge and the Gateway
      Given the same agent id, peer, and account
      When the bridge and the Gateway each build the session key
      Then both produce the same key
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Keep the core free of transport dependencies
      Given the @openclaw/acp-core package
      When its module graph is inspected
      Then it pulls in no WebSocket, no stdio, and no Gateway client module
    ```

## Conflicts

None identified yet.

## Open Questions

1. `acp.allowedAgents` defaults to empty, which permits every agent, so a deployment that wants a closed set has to configure it explicitly.
2. The ACP replay ledger lives in the state database, so a Gateway with heavy ACP traffic grows that database; there is no separate retention job for the replay tables.
3. The route binding match order is fixed in code rather than configurable, so an operator cannot put a channel-wide binding ahead of a peer binding.
4. A configured ACP binding whose backend changes closes and recreates the session, so a backend rollout interrupts the bound conversation.
