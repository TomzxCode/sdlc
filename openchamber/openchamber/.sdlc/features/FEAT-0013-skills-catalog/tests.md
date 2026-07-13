---
title: "Skills Catalog"
status: done
---

# Test Plan: Skills Catalog

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Skills CRUD works | Skill data | Correct install/uninstall/config |
| TC-2 | NPM registry resolves packages | Package name | Correct registry metadata |

## Test Files

- `packages/web/server/lib/opencode/skills.test.js`
- `packages/web/server/lib/opencode/npm-registry.test.js`
- `packages/vscode/src/opencodeConfig.skills.test.js`
