---
description: Perform a full clean, upgrade, and verification cycle for mygooglib
---

1. Update Dependencies
// turbo
   - `uv lock --upgrade`
   - `uv sync`
   - **Goal**: Get latest versions of google-api-python-client, google-auth, etc.

2. Deep Clean
// turbo
   - `/clean_reset`
   - **Goal**: Remove stale `__pycache__`, `.egg-info`, etc.

3. Reinstall
// turbo
   - `pip install -e ".[dev,cli]"`

4. Verify Everything
// turbo
   - `/ci_local`
   - **Must pass**: Linting, tests, smoke tests, CLI.

5. Synchronize Documentation
// turbo
   - `/update_docs`
   - **Check**: Do examples still run with upgraded dependencies?

6. Update Roadmap (if applicable)
   - If dependencies enable new features, update `docs/development/roadmap.md`.
   - Consider adding new feature ideas from `AUTOMATION_GOALS.md` Section 6.
