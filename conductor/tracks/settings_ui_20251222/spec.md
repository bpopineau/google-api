# Track Specification: Implement functional Settings UI with Theme Switcher

## Goal
To implement a fully functional Settings page in the MyGoog GUI that allows users to toggle between Light and Dark themes, with persistence across application restarts.

## Requirements

### Functional
1.  **Theme Toggle:**
    -   A UI control (e.g., Switch or ComboBox) on the Settings page to select "Light" or "Dark" mode.
    -   Changing the setting must immediately update the application's visual appearance.
2.  **Persistence:**
    -   The selected theme must be saved to the application's configuration file (`config.json` or similar).
    -   On application startup, the saved theme must be loaded and applied automatically.
3.  **UI Feedback:**
    -   Visual confirmation (immediate style change) serves as feedback.

### Non-Functional
1.  **Performance:** Theme switching should happen instantly (<200ms) without blocking the UI thread.
2.  **Usability:** The settings control should be clearly labeled and intuitive.

## Tech Stack Alignment
*   **GUI:** PySide6 (QWidget/QMainWindow styling).
*   **Config:** `mygooglib.core.config` (assuming existing config handling).
*   **Testing:** `pytest-qt` for GUI interaction tests.

## Out of Scope
*   Adding other settings (e.g., account management) in this specific track.
*   Custom color picking (preset themes only).
