import sys
from pathlib import Path

import typer

# Add scripts directory to path to import utils
sys.path.append(str(Path(__file__).parent))
from scaffold_utils import get_project_root, validate_name, write_file

app = typer.Typer()

CLI_TEMPLATE = """import typer
from typing_extensions import Annotated
from rich import print

# Create a Typer app for this command group
app = typer.Typer(help="{command_description}")

@app.command()
def example_action(
    name: Annotated[str, typer.Argument(help="Name to print")] = "World",
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
):
    \"\"\"
    Example action for {command_name}.
    \"\"\"
    print(f"[bold green]Hello {{name}} from {command_name}![/bold green]")
    if verbose:
        print(f"Verbose mode enabled for {command_name}")

if __name__ == "__main__":
    app()
"""


@app.command()
def main(name: str):
    """
    Scaffold a new CLI command in mygoog_cli/.

    NAME: The snake_case name of the command (e.g., 'calendar', 'drive_sync').
    """
    valid_name = validate_name(name)
    command_name = valid_name.replace("_", "-")

    # Generate content
    content = CLI_TEMPLATE.format(
        command_name=command_name,
        command_description=f"CLI commands for {command_name}",
    )

    # Define target path
    root = get_project_root()
    target_file = root / "mygoog_cli" / f"{valid_name}.py"

    if write_file(target_file, content):
        print("\n[bold green]Success![/bold green]")
        print("Next steps:")
        print(f"1. Open [bold]{target_file}[/bold]")
        print("2. Implement your commands using the `app` object.")
        print("3. Register in [bold]mygoog_cli/main.py[/bold]:")
        print(f"   from . import {valid_name}")
        print(f'   app.add_typer({valid_name}.app, name="{command_name}")')


if __name__ == "__main__":
    app()
