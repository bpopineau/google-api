"""Unified entry point for the MyGoog application."""

from __future__ import annotations

import sys
from typing import NoReturn


def main() -> NoReturn:
    """Main entry point.

    Dispatches to the CLI if arguments are provided, otherwise launches the GUI.
    """
    args = sys.argv[1:]

    # Heuristic: if no args or first arg is not a command/flag, run GUI
    # However, standard CLI usually has 'mygoog command ...'
    # So if len(args) == 0, run GUI.
    if not args:
        from mygooglib.gui.main import run_app

        run_app()
        sys.exit(0)

    # Allow explicit GUI launch flag
    if args[0] in ("--gui", "-g"):
        from mygooglib.gui.main import run_app

        run_app()
        sys.exit(0)

    # Otherwise run CLI
    from mygooglib.cli import main as cli_main

    sys.exit(cli_main())


if __name__ == "__main__":
    main()
