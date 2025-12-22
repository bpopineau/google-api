from __future__ import annotations

import typer

from mygooglib import get_clients
from mygooglib.workflows import import_events_from_sheets

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Cross-service workflow commands.", no_args_is_help=True)


@app.command("sheets-to-calendar")
def sheets_to_calendar(
    ctx: typer.Context,
    spreadsheet_id: str = typer.Argument(..., help="Spreadsheet ID or Title."),
    range_name: str = typer.Argument(
        ..., help="Range containing event data (e.g., 'Events!A2:D50')."
    ),
    calendar_id: str = typer.Option(
        "primary", "--calendar", help="Target calendar ID."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without creating events."
    ),
) -> None:
    """Import calendar events from a Google Sheet.

    Expected columns: [Summary, Start, End/Duration, Description]
    """
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    # Note: spreadsheet_id resolution (title -> id) is handled within sheets.get_range if implemented,
    # but here we might want to use the clients.sheets method which might already handle it.

    # We'll use the spreadsheet_id as is; if it's a title, the underlying lib should handle it
    # if we use the right method. clients.sheets.get_range does NOT currently handle titles
    # unless we wrapped it that way. Actually, sheets.py helpers usually take ID.

    resolved_ss_id = spreadsheet_id
    if "/" not in spreadsheet_id and len(spreadsheet_id) < 20:  # Heuristic for title
        try:
            resolved_ss_id = clients.sheets.resolve_spreadsheet(spreadsheet_id)
        except Exception:
            pass  # Fallback to using it as ID

    result = import_events_from_sheets(
        clients,
        resolved_ss_id,
        range_name,
        calendar_id=calendar_id,
        dry_run=dry_run,
    )

    if state.json:
        state.console.print(format_output(result, json_mode=True))
        return

    if dry_run:
        state.console.print("[bold yellow]DRY RUN - No events created[/bold yellow]")

    print_success(state.console, "Import complete")
    print_kv(state.console, "created", result["created"])
    print_kv(state.console, "skipped", result["skipped"])

    if result["errors"]:
        state.err_console.print(f"[red]Errors ({len(result['errors'])}):[/red]")
        for err in result["errors"]:
            state.err_console.print(f"- {err}")
