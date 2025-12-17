from __future__ import annotations

import datetime as dt

import typer
from rich.prompt import Prompt
from rich.table import Table

from mygooglib import get_clients
from mygooglib.tasks import add_task, complete_task, list_tasklists, list_tasks

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Google Tasks commands.", no_args_is_help=True)


@app.command("list-lists")
def list_lists_cmd(
    ctx: typer.Context,
    max_results: int = typer.Option(100, help="Max results."),
) -> None:
    """List task lists."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    results = list_tasklists(clients.tasks, max_results=max_results)

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Task lists ({len(results)})")
    table.add_column("title", overflow="fold")
    table.add_column("id", overflow="fold")

    for item in results:
        table.add_row(
            str(item.get("title") or ""),
            str(item.get("id") or ""),
        )

    state.console.print(table)


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    tasklist_id: str = typer.Option("@default", help="Task list ID."),
    completed: bool = typer.Option(
        True, "--completed/--no-completed", help="Show completed."
    ),
    max_results: int = typer.Option(100, help="Max results."),
) -> None:
    """List tasks."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    results = list_tasks(
        clients.tasks,
        tasklist_id=tasklist_id,
        show_completed=completed,
        max_results=max_results,
    )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Tasks ({len(results)})")
    table.add_column("status", width=10)
    table.add_column("title", overflow="fold")
    table.add_column("due")
    table.add_column("id", overflow="fold")

    for item in results:
        status = item.get("status") or ""
        style = "green" if status == "completed" else "yellow"
        table.add_row(
            f"[{style}]{status}[/{style}]",
            str(item.get("title") or ""),
            str(item.get("due") or ""),
            str(item.get("id") or ""),
        )

    state.console.print(table)


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
        clients.tasks,
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
        tasks = list_tasks(clients.tasks, tasklist_id=tasklist_id, show_completed=False)
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
        choice = Prompt.ask(
            "Select task number to complete (or 'q' to quit)", default="q"
        )
        if choice.lower() == "q":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tasks):
                task_id = tasks[idx]["id"]
            else:
                state.console.print("[red]Invalid selection.[/red]")
                return
        except ValueError:
            state.console.print("[red]Invalid input.[/red]")
            return

    complete_task(clients.tasks, task_id, tasklist_id=tasklist_id)

    if state.json:
        state.console.print(
            format_output({"id": task_id, "status": "completed"}, json_mode=True)
        )
        return

    print_success(state.console, f"Task completed: {task_id}")
