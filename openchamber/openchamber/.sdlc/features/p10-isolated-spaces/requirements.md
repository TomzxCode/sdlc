---
title: "Isolated Spaces (Docker Place and Space Manager)"
status: done
---

# Requirements: Isolated Spaces

## Overview

Agents should be able to work inside an isolated container on a copy of the project, so the user's machine is protected, permission prompts can go away, and host secrets stay out of reach.
The implemented slice (stage 1a) is the unwired backend foundation: a space manager, a place registry, and a local Docker place that creates, finds, stops, starts, removes, and verifies hardened spaces.
Nothing imports the module yet: there are no routes, no settings, and no UI.
The full product vision (gatekeeper, dispatcher, grants, apply/discard flows) is defined in `docs/isolated-spaces/DESIGN.md` and remains future work.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Run agents in isolated containers without hand-managing Docker |
| Maintainers | A place contract that later places (SSH Docker, Kubernetes, Apple `container`) can implement |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall create, find, stop, start, and remove isolated spaces on a place through the space manager. |
| FR-2 | Must | The system shall keep a sealed-after-boot place registry that rejects any place missing a contract operation. |
| FR-3 | Must | The system shall provide a local Docker place implementing the full place contract (`check`, `create`, `list`, `exec`, `stop`, `start`, `remove`, `verify`). |
| FR-4 | Must | The system shall create space containers with the hardening restrictions and verify them against `docker inspect` before they ever run. |
| FR-5 | Must | The system shall record spaces using labels only: every container, network, and volume carries the full `openchamber.space` label set. |
| FR-6 | Must | The system shall roll back a failed `create` by removing everything labelled with the new id, and report what it could not remove. |
| FR-7 | Must | The system shall isolate owners: two installs sharing one Docker daemon shall not see or touch each other's spaces. |
| FR-8 | Must | The system shall run commands inside a space as the space user and report exit code, stdout, and stderr for any command exit code. |
| FR-9 | Should | The system shall report place availability with an actionable message naming what the user must fix. |
| FR-10 | Should | The system shall detect engines that silently ignore the isolated gateway mode and fail `create` closed with a clean rollback. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall run the agent as a non-root user with a read-only filesystem, no new privileges, no capabilities, and its own isolated network. |
| NFR-2 | Must | Security | The system shall never present bind mounts, `--volumes-from`, the runtime socket, privileged mode, shared namespaces, devices, or published ports in a space. |
| NFR-3 | Must | Reliability | The system shall never resolve an empty space list instead of rejecting on a place failure. |
| NFR-4 | Must | Reliability | The system shall spawn Docker directly with an argv array, no shell, a killing timeout, and an output cap. |
| NFR-5 | Should | Reliability | The system shall bound space logging on the Docker host so agent output cannot fill the disk. |

## Constraints

- Docker Engine 28 or newer is required for the isolated gateway mode the checker enforces.
- Named volumes of the default driver have no size limit: a space can fill the Docker host disk through its work or home volume.
- The module is unwired: no routes, no settings, and no UI import it yet.
- The base image digest must be the multi-arch index digest, or spaces break on the other CPU architecture.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: create and remove a space
      Given a registered Docker place with an available daemon
      When the manager creates a space and then removes it
      Then the space runs and verifies clean, and afterwards no labelled resource with its id remains
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: registry rejects an incomplete place
      Given a place object missing one contract operation
      When it is registered
      Then registration rejects the place
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Docker place passes the contract suite
      Given a Docker daemon
      When the place contract suite runs against the Docker place
      Then every contract operation behaves per its contract
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: unverified container never runs
      Given a container spec that violates a hardening restriction
      When the Docker place creates it
      Then verification fails, the container never starts, and creation rolls back
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: labels identify every resource
      Given a created space
      When its container, network, and volumes are inspected
      Then each carries the marker, id, role, owner, project, name, and created labels
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: failed create rolls back
      Given a create that fails after resources exist
      When the failure surfaces
      Then labelled resources for the new id are removed and the error lists rollback failures
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: owners do not see each other
      Given spaces owned by install A on a shared daemon
      When install B lists spaces
      Then none of install A's spaces appear, and B cannot exec into them
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: exec reports command results
      Given a running space
      When a command exits non-zero inside it
      Then exec resolves with the exit code, stdout, and stderr
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: unavailable place explains itself
      Given a Docker place whose CLI is missing
      When check runs
      Then it resolves unavailable with a message naming what the user must fix
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: engine ignoring the isolated mode fails closed
      Given an engine that accepts the isolated gateway option but still assigns a gateway address
      When a space is created
      Then the checker reports it and create fails with a clean rollback
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: escape suite passes in a real space
      Given a running space on a verified engine
      When the escape suite runs inside it
      Then every escape attempt fails (network, privilege, filesystem, namespace probes)
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: forbidden flags are reported
      Given an inspected container with a published port
      When the hardening checker runs
      Then it reports a violation
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: list failure rejects
      Given a place whose inspect fails unexpectedly
      When list runs
      Then it rejects instead of resolving an empty list
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: hung Docker CLI is killed
      Given a Docker invocation that hangs
      When its timeout expires
      Then the child process is killed and the call rejects with a timeout code
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: log output is capped
      Given a space writing unbounded output
      When it runs
      Then the Docker host log stays within the configured local-driver cap
    ```

## Conflicts

None identified yet.

## Open Questions

1. Which place comes next (SSH Docker, Kubernetes, Apple `container`), and what does its contract delta look like?
2. What is the gatekeeper protocol for stage 2, and how are grants represented?
3. What are the per-space idle-stop default threshold and setting shape?
