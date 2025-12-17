from __future__ import annotations

import typer
from rich.table import Table

from mygooglib import get_clients
from mygooglib.sheets import append_row, get_range, update_range

from .common import CliState, format_output, print_kv, print_success

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
) -> None:
    """Read a range from a spreadsheet."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    values = get_range(
        clients.sheets,
        identifier,
        a1_range,
        drive=clients.drive,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
    )

    if state.json:
        state.console.print(format_output(values, json_mode=True))
        return

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
        clients.sheets,
        identifier,
        sheet_name,
        values,
        drive=clients.drive,
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
        clients.sheets,
        identifier,
        a1_range,
        values,
        drive=clients.drive,
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
