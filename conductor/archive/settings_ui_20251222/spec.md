# Specification: Settings & Theming (Personalization)

## 1. Overview
This feature introduces a comprehensive **Settings** interface to the `mygoog_gui` application. It focuses on user personalization through theme and accent color customization, while establishing a robust, file-based configuration system (`config.json`) that can be shared between the GUI and CLI components. The Settings page will be structured with navigation categories (General, Appearance, Accounts, Sync) to support future scalability.

## 2. Functional Requirements

### 2.1. Configuration Persistence
*   **Storage:** User preferences must be stored in a transparent, human-readable file (e.g., `~/.mygoog/config.json`).
*   **Scope:** The configuration file must be accessible and parsable by both the `mygoog_gui` and `mygoog_cli` components.
*   **Behavior:**
    *   On startup, the application loads settings from this file.
    *   If the file is missing, default settings are applied and the file is created.
    *   Changes made in the UI are immediately saved to the file.

### 2.2. User Interface (Settings Page)
*   **Structure:** The Settings page must use a Sidebar or Tabbed layout with the following sections:
    1.  **General:** (Placeholder for startup options/system tray).
    2.  **Appearance:** Controls for visual customization.
    3.  **Accounts:** (Placeholder/Display for connected Google user status).
    4.  **Sync:** (Placeholder for cache paths and refresh intervals).

### 2.3. Appearance Customization
*   **Theme Modes:**
    *   **Options:** System Default (follows OS), Light Mode, Dark Mode.
    *   **Behavior:** Changing the mode applies the visual style immediately without requiring an application restart.
*   **Accent Colors:**
    *   **Options:** A selection of predefined brand colors (e.g., Blue, Green, Purple, Orange).
    *   **Behavior:** Selection updates UI highlights (buttons, active tabs, focus rings) immediately.

## 3. Non-Functional Requirements
*   **Responsiveness:** Theme switching should be near-instantaneous (< 200ms).
*   **Hackability:** Users should be able to edit the `config.json` file manually while the app is closed, and see changes reflected upon next launch.
*   **Maintainability:** The configuration loading/saving logic should be encapsulated in `mygooglib` (or `mygoog_gui` utils) to keep UI code clean.

## 4. Acceptance Criteria
*   [ ] **Persistence:** A `config.json` file is created in the user's home directory (or platform-specific app data folder).
*   [ ] **UI Navigation:** User can navigate between "Appearance", "Accounts", and "Sync" sections in the Settings page.
*   [ ] **Theme Switching:**
    *   User can switch between Light and Dark modes.
    *   The application UI colors update immediately.
    *   The preference persists after restarting the application.
*   [ ] **Accent Color:**
    *   User can select a different accent color.
    *   Primary buttons and active elements reflect the new color.
*   [ ] **Manual Override:** Manually editing the `config.json` file (e.g., changing theme from "dark" to "light") changes the app state on the next launch.

## 5. Out of Scope
*   Implementation of complex "Sync" logic (background workers, deep conflict resolution) is out of scope for *this* track; only the UI placeholders and config persistence for these settings are required.
*   Account OAuth login flows (handled in `auth` track/module), though the "Accounts" tab may display current status.