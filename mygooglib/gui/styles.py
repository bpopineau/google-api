"""QSS Stylesheet and theme colors for the PySide6 GUI."""

from __future__ import annotations

# Color palette - dark theme
COLORS = {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_tertiary": "#0f3460",
    "accent": "#e94560",
    "accent_hover": "#ff6b6b",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0a0",
    "text_muted": "#6a6a6a",
    "border": "#2a2a4a",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "error": "#ef4444",
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
    background-color: {COLORS["accent"]};
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
