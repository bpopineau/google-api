from __future__ import annotations

from pathlib import Path

import typer
from rich.prompt import Prompt
from rich.table import Table

from mygooglib import get_clients
from mygooglib.gmail import get_message, mark_read, search_messages, send_email

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Gmail commands.", no_args_is_help=True)


def _split_emails(values: list[str]) -> list[str]:
    out: list[str] = []
    for v in values:
        parts = [p.strip() for p in v.split(",")]
        out.extend([p for p in parts if p])
    return out


@app.command("send")
def send_cmd(
    ctx: typer.Context,
    to: list[str] = typer.Option(
        ..., "--to", help="Recipient email (repeatable; commas allowed)."
    ),
    subject: str = typer.Option(..., "--subject"),
    body: str = typer.Option(..., "--body", help="Plain text body."),
    attachments: list[Path] = typer.Option(
        [],
        "--attach",
        help="Attachment file path (repeatable).",
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
    ),
    cc: list[str] = typer.Option(
        [], "--cc", help="CC email (repeatable; commas allowed)."
    ),
    bcc: list[str] = typer.Option(
        [], "--bcc", help="BCC email (repeatable; commas allowed)."
    ),
) -> None:
    """Send an email via Gmail API."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    msg_id = send_email(
        clients.gmail.service,
        to=_split_emails(to),
        subject=subject,
        body=body,
        attachments=attachments,
        cc=_split_emails(cc) if cc else None,
        bcc=_split_emails(bcc) if bcc else None,
    )

    if state.json:
        state.console.print(format_output({"id": msg_id}, json_mode=True))
        return

    print_success(state.console, "Sent")
    print_kv(state.console, "id", msg_id)


@app.command("search")
def search_cmd(
    ctx: typer.Context,
    query: str = typer.Argument(..., help='Gmail query, e.g. "newer_than:7d"'),
    max_results: int = typer.Option(50, "--max", min=1, max=500),
    include_spam_trash: bool = typer.Option(False, "--include-spam-trash"),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively view messages."
    ),
) -> None:
    """Search messages and print lightweight results."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    results = search_messages(
        clients.gmail.service,
        query,
        max_results=max_results,
        include_spam_trash=include_spam_trash,
    )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Messages ({len(results)})")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("id", overflow="fold")
    table.add_column("from", overflow="fold")
    table.add_column("subject", overflow="fold")
    table.add_column("date", overflow="fold")

    for i, msg in enumerate(results, 1):
        row = [
            str(msg.get("id") or ""),
            str(msg.get("from") or ""),
            str(msg.get("subject") or ""),
            str(msg.get("date") or ""),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)

    state.console.print(table)

    if interactive and results:
        while True:
            choice = Prompt.ask(
                "Select message number to view (or 'q' to quit)", default="q"
            )
            if choice.lower() == "q":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    view_cmd(ctx, results[idx]["id"])
                else:
                    state.console.print("[red]Invalid selection.[/red]")
            except ValueError:
                state.console.print("[red]Invalid input.[/red]")


@app.command("mark-read")
def mark_read_cmd(
    ctx: typer.Context,
    message_id: str = typer.Argument(..., help="Message ID"),
) -> None:
    """Remove the UNREAD label from a message."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    _ = mark_read(clients.gmail.service, message_id)

    if state.json:
        state.console.print(
            format_output({"id": message_id, "markedRead": True}, json_mode=True)
        )
        return

    print_success(state.console, "Marked read")
    print_kv(state.console, "id", message_id)


@app.command("view")
def view_cmd(
    ctx: typer.Context,
    message_id: str = typer.Argument(..., help="Message ID"),
) -> None:
    """View full message details and body."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    msg = get_message(clients.gmail.service, message_id)

    if state.json:
        state.console.print(format_output(msg, json_mode=True))
        return

    state.console.rule(f"[bold]Message: {msg['id']}[/bold]")
    print_kv(state.console, "From", msg.get("from"))
    print_kv(state.console, "To", msg.get("to"))
    print_kv(state.console, "Date", msg.get("date"))
    print_kv(state.console, "Subject", msg.get("subject"))
    state.console.rule()
    state.console.print(msg.get("body") or "[italic]No plain text body found.[/italic]")
    state.console.rule()
