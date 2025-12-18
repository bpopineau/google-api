"""CLI commands for Google Contacts (People API)."""

from __future__ import annotations

import typer
from rich.table import Table

from mygooglib import get_clients
from mygooglib.contacts import list_contacts, search_contacts

from .common import CliState, format_output

app = typer.Typer(help="Google Contacts commands.", no_args_is_help=True)


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    page_size: int = typer.Option(
        30, "--page-size", "-n", help="Number of contacts to fetch."
    ),
    sort_order: str = typer.Option(
        "FIRST_NAME_ASCENDING",
        "--sort",
        help="Sort order (FIRST_NAME_ASCENDING / LAST_NAME_ASCENDING).",
    ),
) -> None:
    """List contacts."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    contacts = list_contacts(
        clients.contacts.service, page_size=page_size, sort_order=sort_order
    )

    if state.json:
        state.console.print(format_output(contacts, json_mode=True))
        return

    table = Table(title="Contacts")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Phone")
    table.add_column("Resource Name")

    for c in contacts:
        table.add_row(
            c.get("name") or "",
            c.get("email") or "",
            c.get("phone") or "",
            c.get("resourceName") or "",
        )
    state.console.print(table)


@app.command("search")
def search_cmd(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query (e.g. 'John', 'example.com')."),
) -> None:
    """Search for contacts."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    contacts = search_contacts(clients.contacts.service, query=query)

    if state.json:
        state.console.print(format_output(contacts, json_mode=True))
        return

    table = Table(title=f"Search Results: '{query}'")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Phone")
    table.add_column("Resource Name")

    for c in contacts:
        table.add_row(
            c.get("name") or "",
            c.get("email") or "",
            c.get("phone") or "",
            c.get("resourceName") or "",
        )
    state.console.print(table)
