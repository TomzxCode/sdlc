---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: specification for Internal Event Hooks

## Sync drift: 2026-11-16

The approach, data models, config contract, CLI contract, and RPC contract match the current code.

The implementation adds behavior that the specification does not describe.

- The Gmail setup sequence in `src/hooks/gmail-ops.ts` inspects the `gog` binary for token environment support and may run an automatic upgrade through `offerGogUpgrade`. The architecture diagram and sequences do not include `src/hooks/gmail-gog.ts` or this setup branch.
- The watch serve invocation can pass the push token and hook token through environment variables instead of command line arguments, selected by the `GmailTokenTransport` default of `env` in `src/hooks/gmail.ts`. The specification describes the shared token delivery but does not name this transport choice.

## Sync drift: 2026-11-23

The architecture, data models, config contract, CLI contract, RPC contract, event catalog, dispatch sequence, and numeric bounds match the current code.
Evidence includes the five discovery roots in `src/hooks/workspace.ts:96`, source precedence in `src/hooks/policy.ts:18`, awaited family-before-exact dispatch in `src/hooks/internal-hooks.ts:87`, the hidden relay verb in `src/cli/hooks-cli.ts:570`, and the `nativeHook.invoke` call in `src/cli/native-hook-relay-cli.ts:169`.

The drift recorded on 2026-11-16 is still present on 2026-11-23.

- The architecture diagram and event sequence omit the gog inspection and upgrade path. `inspectGog` is at `src/hooks/gmail-gog.ts:104`, `inspectGogUpgrade` at `src/hooks/gmail-gog.ts:132`, and `offerGogUpgrade` at `src/hooks/gmail-ops.ts:74`.
- The setup path calls the upgrade at `src/hooks/gmail-ops.ts:112` and registers it as `prepareGog` at `src/hooks/gmail-ops.ts:377`.
- The watch serve token transport is negotiated rather than fixed. `GmailTokenTransport` is declared at `src/hooks/gmail.ts:31`, the argv and env flags are selected at `src/hooks/gmail.ts:235` and `src/hooks/gmail.ts:239`, and `src/hooks/gmail-watcher.ts:359` picks `env` only when gog reports support.
- The Gmail delivery decision at `specification.md:298` and the event sequence at `specification.md:234` do not name this transport choice.
