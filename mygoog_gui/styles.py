"""QSS Stylesheet and theme colors for the PySide6 GUI."""

from __future__ import annotations

# Color palette - Modern Neutral with better contrast
COLORS = {
    # Backgrounds (higher contrast)
    "bg_primary": "#0a0c10",  # Main background (darker)
    "bg_secondary": "#161b22",  # Cards, sidebar
    "bg_tertiary": "#2d333b",  # Hover states, headers (lighter for contrast)
    "bg_elevated": "#3d444d",  # Elevated surfaces, dropdowns
    # Accent colors (muted green - professional)
    "accent": "#238636",  # Primary green (GitHub green)
    "accent_hover": "#2ea043",  # Lighter green on hover
    "accent_muted": "#196c2e",  # Darker green for pressed states
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

# Main application stylesheet
STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["bg_primary"]};
}}

QWidget {{
    color: {COLORS["text_primary"]};
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}}

/* Sidebar styling */
#sidebar {{
    background-color: {COLORS["bg_secondary"]};
    border-right: 1px solid {COLORS["border"]};
}}

#sidebar QPushButton {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    color: {COLORS["text_secondary"]};
}}

#sidebar QPushButton:hover {{
    background-color: {COLORS["bg_tertiary"]};
    color: {COLORS["text_primary"]};
}}

#sidebar QPushButton:checked {{
    background-color: {COLORS["accent"]};
    color: {COLORS["text_primary"]};
}}

/* Content area */
#content {{
    background-color: {COLORS["bg_primary"]};
    padding: 20px;
}}

/* Cards */
.card {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 16px;
}}

/* Headers */
QLabel#header {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
}}

QLabel#subheader {{
    font-size: 14px;
    color: {COLORS["text_secondary"]};
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS["accent"]};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    color: {COLORS["text_primary"]};
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLORS["accent_hover"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["accent_muted"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["bg_tertiary"]};
    color: {COLORS["text_muted"]};
}}

/* Input fields */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS["text_primary"]};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {COLORS["accent"]};
}}

/* Tables */
QTableView, QTreeView, QListView {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    gridline-color: {COLORS["border"]};
}}

QTableView::item, QTreeView::item, QListView::item {{
    padding: 8px;
}}

QTableView::item:selected, QTreeView::item:selected, QListView::item:selected {{
    background-color: {COLORS["bg_tertiary"]};
}}

QHeaderView::section {{
    background-color: {COLORS["bg_tertiary"]};
    border: none;
    padding: 8px;
    font-weight: 600;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {COLORS["bg_secondary"]};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["border"]};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["text_muted"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* Status messages */
QLabel.success {{
    color: {COLORS["success"]};
}}

QLabel.warning {{
    color: {COLORS["warning"]};
}}

QLabel.error {{
    color: {COLORS["error"]};
}}

/* Menu bar */
QMenuBar {{
    background-color: {COLORS["bg_secondary"]};
    border-bottom: 1px solid {COLORS["border"]};
}}

QMenuBar::item:selected {{
    background-color: {COLORS["bg_tertiary"]};
}}

QMenu {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
}}

QMenu::item:selected {{
    background-color: {COLORS["bg_tertiary"]};
}}

/* Tooltips */
QToolTip {{
    background-color: {COLORS["bg_tertiary"]};
    border: 1px solid {COLORS["border"]};
    color: {COLORS["text_primary"]};
    padding: 4px 8px;
}}
"""

