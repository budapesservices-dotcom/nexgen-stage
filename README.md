# NexGen Portable Staging — Homepage Redesign

A lightweight homepage redesign concept built with plain HTML, CSS, and a small vanilla-JavaScript navigation controller.

## Design direction

- **Concept:** Engineered Energy — “From one module. To any stage.”
- **Palette:** Deep Forest `#063D32`, Electric Lime `#B7EF59`, Studio White `#F5F7F2`, Carbon `#171D19`.
- **Typography:** Barlow Condensed for display headlines; Inter for body copy and UI.
- **Visual principle:** nested-square geometry inspired by the NexGen mark, purposeful diagonals, and product-first storytelling.

## Editing rules

- `index.html` contains semantic page structure and content.
- `styles/tokens.css` contains reusable design values.
- `styles/base.css` contains reset, typography defaults, and accessibility foundations.
- `styles/components.css` contains shared UI patterns and buttons.
- `styles/sections.css` contains section-specific desktop styles.
- `styles/responsive.css` contains breakpoint adjustments.
- `scripts/main.js` contains only the mobile navigation interaction.
- `assets/images/*.svg` are temporary concept illustrations and must be replaced with approved client assets before final delivery.

## Technical principles

- No framework, bundler, or third-party JavaScript dependency.
- Keep JavaScript small and add behavior only when native HTML/CSS cannot do the job.
- Preserve semantic HTML, keyboard usability, visible focus, contrast, and reduced-motion preferences.
- The contest brief requires preservation of the live site's SEO. The current meta description is editorial draft copy, not a verified copy of the live value. Before final delivery, compare the prototype against the supplied/live source HTML and preserve the exact title, meta description, canonical, schema, H1–H3 hierarchy, alt text, URLs, and internal links.
- Do not treat prototype copy, illustrative SVGs, or placeholder metadata as verified product claims or production assets.

## Run locally

Open `index.html` directly for a quick review, or run `python -m http.server 8000` from the repository root and open `http://localhost:8000`.

## Commit policy

Commit complete, testable task batches. Avoid commits for individual styling tweaks or single files unless a fix must be isolated. Check local links, JavaScript syntax, SVG parsing, responsive breakpoints, and keyboard behavior before committing.
