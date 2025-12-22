# Product Guidelines - MyGoog (mg)

## Tone & Voice
The project adopts a **"Professional yet Personal"** tone, striking a balance between technical precision and user-centered accessibility.

*   **GUI (Desktop App):** Friendly & Accessible. Use clear labels, helpful tooltips, and plain language.
*   **API & Documentation:** Professional & Technical. Focus on precision, explicit types, and concise, high-value examples.
*   **Error Messages:** Friendly but Direct. Provide actionable feedback rather than raw stack traces or error codes.

## Design Principles (GUI)
The desktop interface is built for efficiency and long-term usability, prioritized as follows:

1.  **Speed First (Highest Priority):** Instant responsiveness is non-negotiable. Minimize UI blocking, use asynchronous workers for all network calls, and prioritize keyboard shortcuts.
2.  **Visual Hierarchy:** Use clear spacing, typography, and dark-mode optimization to reduce cognitive load. Group related information logically to maintain clarity during extended sessions.
3.  **Information Density:** Provide a high-level overview of digital life (Events, Files, Emails) at a glance. Balance density with hierarchy—show metadata on-demand via tooltips or expandable details to avoid clutter.

## Engineering Guidelines
*   **Ergonomic > Exhaustive:** Prioritize the "happy path" with sane defaults.
*   **Fast Startup:** Auth once, reuse clients, and verify credentials in the background.
*   **"Hackable" by Design:** Keep the core library clean and well-documented to encourage personal extensions.
