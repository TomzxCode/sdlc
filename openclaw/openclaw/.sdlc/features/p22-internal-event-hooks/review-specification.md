---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification for Internal Event Hooks

## Sync drift: 2026-11-16

The approach, data models, config contract, CLI contract, and RPC contract match the current code.

The implementation adds behavior that the specification does not describe.

- The Gmail setup sequence in `src/hooks/gmail-ops.ts` inspects the `gog` binary for token environment support and may run an automatic upgrade through `offerGogUpgrade`. The architecture diagram and sequences do not include `src/hooks/gmail-gog.ts` or this setup branch.
- The watch serve invocation can pass the push token and hook token through environment variables instead of command line arguments, selected by the `GmailTokenTransport` default of `env` in `src/hooks/gmail.ts`. The specification describes the shared token delivery but does not name this transport choice.
