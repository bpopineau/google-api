"""CLI command to launch the PySide6 GUI."""

from __future__ import annotations

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Launch the desktop GUI application.")


@app.command("run")
def run_gui() -> None:
    """Launch the PySide6 desktop application."""
    try:
        from mygoog_gui.main import main as run_app
    except ImportError as e:
        console.print(
            "[red]PySide6 is not installed.[/red]\n"
            "Install it with: [cyan]pip install mygooglib[gui][/cyan]"
        )
        raise typer.Exit(1) from e

    console.print("[green]Launching MyGoog Desktop...[/green]")
    run_app()
