
import pytest
from IPython.core.interactiveshell import InteractiveShell
from mygoog_cli.console import build_context

@pytest.fixture
def shell():
    shell = InteractiveShell()
    context = build_context()
    shell.user_ns.update(context)
    return shell

def test_smoke_drive_list(shell):
    if "drive" not in shell.user_ns:
        pytest.skip("Drive client not available (Auth likely failed)")
    
    # Run drive.list_files(max_results=1)
    # We use shell.run_cell to simulate user input
    result = shell.run_cell("drive.list_files(max_results=1)")
    assert result.success
    assert isinstance(result.result, list)

def test_smoke_gmail_labels(shell):
    if "gmail" not in shell.user_ns:
        pytest.skip("Gmail client not available")
    
    result = shell.run_cell("gmail.list_labels()")
    assert result.success
    assert isinstance(result.result, list)

def test_smoke_sheets_service(shell):
    if "sheets" not in shell.user_ns:
        pytest.skip("Sheets client not available")
    
    # Test that we can access the underlying service via __getattr__
    result = shell.run_cell("sheets.spreadsheets()")
    assert result.success
    # result.result should be a Resource object
    assert hasattr(result.result, "get")

def test_smoke_shortcuts(shell):
    if "drv" not in shell.user_ns:
        pytest.skip("Shortcuts not available")
    
    result = shell.run_cell("drv == drive")
    assert result.success
    assert result.result is True

def test_smoke_types(shell):
    # Verify SpreadsheetDict is in global namespace
    result = shell.run_cell("SpreadsheetDict")
    assert result.success
    # It should be a TypedDict or similar
    assert "SpreadsheetDict" in str(result.result)
