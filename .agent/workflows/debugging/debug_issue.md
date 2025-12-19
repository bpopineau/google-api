---
description: Systematically identify, reproduce, and fix mygooglib issues
---

1. Reproduce the Issue
   - **Action**: Create `scripts/repro.py` with minimal reproduction code:
     ```python
     from mygooglib import get_clients
     clients = get_clients()
     # Reproduce the failing operation here
     ```
   - **Alt**: Create a test in `tests/test_[module].py` to capture the failure.
   - **Reference**: Use `python scripts/smoke_test.py [command]` if it's a known operation.

2. Analyze and Locate
   - **Read traceback**: Check for errors from `mygooglib/` modules.
   - **Search codebase**: `Select-String -Path "mygooglib\*.py" -Pattern "error_message" -Recurse`
   - **Check utils**: Look at `mygooglib/utils/` for retry/logging issues.
   - **Debugger**: `python -m pdb scripts/repro.py` for step-through debugging.
   - **Key modules**:
     - `mygooglib/auth.py` — credential/token issues
     - `mygooglib/exceptions.py` — custom exceptions
     - `mygooglib/drive.py`, `sheets.py`, `gmail.py`, etc. — service-specific

3. Implement the Fix
   - **Constraint**: Make the smallest change possible.
   - **Location**: Most likely in `mygooglib/[service].py` or `mygooglib/utils/`.
   - **Style**: Follow existing patterns (check similar methods in same file).

4. Verify the Fix
   - **Run repro**: `python scripts/repro.py` should now succeed.
   - **Or run test**: `pytest tests/test_[module].py::test_specific_case -v`

5. Regression Check
// turbo
   - `ruff format . && ruff check . --fix`
   - `pytest`
   - `python scripts/smoke_test.py all`

6. Cleanup
   - Delete `scripts/repro.py` or promote to `tests/test_[module].py`.
   - Remove debug prints; consider adding to `logging` if valuable long-term.
