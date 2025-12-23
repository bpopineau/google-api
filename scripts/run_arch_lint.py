#!/usr/bin/env python3
"""Wrapper script to run the architecture linter with pretty output."""

import subprocess
import sys

try:
    from rich.console import Console
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

def main():
    if HAS_RICH:
        console = Console()
        console.print("[bold blue]Running Architecture Linter...[/bold blue]")
    else:
        print("Running Architecture Linter...")
    
    try:
        # We use lint-imports directly as it's the CLI for import-linter
        result = subprocess.run(["lint-imports"], capture_output=False)
        
        if result.returncode == 0:
            if HAS_RICH:
                console.print("\n[bold green]✅ Architecture linting passed![/bold green]")
            else:
                print("\nArchitecture linting passed!")
        else:
            if HAS_RICH:
                console.print("\n[bold red]❌ Architecture linting failed.[/bold red]")
                console.print("[yellow]Review the violations above and adjust your imports to maintain architectural boundaries.[/yellow]")
            else:
                print("\nArchitecture linting failed.")
        
        sys.exit(result.returncode)
        
    except FileNotFoundError:
        if HAS_RICH:
            console.print("\n[bold red]❌ Error: 'lint-imports' command not found.[/bold red]")
            console.print("Please ensure you have installed the dev dependencies (import-linter).")
            console.print("Try running: [bold]uv sync --all-extras[/bold]")
        else:
            print("\nError: 'lint-imports' command not found.")
            print("Please ensure you have installed the dev dependencies (import-linter).")
            print("Try running: uv sync --all-extras")
        sys.exit(1)

if __name__ == "__main__":
    main()
