---
title: "DuckDB Mirror"
status: draft
---

# Specification: DuckDB Mirror

## Overview

The DuckDB integration mirrors SQLite data to DuckDB for portable analytics. It supports CGO-based and pure Go (modernc) DuckDB drivers. The Quack protocol exposes the DuckDB file over the network with token-based authentication. Read-only serve implements `db.Store` for DuckDB-backed queries.

## Architecture

```
SQLite DB → Push Engine (fingerprint diff) → DuckDB File
                                                  ↓
                                         Quack Server (remote protocol)
                                                  ↓
                                         Remote DuckDB Clients
```

## Data Models

### DuckDB Config

| Field | Type | Description |
|---|---|---|
| path | string | Path to DuckDB file |
| quack_bind | string | Quack server bind address |
| quack_token | string | Quack authentication token |

## Sequences

### Push
```
1. Query SQLite for sessions with fingerprint > last_push_fingerprint
2. Bulk insert into DuckDB using prepared statements
3. Record max fingerprint
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Driver | CGO + modernc (pure Go) fallback | Platform compatibility |
| Protocol | Quack | DuckDB-native remote protocol |
| Authentication | Bearer token | Simple, secure enough for local network |

## Risks and Unknowns

1. DuckDB driver compatibility across platforms
2. Quack protocol maturity and feature support
