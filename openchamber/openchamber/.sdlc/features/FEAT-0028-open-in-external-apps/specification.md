---
title: "Open In External Apps"
status: done
---

# Specification: "Open In" External Apps

## Overview

The "Open In" system uses `packages/ui/src/lib/openInApps.ts` for the app catalog and launch logic, `useOpenInAppsStore.ts` for preference management, and `OpenInAppButton.tsx` for the UI trigger.

## Architecture

```
OpenInAppButton (packages/ui/src/components/desktop/OpenInAppButton.tsx)
    |
    v
openInApps.ts (catalog of 23+ apps, install detection, launch logic)
    |
    v
useOpenInAppsStore.ts (preferred app selection)
    |
    v
Server (launch external process via child_process)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Detection | Check for binary existence on PATH | Simple and reliable for most desktop apps |
| Launch | Server-side child_process | Browser/webview cannot launch external processes |

## Out of Scope

- Custom app registration
- Per-file-type app association
