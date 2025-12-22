"""
Script to generate a 'Context Map' for AI agents.
It inspects the 'mygooglib' package and dumps the public API surface
(classes, methods, signatures, docstrings) to a Markdown file.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path
from types import ModuleType

import mygooglib.services
from mygooglib.core.client import Clients

OUTPUT_FILE = Path("conductor/context_map.md")


def get_public_methods(cls):
    """Return list of (name, signature, docstring) for public methods."""
    methods = []
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if not inspect.isfunction(member) and not inspect.ismethod(member):
            continue

        sig: str | inspect.Signature
        try:
            sig = inspect.signature(member)
        except ValueError:
            sig = "(?)"

        doc = inspect.getdoc(member) or ""
        # Keep docstring brief (first line)
        doc_summary = doc.split("\n")[0] if doc else ""
        methods.append((name, sig, doc_summary))
    return methods


def generate_map():
    lines = [
        "# MyGoog Library Context Map",
        "",
        "This file is auto-generated. It lists the available tools in `mygooglib`.",
        "",
    ]

    # 1. Document the Main Entry Point (Clients)
    lines.append("## Core: `mygooglib.core.client.Clients`")
    lines.append("The main entry point factory. Accessed via `get_clients()`.")
    lines.append("")

    # Inspect properties of Clients to find available services
    client_properties = []
    for name, member in inspect.getmembers(Clients):
        if isinstance(member, property):
            # Check return type annotation if possible, or infer from code
            # For now, we know the structure.
            lines.append(f"* `clients.{name}` -> Returns Service Client")
            client_properties.append(name)

    lines.append("")

    # 2. Document each Service Client
    # We'll iterate through the modules in mygooglib.services
    package = mygooglib.services
    prefix = package.__name__ + "."

    for _, name, _ in pkgutil.iter_modules(package.__path__, prefix):
        try:
            module = importlib.import_module(name)
        except ImportError:
            continue

        # Find the Client class in this module
        for member_name, member in inspect.getmembers(module):
            if (
                member_name.endswith("Client")
                and inspect.isclass(member)
                and member.__module__ == name
            ):
                lines.append(f"## Service: `{member_name}`")
                lines.append(f"Defined in: `{name}`")
                lines.append("```python")

                methods = get_public_methods(member)
                for m_name, m_sig, m_doc in methods:
                    lines.append(f"def {m_name}{m_sig}:")
                    lines.append(f'    """{m_doc}"""')

                lines.append("```")
                lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated context map at {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_map()
