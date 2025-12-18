from __future__ import annotations

import webbrowser

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from mygooglib import get_clients
from mygooglib.sheets import (
    append_row,
    get_range,
    get_sheets,
    to_dataframe,
    update_range,
)

from .common import CliState, format_output, print_kv, print_success, prompt_selection

app = typer.Typer(help="Google Sheets commands.", no_args_is_help=True)


def _parse_rows(rows: list[str], *, delimiter: str) -> list[list[str]]:
    parsed: list[list[str]] = []
    for row in rows:
        parsed.append([cell.strip() for cell in row.split(delimiter)])
    return parsed


@app.command("get")
def get_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
    a1_range: str = typer.Argument(..., help='A1 range, e.g. "Sheet1!A1:C10".'),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Optional Drive folder ID to scope title searches."
    ),
    allow_multiple: bool = typer.Option(
        False, "--allow-multiple", help="Allow multiple title matches (uses first)."
    ),
    chunk_size: int | None = typer.Option(
        None, "--chunk-size", help="Read in chunks of this many rows/cols."
    ),
) -> None:
    """Read a range from a spreadsheet."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    if state.json or not chunk_size:
        values = get_range(
            clients.sheets.service,
            identifier,
            a1_range,
            drive=clients.drive.service,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            chunk_size=chunk_size,
        )
        if state.json:
            state.console.print(format_output(values, json_mode=True))
            return
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=state.console,
        ) as progress:
            task = progress.add_task("Reading range...", total=None)

            def _cb(current, total):
                progress.update(
                    task,
                    completed=current,
                    total=total,
                    description=f"Reading: {current}/{total}",
                )

            values = get_range(
                clients.sheets.service,
                identifier,
                a1_range,
                drive=clients.drive.service,
                parent_id=parent_id,
                allow_multiple=allow_multiple,
                chunk_size=chunk_size,
                progress_callback=_cb,
            )

    table = Table(title="Values")
    table.add_column("row")
    for r in values:
        table.add_row(str(r))
    state.console.print(table)


@app.command("append")
def append_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
    sheet_name: str = typer.Argument(..., help="Sheet/tab name."),
    values: list[str] = typer.Argument(..., help="Cell values for the appended row."),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Optional Drive folder ID to scope title searches."
    ),
    allow_multiple: bool = typer.Option(
        False, "--allow-multiple", help="Allow multiple title matches (uses first)."
    ),
    user_entered: bool = typer.Option(
        False, "--user-entered", help="Use USER_ENTERED input option."
    ),
) -> None:
    """Append one row to a sheet."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    result = append_row(
        clients.sheets.service,
        identifier,
        sheet_name,
        values,
        drive=clients.drive.service,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
        value_input_option="USER_ENTERED" if user_entered else "RAW",
    )

    if state.json:
        state.console.print(format_output(result or {}, json_mode=True))
        return

    print_success(state.console, "Row appended")
    if result:
        for k, v in result.items():
            print_kv(state.console, k, v)


@app.command("update")
def update_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
    a1_range: str = typer.Argument(..., help='A1 range, e.g. "Sheet1!A1:B2".'),
    row: list[str] = typer.Option(
        ...,
        "--row",
        help='Row values as a delimited string (repeat flag for multiple rows). Example: --row "a,b" --row "c,d"',
    ),
    delimiter: str = typer.Option(
        ",", "--delimiter", help="Delimiter for --row parsing."
    ),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Optional Drive folder ID to scope title searches."
    ),
    allow_multiple: bool = typer.Option(
        False, "--allow-multiple", help="Allow multiple title matches (uses first)."
    ),
    user_entered: bool = typer.Option(
        False, "--user-entered", help="Use USER_ENTERED input option."
    ),
) -> None:
    """Update a range in a spreadsheet."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    values = _parse_rows(row, delimiter=delimiter)

    result = update_range(
        clients.sheets.service,
        identifier,
        a1_range,
        values,
        drive=clients.drive.service,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
        value_input_option="USER_ENTERED" if user_entered else "RAW",
    )

    if state.json:
        state.console.print(format_output(result or {}, json_mode=True))
        return

    print_success(state.console, "Range updated")
    if result:
        for k, v in result.items():
            print_kv(state.console, k, v)


@app.command("list-tabs")
def list_tabs_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Optional Drive folder ID to scope title searches."
    ),
    allow_multiple: bool = typer.Option(
        False, "--allow-multiple", help="Allow multiple title matches (uses first)."
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively select a tab for actions."
    ),
) -> None:
    """List all sheets (tabs) in a spreadsheet."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    results = get_sheets(
        clients.sheets.service,
        identifier,
        drive=clients.drive.service,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
    )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Sheets in {identifier}")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("index", justify="right")
    table.add_column("title")
    table.add_column("id")
    table.add_column("type")

    for i, s in enumerate(results, 1):
        row = [
            str(s.get("index")),
            str(s.get("title")),
            str(s.get("id")),
            str(s.get("type")),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)
    state.console.print(table)

    if interactive and results:
        selected_title = prompt_selection(
            state.console, results, label_key="title", id_key="title"
        )
        if selected_title:
            action = typer.prompt(
                "Action: [g]et range, [a]ppend row, [q]uit", default="g"
            )
            if action == "g":
                a1 = typer.prompt("A1 range", default=f"{selected_title}!A1:Z100")
                get_cmd(ctx, identifier, a1)
            elif action == "a":
                vals = typer.prompt("Values (comma separated)")
                append_cmd(ctx, identifier, selected_title, vals.split(","))


@app.command("open")
def open_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
) -> None:
    """Open a spreadsheet in the default web browser."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    from mygooglib.sheets import resolve_spreadsheet

    spreadsheet_id = resolve_spreadsheet(clients.drive.service, identifier)

    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    if state.json:
        state.console.print(
            format_output({"id": spreadsheet_id, "url": url}, json_mode=True)
        )
        return

    state.console.print(f"Opening: {url}")
    webbrowser.open(url)


@app.command("to-df")
def to_df_cmd(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Spreadsheet ID, title, or URL."),
    a1_range: str = typer.Argument(..., help='A1 range, e.g. "Sheet1!A1:C10".'),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Optional Drive folder ID."
    ),
    header: bool = typer.Option(True, help="Use first row as header."),
) -> None:
    """Read a range into a Pandas DataFrame and print as CSV.

    Requires 'pandas' to be installed.
    """
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    try:
        df = to_dataframe(
            clients.sheets.service,
            identifier,
            a1_range,
            drive=clients.drive.service,
            header=header,
        )
    except ImportError:
        state.console.print("[red]Error:[/red] 'pandas' not installed.")
        state.console.print("Run: pip install '.[data]'")
        raise typer.Exit(1)

    if state.json:
        # JSON output for DataFrame
        import json

        state.console.print(json.dumps(df.to_dict(orient="records")))
    else:
        # Default behavior: Print CSV to stdout
        print(df.to_csv(index=False))
