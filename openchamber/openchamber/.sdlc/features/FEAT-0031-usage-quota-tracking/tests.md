---
title: "Usage & Quota Tracking"
status: done
---

# Test Plan: Usage & Quota Tracking

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Quota formatters produce correct output | Raw quota data | Formatted display strings |
| TC-2 | Provider quota limits resolve correctly | Provider config | Correct quota window and limits |

## Test Files

- `packages/web/server/lib/quota/utils/formatters.test.js`
- `packages/web/server/lib/quota/providers/index.test.js`
- `packages/web/server/lib/quota/providers/codex.test.js`
- `packages/web/server/lib/quota/providers/ollama-cloud.test.js`
- `packages/web/server/lib/quota/providers/opencode-go.test.js`
- `packages/web/server/lib/quota/credentials/store.test.js`
- `packages/web/server/lib/quota/opencode-go-credentials.test.js`
- `packages/web/server/lib/quota/routes.test.js`
