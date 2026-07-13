---
title: "Preview Browser"
status: done
---

# Test Plan: Preview Browser

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Proxy runtime handles HTML rewriting | HTML page with relative URLs | Correctly rewritten for proxy context |

## Test Files

- `packages/web/server/lib/preview/proxy-runtime.test.js`
