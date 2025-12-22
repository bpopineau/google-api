"""QSS Stylesheet and theme colors for the PySide6 GUI."""

from __future__ import annotations

from typing import Literal

# Type aliases
ThemeType = Literal["dark", "light", "system"]
AccentType = Literal["blue", "green", "purple", "orange"]

# Dark color palette - Modern Neutral with better contrast
DARK_COLORS = {
    # Backgrounds (higher contrast)
    "bg_primary": "#0a0c10",  # Main background (darker)
    "bg_secondary": "#161b22",  # Cards, sidebar
    "bg_tertiary": "#2d333b",  # Hover states, headers (lighter for contrast)
    "bg_elevated": "#3d444d",  # Elevated surfaces, dropdowns
    # Text (brighter for better contrast)
    "text_primary": "#f0f6fc",  # Main text (bright white)
    "text_secondary": "#9198a1",  # Secondary text
    "text_muted": "#6e7681",  # Muted/disabled text
    # Borders
    "border": "#3d444d",  # Default border (more visible)
    "border_muted": "#2d333b",  # Subtle border
    # Status colors
    "success": "#3fb950",  # Green
    "warning": "#d29922",  # Amber
    "error": "#f85149",  # Red
}

# Light color palette
LIGHT_COLORS = {
    # Backgrounds
    "bg_primary": "#ffffff",  # Main background
    "bg_secondary": "#f6f8fa",  # Cards, sidebar
    "bg_tertiary": "#e1e4e8",  # Hover states, headers
    "bg_elevated": "#d0d7de",  # Elevated surfaces, dropdowns
    # Text
    "text_primary": "#1f2328",  # Main text (dark)
    "text_secondary": "#656d76",  # Secondary text
    "text_muted": "#8b949e",  # Muted/disabled text
    # Borders
    "border": "#d0d7de",  # Default border
    "border_muted": "#e1e4e8",  # Subtle border
    # Status colors
    "success": "#1a7f37",  # Green
    "warning": "#9a6700",  # Amber
    "error": "#cf222e",  # Red
}

# Accent color palettes (primary, hover, muted)
ACCENT_PALETTES = {
    "blue": {
        "accent": "#2563eb",
        "accent_hover": "#3b82f6",
        "accent_muted": "#1d4ed8",
    },
    "green": {
        "accent": "#238636",  # GitHub green
        "accent_hover": "#2ea043",
        "accent_muted": "#196c2e",
    },
    "purple": {
        "accent": "#8b5cf6",
        "accent_hover": "#a78bfa",
        "accent_muted": "#7c3aed",
    },
    "orange": {
        "accent": "#ea580c",
        "accent_hover": "#f97316",
        "accent_muted": "#c2410c",
    },
}

# For backward compatibility
COLORS = {**DARK_COLORS, **ACCENT_PALETTES["green"]}


def get_stylesheet(theme: str = "dark", accent_color: str = "green") -> str:
    """Generate QSS stylesheet for the given theme and accent color.

    Args:
        theme: "dark" or "light"
        accent_color: "blue", "green", "purple", or "orange"

    Returns:
        Complete QSS stylesheet string
    """
    # Select base colors
    colors = DARK_COLORS.copy() if theme == "dark" else LIGHT_COLORS.copy()

    # Merge accent colors
    accent = ACCENT_PALETTES.get(accent_color, ACCENT_PALETTES["green"])
    colors.update(accent)

    return _generate_qss(colors)


def _generate_qss(colors: dict[str, str]) -> str:
    """Generate the full QSS string from a color dictionary."""
    return f"""
QMainWindow {{
    background-color: {colors["bg_primary"]};
}}

QWidget {{
    color: {colors["text_primary"]};
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}}

/* Sidebar styling */
#sidebar {{
    background-color: {colors["bg_secondary"]};
    border-right: 1px solid {colors["border"]};
}}

#sidebar QPushButton {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    color: {colors["text_secondary"]};
}}

#sidebar QPushButton:hover {{
    background-color: {colors["bg_tertiary"]};
    color: {colors["text_primary"]};
}}

#sidebar QPushButton:checked {{
    background-color: {colors["accent"]};
    color: {colors["text_primary"]};
}}

/* Content area */
#content {{
    background-color: {colors["bg_primary"]};
    padding: 20px;
}}

/* Cards */
.card {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
    border-radius: 12px;
    padding: 16px;
}}

/* Headers */
QLabel#header {{
    font-size: 24px;
    font-weight: bold;
    color: {colors["text_primary"]};
}}

QLabel#subheader {{
    font-size: 14px;
    color: {colors["text_secondary"]};
}}

/* Buttons */
QPushButton {{
    background-color: {colors["accent"]};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    color: {colors["text_primary"]};
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {colors["accent_hover"]};
}}

QPushButton:pressed {{
    background-color: {colors["accent_muted"]};
}}

QPushButton:disabled {{
    background-color: {colors["bg_tertiary"]};
    color: {colors["text_muted"]};
}}

/* Input fields */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
    border-radius: 6px;
    padding: 8px 12px;
    color: {colors["text_primary"]};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {colors["accent"]};
}}

/* Combo boxes */
QComboBox {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
    border-radius: 6px;
    padding: 8px 12px;
    color: {colors["text_primary"]};
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: {colors["accent"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
    selection-background-color: {colors["bg_tertiary"]};
    color: {colors["text_primary"]};
}}

/* Tables */
QTableView, QTreeView, QListView {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
    border-radius: 8px;
    gridline-color: {colors["border"]};
}}

QTableView::item, QTreeView::item, QListView::item {{
    padding: 8px;
}}

QTableView::item:selected, QTreeView::item:selected, QListView::item:selected {{
    background-color: {colors["bg_tertiary"]};
}}

QHeaderView::section {{
    background-color: {colors["bg_tertiary"]};
    border: none;
    padding: 8px;
    font-weight: 600;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {colors["bg_secondary"]};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: {colors["border"]};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors["text_muted"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {colors["bg_secondary"]};
    height: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:horizontal {{
    background-color: {colors["border"]};
    border-radius: 5px;
    min-width: 30px;
}}

/* Status messages */
QLabel.success {{
    color: {colors["success"]};
}}

QLabel.warning {{
    color: {colors["warning"]};
}}

QLabel.error {{
    color: {colors["error"]};
}}

/* Menu bar */
QMenuBar {{
    background-color: {colors["bg_secondary"]};
    border-bottom: 1px solid {colors["border"]};
}}

QMenuBar::item:selected {{
    background-color: {colors["bg_tertiary"]};
}}

QMenu {{
    background-color: {colors["bg_secondary"]};
    border: 1px solid {colors["border"]};
}}

QMenu::item:selected {{
    background-color: {colors["bg_tertiary"]};
}}

/* Tooltips */
QToolTip {{
    background-color: {colors["bg_tertiary"]};
    border: 1px solid {colors["border"]};
    color: {colors["text_primary"]};
    padding: 4px 8px;
}}

/* Tab widgets */
QTabWidget::pane {{
    border: 1px solid {colors["border"]};
    background-color: {colors["bg_secondary"]};
    border-radius: 8px;
}}

QTabBar::tab {{
    background-color: {colors["bg_tertiary"]};
    border: 1px solid {colors["border"]};
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {colors["accent"]};
    color: {colors["text_primary"]};
}}
"""


# Legacy: Static stylesheet for backward compatibility
STYLESHEET = get_stylesheet("dark", "green")
