---
description: Bootstrap the tests directory for mygooglib with pytest fixtures
---

1. Create Directory Structure
   - `New-Item -ItemType Directory -Path tests -Force`
   - `New-Item -ItemType File -Path tests/__init__.py -Force`

2. Create Base Test Fixture
   - **File**: `tests/conftest.py`
   - **Content**: Setup pytest fixtures with mocked Google service clients:
     ```python
     import pytest
     from unittest.mock import MagicMock, patch

     @pytest.fixture
     def mock_clients():
         """Return a mocked ClientCollection for unit tests."""
         with patch("mygooglib.core.client.get_clients") as mock:
             clients = MagicMock()
             clients.drive = MagicMock()
             clients.sheets = MagicMock()
             clients.gmail = MagicMock()
             clients.docs = MagicMock()
             clients.calendar = MagicMock()
             clients.tasks = MagicMock()
             mock.return_value = clients
             yield clients
     ```

3. Create Import Smoke Test
   - **File**: `tests/test_smoke.py`
   - **Content**:
     ```python
     def test_import():
         import mygooglib
         assert hasattr(mygooglib, "get_clients")
         assert hasattr(mygooglib, "get_creds")
         assert hasattr(mygooglib, "create")

     def test_client_factory_signature():
         from mygooglib import get_clients
         import inspect
         sig = inspect.signature(get_clients)
         # Should accept no required args
         assert len([p for p in sig.parameters.values() if p.default is inspect.Parameter.empty]) == 0
     ```

4. Create Service Module Tests
   - **File**: `tests/test_drive.py` — test `list_files`, `find_by_name`, `sync_folder`
   - **File**: `tests/test_sheets.py` — test `get_range`, `append_row`, `update_range`
   - **File**: `tests/test_gmail.py` — test `send_email`, `search_messages`, `mark_read`
   - **File**: `tests/test_calendar.py` — test `add_event`, `list_events`
   - **File**: `tests/test_tasks.py` — test `list_tasklists`, `add_task`, `complete_task`
   - **File**: `tests/test_docs.py` — test `create`, `get_text`, `render_template`

5. Verify pytest discovers tests
// turbo
   - `pytest --collect-only`

6. Run first test
// turbo
   - `pytest tests/test_smoke.py -v`

