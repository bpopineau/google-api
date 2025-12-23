"""Unified Debug Console (REPL)."""
from typing import Any

from IPython import start_ipython  # type: ignore
from traitlets.config import Config  # type: ignore

from mygooglib import (
    AppConfig,
    get_clients,
    get_creds,
)
from mygooglib.core.utils import logging
from mygooglib.core import types

def build_context() -> dict[str, Any]:
    """Build the context dictionary for the REPL."""
    print("Initializing Unified Debug Console...")
    
    # 1. Auth & Clients
    try:
        clients = get_clients()
        print("✅ Authenticated and Clients initialized.")
    except Exception as e:
        print(f"⚠️  Authentication failed: {e}")
        print("   Running without active clients. Use 'get_clients()' to retry.")
        clients = None

    context = {
        "clients": clients,
        "get_clients": get_clients,
        "get_creds": get_creds,
        "AppConfig": AppConfig,
        "config": AppConfig(),
        "get_logger": logging.get_logger,
        "types": types,
    }

    # Add services shortcuts
    if clients:
        context.update({
            "drive": clients.drive,
            "sheets": clients.sheets,
            "gmail": clients.gmail,
            "calendar": clients.calendar,
            "tasks": clients.tasks,
            "drv": clients.drive,
            "sht": clients.sheets,
            "gml": clients.gmail,
            "cal": clients.calendar,
            "tsk": clients.tasks,
        })
    
    # Add types to global namespace
    for name in dir(types):
        if not name.startswith("_") and name[0].isupper():
             context[name] = getattr(types, name)

    return context

def start_console() -> None:
    """Start the interactive IPython session."""
    context = build_context()
    
    c = Config()
    c.InteractiveShell.colors = "Neutral"
    c.InteractiveShell.confirm_exit = False
    c.Completer.greedy = True
    c.InteractiveShellApp.exec_lines = [
        "print()",
        "print('Welcome to the MyGoog Debug Console!')",
        "print('Available objects: clients, drive, sheets, gmail, calendar, tasks, config')",
        "print('Shortcuts: drv, sht, gml, cal, tsk')",
        "print('Utils: get_clients, get_creds, get_logger')",
        "print('Types are available in the global namespace (e.g., SpreadsheetDict).')",
    ]

    
    # Start IPython with the context
    start_ipython(argv=[], user_ns=context, config=c)
