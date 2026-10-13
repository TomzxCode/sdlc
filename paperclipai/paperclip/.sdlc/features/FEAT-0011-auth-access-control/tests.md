---
title: "Auth & Access Control"
status: done
session_link: "reverse-engineered during sync 2026-10-13"
---

# Test Plan: Auth & Access Control

## Scope

Covers deployment modes, session auth, company access boundaries, board/agent API keys, invites, join requests, permission grants, and CLI auth.
Out of scope: OAuth2/OIDC federation and SAML/SSO (per specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Board auth mode resolution | Deployment config local_trusted vs authenticated | Correct actor resolution per mode (`server/src/services/board-auth.test.ts`) |
| TC-2 | Authorization service gates | Action on resource per actor | Allow/deny per policy (`server/src/__tests__/authorization-service.test.ts`) |
| TC-3 | Company access enforcement | Cross-company request | 403/404 rejection (`server/src/__tests__/authz-company-access.test.ts`) |
| TC-4 | Agent API key hashing | New key creation | Hash stored, plaintext returned once |
| TC-5 | Invite token entropy | Invite creation | High-entropy unique token (`server/src/__tests__/invite-token-entropy.test.ts`) |
| TC-6 | Invite rate limiting | Rapid invite creation | Throttled per policy (`server/src/__tests__/invite-rate-limit.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Auth routes end-to-end | Seeded company and user | Session login/me/logout succeed (`server/src/__tests__/auth-routes.test.ts`) |
| TC-8 | CLI auth challenge flow | Pending challenge | Challenge/respond completes (`server/src/__tests__/cli-auth-routes.test.ts`) |
| TC-9 | Invite accept flow | Pending invite | Membership created (`server/src/__tests__/invite-accept-replay.test.ts`, `invite-join-manager.test.ts`) |
| TC-10 | Cross-tenant agent isolation | Two companies with agents | Agent key for A rejected on B (`server/src/__tests__/agent-cross-tenant-authz-routes.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-11 | Agent auth middleware | Bearer key request through middleware | Company context set or 401/403 (`server/src/__tests__/agent-auth-middleware.test.ts`) |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-12 | Expired invite accept | Accept after expiry returns error (`server/src/__tests__/invite-expiry.test.ts`) |
| TC-13 | Duplicate member invite accept | Accept for existing member is idempotent (`server/src/__tests__/invite-accept-existing-member.test.ts`) |

## Test Infrastructure

- Vitest suites under `server/src/__tests__/` and `server/src/services/`.
- Seeded companies, users, invites, and API keys as fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-7 |
| FR-03 | TC-4 |
| FR-04 | TC-3, TC-10, TC-11 |
| FR-05 | TC-1 |
| FR-06 | TC-8 |
| FR-07 | TC-2 |
| FR-09 | TC-9, TC-12, TC-13 |
| FR-10 | TC-9 |
| FR-11 | TC-2 |
| FR-12 | TC-4 |
| NFR-01 | TC-10 |
