---
title: "Changes Walkthrough"
status: done
---

# Specification: Changes Walkthrough

## Overview

The walkthrough subsystem (`packages/web/server/lib/walkthrough/`) parses a unified diff into stable hunks, builds a small-model digest, and asks the small model to group the hunks into an ordered, explained tour. The UI (`packages/ui/src/components/views/walkthrough/`) renders stops interleaved with code. Generation is user-initiated and results are cached by content hash.

## Architecture

```
User clicks "Generate" in WalkthroughView
    |
    v
POST /api/walkthrough/generate
    |
    v
walkthrough/index.js (orchestration)
    |
    +--> hunks.js        parse diff -> files/hunks, content-addressed ids
    +--> sources.js      diff source descriptor -> sections
    +--> generated.js    filter tool-produced files
    +--> digest.js       build model digest + alias/id mapping
    +--> prompt.js       system prompt + PROMPT_VERSION
    +--> schema.js       response schema + tolerant parsing
    +--> small-model     LLM call (feature model override or default)
    +--> store.js        content-addressed cache + mutable pointers
    |
    v
GET /api/walkthrough  (load cached/current), GET /api/walkthrough/progress,
POST /api/walkthrough/cancel
    |
    v
WalkthroughView.tsx + useWalkthroughStore.ts (stops interleaved with code)
```

## Data Models

### Hunk

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | `<scope>:<path>:<sha1(header + body)[:8]>`, with `-2`, `-3` suffix for byte-identical repeats within a file |
| scope | enum | staged \| working \| branch \| pr | Keeps staged and unstaged versions of the same lines apart |
| path | string | not null | File path |
| patch | string | not null | Patch body |

### Walkthrough

| Field | Type | Constraints | Description |
|---|---|---|---|
| stops | array | not null | Ordered groups of hunk ids with prose |
| chapters | array | optional | Chapter grouping over stops |
| source | enum | working-tree \| branch \| pr | Diff source kind |
| cacheKey | string | content-addressed | Deterministic cache identity |

## API Contracts

### POST /api/walkthrough/generate

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| source | object | yes | { kind: working-tree \| branch \| pr, ... } |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| id | string | Walkthrough id |
| status | string | queued / running / done / cancelled |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_SOURCE | Unknown diff source kind |
| 500 | GENERATION_FAILED | Small-model call failed |

### GET /api/walkthrough/progress

Returns generation progress percentage and current step for an in-flight walkthrough.

### POST /api/walkthrough/cancel

Cancels an in-progress generation.

### GET /api/walkthrough

Returns the walkthrough for the current session's diff (from cache or current generation).

## Sequences

### Generate a walkthrough

```
WalkthroughView --POST /generate--> index.js --diff source--> hunks.js
index.js --digest--> small-model --stops/chapters--> schema.js (normalize)
index.js --store.js--> cache --response--> WalkthroughView
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Hunk identity | Content-addressed hash in hunks.js only | Stale anchors become provable; edits invalidate only affected stops |
| Generation trigger | Explicit user action only | Token cost; no background/timed generation |
| Cache | Content-addressed store with mutable pointers | Cheap regenerations; safe invalidation |
| Model | Feature-level model override, defaulting to small model | Predictable quality and cost per request |
| PR support | Shared GitHub octokit helper | Reuses existing GitHub integration |

## Risks and Unknowns

1. Large diffs can exceed the small model's context; stop granularity guidance is heuristic.
2. Hunk-id scheme changes would silently mis-anchor existing cached stops.

## Out of Scope

- Automated/scheduled walkthrough generation
- Summarizing commits rather than diffs
