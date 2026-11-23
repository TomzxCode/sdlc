---
title: "Git Identities / Profiles"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Git Identities / Profiles

## Scope

This plan records the tests that exist for author profiles, per-repository identity selection, discovered Git identity data, and SSH credential handling.
The Gitmoji picker and its TTL cache are outside the recorded test coverage.
No browser or desktop end-to-end test drives the Git Identities settings page.

## Unit tests

| ID | Test file | Behavior covered |
|---|---|---|
| TC-1 | `packages/ui/src/stores/useGitIdentitiesStore.test.ts` | Profile create and update send only public author fields, rejected writes preserve the stored profile, global Git config becomes a selectable identity, and stale loads or writes cannot publish into a replaced runtime. |
| TC-2 | `packages/ui/src/lib/api/git-identity.test.ts` | The profile schema accepts known and unknown account provider ids and rejects a malformed provider id. |
| TC-3 | `packages/ui/src/lib/source-control/identity.test.ts` | The schema treats legacy profiles as System Git, accepts account and SSH transports, proposes an identity by remote host, filters selectable identities, and names them for display. |
| TC-4 | `packages/ui/src/lib/source-control/applyIdentity.test.ts` | Applying an identity validates instance scope, writes the account, transport, and signature, handles runtime switches and partial failures, and applies System Git as the absence of an override. |
| TC-5 | `packages/ui/src/lib/gitApiHttp.test.ts` | The public Git identity summary parser rejects transport configuration fields. |
| TC-6 | `packages/ui/src/components/views/git/gitAuthors.test.ts` | The Git view offers stored and global identities, deduplicates them by id, preserves signing data, resolves the active author, and derives a local author from name and email. |
| TC-7 | `packages/vscode/webview/api/git.test.ts` | The VS Code webview Git API keeps author profiles in memory for the view lifetime and rejects an update whose id does not match. |
| TC-8 | `packages/ui/src/lib/i18n/messages/git-identity-editor.i18n.test.ts` | Every locale carries the English keys used by the identity editor. |
| TC-9 | `packages/ui/src/components/session/useExistingRepositorySummary.test.ts` | The repository summary hook reports the current Git identity and keeps the other repository data when the author read fails. |

## Integration tests

| ID | Test file | Behavior covered |
|---|---|---|
| TC-10 | `packages/web/server/lib/git/routes.test.js` | Git HTTP routes project stored profiles to the public author DTO, reject legacy fields on create and update, apply the global or a stored author to a project, and omit SSH command data from identity summaries. |
| TC-11 | `packages/web/server/lib/git/service.test.js` | Tests against temporary Git repositories check global and local author resolution, commits with the machine author, and author writes that exclude transport configuration. |
| TC-12 | `packages/web/server/lib/git/credentials.test.js` | Tests with generated SSH keys check discovery, import, and binding of managed SSH credentials, including encrypted and malformed keys. |

## End-to-end tests

No end-to-end tests exist for this feature.

## Edge cases and failure scenarios

| ID | Scenario | Expected behavior |
|---|---|---|
| TC-13 | A stored or submitted profile carries a legacy `sshKey`, `authType`, or `host` field. | The client rejects the stored profile and the server returns 400 without creating or updating it. |
| TC-14 | A profile edit write fails. | The store returns false and keeps the previously stored public profile. |
| TC-15 | A profile load or apply finishes after a runtime switch. | The stale result is discarded and the replacement runtime state stays intact. |
| TC-16 | The machine has no Git author. | The store still creates a selectable System identity with empty author fields. |
| TC-17 | A repository author cannot be read. | The repository summary keeps its remaining data. |
| TC-18 | An SSH key is encrypted, has loose permissions, is behind a symlink, or changes fingerprint after discovery. | Discovery reports it safely, avoids recursion, and refuses to import or use a replaced key. |

## Test infrastructure

- `bun:test` runs the UI, store, schema, helper, and web route tests.
- Vitest runs the managed SSH credential tests.
- Express and Supertest exercise the Git HTTP routes.
- `happy-dom`, React `act`, and hook harnesses support the UI hook tests.
- Fetch spies and a configured runtime URL resolver isolate store and API tests.
- Temporary Git repositories and `ssh-keygen` fixtures support the server integration tests.

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-01 | TC-1, TC-2, TC-3, TC-6, TC-7, TC-11 |
| FR-02 | TC-4, TC-6, TC-10, TC-11, TC-9 |
| FR-03 | TC-1, TC-3, TC-9, TC-11, TC-12, TC-16, TC-17 |
| FR-04 | Gap: no test opens the Gitmoji picker or inserts a gitmoji into a commit message. |
| FR-05 | TC-2, TC-3, TC-4, TC-12, TC-13, TC-18 |
| FR-06 | Gap: no test covers `useGitmojiList` fetching or TTL cache reuse. |
| FR-07 | TC-1, TC-4, TC-6, TC-7, TC-10, TC-14, TC-15 |

## Gaps

No test renders `GitPage` or `GitIdentityEditorDialog` to verify profile creation and selection through the settings UI.
No test covers Gitmoji fetching, cache expiry, picker search, or picker insertion.
