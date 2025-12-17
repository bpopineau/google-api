"""Minimal smoke tests for mygooglib.

This script is intentionally conservative:
- It does not make API calls unless you pass explicit flags.
- It never prints tokens/credentials.

Examples:
  # Show available options
  python scripts/smoke_test.py --help

    # Drive: sync a local folder into a Drive folder
    python scripts/smoke_test.py drive-sync --local-path "C:\\path\\to\\folder" --drive-folder-id "<FOLDER_ID>"

    # Run a full smoke pass (read-only by default)
    python scripts/smoke_test.py all

    # Run the full smoke pass including writes (sends an email, appends a row, updates a cell)
    python scripts/smoke_test.py all --write

  # Gmail: send an email to yourself
  python scripts/smoke_test.py gmail-send --to you@example.com --subject "Test" --body "Hello"

  # Gmail: search and (optionally) mark the first result as read
  python scripts/smoke_test.py gmail-search --query "newer_than:1d" --max 5
  python scripts/smoke_test.py gmail-search --query "is:unread newer_than:7d" --max 1 --mark-read

  # Sheets: read a range
    python scripts/smoke_test.py sheets-get --identifier <ID_OR_TITLE_OR_URL> --range "Sheet1!A1:C3"

  # Sheets: append a row
    python scripts/smoke_test.py sheets-append --identifier <ID_OR_TITLE_OR_URL> --sheet "Sheet1" --values "a" "b" "c"
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from typing import Any

from mygooglib import get_clients

# Defaults for local testing (safe to keep in-repo for personal use).
DEFAULT_TEST_SPREADSHEET_IDENTIFIER = "17KBIrDF3CZ0s5U8QQf0aUHmkttVbkHWt44-ApGFTvSw"
DEFAULT_TEST_EMAIL_TO = "brandon@esscoelectric.com"

# Safe default ranges/targets for smoke operations.
DEFAULT_TEST_SHEETS_READ_RANGE = "Sheet1!A1:C3"
DEFAULT_TEST_SHEETS_APPEND_SHEET = "Sheet1"
DEFAULT_TEST_SHEETS_UPDATE_RANGE = "Sheet1!Z1:Z1"
DEFAULT_TEST_GMAIL_QUERY = "newer_than:7d"


def _print_jsonable(obj: Any) -> None:
    # Keep output small and readable; avoid printing huge payloads.
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        print(obj)
        return
    if isinstance(obj, list):
        print(f"list[{len(obj)}]")
        for i, item in enumerate(obj[:10]):
            print(f"  [{i}] {item}")
        if len(obj) > 10:
            print("  ...")
        return
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        print(f"dict[{len(keys)}] keys={keys}")
        # print a few important keys if present
        for k in (
            "id",
            "threadId",
            "created",
            "updated",
            "skipped",
            "errors",
            "updatedRange",
            "updatedRows",
            "updatedCells",
        ):
            if k in obj:
                print(f"  {k}: {obj.get(k)}")
        return
    print(repr(obj))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke tests for mygooglib")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_all = sub.add_parser(
        "all",
        help=(
            "Run a full smoke pass across Drive/Sheets/Gmail. "
            "Read-only by default; use --write for mutations."
        ),
    )
    p_all.add_argument(
        "--write",
        action="store_true",
        help="Enable write operations (sends an email + writes to Sheets + optional Drive sync)",
    )
    p_all.add_argument(
        "--drive-sync-local-path",
        default=None,
        help="If provided with --drive-sync-folder-id, performs a Drive sync",
    )
    p_all.add_argument(
        "--drive-sync-folder-id",
        default=None,
        help="If provided with --drive-sync-local-path, performs a Drive sync",
    )
    p_all.add_argument(
        "--sheets-identifier",
        default=DEFAULT_TEST_SPREADSHEET_IDENTIFIER,
        help=f"Sheets identifier (default {DEFAULT_TEST_SPREADSHEET_IDENTIFIER})",
    )
    p_all.add_argument(
        "--sheets-read-range",
        default=DEFAULT_TEST_SHEETS_READ_RANGE,
        help=f"Sheets A1 range to read (default {DEFAULT_TEST_SHEETS_READ_RANGE})",
    )
    p_all.add_argument(
        "--sheets-append-sheet",
        default=DEFAULT_TEST_SHEETS_APPEND_SHEET,
        help=f"Sheet/tab name to append into (default {DEFAULT_TEST_SHEETS_APPEND_SHEET})",
    )
    p_all.add_argument(
        "--sheets-update-range",
        default=DEFAULT_TEST_SHEETS_UPDATE_RANGE,
        help=f"Sheets A1 range to update (default {DEFAULT_TEST_SHEETS_UPDATE_RANGE})",
    )
    p_all.add_argument(
        "--gmail-query",
        default=DEFAULT_TEST_GMAIL_QUERY,
        help=f"Gmail search query (default {DEFAULT_TEST_GMAIL_QUERY})",
    )
    p_all.add_argument(
        "--gmail-max",
        type=int,
        default=3,
        help="Max Gmail results to print (default 3)",
    )
    p_all.add_argument(
        "--mark-read",
        action="store_true",
        help="Mark the first returned Gmail message as read",
    )
    p_all.add_argument(
        "--email-to",
        default=DEFAULT_TEST_EMAIL_TO,
        help=f"Recipient for test email when --write is enabled (default {DEFAULT_TEST_EMAIL_TO})",
    )

    p_drive_sync = sub.add_parser(
        "drive-sync",
        help="Sync a local folder into a Drive folder (upload/update only; no deletes)",
    )
    p_drive_sync.add_argument(
        "--local-path",
        required=True,
        help="Local folder path to sync",
    )
    p_drive_sync.add_argument(
        "--drive-folder-id",
        required=True,
        help="Destination Drive folder id",
    )

    p_send = sub.add_parser("gmail-send", help="Send a test email")
    p_send.add_argument(
        "--to",
        default=DEFAULT_TEST_EMAIL_TO,
        help=f"Recipient email (default {DEFAULT_TEST_EMAIL_TO})",
    )
    p_send.add_argument("--subject", required=True, help="Subject")
    p_send.add_argument("--body", required=True, help="Plain text body")
    p_send.add_argument("--cc", default=None, help="CC email(s), comma-separated")
    p_send.add_argument("--bcc", default=None, help="BCC email(s), comma-separated")
    p_send.add_argument(
        "--attach", action="append", default=[], help="Attachment path (repeatable)"
    )

    p_search = sub.add_parser("gmail-search", help="Search messages")
    p_search.add_argument("--query", required=True, help="Gmail search query")
    p_search.add_argument("--max", type=int, default=5, help="Max results (default 5)")
    p_search.add_argument(
        "--mark-read",
        action="store_true",
        help="Mark the first returned message as read",
    )

    p_get = sub.add_parser("sheets-get", help="Read a range from Sheets")
    p_get.add_argument(
        "--identifier",
        default=DEFAULT_TEST_SPREADSHEET_IDENTIFIER,
        help=(
            "Spreadsheet id, title, or full URL "
            f"(default {DEFAULT_TEST_SPREADSHEET_IDENTIFIER})"
        ),
    )
    p_get.add_argument("--range", required=True, help='A1 range, e.g. "Sheet1!A1:C3"')
    p_get.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_get.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_append = sub.add_parser("sheets-append", help="Append a row to a sheet")
    p_append.add_argument(
        "--identifier",
        default=DEFAULT_TEST_SPREADSHEET_IDENTIFIER,
        help=(
            "Spreadsheet id, title, or full URL "
            f"(default {DEFAULT_TEST_SPREADSHEET_IDENTIFIER})"
        ),
    )
    p_append.add_argument("--sheet", required=True, help="Sheet/tab name")
    p_append.add_argument("--values", nargs="+", required=True, help="Row values")
    p_append.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_append.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_update = sub.add_parser("sheets-update", help="Update a range in Sheets")
    p_update.add_argument(
        "--identifier",
        default=DEFAULT_TEST_SPREADSHEET_IDENTIFIER,
        help=(
            "Spreadsheet id, title, or full URL "
            f"(default {DEFAULT_TEST_SPREADSHEET_IDENTIFIER})"
        ),
    )
    p_update.add_argument(
        "--range",
        required=True,
        help='A1 range, e.g. "Sheet1!A1:C3"',
    )
    p_update.add_argument(
        "--row",
        action="append",
        required=True,
        help=(
            "Row values, comma-separated (repeat for multiple rows). "
            "Example: --row a,b,c --row 1,2,3"
        ),
    )
    p_update.add_argument(
        "--user-entered",
        action="store_true",
        help="Use USER_ENTERED (default is RAW)",
    )
    p_update.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_update.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_open = sub.add_parser(
        "sheets-open-by-title", help="Resolve spreadsheet id by title"
    )
    p_open.add_argument("--title", required=True, help="Exact spreadsheet title")
    p_open.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope the search",
    )
    p_open.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple matches (returns the first)",
    )

    p_resolve = sub.add_parser(
        "sheets-resolve",
        help="Resolve a spreadsheet ID/title/URL to an id",
    )
    p_resolve.add_argument(
        "--identifier",
        default=DEFAULT_TEST_SPREADSHEET_IDENTIFIER,
        help=(
            "Spreadsheet id, title, or full URL "
            f"(default {DEFAULT_TEST_SPREADSHEET_IDENTIFIER})"
        ),
    )
    p_resolve.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_resolve.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    clients = get_clients()

    if args.cmd == "all":
        now = datetime.now(timezone.utc).isoformat()

        print("== Drive: list (root, first 5) ==")
        files = clients.drive.list_files(page_size=5)
        _print_jsonable(files)

        if args.drive_sync_local_path and args.drive_sync_folder_id:
            if not args.write:
                print("== Drive: sync_folder skipped (provide --write to enable) ==")
            else:
                print("== Drive: sync_folder ==")
                summary = clients.drive.sync_folder(
                    args.drive_sync_local_path,
                    args.drive_sync_folder_id,
                )
                _print_jsonable(summary)
        else:
            print(
                "== Drive: sync_folder skipped (missing --drive-sync-local-path/--drive-sync-folder-id) =="
            )

        print("== Sheets: get_range ==")
        values = clients.sheets.get_range(
            args.sheets_identifier,
            args.sheets_read_range,
        )
        _print_jsonable(values)

        if args.write:
            print("== Sheets: append_row ==")
            append_result = clients.sheets.append_row(
                args.sheets_identifier,
                args.sheets_append_sheet,
                ["mygooglib-smoke", now],
            )
            _print_jsonable(append_result)

            print("== Sheets: update_range ==")
            update_result = clients.sheets.update_range(
                args.sheets_identifier,
                args.sheets_update_range,
                [[now]],
                value_input_option="RAW",
            )
            _print_jsonable(update_result)
        else:
            print("== Sheets: write ops skipped (use --write) ==")

        print("== Gmail: search_messages ==")
        results = clients.gmail.search_messages(
            args.gmail_query,
            max_results=args.gmail_max,
        )
        _print_jsonable(results)
        if args.mark_read and results:
            msg_id = results[0].get("id")
            if msg_id:
                if args.write:
                    clients.gmail.mark_read(msg_id)
                    print(f"marked read: {msg_id}")
                else:
                    print("mark_read skipped (use --write)")

        if args.write:
            print("== Gmail: send_email ==")
            message_id = clients.gmail.send_email(
                to=args.email_to,
                subject=f"mygooglib smoke all {now}",
                body=f"mygooglib smoke all run at {now}",
            )
            print("sent message id:")
            _print_jsonable(message_id)
        else:
            print("== Gmail: send_email skipped (use --write) ==")

        print("== Calendar: list_events (primary, next 7 days) ==")
        now_dt = datetime.now(timezone.utc)
        next_week = now_dt + timedelta(days=7)
        events = clients.calendar.list_events(time_min=now_dt, time_max=next_week)
        _print_jsonable(events)

        if args.write:
            print("== Calendar: add_event ==")
            event_id = clients.calendar.add_event(
                summary=f"mygooglib smoke test {now}",
                start=now_dt + timedelta(hours=1),
                duration_minutes=30,
            )
            print(f"added event id: {event_id}")
        else:
            print("== Calendar: add_event skipped (use --write) ==")

        print("== Tasks: list_tasklists ==")
        tasklists = clients.tasks.list_tasklists()
        _print_jsonable(tasklists)

        print("== Tasks: list_tasks (@default) ==")
        tasks = clients.tasks.list_tasks()
        _print_jsonable(tasks)

        if args.write:
            print("== Tasks: add_task ==")
            task_id = clients.tasks.add_task(
                title=f"mygooglib smoke task {now}",
                due=now_dt + timedelta(days=1),
            )
            print(f"added task id: {task_id}")
        else:
            print("== Tasks: add_task skipped (use --write) ==")

        return 0

    if args.cmd == "drive-sync":
        summary = clients.drive.sync_folder(
            args.local_path,
            args.drive_folder_id,
        )
        _print_jsonable(summary)
        return 0

    if args.cmd == "gmail-send":
        cc = [s.strip() for s in (args.cc or "").split(",") if s.strip()] or None
        bcc = [s.strip() for s in (args.bcc or "").split(",") if s.strip()] or None
        message_id = clients.gmail.send_email(
            to=args.to,
            subject=args.subject,
            body=args.body,
            attachments=args.attach or None,
            cc=cc,
            bcc=bcc,
        )
        print("sent message id:")
        _print_jsonable(message_id)
        return 0

    if args.cmd == "gmail-search":
        results = clients.gmail.search_messages(args.query, max_results=args.max)
        _print_jsonable(results)
        if args.mark_read and results:
            msg_id = results[0].get("id")
            if msg_id:
                clients.gmail.mark_read(msg_id)
                print(f"marked read: {msg_id}")
        return 0

    if args.cmd == "sheets-get":
        values = clients.sheets.get_range(
            args.identifier,
            args.range,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(values)
        return 0

    if args.cmd == "sheets-append":
        result = clients.sheets.append_row(
            args.identifier,
            args.sheet,
            args.values,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(result)
        return 0

    if args.cmd == "sheets-update":
        values = [row.split(",") for row in args.row]
        result = clients.sheets.update_range(
            args.identifier,
            args.range,
            values,
            value_input_option="USER_ENTERED" if args.user_entered else "RAW",
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(result)
        return 0

    if args.cmd == "sheets-open-by-title":
        sheet_id = clients.sheets.open_by_title(
            args.title,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        print("spreadsheet id:")
        _print_jsonable(sheet_id)
        return 0

    if args.cmd == "sheets-resolve":
        sheet_id = clients.sheets.resolve_spreadsheet(
            args.identifier,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        print("spreadsheet id:")
        _print_jsonable(sheet_id)
        return 0

    raise AssertionError(f"Unhandled command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
