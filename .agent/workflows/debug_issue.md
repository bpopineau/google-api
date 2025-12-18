---
description: Systematically identify, reproduce, and fix software issues
---

1. Reproduce the Issue
   - **Action**: Create a minimal reproduction script (repro.py) or a new test case.
   - **Goal**: See the failure happen reliably. "If it's not red, you can't make it green."
   - **Tools**:
     - `python scripts/smoke_test.py` (if it's a general breakage)
     - `pytest tests/test_specific_case.py` (if it's a specific logic bug)

2. Analyze and Locate
   - **Action**: Read the traceback carefully.
   - **Action**: Use `grep` to find where the error message originates.
   - **Action**: Add temporary `print()` debugging or use `logging`.
   - **Question**: "What is the state of the system right before the crash?"

3. Implement the Fix
   - **Action**: Modify the code to handle the edge case or correct the logic.
   - **Constraint**: Make the smallest change possible to fix the issue.

4. Verify the Fix
   - **Action**: Run the reproduction script/test from Step 1.
   - **Success**: It should now pass (exit code 0).

5. Regression Check
// turbo
   - `/development`
   - **Goal**: Ensure the fix didn't break anything else.

6. Cleanup
   - **Action**: Remove temporary `repro.py` (or promote it to a real test).
   - **Action**: Remove debugging print statements.
