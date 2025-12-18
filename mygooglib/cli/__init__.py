"""Typer + Rich CLI for mygooglib.

Install:
    pip install -e ".[cli]"

Run:
    mygoog --help
"""

from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.traceback import install as install_rich_traceback

from mygooglib import get_clients
from mygooglib.exceptions import GoogleApiError

from . import auth as auth_cmd
from . import calendar as calendar_cmd
from . import contacts as contacts_cmd
from . import docs as docs_cmd
from . import drive as drive_cmd
from . import gmail as gmail_cmd
from . import sheets as sheets_cmd
from . import tasks as tasks_cmd
from . import workflows as workflows_cmd
from .common import CliState, configure_environment, format_output, print_error

app = typer.Typer(
    name="mygoog",
    help="Personal Google automation CLI (Drive/Sheets/Gmail/Calendar/Tasks/Docs).",
    add_completion=True,
    no_args_is_help=True,
)

app.add_typer(auth_cmd.app, name="auth")
app.add_typer(drive_cmd.app, name="drive")
app.add_typer(sheets_cmd.app, name="sheets")
app.add_typer(gmail_cmd.app, name="gmail")
app.add_typer(calendar_cmd.app, name="calendar")
app.add_typer(tasks_cmd.app, name="tasks")
app.add_typer(tasks_cmd.app, name="tasks")
app.add_typer(docs_cmd.app, name="docs")
app.add_typer(contacts_cmd.app, name="contacts")
app.add_typer(workflows_cmd.app, name="workflows")


@app.callback()
def _global_options(
    ctx: typer.Context,
    creds_path: Path | None = typer.Option(
        None,
        "--creds-path",
        help="Path to OAuth client credentials.json (overrides MYGOOGLIB_CREDENTIALS_PATH).",
        exists=False,
        dir_okay=False,
        file_okay=True,
        readable=True,
    ),
    token_path: Path | None = typer.Option(
        None,
        "--token-path",
        help="Path to token.json (overrides MYGOOGLIB_TOKEN_PATH).",
        exists=False,
        dir_okay=False,
        file_okay=True,
        readable=False,
        writable=True,
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Show full tracebacks and enable library debug logging.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit JSON to stdout (useful for scripting).",
    ),
) -> None:
    state = CliState(
        console=Console(stderr=False),
        err_console=Console(stderr=True),
        debug=debug,
        json=json_output,
        creds_path=creds_path,
        token_path=token_path,
    )
    ctx.obj = state

    configure_environment(state)
    # Ensure our output starts on a fresh line in terminals.
    # This avoids occasional visual artifacts where a long wrapped command line
    # appears adjacent to Rich output (notably in some captured terminal logs).
    if not json_output:
        state.console.line()
    if debug:
        install_rich_traceback(show_locals=False, suppress=[typer])


@app.command("version")
def version_cmd(ctx: typer.Context) -> None:
    """Print the library version."""
    state = CliState.from_ctx(ctx)
    # In a real package, we'd use importlib.metadata.version("mygooglib")
    # For this local dev setup, we'll just hardcode it or read from pyproject.toml
    version = "0.2.0"
    if state.json:
        state.console.print(format_output({"version": version}, json_mode=True))
    else:
        state.console.print(f"mygooglib v{version}")


@app.command("clients")
def clients_cmd(ctx: typer.Context) -> None:
    """Build clients and print which services are available."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    output = {
        "drive": bool(getattr(clients, "drive", None)),
        "sheets": bool(getattr(clients, "sheets", None)),
        "gmail": bool(getattr(clients, "gmail", None)),
        "calendar": bool(getattr(clients, "calendar", None)),
        "tasks": bool(getattr(clients, "tasks", None)),
        "docs": bool(getattr(clients, "docs", None)),
        "contacts": bool(getattr(clients, "contacts", None)),
    }
    state.console.print(format_output(output, json_mode=state.json))


def main() -> None:
    """Console script entrypoint."""
    try:
        app()
    except GoogleApiError as e:
        if os.environ.get("MYGOOGLIB_DEBUG"):
            raise
        console = Console(stderr=True)
        print_error(console, str(e))
        raise typer.Exit(code=2)
    except FileNotFoundError as e:
        if os.environ.get("MYGOOGLIB_DEBUG"):
            raise
        console = Console(stderr=True)
        print_error(console, str(e))
        raise typer.Exit(code=2)
    except (ValueError, NotADirectoryError) as e:
        if os.environ.get("MYGOOGLIB_DEBUG"):
            raise
        console = Console(stderr=True)
        print_error(console, str(e))
        raise typer.Exit(code=2)
    except KeyboardInterrupt:
        raise typer.Exit(code=130)
