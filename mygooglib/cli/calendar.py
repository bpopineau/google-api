from __future__ import annotations

import datetime as dt

import webbrowser

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from mygooglib import get_clients
from mygooglib.calendar import add_event, delete_event, list_events

from .common import CliState, format_output, print_kv, print_success, prompt_selection

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
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively select an event for actions."
    ),
) -> None:
    """List calendar events."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=state.console,
        transient=True,
    ) as progress:
        task = progress.add_task("Fetching events...", total=None)

        def update_progress(count: int) -> None:
            progress.update(task, advance=count)

        results = list_events(
            clients.calendar.service,
            calendar_id=calendar_id,
            time_min=time_min,
            time_max=time_max,
            max_results=max_results,
            progress_callback=update_progress,
        )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Calendar events ({len(results)})")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("start", overflow="fold")
    table.add_column("summary", overflow="fold")
    table.add_column("id", overflow="fold")

    for i, item in enumerate(results, 1):
        start = item.get("start", {})
        start_val = start.get("dateTime") or start.get("date") or ""
        row = [
            str(start_val),
            str(item.get("summary") or ""),
            str(item.get("id") or ""),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)

    state.console.print(table)

    if interactive and results:
        selected = prompt_selection(
            state.console, results, label_key="summary", id_key="id"
        )
        if selected:
            action = typer.prompt(
                "Action: [v]iew, [d]elete, [o]pen in browser, [q]uit", default="v"
            )
            if action == "v":
                state.console.print(format_output(selected, json_mode=False))
            elif action == "d":
                if typer.confirm(f"Delete event '{selected.get('summary')}'?"):
                    delete_cmd(ctx, selected["id"], calendar_id=calendar_id)
            elif action == "o":
                open_cmd(ctx, selected["id"], calendar_id=calendar_id)


@app.command("delete")
def delete_cmd(
    ctx: typer.Context,
    event_id: str = typer.Argument(..., help="Event ID to delete."),
    calendar_id: str = typer.Option("primary", help="Calendar ID."),
) -> None:
    """Delete an event."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    delete_event(clients.calendar.service, event_id, calendar_id=calendar_id)

    if state.json:
        state.console.print(format_output({"id": event_id, "status": "deleted"}, json_mode=True))
        return

    print_success(state.console, f"Event {event_id} deleted")


@app.command("open")
def open_cmd(
    ctx: typer.Context,
    event_id: str | None = typer.Argument(None, help="Optional Event ID to open."),
    calendar_id: str = typer.Option("primary", help="Calendar ID."),
) -> None:
    """Open Google Calendar in the browser."""
    state = CliState.from_ctx(ctx)
    
    if event_id:
        # Google Calendar event URLs are a bit tricky (base64 encoded), 
        # but we can use the eid parameter if we have it.
        # For simplicity, we'll just open the calendar if no ID, 
        # or try to construct a search URL if we have an ID.
        url = f"https://calendar.google.com/calendar/u/0/r/eventedit/{event_id}"
    else:
        url = "https://calendar.google.com/calendar"

    if state.json:
        state.console.print(format_output({"url": url}, json_mode=True))
        return

    state.console.print(f"Opening: {url}")
    webbrowser.open(url)


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
        clients.calendar.service,
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
