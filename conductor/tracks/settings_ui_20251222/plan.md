# Plan: Settings & Theming (Personalization)

This plan outlines the implementation of a structured Settings UI and a dynamic theming system for the MyGoog GUI.

## Phase 1: Core Configuration & Persistence (mygooglib)
Enhance the existing configuration system to support new personalization options.

- [ ] **Task 1: Update Config Schema**
    - Add `accent_color` (string) to `Config` dataclass in `mygooglib/core/config.py`.
    - Update `AppConfig` to support `accent_color` property with auto-save.
- [ ] **Task 2: Write Config Tests**
    - Create `tests/test_config.py`.
    - Verify that `accent_color` persists correctly to `config.json`.
    - Verify that `Config.from_dict` handles missing or extra keys gracefully.
- [ ] **Task 3: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)**

## Phase 2: Dynamic Theming Engine (mygoog_gui)
Refactor the styling system to support light/dark modes and dynamic accent colors.

- [ ] **Task 1: Refactor Stylesheet Generation**
    - Update `mygoog_gui/styles.py` to define multiple palettes (Dark, Light).
    - Create a function `get_stylesheet(theme: str, accent_color: str) -> str` that generates the QSS.
- [ ] **Task 2: Implement Theme Manager**
    - Create `mygoog_gui/theme_manager.py` to centralize theme application.
    - Implement logic to detect system theme (using PySide6 features).
    - Provide a signal or callback to notify UI components of theme changes.
- [ ] **Task 3: Unit Test Theming Logic**
    - Create `tests/gui/test_theme_manager.py`.
    - Verify stylesheet generation with different theme/accent combinations.
- [ ] **Task 4: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)**

## Phase 3: Structured Settings UI (mygoog_gui)
Refactor the Settings page to use a multi-section layout and implement personalization controls.

- [ ] **Task 1: Refactor SettingsPage Layout**
    - Modify `mygoog_gui/pages/settings.py` to use a `QStackedWidget` for content and a small sidebar (or `QListWidget`) for section navigation (General, Appearance, Accounts, Sync).
- [ ] **Task 2: Implement Appearance Section**
    - Create the Appearance UI with:
        - Theme dropdown (System, Light, Dark).
        - Accent color picker (Blue, Green, Purple, Orange).
    - Connect UI signals to `AppConfig` and `ThemeManager` for immediate application.
- [ ] **Task 3: Add Section Placeholders**
    - Implement basic layouts for "General", "Accounts", and "Sync" sections as specified.
- [ ] **Task 4: Functional Tests for Settings UI**
    - Create `tests/gui/test_settings_page.py`.
    - Verify that changing theme/accent in the UI updates the `AppConfig`.
- [ ] **Task 5: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)**

## Phase 4: Integration & Polish
Ensure the theme is applied globally and consistently.

- [ ] **Task 1: Apply Theme on App Startup**
    - Update `mygoog_gui/main.py` to initialize `ThemeManager` and apply the saved theme before showing the main window.
- [ ] **Task 2: Final Verification & Cleanup**
    - Run full test suite.
    - Verify "Hackability" (manual config edit reflected on restart).
- [ ] **Task 3: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)**