---
title: "Attachments & Work Products"
status: draft
---

# Specification: Attachments & Work Products

## Overview

Attachments are stored as `assets` records with provider routing (local disk or S3). Uploads go through allowlist and size validation. Inline serving respects content negotiation; download forces attachment disposition. Byte-range requests are handled for video playback. Work products link typed deliverables (artifact or workspace_file) to issues.

## Architecture

```
Upload: POST /.../attachments (multipart) → asset validation → storage provider → assets table
Serve:  GET /attachments/:id/content → provider read → stream to client (content-type, range)
Work product: POST /issues/:id/work-products → type=artifact|workspace_file → issue_work_products
```

## Data Models

### assets

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| file_name | text | not null | Original filename |
| content_type | text | not null | MIME type |
| byte_size | int | not null | File size |
| storage_provider | text | not null | `local_disk | s3` |
| storage_key | text | not null | Provider-specific key |
| uploaded_by_actor_type | text | not null | `agent | user` |
| uploaded_by_actor_id | uuid | not null | Who uploaded |
| created_at | timestamptz | not null | Upload timestamp |

### issue_attachments

| Field | Type | Constraints | Description |
|---|---|---|---|
| issue_id | uuid | FK, PK | Issue |
| asset_id | uuid | FK, PK | Asset |
| comment_id | uuid | FK, null | Optional comment link |

### issue_work_products

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| issue_id | uuid | FK, not null | Parent issue |
| type | enum | not null | `artifact | workspace_file` |
| asset_id | uuid | FK, null | For artifact type |
| file_path | text | null | For workspace_file type |
| title | text | not null | Display title |

## API Contracts

### POST /companies/:companyId/issues/:issueId/attachments

Upload attachment to issue.

### GET /attachments/:attachmentId/content

Inline content serving. Supports `Range` header for video.

### DELETE /attachments/:attachmentId

Delete attachment.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Disallowed file type or exceeds size limit |
| 404 | NOT_FOUND | Attachment not found |
| 403 | UNAUTHORIZED | Caller lacks company access |

## Sequences

### Upload and serve

```
Agent → POST attachment (multipart) → validate allowlist + size → store via provider → assets + issue_attachments → return asset id
Board → GET /attachments/:id/content (with Range) → provider read → 206/200 with content-type
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage abstraction | Provider pattern (local_disk, s3) | Extensible; local is free, S3 for production |
| Content serving | Direct from server | Simple V1; CDN offload deferred |
| Work products | Separate table from attachments | Different metadata for artifact vs workspace file |

## Risks and Unknowns

1. Very large file uploads may need streaming/chunked upload support.
2. Malware scanning integration is not implemented; local disk storage means malware could be served.

## Out of Scope

- CDN offload for attachment serving (deferred)
- Image thumbnail/resize generation (deferred)
- Drag-and-drop file organization in the UI
