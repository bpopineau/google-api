from __future__ import annotations

import datetime as dt

import typer
from rich.table import Table

from mygooglib import get_clients
from mygooglib.calendar import add_event, list_events

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Google Calendar commands.", no_args_is_help=True)


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    calendar_id: str = typer.Option("primary", help="Calendar ID."),
    time_min: dt.datetime | None = typer.Option(
        None, help="Lower bound for event end time."
    ),
    time_max: dt.datetime | None = typer.Option(
        None, help="Upper bound for event start time."
    ),
    max_results: int = typer.Option(100, help="Max results."),
) -> None:
    """List calendar events."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    results = list_events(
        clients.calendar,
        calendar_id=calendar_id,
        time_min=time_min,
        time_max=time_max,
        max_results=max_results,
    )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Calendar events ({len(results)})")
    table.add_column("start", overflow="fold")
    table.add_column("summary", overflow="fold")
    table.add_column("id", overflow="fold")

    for item in results:
        start = item.get("start", {})
        start_val = start.get("dateTime") or start.get("date") or ""
        table.add_row(
            str(start_val),
            str(item.get("summary") or ""),
            str(item.get("id") or ""),
        )

    state.console.print(table)


@app.command("add")
def add_cmd(
    ctx: typer.Context,
    summary: str = typer.Argument(..., help="Event title."),
    start: dt.datetime = typer.Argument(..., help="Start datetime."),
    end: dt.datetime | None = typer.Option(None, help="End datetime."),
    duration: int | None = typer.Option(
        None, "--duration", help="Duration in minutes."
    ),
    description: str | None = typer.Option(None, help="Event description."),
    location: str | None = typer.Option(None, help="Location."),
    calendar_id: str = typer.Option("primary", help="Calendar ID."),
) -> None:
    """Add a new event."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    event_id = add_event(
        clients.calendar,
        summary=summary,
        start=start,
        end=end,
        duration_minutes=duration,
        description=description,
        location=location,
        calendar_id=calendar_id,
    )

    if state.json:
        state.console.print(format_output({"id": event_id}, json_mode=True))
        return

    print_success(state.console, "Event added")
    print_kv(state.console, "id", event_id)
