from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Launch the Web Dashboard.")


@app.command("run")
def run_dashboard(
    ctx: typer.Context,
    port: int = typer.Option(8501, help="Port to run the dashboard on."),
) -> None:
    """Launch the Streamlit dashboard."""
    # Find the dashboard directory relative to this file
    # mygooglib/cli/dashboard.py -> mygooglib/dashboard/Home.py
    current_dir = Path(__file__).parent
    dashboard_home = current_dir.parent / "dashboard" / "Home.py"

    if not dashboard_home.exists():
        console.print(f"[red]Dashboard file not found at: {dashboard_home}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Launching dashboard on port {port}...[/green]")
    console.print(f"Path: {dashboard_home}")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(dashboard_home),
        "--server.port",
        str(port),
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped.[/yellow]")
