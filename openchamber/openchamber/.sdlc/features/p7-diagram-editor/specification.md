---
title: "Diagram Editor"
status: done
---

# Specification: Diagram Editor

## Overview

The diagram editor is a shared UI component (`packages/ui/src/components/diagram/DiagramEditor.tsx`) wrapping the `react-drawio` embedded DrawIO editor. The Diagram View (`packages/ui/src/components/views/DiagramView.tsx`) loads a diagram file's XML through the files runtime API, hosts the editor, and writes the serialized XML back on save.

## Architecture

```
FilesView / session action -> pendingDiagramFile (useUIStore)
    |
    v
DiagramView.tsx
    |   files.readText(path) -> xml
    v
DiagramEditor.tsx (react-drawio embed, blank template, dark detection, ref handle getXml)
    |   onChange(xml) / onSave
    v
files.writeText(path, xml)
```

## Data Models

### Diagram document

| Field | Type | Constraints | Description |
|---|---|---|---|
| xml | string | mxGraph XML | `mxfile`/`mxGraphModel` document |
| path | string | not null | File path on the server |
| readOnly | boolean | — | Disables editing when true |

## API Contracts

The feature uses the existing shared files runtime API (`files.readText`, `files.writeText`) and the pending-diagram-file signal in `useUIStore`. No dedicated backend endpoints are introduced.

## Sequences

### Open and edit a diagram

```
User selects diagram file -> pendingDiagramFile set -> DiagramView mounts
DiagramView reads xml via files.readText -> DiagramEditor loads XML
User edits canvas -> editor emits updated xml -> user saves -> files.writeText
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Editor engine | react-drawio (DrawIO iframe) | Full-featured diagram canvas without a custom renderer |
| Format | mxGraph XML | Native DrawIO format, interoperable with external tools |
| Save | Serialize via editor ref handle on demand | View controls when to write; avoids autosave surprises |
| Theme | data-theme attribute / prefers-color-scheme detection | Editor matches app appearance without a settings surface |

## Risks and Unknowns

1. The embedded DrawIO iframe is a third-party bundle; offline or CSP environments may need allowances.
2. Blank-template XML is a minimal valid document; richer templates could be added later.

## Out of Scope

- Diagram rendering of Mermaid or other non-DrawIO formats
- Collaborative/real-time diagram editing
