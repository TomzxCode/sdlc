---
title: "Attachments & Work Products"
status: done
---

# Requirements: Attachments & Work Products

## Overview

Attachments allow agents and board operators to upload files to issues and comments. Work products are typed deliverables attached to issues, either backed by an artifact file or referencing a workspace file. The attachment system handles upload, storage (local disk or S3), inline serving, download, range requests for video content, and deletion.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Upload, view, download, and delete attachments on issues |
| Agent | Upload work products (artifacts, reports) and reference workspace files |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support file uploads to issues and comments with an upload allowlist and per-company size limits. |
| FR-02 | Must | The system shall support inline content serving with content-type negotiation. |
| FR-03 | Must | The system shall support file downloads via a dedicated download endpoint. |
| FR-04 | Must | The system shall support byte-range requests for video files (HTTP 206 Partial Content). |
| FR-05 | Must | The system shall support attachment deletion. |
| FR-06 | Should | The system shall support work products of type `artifact` (with attachment) and `workspace_file` (file reference). |
| FR-07 | Should | The system shall support multiple storage providers: local disk and S3-compatible object storage. |
| FR-08 | Should | The system shall scan uploads for security threats (malware scanning). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Uploads must be validated against the allowlist and size limits before storage. |
| NFR-02 | Should | Performance | Video range requests should support streaming without loading the entire file into memory. |

## Constraints

- Per-company `attachment_max_bytes` limits total attachment size.
- Storage provisioning is configured per deployment (local disk default, S3 optional).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a valid file type within size limits
    - **When** uploaded to an issue
    - **Then** the file is stored and an attachment record is created
- [ ] **FR-02**
    - **Given** an image attachment
    - **When** the inline content URL is requested
    - **Then** the image is served with the correct content type
- [ ] **FR-04**
    - **Given** a video attachment
    - **When** a byte range is requested
    - **Then** the server responds 206 with Content-Range and Accept-Ranges: bytes
- [ ] **NFR-01**
    - **Given** a disallowed file type or oversized file
    - **When** upload is attempted
    - **Then** the request is rejected with a descriptive error

## Conflicts

None identified yet.

## Open Questions

1. What is the full allowlist of supported file types for V1?
2. Should uploaded files be scanned for malware before storage?
