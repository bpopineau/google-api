from __future__ import annotations

import re
import webbrowser
from pathlib import Path

import typer
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table

from mygooglib import get_clients
from mygooglib.services.drive import (
    create_folder,
    delete_file,
    download_file,
    find_by_name,
    list_files,
    resolve_path,
    sync_folder,
    upload_file,
)

from .common import CliState, format_output, print_kv, print_success, prompt_selection

app = typer.Typer(help="Google Drive commands.", no_args_is_help=True)


def _resolve_id(identifier: str) -> str:
    """Helper to resolve a Drive ID or Path to an ID."""
    # Heuristic: Drive IDs are usually ~33 chars and alphanumeric (+ underscore/hyphen).
    # Human names/paths often have spaces, dots, or slashes, or are shorter.
    if re.match(r"^[a-zA-Z0-9_-]{25,}$", identifier):
        return identifier

    # Try resolving as path
    clients = get_clients()
    meta = resolve_path(clients.drive.service, identifier)
    if meta:
        return meta["id"]

    # Raise error if we can't resolve and it doesn't look like an ID
    raise typer.BadParameter(f"Could not resolve path or name: {identifier}")


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    query: str | None = typer.Option(
        None, "--query", "-q", help="Drive query string (q=...)."
    ),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Limit to a folder ID."
    ),
    mime_type: str | None = typer.Option(
        None, "--mime-type", help="Filter by MIME type."
    ),
    trashed: bool = typer.Option(False, "--trashed", help="Include trashed files."),
    page_size: int = typer.Option(100, "--page-size", min=1, max=1000),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactively select a file for actions."
    ),
) -> None:
    """List Drive files (paginates)."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_parent_id = _resolve_id(parent_id) if parent_id else None

    results = list_files(
        clients.drive.service,
        query=query,
        parent_id=real_parent_id,
        mime_type=mime_type,
        trashed=trashed,
        page_size=page_size,
    )

    if state.json:
        state.console.print(format_output(results, json_mode=True))
        return

    table = Table(title=f"Drive files ({len(results)})")
    if interactive:
        table.add_column("#", justify="right")
    table.add_column("name", overflow="fold")
    table.add_column("id", overflow="fold")
    table.add_column("mimeType", overflow="fold")
    table.add_column("modifiedTime")

    for i, item in enumerate(results, 1):
        row = [
            str(item.get("name") or ""),
            str(item.get("id") or ""),
            str(item.get("mimeType") or ""),
            str(item.get("modifiedTime") or ""),
        ]
        if interactive:
            row.insert(0, str(i))
        table.add_row(*row)

    state.console.print(table)

    if interactive and results:
        selected_id = prompt_selection(
            state.console, results, label_key="name", id_key="id"
        )
        if selected_id:
            # Offer actions for the selected file
            action = typer.prompt(
                "Action: [v]iew metadata, [o]pen in browser, [d]ownload, [delete], [q]uit",
                default="v",
            )
            if action == "v":
                find_cmd(ctx, selected_id)  # find_cmd can take ID too if we adjust it
            elif action == "o":
                open_cmd(ctx, selected_id)
            elif action == "d":
                dest = typer.prompt("Destination path", default=f"./{selected_id}")
                download_cmd(ctx, selected_id, Path(dest))
            elif action == "delete":
                delete_cmd(ctx, selected_id)


@app.command("find")
def find_cmd(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Exact filename to match."),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Limit search to this folder."
    ),
    mime_type: str | None = typer.Option(
        None, "--mime-type", help="Filter by MIME type."
    ),
) -> None:
    """Find a file by exact name."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    real_parent_id = _resolve_id(parent_id) if parent_id else None
    result = find_by_name(
        clients.drive.service, name, parent_id=real_parent_id, mime_type=mime_type
    )

    if state.json:
        state.console.print(format_output(result, json_mode=True))
        return

    if not result:
        state.console.print(f"File not found: {name}")
        raise typer.Exit(1)

    print_success(state.console, "Found")
    for k in ("name", "id", "mimeType", "modifiedTime"):
        print_kv(state.console, k, result.get(k))


@app.command("create-folder")
def create_folder_cmd(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Folder name."),
    parent_id: str | None = typer.Option(None, "--parent-id", help="Parent folder ID."),
) -> None:
    """Create a new folder."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()
    folder_id = create_folder(clients.drive.service, name, parent_id=parent_id)

    if state.json:
        state.console.print(format_output({"id": folder_id}, json_mode=True))
        return

    print_success(state.console, "Folder created")
    print_kv(state.console, "id", folder_id)


@app.command("upload")
def upload_cmd(
    ctx: typer.Context,
    local_path: Path = typer.Argument(
        ..., exists=True, dir_okay=False, file_okay=True, readable=True
    ),
    parent_id: str | None = typer.Option(
        None, "--parent-id", help="Destination folder ID."
    ),
    name: str | None = typer.Option(None, "--name", help="Override filename in Drive."),
) -> None:
    """Upload a local file to Drive."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_parent_id = _resolve_id(parent_id) if parent_id else None

    if state.json:
        file_id = upload_file(
            clients.drive.service, local_path, parent_id=real_parent_id, name=name
        )
        state.console.print(format_output({"id": file_id}, json_mode=True))
        return

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=state.console,
    ) as progress:
        task = progress.add_task(
            f"Uploading {local_path.name}", total=local_path.stat().st_size
        )

        def _cb(sent, total):
            progress.update(task, completed=sent, total=total)

        file_id = upload_file(
            clients.drive.service,
            local_path,
            parent_id=real_parent_id,
            name=name,
            progress_callback=_cb,
        )

    print_success(state.console, "Uploaded")
    print_kv(state.console, "id", file_id)


@app.command("download")
def download_cmd(
    ctx: typer.Context,
    file_id: str = typer.Argument(..., help="Drive file ID."),
    dest_path: Path = typer.Argument(..., help="Local destination path."),
    export_mime_type: str | None = typer.Option(
        None,
        "--export-mime-type",
        help="For Google Docs/Sheets/Slides, export as this MIME type (e.g., application/pdf).",
    ),
) -> None:
    """Download a Drive file (export for Google Workspace files)."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_file_id = _resolve_id(file_id)

    if state.json:
        out_path = download_file(
            clients.drive.service,
            real_file_id,
            dest_path,
            export_mime_type=export_mime_type,
        )
        state.console.print(format_output({"path": str(out_path)}, json_mode=True))
        return

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=state.console,
    ) as progress:
        task = progress.add_task(f"Downloading {file_id}", total=None)

        def _cb(received, total):
            progress.update(task, completed=received, total=total)

        out_path = download_file(
            clients.drive.service,
            real_file_id,
            dest_path,
            export_mime_type=export_mime_type,
            progress_callback=_cb,
        )

    print_success(state.console, "Downloaded")
    print_kv(state.console, "path", out_path)


@app.command("sync")
def sync_cmd(
    ctx: typer.Context,
    local_path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    drive_folder_id: str = typer.Argument(..., help="Target Drive folder ID."),
    recursive: bool = typer.Option(
        True, "--recursive/--no-recursive", help="Sync subfolders recursively."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without making changes."
    ),
) -> None:
    """Sync a local folder to a Drive folder (safe: no deletes)."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_folder_id = _resolve_id(drive_folder_id)

    if state.json:
        summary = sync_folder(
            clients.drive.service,
            local_path,
            real_folder_id,
            recursive=recursive,
            dry_run=dry_run,
        )
        state.console.print(format_output(summary, json_mode=True))
        return

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        console=state.console,
    ) as progress:
        task = progress.add_task("Syncing...", total=None)

        def _cb(current, total, item_name):
            progress.update(
                task,
                completed=current,
                total=total,
                description=f"Syncing: {item_name}",
            )

        summary = sync_folder(
            clients.drive.service,
            local_path,
            real_folder_id,
            recursive=recursive,
            dry_run=dry_run,
            progress_callback=_cb,
        )

    if dry_run:
        state.console.print("[bold yellow]DRY RUN - No changes made[/bold yellow]")

    print_success(state.console, "Sync complete" if not dry_run else "Dry run complete")
    for k in ("created", "updated", "skipped"):
        print_kv(state.console, k, summary.get(k))
    errors = summary.get("errors") or []
    if errors:
        state.err_console.print(f"errors: {len(errors)}")
        for err in errors:
            state.err_console.print(f"- {err}")


@app.command("delete")
def delete_cmd(
    ctx: typer.Context,
    file_id: str = typer.Argument(..., help="Drive file ID."),
    permanent: bool = typer.Option(
        False, "--permanent", help="Delete permanently instead of moving to trash."
    ),
) -> None:
    """Delete a file or move it to trash."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_file_id = _resolve_id(file_id)
    delete_file(clients.drive.service, real_file_id, permanent=permanent)

    if state.json:
        state.console.print(
            format_output(
                {"id": real_file_id, "deleted": True, "permanent": permanent},
                json_mode=True,
            )
        )
        return

    print_success(state.console, "Deleted" if permanent else "Moved to trash")
    print_kv(state.console, "id", real_file_id)


@app.command("open")
def open_cmd(
    ctx: typer.Context,
    file_id: str = typer.Argument(..., help="Drive file ID."),
) -> None:
    """Open a Drive file in the default web browser."""
    state = CliState.from_ctx(ctx)
    clients = get_clients()

    real_file_id = _resolve_id(file_id)

    # Get webViewLink
    meta = (
        clients.drive.service.files()
        .get(fileId=real_file_id, fields="webViewLink")
        .execute()
    )
    link = meta.get("webViewLink")

    if not link:
        state.console.print(f"[red]Could not find webViewLink for file {file_id}[/red]")
        raise typer.Exit(1)

    if state.json:
        state.console.print(format_output({"id": file_id, "url": link}, json_mode=True))
        return

    state.console.print(f"Opening: {link}")
    webbrowser.open(link)
