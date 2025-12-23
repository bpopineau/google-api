import pytest
from scaffold_utils import get_project_root, validate_name, write_file


def test_validate_name_valid():
    assert validate_name("my_service") == "my_service"
    assert validate_name("service") == "service"
    assert validate_name("drive_v3") == "drive_v3"


def test_validate_name_invalid():
    with pytest.raises(SystemExit):
        validate_name("MyService")
    with pytest.raises(SystemExit):
        validate_name("my-service")
    with pytest.raises(SystemExit):
        validate_name("123service")
    # Verify stderr output for invalid name
    # We need to capture stderr to assert the message
    # Since validate_name calls sys.exit(1), we can't easily capture output unless we mock or use capsys with a wrapper
    # But for now, ensuring it exits is the main requirement.


def test_validate_name_error_message(capsys):
    """Test that invalid name prints useful error message."""
    with pytest.raises(SystemExit):
        validate_name("MyService")
    captured = capsys.readouterr()
    assert "not a valid Python identifier" in captured.err
    assert "Use snake_case" in captured.err


def test_get_project_root(tmp_path):
    # This test might be tricky if not running in actual repo,
    # but we can trust it finds *some* root or cwd.
    # In this environment, it should find the actual repo root.
    root = get_project_root()
    assert (root / "pyproject.toml").exists()


def test_write_file(tmp_path):
    target = tmp_path / "test_file.py"
    assert write_file(target, "content") is True
    assert target.read_text(encoding="utf-8") == "content"

    # Test overwrite protection (defaults to False and returns False if exists)
    # The current utils prints to stderr and returns False
    assert write_file(target, "new content") is False
    assert target.read_text(encoding="utf-8") == "content"


def test_scaffold_cli_integration(tmp_path, monkeypatch):
    """Test that scaffold_cli.py creates a file with expected content."""
    # Mock get_project_root to return tmp_path/root_mock
    root_mock = tmp_path / "root_mock"
    root_mock.mkdir()
    (root_mock / "pyproject.toml").touch()

    import scaffold_utils

    monkeypatch.setattr(scaffold_utils, "get_project_root", lambda: root_mock)

    # We need to import the module dynamically or via runpy to test it,
    # but since it's a script, we can also import the main function if we structure it right.
    # However, scaffold_cli.py doesn't exist yet, so we can't import it.
    # This test will fail importing it, which counts as RED phase.

    from typer.testing import CliRunner

    # Import the module - since it's a script in a non-package dir, this is a bit hacky but works due to sys.path append in conftest or earlier in file
    try:
        import scaffold_cli
    except ImportError:
        pytest.fail("Could not import scaffold_cli")

    runner = CliRunner()
    result = runner.invoke(scaffold_cli.app, ["my_new_cmd"])

    assert result.exit_code == 0
    assert "Success!" in result.stdout

    # Check file created
    expected_file = root_mock / "mygoog_cli" / "my_new_cmd.py"
    assert expected_file.exists()
    # Read text to ensure it's readable
    expected_file.read_text(encoding="utf-8")


def test_write_file_dry_run(tmp_path, capsys):
    target = tmp_path / "test_file_dry.py"

    # Check dry_run=True (should not write, should print)
    # Note: write_file signature needs update to accept dry_run default=False
    # This call will fail TypeError before implementation, which is good RED phase
    try:
        assert write_file(target, "content", dry_run=True) is True
    except TypeError:
        pytest.fail("write_file does not accept dry_run argument yet")

    assert not target.exists()
    captured = capsys.readouterr()
    assert "Dry Run" in captured.out or "content" in captured.out

    # Check dry_run=False (should write)
    assert write_file(target, "content", dry_run=False) is True
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "content"
