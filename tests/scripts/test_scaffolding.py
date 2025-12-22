import sys
from pathlib import Path

import pytest

# Ensure scripts path is in sys.path
scripts_dir = Path(__file__).parents[2] / "scripts"
sys.path.append(str(scripts_dir))

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
