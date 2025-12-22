from __future__ import annotations

import datetime as dt
import webbrowser
from typing import Any, cast

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from mygooglib import get_clients
from mygooglib.services.tasks import (
    add_task,
    complete_task,
    delete_task,
    list_tasklists,
    list_tasks,
)

from .common import CliState, format_output, print_kv, print_success, prompt_selection

app = typer.Typer(help="Google Tasks commands.", no_args_is_help=True)


@app.command("list-lists")
def list_lists_cmd(
    ctx: typer.Context,
    max_results: int = typer.Option(100, help="Max results."),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively select a list."
    ),
) -> None:
    """List task lists."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    results = list_tasklists(clients.tasks.service, max_results=max_results)

    # Ensure results is a list
    if not isinstance(results, list):
        results = results.get("items", [])

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Task lists ({len(results)})")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("title", overflow="fold")
    table.add_column("id", overflow="fold")

    for i, item in enumerate(results, 1):
        row = [
            str(item.get("title") or ""),
            str(item.get("id") or ""),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)

    state.console.print(table)

    if interactive and results:
        results_list = cast(list[dict[Any, Any]], results)
        selected = prompt_selection(
            state.console, results_list, label_key="title", id_key=None
        )
        if selected:
            action = typer.prompt(
                "Action: [l]ist tasks, [o]pen in browser, [q]uit", default="l"
            )
            if action == "l":
                list_cmd(ctx, tasklist_id=selected["id"])
            elif action == "o":
                open_cmd(ctx, tasklist_id=selected["id"])


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
    completed: bool = typer.Option(
        True, "--completed/--no-completed", help="Show completed."
    ),
    max_results: int = typer.Option(100, help="Max results."),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively select a task for actions."
    ),
) -> None:
    """List tasks."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=state.console,
        transient=True,
    ) as progress:
        task = progress.add_task("Fetching tasks...", total=None)

        def update_progress(count: int) -> None:
            progress.update(task, advance=count)

        results = list_tasks(
            clients.tasks.service,
            tasklist_id=tasklist_id,
            show_completed=completed,
            max_results=max_results,
            progress_callback=update_progress,
        )

    # Ensure results is a list
    if not isinstance(results, list):
        results = results.get("items", [])

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Tasks ({len(results)})")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("status", width=10)
    table.add_column("title", overflow="fold")
    table.add_column("due")
    table.add_column("id", overflow="fold")

    for i, item in enumerate(results, 1):
        status = item.get("status") or ""
        style = "green" if status == "completed" else "yellow"
        row = [
            f"[{style}]{status}[/{style}]",
            str(item.get("title") or ""),
            str(item.get("due") or ""),
            str(item.get("id") or ""),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)

    state.console.print(table)

    if interactive and results:
        tasks_list = cast(list[dict[Any, Any]], results)
        selected = prompt_selection(
            state.console, tasks_list, label_key="title", id_key=None
        )
        if selected:
            action = typer.prompt(
                "Action: [v]iew, [c]omplete, [d]elete, [q]uit", default="v"
            )
            if action == "v":
                state.console.print(format_output(selected, json_mode=False))
            elif action == "c":
                complete_cmd(ctx, selected["id"], tasklist_id=tasklist_id)
            elif action == "d":
                if typer.confirm(f"Delete task '{selected.get('title')}'?"):
                    delete_cmd(ctx, selected["id"], tasklist_id=tasklist_id)


@app.command("delete")
def delete_cmd(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID to delete."),
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
) -> None:
    """Delete a task."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    delete_task(clients.tasks.service, task_id, tasklist_id=tasklist_id)

    if state.json:
        state.console.print(
            format_output({"id": task_id, "status": "deleted"}, json_mode=True)
        )
        return

    print_success(state.console, f"Task {task_id} deleted")


@app.command("open")
def open_cmd(
    ctx: typer.Context,
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
) -> None:
    """Open Google Tasks in the browser."""
    state = CliState.from_ctx(ctx)

    # Tasks doesn't have a great direct URL for specific lists,
    # but we can open the side panel in Gmail or Calendar.
    # The most direct "full screen" tasks is actually via Canvas or a specific URL.
    url = "https://tasks.google.com/embed/list/~default"
    if tasklist_id != "@default":
        url = f"https://tasks.google.com/embed/list/{tasklist_id}"

    if state.json:
        state.console.print(format_output({"url": url}, json_mode=True))
        return

    state.console.print(f"Opening: {url}")
    webbrowser.open(url)


@app.command("add")
def add_cmd(
    ctx: typer.Context,
    title: str = typer.Argument(..., help="Task title."),
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
    notes: str | None = typer.Option(None, help="Notes."),
    due: dt.datetime | None = typer.Option(None, help="Due date."),
) -> None:
    """Add a new task."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    task_id = add_task(
        clients.tasks.service,
        title=title,
        tasklist_id=tasklist_id,
        notes=notes,
        due=due,
    )

    if state.json:
        state.console.print(format_output({"id": task_id}, json_mode=True))
        return

    print_success(state.console, "Task added")
    print_kv(state.console, "id", task_id)


@app.command("complete")
def complete_cmd(
    ctx: typer.Context,
    task_id: str | None = typer.Argument(
        None, help="Task ID. If omitted, interactive mode starts."
    ),
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
) -> None:
    """Mark a task as completed."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    if not task_id:
        # Interactive mode
        tasks = list_tasks(
            clients.tasks.service, tasklist_id=tasklist_id, show_completed=False
        )
        # Ensure tasks is a list
        if not isinstance(tasks, list):
            tasks = tasks.get("items", [])

        if not tasks:
            state.console.print("No pending tasks found.")
            return

        table = Table(title="Pending Tasks")
        table.add_column("#", justify="right")
        table.add_column("title")
        table.add_column("id")

        for i, t in enumerate(tasks, 1):
            table.add_row(str(i), t.get("title"), t.get("id"))

        state.console.print(table)
        tasks_casted = cast(list[dict[Any, Any]], tasks)
        task_id = prompt_selection(
            state.console, tasks_casted, label_key="title", id_key="id"
        )
        if not task_id:
            return

    complete_task(clients.tasks.service, task_id, tasklist_id=tasklist_id)

    if state.json:
        state.console.print(
            format_output({"id": task_id, "status": "completed"}, json_mode=True)
        )
        return

    print_success(state.console, f"Task completed: {task_id}")

