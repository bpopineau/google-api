"""CLI commands for Google Contacts (People API)."""

from __future__ import annotations

import typer
from rich.table import Table

from mygooglib import get_clients
from mygooglib.services.contacts import (
    create_contact,
    delete_contact,
    list_contacts,
    search_contacts,
    update_contact,
)

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


@app.command("add")
def add_cmd(
    ctx: typer.Context,
    given_name: str = typer.Option(..., "--name", "-n", help="First name (required)."),
    family_name: str = typer.Option(None, "--family", "-f", help="Last name."),
    email: str = typer.Option(None, "--email", "-e", help="Email address."),
    phone: str = typer.Option(None, "--phone", "-p", help="Phone number."),
) -> None:
    """Create a new contact."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    contact = create_contact(
        clients.contacts.service,
        given_name=given_name,
        family_name=family_name,
        email=email,
        phone=phone,
    )

    if state.json:
        state.console.print(format_output(contact, json_mode=True))
    else:
        state.console.print(f"[green]Created contact:[/green] {contact.get('name')}")
        state.console.print(f"  Resource: {contact.get('resourceName')}")


@app.command("update")
def update_cmd(
    ctx: typer.Context,
    resource_name: str = typer.Argument(
        ..., help="Resource name (e.g., 'people/c123...')."
    ),
    given_name: str = typer.Option(None, "--name", "-n", help="New first name."),
    family_name: str = typer.Option(None, "--family", "-f", help="New last name."),
    email: str = typer.Option(None, "--email", "-e", help="New email address."),
    phone: str = typer.Option(None, "--phone", "-p", help="New phone number."),
) -> None:
    """Update an existing contact."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    contact = update_contact(
        clients.contacts.service,
        resource_name,
        given_name=given_name,
        family_name=family_name,
        email=email,
        phone=phone,
    )

    if state.json:
        state.console.print(format_output(contact, json_mode=True))
    else:
        state.console.print(f"[green]Updated contact:[/green] {contact.get('name')}")


@app.command("delete")
def delete_cmd(
    ctx: typer.Context,
    resource_name: str = typer.Argument(
        ..., help="Resource name (e.g., 'people/c123...')."
    ),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
) -> None:
    """Delete a contact."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    if not confirm:
        typer.confirm(f"Delete contact {resource_name}?", abort=True)

    delete_contact(clients.contacts.service, resource_name)
    state.console.print(f"[green]Deleted contact:[/green] {resource_name}")

