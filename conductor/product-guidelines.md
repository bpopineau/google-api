# Product Guidelines: MyGoog (mg)

## Communication & Tone
*   **Voice:** Efficient, precise, and empowering. Speak to the user as a peer (power user/developer).
*   **Conciseness:** Avoid fluff. Get straight to the point.
*   **Technicality:** Don't shy away from technical details, but keep them accessible.
*   **Feedback:** Provide clear, actionable feedback for all operations.

## Design Philosophy
*   **Keyboard-Centric:** The primary mode of interaction should be the keyboard. Hotkeys and command palettes take precedence over mouse clicks.
*   **Speed & Responsiveness:** The application must feel instant. Optimistic UI updates and background processing are preferred over blocking loading screens.
*   **Premium Utility:** A clean, clutter-free aesthetic that emphasizes data and functionality. "Tools, not toys."
*   **Dark Mode First:** Designed primarily for dark mode to reduce eye strain for heavy users, with a high-contrast light mode option.

## UX Patterns
*   **Command Palette:** specific actions should be accessible via a searchable command interface (Ctrl/Cmd+K style).
*   **Contextual Actions:** Show actions relevant to the current selection (e.g., right-click context menus, toolbar updates).
*   **Non-Blocking operations:** Long-running tasks (syncs, API calls) must happen in the background with status indicators, never freezing the UI.
*   **Undo/Redo:** Support undo for destructive actions where possible.

## Visual Identity
*   **Typography:** Clean, monospaced fonts for data/code (e.g., JetBrains Mono, Fira Code) mixed with modern sans-serif for UI elements (Inter, Roboto).
*   **Color Palette:**
    *   **Backgrounds:** Deep grays/blacks (#1e1e1e) rather than pure black.
    *   **Accents:** Google Brand colors (Blue, Red, Yellow, Green) used sparingly to highlight status or specific services.
    *   **Status Indicators:** specific colors for success (Green), warning (Yellow), error (Red), and processing (Blue).
*   **Iconography:** Consistent, distinct icons for file types and actions (e.g., Material Symbols).
