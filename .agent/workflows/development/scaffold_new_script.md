---
description: Create a new mygooglib automation script with boilerplate
---

# /scaffold_new_script

**Goal**: Create a correctly structured script.

## ⚠️ Task Management
- **Rule**: Create a sub-task in `task.md` (e.g., `[ ] Scaffold <script_name>`) and mark `[/]` BEFORE starting.

---

1. Choose Location and Name
   - **Scripts**: `scripts/` (internal)
   - **Examples**: `examples/` (demos)
   - **Gate**:
     - **IF NAME VALID**: Proceed (use snake_case).
     - **IF INVALID**: Stop. Rename. Recurse.

2. Create File with mygooglib Boilerplate
   - **Action**: Create the file with this template:
     ```python
     """[Description]."""
     from __future__ import annotations
     from mygooglib import get_clients

     def main() -> int:
         clients = get_clients()
         # clients.drive, clients.sheets, etc.
         return 0

     if __name__ == "__main__":
         raise SystemExit(main())
     ```
   - **Prove It**: Check file existence.
   - **Gate**:
     - **IF FILE EXISTS**: Proceed.
     - **IF MISSING**: Stop. Retry creation. Recurse.

3. Run Initial Test
   - `python path/to/script.py`
   - **Gate**:
     - **IF RUNS (exit 0)**: Proceed.
     - **IF IMPORT ERROR**: Stop. Check env/path. Recurse.

4. Add to Smoke Test (optional)
   - If mostly read-only, add to `scripts/smoke_test.py`.

5. Document
   - Update `docs/guides/usage.md`.

---

**Result**: Mark `[x]` for the scaffold task in `task.md`.

