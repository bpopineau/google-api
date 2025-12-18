from __future__ import annotations

from datetime import datetime, timezone

import typer
from google.oauth2.credentials import Credentials
from rich.table import Table

from mygooglib.auth import SCOPES, get_auth_paths, get_creds

from .common import CliState, format_output, print_kv, print_success

app = typer.Typer(help="Authentication helpers.", no_args_is_help=True)


@app.command("paths")
def paths_cmd(ctx: typer.Context) -> None:
    """Show where credentials.json and token.json are expected."""
    state = CliState.from_ctx(ctx)
    creds_path, token_path = get_auth_paths()

    if state.json:
        state.console.print(
            format_output(
                {"credentials": str(creds_path), "token": str(token_path)},
                json_mode=True,
            )
        )
        return

    table = Table(title="Auth paths", show_header=True, header_style="bold")
    table.add_column("Kind")
    table.add_column("Path")
    table.add_row("credentials.json", str(creds_path))
    table.add_row("token.json", str(token_path))
    state.console.print(table)


@app.command("login")
def login_cmd(ctx: typer.Context) -> None:
    """Run OAuth login (opens a browser) and save/refresh token.json."""
    state = CliState.from_ctx(ctx)
    _ = get_creds(scopes=SCOPES)
    creds_path, token_path = get_auth_paths()

    if state.json:
        state.console.print(format_output({"token": str(token_path)}, json_mode=True))
        return

    print_success(state.console, "OAuth credentials ready")
    print_kv(state.console, "token", token_path)


@app.command("refresh")
def refresh_cmd(ctx: typer.Context) -> None:
    """Force a token refresh without re-authenticating (no browser)."""
    from google.auth.transport.requests import Request

    state = CliState.from_ctx(ctx)
    _, token_path = get_auth_paths()

    creds = _load_token_only(token_path)
    if creds is None:
        state.console.print("[red]No token found. Run 'mygoog auth login' first.[/red]")
        raise typer.Exit(code=1)

    if not creds.refresh_token:
        state.console.print(
            "[red]Token has no refresh_token. Re-run 'mygoog auth login'.[/red]"
        )
        raise typer.Exit(code=1)

    old_expiry = creds.expiry

    try:
        creds.refresh(Request())
    except Exception as e:
        state.console.print(f"[red]Refresh failed: {e}[/red]")
        state.console.print(
            "[yellow]Your token may be revoked. Delete token.json and run 'mygoog auth login'.[/yellow]"
        )
        raise typer.Exit(code=1)

    token_path.write_text(creds.to_json(), encoding="utf-8")

    if state.json:
        state.console.print(
            format_output(
                {
                    "refreshed": True,
                    "old_expiry": old_expiry.isoformat() if old_expiry else None,
                    "new_expiry": creds.expiry.isoformat() if creds.expiry else None,
                },
                json_mode=True,
            )
        )
        return

    print_success(state.console, "Token refreshed")
    print_kv(state.console, "old_expiry", str(old_expiry))
    print_kv(state.console, "new_expiry", str(creds.expiry))


def _load_token_only(token_path) -> Credentials | None:
    if not token_path.exists():
        return None
    try:
        return Credentials.from_authorized_user_file(str(token_path), scopes=SCOPES)
    except Exception:
        return None


@app.command("status")
def status_cmd(ctx: typer.Context) -> None:
    """Check token.json presence and expiry without triggering OAuth."""
    state = CliState.from_ctx(ctx)
    _, token_path = get_auth_paths()

    creds = _load_token_only(token_path)
    if creds is None:
        if state.json:
            state.console.print(
                format_output(
                    {"token": str(token_path), "present": False}, json_mode=True
                )
            )
            return
        print_kv(state.console, "token", token_path)
        state.console.print("present: False")
        return

    expiry = getattr(creds, "expiry", None)
    expiry_iso = None
    if isinstance(expiry, datetime):
        expiry_iso = expiry.astimezone(timezone.utc).isoformat()

    payload = {
        "token": str(token_path),
        "present": True,
        "expired": bool(getattr(creds, "expired", None)),
        "valid": bool(getattr(creds, "valid", None)),
        "expiry": expiry_iso,
        "scopes": list(getattr(creds, "scopes", None) or []),
    }

    if state.json:
        state.console.print(format_output(payload, json_mode=True))
        return

    table = Table(title="Auth status", show_header=False)
    table.add_row("token", str(token_path))
    table.add_row("present", "True")
    table.add_row("valid", str(payload["valid"]))
    table.add_row("expired", str(payload["expired"]))
    table.add_row("expiry (UTC)", str(payload["expiry"]))
    state.console.print(table)
