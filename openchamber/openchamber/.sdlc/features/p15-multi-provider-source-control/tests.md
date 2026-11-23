---
title: "Multi-provider source control"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Multi-provider source control

## Scope

Automated coverage for the provider-neutral registry, descriptors, route shell, bindings, auth stores, status cache, mutation executor, built-in provider modules, UI descriptor handling, source board repository, and web API adapter is included.
Tests for the OpenCode server, changelog generation, and end-to-end browser flows are out of scope.
Test file paths below are repository relative.

## Unit Tests

| ID | Description | Test file(s) | Input | Expected Output |
|---|---|---|---|---|
| TC-1 | Provider ID and descriptor validation | `packages/web/server/lib/source-control/provider-id.test.js`<br>`packages/web/server/lib/source-control/provider-descriptors.test.js`<br>`packages/web/server/lib/source-control/provider-registry.test.js`<br>`packages/web/server/lib/source-control/provider-publication-freeze.test.js`<br>`packages/web/server/lib/source-control/provider-open-ids.test.js`<br>`packages/web/server/lib/source-control/provider-instance.test.js`<br>`packages/web/server/lib/source-control/repository-identity.test.js`<br>`packages/web/server/lib/source-control/repository-network.test.js` | IDs, descriptors, registry operations, and public descriptor snapshots | Valid IDs register, invalid IDs fail, built-ins keep order, and public fields stay stable |
| TC-2 | Extension provider contracts | `packages/web/server/lib/source-control/extension-descriptor.test.js`<br>`packages/web/server/lib/source-control/extension-provider.contract.test.js`<br>`packages/web/server/lib/source-control/extension-provider.test.js` | Extension descriptors, guest metadata, and implementation factories | Extension IDs use `ext-` prefix and contracts validate before registration |
| TC-3 | Auth and account storage | `packages/web/server/lib/source-control/auth-storage.test.js`<br>`packages/web/server/lib/source-control/pat-account-auth.test.js`<br>`packages/web/server/lib/source-control/oauth-flow-registry.test.js`<br>`packages/web/server/lib/source-control/audit-storage.test.js`<br>`packages/web/server/lib/source-control/instance-aliases.test.js` | Tokens, PAT accounts, device flows, audit records, and aliases | Secrets are stored in provider auth state, flows are bounded, and aliases round-trip |
| TC-4 | Binding and file state | `packages/web/server/lib/source-control/binding-storage.test.js`<br>`packages/web/server/lib/source-control/binding-contract.test.js`<br>`packages/web/server/lib/source-control/repository-id-storage.test.js`<br>`packages/web/server/lib/source-control/file-lock.test.js`<br>`packages/web/server/lib/source-control/outbound-handles.test.js` | Binding records, repository ids, lock contention, and handle records | Redacted bindings persist, locks are reclaimed only when safe, and handles close cleanly |
| TC-5 | Status cache and parsing helpers | `packages/web/server/lib/source-control/status-cache.test.js`<br>`packages/web/server/lib/source-control/change-id.test.js`<br>`packages/web/server/lib/source-control/review-position.test.js`<br>`packages/web/server/lib/source-control/project-path.test.js` | Cache contexts, Change-Id values, review positions, and project paths | Cache keys include revisions, parsing is strict, and path styles resolve correctly |
| TC-6 | Mutation contracts and replay | `packages/web/server/lib/source-control/standard-mutations.test.js`<br>`packages/web/server/lib/source-control/mutation-executor.test.js`<br>`packages/web/server/lib/source-control/mutation-storage.test.js`<br>`packages/web/server/lib/source-control/mutation-digest-freeze.test.js` | Mutation bodies, replay records, digests, and completion states | Supported routes prepare and reconcile mutations, and conflicting replay fails |
| TC-7 | GitHub provider modules | `packages/web/server/lib/github/merge-follow.test.js`<br>`packages/web/server/lib/github/reference-search.test.js`<br>`packages/web/server/lib/github/gh-cli-logins.test.js`<br>`packages/web/server/lib/github/resources.test.js`<br>`packages/web/server/lib/github/device-flow.test.js`<br>`packages/web/server/lib/github/gh-cli-credential.test.js`<br>`packages/web/server/lib/github/merge-when-ready.test.js`<br>`packages/web/server/lib/github/review-draft.test.js`<br>`packages/web/server/lib/github/pr-status.test.js`<br>`packages/web/server/lib/github/auth.test.js`<br>`packages/web/server/lib/github/octokit.test.js`<br>`packages/web/server/lib/github/pr-summaries.test.js`<br>`packages/web/server/lib/github/mappers.test.js`<br>`packages/web/server/lib/github/pr-status-host-scope.test.js`<br>`packages/web/server/lib/github/media.test.js`<br>`packages/web/server/lib/github/change-request-patch.test.js`<br>`packages/web/server/lib/github/rate-limit.test.js`<br>`packages/web/server/lib/github/provider.test.js`<br>`packages/web/server/lib/github/host-trust.test.js`<br>`packages/web/server/lib/github/repo/index.test.js` | GitHub fixtures, API responses, CLI credentials, and auth flows | GitHub implementation satisfies registry contracts and maps upstream data correctly |
| TC-8 | GitLab provider modules | `packages/web/server/lib/gitlab/resources.test.js`<br>`packages/web/server/lib/gitlab/device-flow.test.js`<br>`packages/web/server/lib/gitlab/instance.test.js`<br>`packages/web/server/lib/gitlab/verify.test.js`<br>`packages/web/server/lib/gitlab/glab-credential.test.js`<br>`packages/web/server/lib/gitlab/mappers.test.js`<br>`packages/web/server/lib/gitlab/client.test.js`<br>`packages/web/server/lib/gitlab/repo.test.js` | GitLab fixtures, instance URLs, device flow responses, and MR data | GitLab instance handling, auth, and reads match provider contract expectations |
| TC-9 | Gitea provider modules | `packages/web/server/lib/gitea/fixtures/fake-fetch.test.js`<br>`packages/web/server/lib/gitea/resources.test.js`<br>`packages/web/server/lib/gitea/verify.test.js`<br>`packages/web/server/lib/gitea/mappers.test.js`<br>`packages/web/server/lib/gitea/client.test.js`<br>`packages/web/server/lib/gitea/gt-cli.test.js`<br>`packages/web/server/lib/gitea/provider.test.js`<br>`packages/web/server/lib/gitea/repo.test.js` | Fake fetch routes, Gitea server responses, and `gt` CLI output | Gitea verification, namespacing, auth, and provider behavior stay stable |
| TC-10 | Gerrit provider modules | `packages/web/server/lib/gerrit/fixtures/fake-fetch.test.js`<br>`packages/web/server/lib/gerrit/resources.test.js`<br>`packages/web/server/lib/gerrit/local-revision.test.js`<br>`packages/web/server/lib/gerrit/verify.test.js`<br>`packages/web/server/lib/gerrit/mappers.test.js`<br>`packages/web/server/lib/gerrit/client.test.js`<br>`packages/web/server/lib/gerrit/provider.test.js`<br>`packages/web/server/lib/gerrit/repo.test.js` | Gerrit change fixtures, votes, revisions, submit requirements, and fetch routes | Change-based reads, local revision detection, and verification follow Gerrit semantics |
| TC-11 | Forgejo provider module | `packages/web/server/lib/forgejo/provider.test.js` | Gitea hosts, older Forgejo versions, Codeberg, and branch status fixtures | Forgejo separates from Gitea, reports its own errors, and stays last among built-ins |
| TC-12 | UI descriptor and registry helpers | `packages/ui/src/lib/source-control/providers/descriptor.test.ts`<br>`packages/ui/src/lib/source-control/providers/zeroCodeProvider.test.tsx`<br>`packages/ui/src/lib/source-control/providers/registry.test.ts`<br>`packages/ui/src/lib/source-control/providers/terminology.test.ts`<br>`packages/ui/src/lib/source-control/providers/urlMatchers.test.ts`<br>`packages/ui/src/lib/source-control/projectPath.test.ts`<br>`packages/ui/src/lib/source-control/identity.test.ts`<br>`packages/ui/src/lib/source-control/applyIdentity.test.ts`<br>`packages/ui/src/lib/source-control/repositoryLinks.test.ts`<br>`packages/ui/src/lib/source-control/repositoryUrl.test.ts`<br>`packages/ui/src/lib/source-control/repositoryProviderMemory.test.ts`<br>`packages/ui/src/lib/source-control/repositoryFilterMemory.test.ts`<br>`packages/ui/src/lib/source-control/repository-binding.test.ts`<br>`packages/ui/src/lib/source-control/issueReference.test.ts`<br>`packages/ui/src/lib/source-control/changeRequestReference.test.ts`<br>`packages/ui/src/lib/source-control/prVisualState.test.ts`<br>`packages/ui/src/lib/source-control/git-operation-recovery.test.ts`<br>`packages/ui/src/lib/source-control/changeRequestCopy.test.ts` | Descriptor schemas, remembered lists, identity objects, links, references, and binding inputs | UI validation and rendering helpers follow descriptor rules and stay stable across providers |
| TC-13 | Source board repository unit logic | `packages/ui/src/components/sourceBoard/boardRepository.test.ts`<br>`packages/ui/src/components/sourceBoard/updateItemText.test.ts`<br>`packages/ui/src/components/sourceBoard/updateItemComment.test.ts`<br>`packages/ui/src/components/sourceBoard/openTrackerItem.test.ts` | Repository ids, provider identities, item text, comments, and tracker links | Board repository resolves providers and updates item content without losing identity |
| TC-14 | Web adapter unit behavior | `packages/web/src/api/source-control-providers.test.ts`<br>`packages/web/src/api/source-control.change-review.test.ts`<br>`packages/web/src/api/source-control.test.ts` | Adapter methods, mocked responses, older-server responses, and malformed payloads | Adapter validates descriptors, normalizes instances, and preserves provider-specific fields |

## Integration Tests

| ID | Description | Test file(s) | Preconditions | Expected Outcome |
|---|---|---|---|---|
| TC-15 | Generic source control shell | `packages/web/server/lib/source-control/routes.test.js` | Express app with source control routes mounted | Provider list, instances, repository context, binding, aliases, and auxiliary endpoints answer with validated data |
| TC-16 | Capability route | `packages/web/server/lib/source-control/provider-routes.capabilities.test.js` | Provider descriptors and implementations registered | Capabilities response merges descriptor flags with dynamic auth capabilities |
| TC-17 | GitHub provider routes | `packages/web/server/lib/source-control/provider-routes.github.test.js`<br>`packages/web/server/lib/source-control/provider-routes.github.auth.test.js`<br>`packages/web/server/lib/source-control/provider-routes.github.aliases.test.js`<br>`packages/web/server/lib/source-control/provider-routes.github.mutations.test.js` | GitHub routes, auth stores, aliases, and mutation executor mounted | Bound reads, auth routes, legacy aliases, and mutations return GitHub results |
| TC-18 | GitLab provider routes | `packages/web/server/lib/source-control/provider-routes.gitlab.test.js` | GitLab descriptor and implementation registered | GitLab instance reads, merge request reads, and errors use GitLab behavior |
| TC-19 | Gerrit provider routes | `packages/web/server/lib/source-control/provider-routes.gerrit.test.js` | Gerrit descriptor and implementation registered | Gerrit appears last among built-ins and answers capability and account routes |
| TC-20 | Extension provider routes | `packages/web/server/lib/source-control/provider-routes.extensions.test.js` | Extension descriptor attached and router mounted | Extension routes answer under the ext prefix and unmount cleanly |
| TC-21 | Provider implementation route behavior | `packages/web/server/lib/gitea/provider.test.js`<br>`packages/web/server/lib/gerrit/provider.test.js`<br>`packages/web/server/lib/forgejo/provider.test.js` | Provider implementations with fixture fetch clients | Providers answer through the same resource and auth methods used by the route shell |
| TC-22 | Binding service integration | `packages/web/server/lib/source-control/binding-service.test.js` | Local repository with binding and alias stores | Provider, transport, and auxiliary bindings resolve and clear through one service |
| TC-23 | Source board component integration | `packages/ui/src/components/sourceBoard/boardRepository.hooks.test.tsx`<br>`packages/ui/src/components/sourceBoard/SourceBoardPickers.test.tsx`<br>`packages/ui/src/components/sourceBoard/SourceBoardReview.test.tsx`<br>`packages/ui/src/components/sourceBoard/SourceBoardReviewers.test.tsx`<br>`packages/ui/src/components/sourceBoard/SourceBoardDraftMenu.test.tsx`<br>`packages/ui/src/components/sourceBoard/SourceBoardTrackerStatus.characterization.test.tsx` | Mocked source control API and board state | Pickers, review views, draft menus, and status rows keep provider identity and terminology |

## End-to-End Tests

No dedicated Playwright or Cypress spec files matching source control were found under `packages/**`.
Route shell, web adapter, and component integration tests are the highest-level automated checks for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-24 | Invalid, reserved, duplicate, or shell-name provider IDs | Registration fails with an invalid provider id error |
| TC-25 | Descriptor capability combinations that conflict | Descriptor validation rejects unsupported merge and discussion combinations |
| TC-26 | Extension attach and detach | Extension list is sorted and the router is removed on detach |
| TC-27 | Older server without the provider route | Web adapter returns GitHub and GitLab built-ins only |
| TC-28 | Malformed provider list response | Web adapter fails validation and never returns an empty list |
| TC-29 | Provider refresh fails with a remembered list | UI status becomes stale and keeps the old list |
| TC-30 | Provider refresh fails on first load | UI status becomes error and retry delay grows with failures |
| TC-31 | Unknown provider id in UI state | UI uses its unknown provider descriptor |
| TC-32 | Unsupported capability or mutation | Route returns 501 with SOURCE_CONTROL_CAPABILITY_UNSUPPORTED |
| TC-33 | Missing directory, project, number, token, or upload parameters | Route returns 400 with a concrete error message |
| TC-34 | Invalid provider token | Route returns 401 with INVALID_TOKEN |
| TC-35 | Busy or unavailable device flow | Route returns 409 or 410 with the matching flow code |
| TC-36 | Retired legacy auth path or `/me` route | Route returns 410 with SOURCE_CONTROL_CONTEXT_REQUIRED |
| TC-37 | Conflicting idempotency key reuse | Route returns 409 with SOURCE_CONTROL_MUTATION_CONFLICT |
| TC-38 | Upstream lookup failures | Route returns 500, 502, or 503 based on failure kind and never returns an authoritative empty result |
| TC-39 | Credential or account invalidation | Status cache entries for that identity are cleared |
| TC-40 | Force refresh on a cached status read | Route calls the provider again and stores a fresh result |
| TC-41 | Multiple connected accounts | Active account selection changes the session used by later reads |
| TC-42 | Top-level and nested project paths | Path style, link templates, and thread keys follow the descriptor |
| TC-43 | Forgejo version and host confusion | Older Forgejo versions are rejected and Gitea hosts route to Gitea |
| TC-44 | Lock contention, dead process, and partial lock initialization | File lock waits or reclaims only under the documented guard and clears partial state |
| TC-45 | Redaction of tokens and sensitive errors | Bindings and logs contain references and redacted metadata only |

## Test Infrastructure

- Bun test runner with `packages/ui/src/test/preload.ts` loaded through `bunfig.toml`.
- Express route tests mount the source control routers with injected services.
- Gitea and Gerrit fake-fetch fixtures replay recorded upstream responses and refusals.
- zod schemas from `@openchamber/sdk` and the UI provider descriptor module validate public data.
- No persistent database is required; tests use temporary JSON stores and in-memory registries.
- Time-based tests cover the 90 second status cache, 12 second timeout, retry delay, and credential revisions.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-11, TC-16, TC-19 |
| FR-2 | TC-1, TC-2, TC-24 |
| FR-3 | TC-1, TC-15, TC-14 |
| FR-4 | TC-1, TC-12, TC-14, TC-23 |
| FR-5 | TC-12, TC-29, TC-30, TC-31 |
| FR-6 | TC-1, TC-2, TC-16, TC-20 |
| FR-7 | TC-3, TC-16, TC-17, TC-18, TC-19, TC-20, TC-21 |
| FR-8 | TC-5, TC-15, TC-17, TC-18, TC-19, TC-21, TC-32, TC-33, TC-38 |
| FR-9 | TC-6, TC-17, TC-20, TC-36, TC-37 |
| FR-10 | TC-2, TC-16, TC-21, TC-32 |
| FR-11 | TC-3, TC-4, TC-45 |
| FR-12 | TC-4, TC-13, TC-15, TC-22 |
| FR-13 | TC-1, TC-3, TC-15, TC-22 |
| FR-14 | TC-14, TC-27, TC-28 |
| FR-15 | TC-13, TC-23 |
| FR-16 | TC-2, TC-20, TC-26 |
| FR-17 | TC-3, TC-17, TC-41 |
| FR-18 | TC-5, TC-17, TC-39, TC-40 |
| FR-19 | TC-5, TC-12, TC-42 |
| FR-20 | TC-12, TC-14, TC-23 |
| FR-21 | TC-3, TC-17 |
| FR-22 | TC-3, TC-17, TC-33 |
| NFR-1 | TC-3, TC-4, TC-45 |
| NFR-2 | TC-8, TC-10, TC-38 |
| NFR-3 | TC-14, TC-27, TC-28 |
| NFR-4 | TC-1, TC-5, TC-40 |
| NFR-5 | TC-1, TC-19, TC-38 |
| NFR-6 | TC-6, TC-37 |
