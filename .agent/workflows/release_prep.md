---
description: Checklist for preparing a new mygooglib version release
---

1. Update Version
   - Edit `pyproject.toml` and bump the `version` field:
     ```toml
     version = "0.2.0"  # or appropriate semver bump
     ```
   - **Note**: Version is ONLY in `pyproject.toml` (not in `__init__.py`).

2. Update CHANGELOG.md
   - Add entry following existing format:
     ```markdown
     ## 0.2.0 — YYYY-MM-DD

     ### Added
     - [New features]

     ### Changed
     - [Modified behavior]

     ### Fixed
     - [Bug fixes]
     ```

3. Verify All Tests Pass
// turbo
   - `pytest`
   - `python scripts/smoke_test.py all`

4. Format and Lint
// turbo
   - `ruff format .`
   - `ruff check . --fix`

5. Verify Documentation
   - Check `README.md` Quick Start is accurate.
   - Check `docs/guides/usage.md` reflects new features.
   - Check `AUTOMATION_GOALS.md` priority order matches what's built.

6. Commit and Tag
   - `git add .`
   - `git commit -m "chore: release vX.Y.Z"`
   - `git tag vX.Y.Z`
   - `git push origin main --tags`

7. (Optional) Build Distribution
   - `pip install build`
   - `python -m build`
   - **Output**: Creates `dist/mygooglib-X.Y.Z-py3-none-any.whl`
