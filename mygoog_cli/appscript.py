"""CLI commands for Apps Script."""

from __future__ import annotations

import json

import typer
from rich.console import Console

from mygooglib import get_clients

app = typer.Typer(help="Google Apps Script commands.", no_args_is_help=True)
console = Console()


@app.command("run")
def run_cmd(
    ctx: typer.Context,
    script_id: str = typer.Argument(..., help="Apps Script project ID."),
    function_name: str = typer.Argument(..., help="Function name to execute."),
    params: str | None = typer.Option(
        None,
        "--params",
        "-p",
        help="JSON array of parameters, e.g. '[\"arg1\", 123]'.",
    ),
    dev_mode: bool = typer.Option(
        False,
        "--dev",
        help="Run in development mode (uses most recent save).",
    ),
) -> None:
    """Execute a function in a deployed Apps Script project.

    Example:
        mg appscript run SCRIPT_ID myFunction --params '["hello", 42]'
    """
    clients = get_clients()

    # Parse parameters
    parameters = None
    if params:
        try:
            parameters = json.loads(params)
            if not isinstance(parameters, list):
                console.print("[red]Error: --params must be a JSON array.[/red]")
                raise typer.Exit(1)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing --params JSON: {e}[/red]")
            raise typer.Exit(1)

    with console.status(f"[bold blue]Running {function_name}...[/bold blue]"):
        try:
            result = clients.appscript.run(
                script_id,
                function_name,
                parameters,
                dev_mode=dev_mode,
            )
        except RuntimeError as e:
            console.print(f"[red]Script error:[/red] {e}")
            raise typer.Exit(1)

    console.print("[green]✓ Function executed successfully[/green]")

    if result is not None:
        console.print("\n[bold]Result:[/bold]")
        if isinstance(result, (dict, list)):
            console.print_json(json.dumps(result, indent=2, default=str))
        else:
            console.print(str(result))

