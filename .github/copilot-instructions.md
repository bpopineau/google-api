# Copilot instructions (google-api)

## Big picture
- This repo is currently **design-first**: there’s no Python package yet; the authoritative requirements are in:
  - [AUTOMATION_GOALS.md](../AUTOMATION_GOALS.md) (workflows, v0.1 scope, API surface, I/O contracts)
  - [TODO.md](../TODO.md) (implementation checklist)
  - [LIBRARY_STRATEGY.md](../LIBRARY_STRATEGY.md) (background + patterns)

## Product intent (don’t fight it)
- Build a **personal-use** Python library that wraps Google Drive/Sheets/Docs/Calendar/Tasks/Gmail.
- Optimize for **ergonomic, stable, small surface area** (“~12 excellent functions”) over exhaustive coverage.
- Prefer **one-liner happy paths** for the v0.1 Must workflows: Drive folder sync, Sheets read/write, Gmail send/search.

## API shape & conventions (from `AUTOMATION_GOALS.md`)
- Return **plain Python types** by default (ids, strings, lists-of-lists, small summary dicts); avoid exposing raw Google response shapes as the primary API.
- Naming is **action-oriented**: `get_range`, `append_row`, `send_email`, `search_messages`, `mark_read`, `sync_folder`.
- Sheets:
  - Row/col helpers are **1-indexed**.
  - Range-oriented methods use **A1 notation** strings.
- Calendar/Tasks:
  - Accept Python `date`/`datetime` inputs without drama; define a sane default TZ for naive datetimes.
- Gmail:
  - `send_email(..., attachments=[...])` accepts file paths; hide MIME/base64 details.
- Provide a deliberate “raw escape hatch” for advanced use (e.g., `raw=True`), but keep it opt-in.

## Auth + clients
- Design for **auth once, reuse clients**: build service clients a single time and share credentials across services.
- Prefer a small factory (e.g., `client.create()` returning typed clients/wrappers) over scattering `build()` calls.

## Errors & diagnostics
- Raise **short, actionable exceptions**; avoid turning normal failures into huge google client stack traces.
- When wrapping `HttpError`, include the HTTP status and a brief hint (auth/scopes, missing file, permissions, quota).

## Secrets & local config
- Never commit `credentials.json` / `token.json` (treat as local secrets); keep paths configurable (env var or a local config file).
- Do not print tokens/secret material in logs or error messages.
