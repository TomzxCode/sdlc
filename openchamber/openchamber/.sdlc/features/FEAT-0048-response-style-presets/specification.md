---
title: "Response Style Presets"
status: done
---

# Specification: Response Style Presets

## Overview

Response style presets are configured in the session input area and sent as part of the prompt context to the AI model. The UI provides a dropdown selector integrated into the chat input controls.

## Architecture

```
Chat Input Controls
    +---> Preset selector dropdown
    |
Selected preset injected into prompt context
    (sent with each message to configure AI output style)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Injection | Prompt context (not system prompt) | Keeps system prompt reserved for agent instructions |
| Scope | Per-session | Different sessions may need different styles |

## Out of Scope

- Custom preset creation
- Preset sharing
- Preset marketplace
