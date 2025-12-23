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
    # Testing tab completion for drive.files.
    completer = shell.Completer

    # Test drive.
    completions = list(completer.completions("drive.", 6))
    texts = [c.text for c in completions]
    assert "files" in texts or "service" in texts

    if "drive" in shell.user_ns:
        # Check if the property exists and returns a Resource with expected methods
        drive = shell.user_ns["drive"]
        files_resource = drive.files
        assert "list" in dir(files_resource)
        assert "create" in dir(files_resource)
        assert "get" in dir(files_resource)