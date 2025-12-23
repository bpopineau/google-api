import pytest
from IPython.core.completer import provisionalcompleter
from IPython.core.interactiveshell import InteractiveShell

from mygoog_cli.console import build_context


@pytest.fixture
def shell():
    shell = InteractiveShell()
    # Use modern completion config (greedy deprecated since IPython 8.8)
    shell.Completer.evaluation = "unsafe"
    shell.Completer.use_jedi = False
    context = build_context()
    shell.user_ns.update(context)
    return shell


def test_drive_completions(shell):
    # Testing tab completion for drive.files.
    completer = shell.Completer

    # Test drive. completions using proper API
    with provisionalcompleter():
        completions = list(completer.completions("drive.", 6))
        texts = [c.text for c in completions]
        # Completions include leading dot (e.g., '.files', '.service')
        assert ".files" in texts or ".service" in texts or "files" in texts

    if "drive" in shell.user_ns:
        # Check if the property exists and returns a Resource with expected methods
        drive = shell.user_ns["drive"]
        files_resource = drive.files
        assert "list" in dir(files_resource)
        assert "create" in dir(files_resource)
        assert "get" in dir(files_resource)
