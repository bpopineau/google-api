from __future__ import annotations

import json
from pathlib import Path

import typer

from mygooglib import get_clients
from mygooglib.docs import export_pdf, render_template

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Google Docs commands.", no_args_is_help=True)


@app.command("render")
def render_cmd(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template document ID."),
    data: str = typer.Argument(
        ..., help="JSON string or path to JSON file with replacement data."
    ),
    title: str | None = typer.Option(None, help="Title for the new document."),
) -> None:
    """Render a document from a template."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    # Parse data
    try:
        if Path(data).exists():
            with open(data, "r") as f:
                data_dict = json.load(f)
        else:
            data_dict = json.loads(data)
    except Exception as e:
        state.err_console.print(f"[red]Error parsing data:[/red] {e}")
        raise typer.Exit(1)

    doc_id = render_template(
        clients.docs,
        template_id,
        data_dict,
        title=title,
        drive=clients.drive,
    )

    if state.json:
        state.console.print(format_output({"id": doc_id}, json_mode=True))
        return

    print_success(state.console, "Document rendered")
    print_kv(state.console, "id", doc_id)


@app.command("export-pdf")
def export_pdf_cmd(
    ctx: typer.Context,
    doc_id: str = typer.Argument(..., help="Document ID."),
    dest_path: Path = typer.Argument(..., help="Local destination path."),
) -> None:
    """Export a document as PDF."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    out_path = export_pdf(clients.drive, doc_id, dest_path)

    if state.json:
        state.console.print(format_output({"path": str(out_path)}, json_mode=True))
        return

    print_success(state.console, "Exported to PDF")
    print_kv(state.console, "path", out_path)
