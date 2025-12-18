---
description: Bootstrap the missing tests directory and create initial tests
---

1. Create Directory Structure
   - `mkdir tests`
   - `touch tests/__init__.py`

2. Create Base Test Fixture
   - **File**: `tests/conftest.py`
   - **Content**: Setup generic pytest fixtures (mocks for google services).

3. Create First Test
   - **File**: `tests/test_smoke.py`
   - **Content**:
     ```python
     def test_import():
         import mygooglib
         assert mygooglib.__version__
     ```

4. Verify
// turbo
   - `pytest`
   - **Goal**: Ensure pytest discovers the new directory.

5. Graduate Smoke Tests
   - **Action**: Port logic from `scripts/smoke_test.py` into formal `tests/test_*.py` files over time.
