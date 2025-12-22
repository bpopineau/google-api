---
description: Write and enforce Google-style docstrings for mygooglib
---

# /write_docstrings

**Goal**: Ensure code is self-documenting.

## ⚠️ Task Management
- **Rule**: Create/Update `task.md` item "Docstrings" `[/]` before starting.

---

1. Select Target & Update Task
   - Identify missing docstrings (e.g., in `mygooglib/drive.py`).
   - Add sub-tasks if needed.

2. Write Docstring (Google Style)
   - Follow standard format (Args, Returns, Raises).

3. Verify Format (Ruff)
// turbo
   - `ruff check mygooglib/ --select D --ignore D100,D104`
   - **Gate**:
     - **IF CLEAN**: Proceed.
     - **IF ERROR**:
       - Stop. Read error code.
       - Fix docstring format.
       - Recurse (Run check again).

4. Verify Clarity (Pydoc)
   - `python -m pydoc mygooglib.module.function`
   - **Gate**:
     - **IF READABLE**: Proceed.
     - **IF MESSY**: Stop. Fix formatting. Recurse.

---

**Result**: Mark `[x]` in `task.md` ONLY if Ruff passes.

