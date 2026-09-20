---
title: "Isolated Spaces (Docker Place and Space Manager)"
status: done
---

# Test Plan: Isolated Spaces

## Scope

Covers the stage-1a backend in `packages/web/server/lib/spaces/`: manager, registry, Docker place, hardening, labels, and process spawning.
Live Docker tests (gated by `OPENCHAMBER_TEST_DOCKER=1`) and later stages (gatekeeper, dispatcher, UI) are out of scope for the committed unit suite.
Run with `bun run --cwd packages/web test -- server/lib/spaces`.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Label keys, resource names, id parsing, and comma-safe label reading | Label fixtures and inspect JSON | Correct keys, `openchamber-space-<id>-<role>` names, parsed ids |
| TC-2 | Hardening argv builders and the inspect checker agree | Specs and inspect fixtures | Expected `docker create` / network argv; violations reported for forbidden flags |
| TC-3 | Manager generates ids, builds the 4 GiB default spec, and re-verifies after create | Fake place | Spec with fresh id and default memory; violating space removed |
| TC-4 | Registry accepts complete places and rejects incomplete ones | Place objects | Accept or reject per contract completeness |
| TC-5 | Docker place maps CLI outcomes to contract results (name taken, rollback list, uncertain flag) | Fake runner transcripts | Correct codes and `details` payloads |
| TC-6 | Process runner spawns directly with timeout and output cap | Hung or verbose fake child | Child killed on timeout; oversized output rejected |

Test files: `places/registry.test.js`, `places/docker.test.js`, `places/labels.test.js`, `hardening.test.js`, `manager.test.js`, `run-command.test.js`.
Shared harnesses (never imported by product code): `places/contract-suite.js`, `places/escape-suite.js`, `places/memory-place.js`, `places/fake-docker.js`, `places/docker-live-support.js`.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Place contract suite passes against the Docker place | Local Docker daemon, `OPENCHAMBER_TEST_DOCKER=1` | All contract operations behave per contract |
| TC-8 | Escape suite fails every escape inside a real space | Live daemon, baseline controls conclusive | Network, privilege, filesystem, and namespace probes all fail |

Live files: `places/contract.docker.live.test.js`, `places/escape.docker.live.test.js`.
Each uses its own owner id, cleans up in `afterAll`, and fails on leftover labelled resources.

## End-to-End Tests

None: the module is unwired and has no user-facing surface yet.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | `create` interrupted mid-step (`command_timeout`, `command_killed`) | Double sweep removes labelled and unlabelled same-name resources; error carries `details.uncertain: true` |
| TC-10 | Resource vanishes between listing and inspect | Entries already found are used; other inspect failures reject |
| TC-11 | Engine 26.x accepts the isolated option but keeps a gateway | Checker reports it; `create` fails closed with clean rollback |
| TC-12 | `remove` on an unknown space | Resolves with both `removed` and `failed` empty |
| TC-13 | `docker volume create` on an existing name | `create` refuses upfront by name check, never adopts a stranger's volume |

## Test Infrastructure

- `fake-docker.js` and `memory-place.js` stand in for the daemon so unit tests never need Docker.
- Live tests require a local Docker daemon and pull ~1.6 GB on first run.
- Leftover check: `docker ps -a`, `docker network ls`, `docker volume ls` filtered by `label=openchamber.space`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-5, TC-7 |
| FR-2 | TC-4 |
| FR-3 | TC-5, TC-7 |
| FR-4 | TC-2, TC-7 |
| FR-5 | TC-1, TC-7 |
| FR-6 | TC-5, TC-9, TC-13 |
| FR-7 | TC-1, TC-7 |
| FR-8 | TC-6, TC-7 |
| FR-9 | TC-5 |
| FR-10 | TC-11 |
| NFR-1 | TC-2, TC-8 |
| NFR-2 | TC-2 |
| NFR-3 | TC-5, TC-10 |
| NFR-4 | TC-6 |
| NFR-5 | TC-2 |
