---
description: Meticulously update mygooglib documentation to ensure accuracy
---

# /update_docs

**Goal**: Zero discrepancy between code and docs.

## ⚠️ Task Management
- **Rule**: Ensure `task.md` item "Update Guides" is `[/]`.

---

1. Audit Recent Code Changes
   - `git log -p -10 --oneline mygooglib/`

2. Verify API Reference Matches Code
   - Run `pydoc` for changed modules.
   - **Gate**:
     - **IF TEXT MATCHES CODE**: Proceed.
     - **IF OUTDATED**: Stop. Fix docstring. Recurse.

3. Update Guides
   - **File**: `docs/guides/usage.md`
   - **File**: `docs/guides/configuration.md`

4. Verify Examples Run (The Proof)
// turbo
   - `python examples/drive_list_files.py` (or relevant example)
   - **Gate**:
     - **IF SUCCEEDS**: Proceed.
     - **IF FAILS**: Stop. Update example or code. Recurse.

5. Maintain Consistency
   - **README.md**: Verify Quick Start.
   - **AUTOMATION_GOALS.md**: Update priorities.
   - **CHANGELOG.md**: Ensure version is current.

6. Check CLI Documentation
   - `mg --help`
   - **Gate**:
     - **IF NEW CMD LISTED**: Proceed.
     - **IF MISSING**: Stop. Fix Typer registration. Recurse.

---

**Result**: Mark `[x]` in `task.md`.

