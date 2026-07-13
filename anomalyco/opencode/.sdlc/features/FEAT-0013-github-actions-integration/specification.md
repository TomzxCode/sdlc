---
title: "GitHub Actions Integration"
status: done
---

# Specification: GitHub Actions Integration

## Architecture

```
GitHub Workflow ──uses: anomalyco/opencode──▶ github/action.yml (composite action)
                                                    │
                                                    ▼
                                            install script -> opencode CLI
                                                    │
                                                    ▼
                                        headless run / PR analysis / code review
                                                    │
                                                    ▼
                                        Check runs, PR comments, workflow artifacts
```

The action is a composite action that wraps the install script and CLI, exposing inputs for common use cases.

## Data Models

No durable models; the action is stateless per invocation.

## API Contracts

### GitHub Action Inputs

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| directory | string | no | `.` | Working directory |
| prompt | string | yes | — | Prompt to execute |
| agent | string | no | `build` | Agent to use |
| model | string | no | — | Model override |
| github-token | string | no | `${{ github.token }}` | GitHub token for API access |

## Sequences

### PR analysis workflow

```
pull_request opened
workflow triggers -> checkout repository
action: anomalyco/opencode -> install opencode
opencode run "analyze this PR diff" -> model analysis
action outputs results -> PR check run + comment
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Action type | Composite | No build step; runs the install script directly |
| Secret handling | GitHub secrets via action inputs | Standard GitHub Actions pattern |
| Output | Check runs and PR comments | Visible in the PR review UI |

## Risks and Unknowns

1. Long-running actions may hit GitHub's 6-hour workflow timeout for complex analyses.
2. Cost of LLM API calls from CI must be managed by the workflow author.

## Out of Scope

- Interactive session support (see FEAT-0001).
- Scheduled/periodic analysis (GitHub cron workflows handle this).
