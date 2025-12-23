import sys
from pathlib import Path

import typer

# Add scripts directory to path to import utils
sys.path.append(str(Path(__file__).parent))
from scaffold_utils import get_project_root, validate_name, write_file

app = typer.Typer()

SERVICE_TEMPLATE = """from typing import List, Optional, TypedDict
from mygooglib.core.service_base import GoogleService
from mygooglib.core.decorators import api_call

class {class_name}Resource(TypedDict):
    id: str
    name: str
    # Add other fields here

class {class_name}Service(GoogleService):
    \"\"\"{class_name} Service wrapper.\"\"\"
    
    SERVICE_NAME = "{service_name}"
    VERSION = "v3"  # Verify correct version
    SCOPES = ["https://www.googleapis.com/auth/{service_name}.readonly"]

    def __init__(self, user: str = "default"):
        super().__init__(user)

    @api_call
    def list_items(self) -> List[{class_name}Resource]:
        \"\"\"List items from the service.\"\"\"
        # Placeholder implementation
        # return self.service.items().list().execute().get('items', [])
        return []
"""


@app.command()
def main(name: str):
    """
    Scaffold a new service in mygooglib/services/.

    NAME: The snake_case name of the service (e.g., 'calendar', 'google_drive').
    """
    valid_name = validate_name(name)
    class_name = "".join(part.title() for part in valid_name.split("_"))

    # Generate content
    content = SERVICE_TEMPLATE.format(service_name=valid_name, class_name=class_name)

    # Define target path
    root = get_project_root()
    target_file = root / "mygooglib" / "services" / f"{valid_name}.py"

    if write_file(target_file, content):
        print("\n[bold green]Success![/bold green]")
        print("Next steps:")
        print(f"1. Open [bold]{target_file}[/bold]")
        print("2. Verify api_call imports and service version.")
        print("3. Register in [bold]mygooglib/services/__init__.py[/bold]:")
        print(f"   from .{valid_name} import {class_name}Service")


if __name__ == "__main__":
    app()
