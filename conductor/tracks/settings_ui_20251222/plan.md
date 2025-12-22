# Track Plan: Implement functional Settings UI with Theme Switcher

## Phase 1: Core Logic & Configuration
This phase focuses on the backend logic for storing and retrieving the theme preference.

- [ ] Task: Create reproduction test for Theme Config persistence
    - [ ] Sub-task: Create `tests/gui/test_theme_config.py`
    - [ ] Sub-task: Write failing test that verifies `config.theme` can be set and retrieved
    - [ ] Sub-task: Run test to confirm failure (Red)

- [ ] Task: Implement Theme Configuration Logic
    - [ ] Sub-task: Update `mygooglib/core/config.py` (or equivalent) to support a `theme` field (defaulting to 'dark' or system default)
    - [ ] Sub-task: Ensure save/load mechanisms handle this field
    - [ ] Sub-task: Run tests to confirm pass (Green)
    - [ ] Sub-task: Refactor if necessary

- [ ] Task: Conductor - User Manual Verification 'Core Logic & Configuration' (Protocol in workflow.md)

## Phase 2: GUI Implementation
This phase connects the backend logic to the visual frontend.

- [ ] Task: Create reproduction test for Settings UI interaction
    - [ ] Sub-task: Create `tests/gui/test_settings_page.py`
    - [ ] Sub-task: Write failing test using `pytest-qt` that simulates clicking the theme toggle and verifying the config update
    - [ ] Sub-task: Run test to confirm failure (Red)

- [ ] Task: Implement Settings Page UI
    - [ ] Sub-task: Update `mygoog_gui/pages/settings.py` to include the Theme Switcher widget (e.g., QComboBox or QCheckBox)
    - [ ] Sub-task: Bind the widget signal to the config update method
    - [ ] Sub-task: Run tests to confirm pass (Green)

- [ ] Task: Implement Live Theme Switching
    - [ ] Sub-task: Create a test or manual verification step for global style application
    - [ ] Sub-task: Implement a `apply_theme(theme_name)` function in `mygoog_gui/styles.py` (or similar)
    - [ ] Sub-task: Wire the Settings page signal to trigger `apply_theme` immediately
    - [ ] Sub-task: Ensure main window listens for theme changes (if needed)

- [ ] Task: Conductor - User Manual Verification 'GUI Implementation' (Protocol in workflow.md)
