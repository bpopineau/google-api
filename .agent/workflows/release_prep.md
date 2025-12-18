---
description: Checklist for preparing a new version release
---

1. Update Version
   - Edit `pyproject.toml` and bump the version number.
   - Edit `mygooglib/__init__.py` if version is hardcoded there.

2. Update Changelog
   - Add a new entry to `CHANGELOG.md` summarizing changes.

3. Verify Health
// turbo
   - `python scripts/smoke_test.py all`

4. Format and Lint
// turbo
   - `ruff format .`
   - `ruff check . --fix`

5. Commit and Tag
   - `git add .`
   - `git commit -m "chore: release vX.Y.Z"`
   - `git tag vX.Y.Z`

6. (Optional) Build
   - `pip install build`
   - `python -m build`
