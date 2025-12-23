# Audit Report: mygoog_gui/widgets/cards.py

## Purpose
- Reusable UI cards for consistent information display across the application dashboard and search results.

## Main Exports
- `StatCard`: A vertical card displaying an icon, a large numeric value, and a descriptive label.
- `ItemCard`: A horizontal card for list items, supporting icons, titles, subtitles, and customizable action buttons.

## Findings
- **Modular Styling:** Cards use the `COLORS` palette and property-based CSS selective (`[class="card"]`) for consistent theming.
- **Interactivity:** `ItemCard` implements hover states and custom signal emission (`clicked`, `action_clicked`), making it a versatile interactive component.
- **Ergonomics:** Action buttons on `ItemCard` (e.g., "Copy ID", "Done") enhance productivity directly from the list view.

## Quality Checklist
- [x] Reusable component design
- [x] Responsive hover states and cursors
- [x] Customizable action buttons
