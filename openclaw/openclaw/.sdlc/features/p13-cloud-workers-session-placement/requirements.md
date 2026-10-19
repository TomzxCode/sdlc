---
title: "Cloud Workers and Session Placement"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Cloud Workers and Session Placement

## Overview

A coding session often needs compute that the Gateway host cannot provide: a Linux box with a different toolchain, a throwaway machine that must be destroyed after one run, or a paired device that already holds the repository. This feature dispatches a session's turn to such a machine while the Gateway keeps everything that matters. The transcript stays on the Gateway and arrives as replayable commit batches, the accepted workspace diff is reconciled back into the session's managed worktree, model credentials stay on the Gateway and reach the worker only as a `{provider, model}` reference, and the worker's own tool calls are proxied back through the Gateway so tool authority never leaves it. The Gateway control plane under `src/gateway/worker-environments/` owns environment lifecycle, placement dispatch, provider provisioning, worker turns, workspace sync, and credential brokering; `src/worker/` owns the restricted worker-side runtime; and `packages/worker-runtime/` owns the bounded worker task pool that both share.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Session owner | Wants the run to happen on a machine that fits the work, with the transcript and the accepted diff landing back in the session they started |
| Gateway operator | Wants a durable, recoverable record of every environment, placement, and turn, and a single place that decides where work runs |
| Provider operator | Wants one allocation per dispatch, a stable lease identity, and a clean teardown even when the Gateway restarts mid-provision |
| Security reviewer | Wants provider credentials, model keys, and publication secrets to stay on the Gateway, and a closed worker ingress that cannot reach operator RPCs |
| Agent runtime | Wants tool calls from a remote turn to run under the same policy, hooks, and cancellation as a local turn |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall manage every worker environment through a durable state machine with the states `requested`, `provisioning`, `bootstrapping`, `ready`, `attached`, `idle`, `draining`, `destroying`, `destroyed`, `failed`, and `orphaned`, and shall persist each transition in `worker_environments` before the transition is observable. |
| FR-2 | Must | The system shall derive both the environment id and the provision operation id deterministically from the caller's idempotency key, so a replayed create request resolves to the same environment and never allocates a second machine. |
| FR-3 | Must | The system shall enforce the configured required worker profile before any allocation, and shall refuse a dispatch whose requested profile does not satisfy `cloudWorkers.requiredProfile`. |
| FR-4 | Must | The system shall mint one worker credential per dispatch, persist only its hash in `worker_environment_credentials`, and admit a worker connection only when the credential hash, environment id, session id, run id, owner epoch, bundle hash, OpenClaw version, RPC set version, and protocol features all match the durable record. |
| FR-5 | Must | The system shall revalidate the live worker connection identity on every worker RPC and shall close the connection with a typed reason when the credential was replaced or expired, the environment became unavailable or was marked for destroy, or the owner epoch changed. |
| FR-6 | Must | The system shall track a session's placement in `worker_session_placements` across the states `local`, `requested`, `provisioning`, `syncing`, `starting`, `active`, `draining`, `reconciling`, `reclaimed`, and `failed`, and shall carry the transition generation and the active owner epoch on every transition. |
| FR-7 | Must | The system shall require an exact turn claim (claim id, run id, claim generation, and owner epoch) before a worker turn executes, shall persist the worker-visible tool surface against that claim in `worker_turn_tool_authorities`, and shall start the restricted worker runtime only from a launch descriptor whose connection endpoint and granted tool surface both validate. |
| FR-8 | Must | The system shall proxy model inference requested by a worker through the Gateway using a `{provider, model}` reference so that Gateway-held provider credentials stay off the worker, and shall support worker-local inference only on an explicitly configured paired-device profile, where the node provisions its own model configuration and the Gateway still sends only the model reference and the authorized placement choice. |
| FR-9 | Must | The system shall execute Gateway-owned tools requested by a worker over one closed worker transport, revalidating the admitted run, turn claim, environment owner epoch, and placement generation on every invocation, and shall never expose an operator RPC to a worker. |
| FR-10 | Must | The system shall commit worker transcript batches through a compare-and-swap against the session's commit head, and shall fail-stop the run on a stale base instead of duplicating or rebasing already-paid output. |
| FR-11 | Must | The system shall sync the session workspace to the remote machine and reconcile the accepted result back into the session's managed worktree, writing a bounded reconciliation journal before any managed-worktree mutation. |
| FR-12 | Must | The system shall record a planned placement move in `worker_session_placement_moves` with the source generation, source owner epoch, and target, shall fence a stale asynchronous completion with the opaque operation id so an old move cannot retire a newer placement, and shall reclaim a session back to the Gateway on stop or reclaim. |
| FR-13 | Should | The system shall bound capacity in two places: a prepared pool that reserves capacity for declared demand and expires preparations it never consumed, and a shared worker task pool that admits work only within its task count and input byte limits and applies the same compute budget across independent pools on one host. |
| FR-14 | May | The system shall expose a desktop control surface for a cloud worker over an RFB transport that is reached by the Gateway, without opening an inbound worker port on the remote machine. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall never send provider credentials, model provider keys, or GitHub publication secrets to the remote machine. The only material that crosses the boundary is the minted worker credential, a `{provider, model}` reference, and a per-turn GitHub token profile bound to the admitted repository session. |
| NFR-2 | Must | Security | The system shall keep worker ingress closed. A worker connection shall reach only the worker method allowlist and shall be denied every operator RPC, with the denial recorded as a runtime action decision. |
| NFR-3 | Must | Reliability | The system shall recover environment, placement, and turn state after a Gateway restart. A recovery pass shall re-derive the live placement, environment, owner epoch, placement generation, and turn claim before any worker launch, and shall refuse to revive a pre-restart claim or to reuse an incompatible execution-context dialect. |
| NFR-4 | Must | Performance | The system shall bound every workspace transfer. The inventory entry count, the manifest size, the reconciliation file size, and the total reconciled patch size shall each have an explicit limit, and exceeding a limit shall fail the operation rather than truncate it silently. |
| NFR-5 | Should | Availability | The system shall keep prepared capacity available for declared demand, and shall expire a preparation that was never consumed instead of holding it indefinitely. |
| NFR-6 | Should | Observability | The system shall record every environment, placement, and turn transition with its state, generation, owner epoch, and timestamps, so an operator can reconstruct what happened after a failure or a restart. |

## Constraints

- The Gateway remains the owner of the transcript, the session database, and tool authority. A worker never opens the session database and never holds a tool policy of its own.
- Provider credentials never reach the remote machine. Model inference is proxied by `{provider, model}` reference, and worker-local inference is opt-in per profile.
- The same idempotency key maps to exactly one environment id and one provision operation id. The provision operation id is unique across the whole environment table.
- A worker credential is stored hashed. The Gateway never persists the credential value in plaintext.
- The worker protocol is a closed method allowlist. A worker cannot call an operator RPC and cannot select a different source session.
- The Gateway owns placement state. The remote machine holds no authority over whether a session is placed, and a stale worker is fenced rather than merged.
- Tool-call ids are idempotency keys only inside one exact source turn claim. An operation from another Gateway instance is ambiguous and is never replayed.
- Placement changes that need provider allocation are control-plane writes and are rate limited like other control-plane mutations.
- The Gateway and the worker must be the same build. A worker bundle that does not match the running Gateway build is rejected as a stale build and the session is redispatched.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: environment transitions are durable
      Given a provider profile that can allocate a machine
      When the operator creates an environment and the Gateway drives it to ready
      Then the environment row records each state in order and no transition is observable before it is persisted
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: replayed create reuses one environment
      Given an environment created with idempotency key K
      When the caller repeats the create request with the same key
      Then the same environment id and provision operation id are returned and no second machine is allocated
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: required profile is enforced before allocation
      Given cloudWorkers.requiredProfile is set to profile-a
      When a dispatch requests profile-b
      Then the dispatch is refused before any provider allocation is attempted
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: admission checks every server-owned binding
      Given a dispatched environment with a minted credential
      When a worker connects with a mismatched bundle hash, version, owner epoch, or credential hash
      Then the connection is refused with the matching admission reason and no turn runs
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: rotation fences a stale socket
      Given a connected worker whose credential was rotated
      When the worker sends another RPC
      Then the connection closes with the credential-replaced reason and the turn does not continue
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: placement state machine is enforced
      Given a session that is dispatched to a worker
      When the placement advances from requested through provisioning, syncing, and starting to active
      Then each transition increments the transition generation and the active owner epoch is set only once the placement is active
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: a turn requires an exact claim and a valid descriptor
      Given an active placement with a claimed turn
      When a worker turn arrives without a matching claim id, run id, generation, and owner epoch
      Then the turn is refused and no tool surface is granted
      And a launch descriptor with an invalid tool authority or connection endpoint is refused at startup
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: inference is proxied by reference
      Given a Gateway-owned model credential
      When a worker turn requests inference
      Then the request reaches the provider through the Gateway using only a provider and model reference, and no provider key is present on the worker
      And a paired-device profile with worker-local inference configured uses node-provisioned model configuration while the Gateway still sends only the model reference
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: worker tool calls revalidate authority
      Given a running worker turn with a granted tool surface
      When the worker invokes a Gateway-owned tool after the placement generation changed
      Then the invocation is refused, the effect does not run, and the denial is recorded as a runtime action decision
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: stale transcript base fails the run
      Given a worker turn committing transcript batches against a session commit head
      When a commit is presented with a base that is behind the current head
      Then the run fails instead of duplicating or rebasing the already-committed output
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: accepted result reconciles into the managed worktree
      Given a completed remote turn with an accepted workspace result
      When the Gateway reconciles the result
      Then a reconciliation journal is written before the managed worktree is mutated and the accepted files land in the session worktree
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: stale move completion is fenced
      Given a placement move to a new target that is still in flight
      When a late completion for the superseded source arrives
      Then the old source placement is not retired and the current placement stays active
    ```

- [x] **FR-13**

    ```gherkin
    @FR-13
    Scenario: capacity is bounded in both places
      Given a prepared pool at its configured maximum and a worker task pool at its admitted byte limit
      When one more preparation and one more task are requested
      Then both are refused rather than exceeding their bounds, and an unused preparation is released when it expires
    ```

- [x] **FR-14**

    ```gherkin
    @FR-14
    Scenario: desktop is reached without inbound ports
      Given a cloud worker with a desktop
      When an operator observes the desktop through the Gateway
      Then the Gateway reaches the worker over the existing authenticated node or worker channel and no inbound port is opened on the remote machine
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: secrets never cross the worker boundary
      Given a dispatched environment with a provider profile, a model credential, and a GitHub publication profile
      When the worker bundle, launch envelope, and worker protocol traffic are inspected
      Then no provider credential, model key, or publication secret appears in any of them
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: operator RPCs are unreachable from a worker
      Given an admitted worker connection
      When the worker attempts an operator RPC method
      Then the method is denied and the denial is recorded with the worker admission decision boundary
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: restart recovery refuses pre-restart claims
      Given a Gateway that restarted while a placement was active
      When the recovery pass runs
      Then it re-derives the live placement, environment, owner epoch, placement generation, and turn claim before any launch, and a pre-restart claim is not revived
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: oversized workspace transfers fail loudly
      Given a remote workspace whose inventory, manifest, or reconciled patch exceeds its limit
      When the sync or reconciliation runs
      Then the operation fails with the limit named and no partial result is accepted
    ```

- [x] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: prepared capacity is reserved and bounded
      Given a prepared pool at its configured maximum
      When a declared demand asks for one more preparation
      Then the request is refused rather than exceeding the pool maximum, and an unused preparation is released when it expires
    ```

- [x] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: transitions are reconstructable
      Given a failed dispatch and a later Gateway restart
      When an operator inspects the environment, placement, and turn records
      Then each record carries its state, generation, owner epoch, and timestamps in the order the transitions happened
    ```

## Conflicts

None identified yet.

## Open Questions

1. The prepared pool keeps capacity reserved for declared demand, but the demand signal and the reservation lifetime come from configuration rather than from an observed queue. Should reservation lifetime follow the request that declared the demand, or a fixed profile-level bound?
2. Worker-local inference currently applies to explicitly configured paired-device profiles. Should the same credential boundary be extended to provider-hosted cloud profiles that advertise a node-provisioned model configuration?
3. The workspace transfer limits are constants in the implementation rather than configuration values. Should operators be able to raise them for very large repositories, and if so, which bound stays fixed regardless of configuration?
