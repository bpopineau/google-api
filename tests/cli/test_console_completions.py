import pytest
from IPython.core.interactiveshell import InteractiveShell
from mygoog_cli.console import build_context

@pytest.fixture
def shell():
    shell = InteractiveShell()
    shell.Completer.greedy = True
    context = build_context()
    shell.user_ns.update(context)
    return shell

def test_drive_completions(shell):
    # Testing tab completion for drive.files().
    # Note: drive is a DynamicService or a mock if auth fails.
    # We want to ensure it has the expected methods.

    # We use the Completer to get completions
    completer = shell.Completer

    # Test drive.
    completions = list(completer.completions("drive.", 6))
    texts = [c.text for c in completions]
    assert "files" in texts or "service" in texts # Depending on how it's wrapped

    if "drive" in shell.user_ns:
        # Check if the methods exist on the object returned by files()
        drive = shell.user_ns["drive"]
        files_resource = drive.files()
        assert "list" in dir(files_resource)
        assert "create" in dir(files_resource)
        
        # Now try completions again but on the variable
        shell.user_ns["f"] = files_resource
        completions = list(completer.completions("f.", 2))
        texts = [c.text for c in completions]
        assert "list" in texts