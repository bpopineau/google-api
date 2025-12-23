import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Returns the project root directory (where pyproject.toml is located)."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    # Fallback to current directory if not found (though this shouldn't happen in valid track)
    return Path.cwd()


def validate_name(name: str) -> str:
    """Validates that a name is a valid Python identifier (snake_case)."""
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print(
            f"Error: '{name}' is not a valid Python identifier. Use snake_case (e.g., 'my_service').",
            file=sys.stderr,
        )
        sys.exit(1)
    return name


def write_file(
    path: Path, content: str, overwrite: bool = False, dry_run: bool = False
) -> bool:
    """
    Writes content to a file, with overwrite protection.

    Args:
        path: Destination path.
        content: Content to write.
        overwrite: If True, overwrite existing files.
        dry_run: If True, print content to console instead of writing.
    """
    if dry_run:
        print(
            f"\n[Dry Run] Would write to: {path.relative_to(get_project_root(), walk_up=True)}"
        )
        print("-" * 20)
        print(content)
        print("-" * 20)
        return True

    if path.exists() and not overwrite:
        print(
            f"Error: File '{path}' already exists. Use --force to overwrite (not yet implemented in utils, manual check required).",
            file=sys.stderr,
        )
        return False

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path.relative_to(get_project_root(), walk_up=True)}")
        return True
    except Exception as e:
        print(f"Error writing to {path}: {e}", file=sys.stderr)
        return False
