---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

## Sync drift: 2026-11-16

### The Workboard schema version is 4, not 3

- Status: BLOCKING
- Evidence:
  - `extensions/workboard/src/workboard-schema.ts:1` exports `SCHEMA_VERSION = 4`.
  - `extensions/workboard/src/sqlite-store-schema.ts:51` and `extensions/workboard/database-port-api.ts:18-38` use that constant for migration ids and version checks.
- Artifact currently says: line 200 states that the plugin owns its own schema version with `SCHEMA_VERSION = 3`.
- What the code actually does: the plugin schema is at version 4 and rejects a database whose version is newer than 4.
- Needed change: correct the stated version to 4 and describe the migrations that bring a store to version 4.

### The Board widget declaration data model omits the queries field

- Status: BLOCKING
- Evidence:
  - `packages/gateway-protocol/src/schema/board.ts:94-111` defines `BoardWidgetDeclaredSchema` with `netOrigins`, `tools`, and `queries`, where `queries` holds at most 8 named live GitHub Actions data queries.
  - `src/boards/board-capabilities.ts:62-118` normalizes and grant-checks `queries` as a third capability category.
  - `api.yaml:929-944` also defines `BoardWidgetDeclared` with only `netOrigins` and `tools`.
- Artifact currently says: the Board widget declaration table at lines 127-132 lists only `netOrigins` and `tools`.
- What the code actually does: a declared capability set has three categories, and the `queries` category carries fixed selectors, result limits, response fields, and a renewed-approval rule.
- Needed change: add the `queries` field to the data model table and to the `BoardWidgetDeclared` schema in `api.yaml`.

### The Workboard taxonomy table omits nine exported constants

- Status: ADVISORY
- Evidence:
  - `packages/workboard-contract/src/index.ts:78-92` exports `WORKBOARD_OBSERVATION_OUTCOMES`, `WORKBOARD_VERIFICATION_OUTCOMES`, `WORKBOARD_DIAGNOSTIC_KINDS`, `WORKBOARD_DIAGNOSTIC_SEVERITIES`, `WORKBOARD_NOTIFICATION_KINDS`, and `WORKBOARD_BOARD_ID_PATTERN`.
  - The same file at lines 264, 291, and 326 exports `WORKBOARD_WORKER_STATES`, `WORKBOARD_DIAGNOSTIC_ACTION_KINDS`, and `WORKBOARD_CHANGED_EVENT`.
- Artifact currently says: the Workboard taxonomy table at lines 225-236 lists ten constants and presents itself as the shared vocabulary of the contract package.
- What the code actually does: the contract package exports nineteen constants, including diagnostic, notification, observation, verification, worker state, and changed-event vocabularies used by the plugin.
- Needed change: add the missing constants to the taxonomy table or state explicitly that the table is a partial list.

### The Workboard RPC surface is larger than the documented twelve methods

- Status: BLOCKING
- Evidence:
  - `extensions/workboard/src/gateway.ts:437-657` registers methods beyond the documented set, including `workboard.cards.create`, `workboard.cards.start`, `workboard.cards.linkDependency`, `workboard.cards.claim`, `workboard.cards.bulk`, `workboard.cards.diagnostics`, `workboard.cards.diagnostics.refresh`, `workboard.cards.specify`, `workboard.cards.decompose`, `workboard.cards.runs`, `workboard.cards.export`, `workboard.boards.archive`, `workboard.boards.delete`, five `workboard.notifications.*` methods, four `workboard.cards.attachments.*` methods, and `workboard.cards.dispatchWithOptions`.
  - `extensions/workboard/src/gateway.ts:325` also handles `workboard.cards.attachments.add`.
  - The API Contracts table at lines 274-285 and the paths in `api.yaml` describe only twelve Workboard methods.
- Artifact currently says: the Workboard plugin exposes the twelve methods listed in the specification and `api.yaml`.
- What the code actually does: the plugin registers roughly thirty-five RPC methods covering notifications, attachments, dependencies, diagnostics, specification and decomposition, and board lifecycle, in addition to the documented card and sessions-board methods.
- Needed change: extend the API Contracts table and `api.yaml` to cover the full registered method set, or state that the documented set is a representative subset.

### Workboard persistence supports a Postgres transport that the specification does not mention

- Status: ADVISORY
- Evidence:
  - `extensions/workboard/src/workboard-postgres-schema.ts` defines the Postgres schema, and `extensions/workboard/src/workboard-schema.postgres.sql` holds the SQL.
  - `extensions/workboard/src/store-engine-schema.ts:13-19` selects a Postgres schema and migration set by engine name.
  - `extensions/workboard/src/sqlite-store-kernel.ts:721-723` and `extensions/workboard/src/sqlite-store-schema.ts:96-126` accept a `postgresInput` and create a database through that path.
  - Runtime and test files such as `extensions/workboard/src/postgres-store.test.ts` and `extensions/workboard/src/sqlite-store.transport.postgres.test.ts` exercise the Postgres transport.
- Artifact currently says: the Overview at line 16 and the Technical Decisions at line 407 describe Workboard persistence as its own SQLite file, with no other transport.
- What the code actually does: the store can run against a Postgres engine as well as SQLite, with engine-specific schema and migration handling.
- Needed change: document the Postgres transport, when it is selected, and how it relates to the plugin state directory SQLite file.
