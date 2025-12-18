---
description: Checklist for preparing a new mygooglib version release
---

# /release_prep

**Goal**: Ship software without shipping bugs.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve` (Phase 6), ensure `task.md` item "Release Prep" is `[/]`.
- **CRITICAL**: This workflow has a **POINT OF NO RETURN** at Step 6.

---

1. Pass All Tests (The First Filter)
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**:
     - **IF PASS**: Proceed.
     - **IF FAIL**: STOP IMMEDIATELY. Fix code. Recurse.

2. Update Version
   - Edit `pyproject.toml`.
   - **Verification**: `grep version pyproject.toml` matches intent.

3. Update CHANGELOG.md
   - Add header: `## X.Y.Z — YYYY-MM-DD`.
   - **Gate**:
     - **IF COMPLETE**: Proceed.
     - **IF EMPTY**: Stop. Fill changelog. Recurse.

4. Format and Lint (The Second Filter)
// turbo
   - `ruff format .`
   - `ruff check . --fix`
   - **Gate**:
     - **IF CLEAN**: Proceed.
     - **IF DIRTY**: Stop. Fix style. Recurse.

5. Verify Documentation
   - Check `README.md` and `docs/guides/usage.md`.

6. Commit and Tag (POINT OF NO RETURN)
   - **Gate**:
     - **IF ALL GATES PASSED**: Proceed.
     - **IF ANY DOUBT**: STOP. Do not tag.
   - `git add .`
   - `git commit -m "chore: release vX.Y.Z"`
   - `git tag vX.Y.Z`
   - `git push origin main --tags`

7. (Optional) Build Distribution
   - `python -m build`
   - **Prove It**: Check `dist/*.whl` exists.

---

**Result**: Mark `[x]` in `task.md`.
