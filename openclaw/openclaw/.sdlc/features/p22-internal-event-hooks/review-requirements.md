---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: requirements for Internal Event Hooks

## Sync drift: 2026-11-16

No requirement was found that contradicts the current code.

One implemented behavior in the feature source paths is not represented in the requirements.

- The Gmail setup path now inspects the `gog` executable for token environment support and can offer an automatic `gog` upgrade through an interactive prompt. This behavior lives in `src/hooks/gmail-gog.ts` and the `offerGogUpgrade` step of `runGmailSetup` in `src/hooks/gmail-ops.ts`. FR-14 covers watcher provisioning and supervision, but it does not cover inspection or automatic upgrade of the `gog` dependency.

## Sync drift: 2026-11-23

Requirements match the current code for discovery roots, source precedence, descriptor metadata, handler precedence, enablement, eligibility, dispatch order, error isolation, event keys, reload generations, CLI verbs, install provenance, native relay bounds, and numeric NFR limits.
Evidence includes source precedence in `src/hooks/policy.ts:18`, family-before-exact dispatch with awaited handlers and error isolation in `src/hooks/internal-hooks.ts:87`, the 16 concurrent and 256 queued bounds with a 2000 ms timeout and 500 character log bound in `src/hooks/fire-and-forget.ts:10`, the handler candidate order in `src/hooks/discovery.ts:84`, the 1 MiB metadata cap in `src/hooks/discovery.ts:16`, the 1500 ms CLI report timeout in `src/cli/hooks-cli.ts:266`, the install state key in `src/hooks/installs.ts:21`, the Gmail bind retry limit in `src/hooks/gmail-watcher.ts:29`, and the 1 MiB relay stdin bound in `src/cli/native-hook-relay-cli.ts:15`.

The drift recorded on 2026-11-16 is still present on 2026-11-23.

- FR-14 does not cover gog inspection or automatic upgrade. `inspectGog` is defined at `src/hooks/gmail-gog.ts:104`, `inspectGogUpgrade` at `src/hooks/gmail-gog.ts:132`, and `offerGogUpgrade` at `src/hooks/gmail-ops.ts:74`.
- The setup path wires the upgrade into `runGmailSetup` at `src/hooks/gmail-ops.ts:112` and passes it as `prepareGog` at `src/hooks/gmail-ops.ts:377`.
- The watcher negotiates token transport at runtime. `src/hooks/gmail-watcher.ts:338` inspects gog and `src/hooks/gmail-watcher.ts:359` selects `env` only when token environment support is reported. FR-14 and NFR-5 do not describe this choice.
