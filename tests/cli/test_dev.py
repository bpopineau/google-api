from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from mygoog_cli.dev import app

runner = CliRunner()


@pytest.fixture
def mock_task_file(tmp_path):
    """Fixture to patch TASK_FILE with a temp path."""
    p = tmp_path / "task.md"
    with patch("mygoog_cli.dev.TASK_FILE", p):
        with patch("mygoog_cli.dev._get_task_file", return_value=p):
            yield p


def test_init_creates_file(mock_task_file):
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert mock_task_file.exists()
    assert "# Task: Evolve Development Cycle" in mock_task_file.read_text("utf-8")


def test_init_fails_if_exists(mock_task_file):
    mock_task_file.write_text("exists")
    result = runner.invoke(app, ["init"])
    assert result.exit_code != 0
    assert "already exists" in result.stdout


def test_status_parses_active(mock_task_file):
    content = """# Task
- [x] Phase 1
- [/] Phase 2
    - [/] Active Task (`echo hi`)
    - [ ] Next Task
"""
    mock_task_file.write_text(content, encoding="utf-8")

    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Active Task" in result.stdout
    assert "Next Task" in result.stdout
    assert "echo hi" in result.stdout


def test_next_advances_state(mock_task_file):
    content = """# Task
- [/] Phase 1
    - [/] Active Task
    - [ ] Next Task
"""
    mock_task_file.write_text(content, encoding="utf-8")

    # We expect verify to be skipped as there is no command, or pass if logic allows empty.
    # Logic: if active.command: verify. Else: just mark done.

    result = runner.invoke(app, ["next"])
    assert result.exit_code == 0

    new_content = mock_task_file.read_text("utf-8")
    assert "- [x] Active Task" in new_content
    assert "- [/] Next Task" in new_content


@patch("mygoog_cli.dev.subprocess.run")
def test_next_runs_verification(mock_run, mock_task_file):
    content = """# Task
- [/] Active (`pytest`)
- [ ] Next
"""
    mock_task_file.write_text(content, encoding="utf-8")

    # Mock success
    mock_run.return_value = MagicMock(returncode=0)

    result = runner.invoke(app, ["next"])
    assert result.exit_code == 0
    mock_run.assert_called_once()

    # Check args
    args, _ = mock_run.call_args
    assert args[0] == ["pytest"]

    # Confirm state advanced
    assert "- [x] Active" in mock_task_file.read_text("utf-8")


@patch("mygoog_cli.dev.subprocess.run")
def test_next_fails_verification(mock_run, mock_task_file):
    content = """# Task
- [/] Active (`pytest`)
- [ ] Next
"""
    mock_task_file.write_text(content, encoding="utf-8")

    # Mock failure
    mock_run.return_value = MagicMock(returncode=1)

    result = runner.invoke(app, ["next"])
    assert result.exit_code != 0
    assert "Verification FAILED" in result.stdout

    # Confirm state DID NOT advance
    assert "- [/] Active" in mock_task_file.read_text("utf-8")


@patch("mygoog_cli.dev.subprocess.run")
def test_check_runs_command(mock_run, mock_task_file):
    content = """# Task
- [/] Active (`echo check`)
"""
    mock_task_file.write_text(content, encoding="utf-8")
    mock_run.return_value = MagicMock(returncode=0)

    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    mock_run.assert_called()

    # Check args
    args, _ = mock_run.call_args
    assert args[0] == ["echo", "check"]


