from __future__ import annotations

import json
from pathlib import Path

import typer

from mygooglib import get_clients
from mygooglib.docs import (
    append_text,
    create,
    export_pdf,
    find_replace,
    get_text,
    render_template,
)

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Google Docs commands.", no_args_is_help=True)


@app.command("create")
def create_cmd(
    ctx: typer.Context,
    title: str = typer.Argument(..., help="Title for the new document."),
) -> None:
    """Create a new empty document."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    doc_id = create(clients.docs.service, title)

    if state.json:
        state.console.print(format_output({"id": doc_id}, json_mode=True))
        return

    print_success(state.console, "Document created")
    print_kv(state.console, "id", doc_id)


@app.command("get-text")
def get_text_cmd(
    ctx: typer.Context,
    doc_id: str = typer.Argument(..., help="Document ID."),
) -> None:
    """Get plain text content of a document."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    text = get_text(clients.docs.service, doc_id)

    if state.json:
        state.console.print(format_output({"text": text}, json_mode=True))
        return

    state.console.print(text)


@app.command("append")
def append_cmd(
    ctx: typer.Context,
    doc_id: str = typer.Argument(..., help="Document ID."),
    text: str = typer.Argument(..., help="Text to append."),
) -> None:
    """Append text to a document."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    append_text(clients.docs.service, doc_id, text)

    if state.json:
        state.console.print(
            format_output({"id": doc_id, "appended": True}, json_mode=True)
        )
        return

    print_success(state.console, "Text appended")


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
        clients.docs.service,
        template_id,
        data_dict,
        title=title,
        drive=clients.drive.service,
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

    out_path = export_pdf(clients.drive.service, doc_id, dest_path)

    if state.json:
        state.console.print(format_output({"path": str(out_path)}, json_mode=True))
        return

    print_success(state.console, "Exported to PDF")
    print_kv(state.console, "path", out_path)


@app.command("replace")
def replace_cmd(
    ctx: typer.Context,
    doc_id: str = typer.Argument(..., help="Document ID."),
    data: str = typer.Argument(
        ..., help="JSON string or path to JSON file with search/replace pairs."
    ),
) -> None:
    """Perform find-and-replace in a document.

    Example:
        mygoog docs replace [DOC_ID] '{"foo": "bar"}'
    """
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    # Parse data
    try:
        if Path(data).exists():
            with open(data, "r") as f:
                replacements = json.load(f)
        else:
            replacements = json.loads(data)
    except Exception as e:
        state.err_console.print(f"[red]Error parsing replacements:[/red] {e}")
        raise typer.Exit(1)

    if not isinstance(replacements, dict):
        state.err_console.print(
            "[red]Error:[/red] Replacements must be a JSON object/dictionary."
        )
        raise typer.Exit(1)

    count = find_replace(clients.docs.service, doc_id, replacements)

    if state.json:
        state.console.print(
            format_output(
                {"id": doc_id, "replaced": True, "occurrences": count}, json_mode=True
            )
        )
        return

    print_success(state.console, f"Replaced {count} occurrences")
