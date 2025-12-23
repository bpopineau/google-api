# mygoog_gui

## Purpose
The Graphical User Interface (GUI) built with `PySide6` (Qt for Python). It provides a desktop application experience for interacting with Google Workspace services, featuring real-time updates, theming, and a widget-based architecture.

## Key Entry Points
- [`main.py`](file:///c:/Users/brand/Projects/google-api/mygoog_gui/main.py): Contains the `MainWindow` class and the main application event loop.
- [`workers.py`](file:///c:/Users/brand/Projects/google-api/mygoog_gui/workers.py): Defines background threads (`QThread`) to perform long-running API tasks without freezing the UI.
- [`styles.py`](file:///c:/Users/brand/Projects/google-api/mygoog_gui/styles.py): Manages application styling, stylesheets, and the central design system.

## Dependencies
- **External:** `PySide6`
- **Internal:** `mygooglib` (consumes core logic and services)
