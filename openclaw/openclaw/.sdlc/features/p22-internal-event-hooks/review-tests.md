---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: test plan for Internal Event Hooks

## Sync drift: 2026-11-16

The test plan lists four test files that no longer exist under the documented paths.

- TC-9 lists `src/hooks/import-url.test.ts`. The file was renamed to `src/hooks/loader.cache-invalidation.test.ts`. The coverage of same-size edits with a restored mtime and the missing-file fallback to `Date.now()` is still present.
- TC-21 lists `src/hooks/llm-slug-generator.test.ts`. The file was renamed to `src/hooks/bundled/session-memory/handler.slug.test.ts`. The four documented behaviors are still covered.
- TC-24 lists `src/hooks/install-policy-warning.test.ts`. No hook-level file with that name exists. The acknowledgement option coverage now lives in `src/cli/install-policy-warning-acknowledgement.test.ts`, and the two-stage scan behavior is covered in `src/hooks/install.test.ts` and `src/hooks/hooks-install.test.ts`.
- TC-27 lists `src/hooks/plugin-hooks.test.ts`. The file does not exist. Its cases were folded into `src/hooks/loader.test.ts` under the bundle plugin hooks block, including published inventory reuse through policy commits and the Claude `hooks.json` case, with a related case in `src/hooks/install.test.ts`.

The test plan does not document several test files that exist in the feature source paths.

- `src/hooks/gmail-gog.test.ts` covers gog binary inspection and the automatic upgrade path.
- `src/hooks/install-npm.test.ts` covers installing a hook pack from an npm spec.
- `src/hooks/loader.imports.test.ts` covers keeping workspace discovery cold when internal hooks are unconfigured.
- `src/cli/plugins-install-hook-fallback.test.ts` covers the plugin installer fallback for hook packs.

The coverage matrix still references TC-9, TC-21, TC-24, and TC-27, so it should be updated when the file paths are reconciled.

## Sync drift: 2026-11-23

The drift recorded on 2026-11-16 is still present on 2026-11-23.

Four paths in the unit test table no longer exist in the checkout.

- TC-9 at `tests.md:27` lists `src/hooks/import-url.test.ts`. The replacement `src/hooks/loader.cache-invalidation.test.ts` still covers the same-size edit with restored mtime at line 63.
- TC-21 at `tests.md:39` lists `src/hooks/llm-slug-generator.test.ts`. The replacement `src/hooks/bundled/session-memory/handler.slug.test.ts` exists.
- TC-24 at `tests.md:42` lists `src/hooks/install-policy-warning.test.ts`. The acknowledgement coverage now lives in `src/cli/install-policy-warning-acknowledgement.test.ts`.
- TC-27 at `tests.md:45` lists `src/hooks/plugin-hooks.test.ts`. The bundle cases now live in `src/hooks/loader.test.ts:370`.

Four existing test files are absent from the test plan.

- `src/hooks/gmail-gog.test.ts` covers gog inspection and upgrade.
- `src/hooks/install-npm.test.ts` covers npm spec installs.
- `src/hooks/loader.imports.test.ts` covers cold workspace discovery when internal hooks are unconfigured.
- `src/cli/plugins-install-hook-fallback.test.ts` covers the plugin installer fallback.

The coverage matrix at `tests.md:121` still references TC-9, TC-21, TC-24, and TC-27.
