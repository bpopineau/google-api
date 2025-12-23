# scripts

## Purpose
A collection of standalone utility scripts for development, maintenance, debugging, and scaffolding. These tools support the lifecycle of the project but are not part of the core library distributed to end-users.

## Key Entry Points
- [`smoke_test.py`](file:///c:/Users/brand/Projects/google-api/scripts/smoke_test.py): A comprehensive health check that verifies core functionality and API connectivity.
- [`oauth_setup.py`](file:///c:/Users/brand/Projects/google-api/scripts/oauth_setup.py): Helper script to generate valid `token.json` credentials for local development.
- [`generate_context_map.py`](file:///c:/Users/brand/Projects/google-api/scripts/generate_context_map.py): Auto-generates the `conductor/context_map.md` file by inspecting the codebase.

## Dependencies
- **Internal:** `mygooglib` (often imported to test or utilize core machinery)
