---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

## Sync drift: 2026-11-16

- API Contracts (line 38) says "The gateway does not expose external HTTP APIs (except the API server adapter, which provides an OpenAI-compatible HTTP endpoint)" and that adapter-to-runner communication is "in-process method calls". Current code exposes several external listeners. `gateway/platforms/api_server.py:1-6` serves `/v1/chat/completions`, `/v1/responses`, `/v1/models`, `/v1/capabilities`, `/api/sessions`, `/v1/runs`, `/api/jobs`, `/health*` and `/p/<profile>/...`, most of which are not OpenAI-compatible endpoints. `gateway/webapp_listener.py:1-8` binds a gateway HTTP listener for the browser-hosted Webapp. `gateway/control_socket.py` answers a versioned JSON socket, and `gateway/platforms/webhook.py`, `msgraph_webhook.py`, `shared_ingress.py` and `tcp_site.py` are further HTTP/TCP servers. The gateway is not limited to a single in-process OpenAI-compatible surface.
- Out of Scope (line 82) says "Webhook adapter (for incoming webhooks from external services) is a separate tool". The webhook adapter is in-tree in the gateway: `gateway/platforms/webhook.py` is a full Generic webhook platform adapter (HMAC validation, prompt rendering, per-route rate limiting, idempotency), supported by `gateway/webhook_ingress.py`, `webhook_delivery.py`, `webhook_filters.py`, `webhook_coalesce.py`, `webhook_mcp_events.py` and `webhook_targets.py`, with `tests/hermes_cli/test_webhook_cli.py`. It is not a separate tool.
- Out of Scope (line 83) says "The gateway does not provide a web UI for configuration". `gateway/webapp_listener.py` serves a browser-hosted Webapp on the gateway's own HTTP listener, with configuration routers under `hermes_cli/web_routers/` (`config_env.py`, `profiles.py`, `messaging.py`, `models.py`, `mcp.py`, `tools.py`, and others). The gateway does provide a web UI that includes configuration.
