# NexGen Portable Staging — Homepage Redesign

A lightweight homepage redesign concept built with plain HTML, CSS, and a small vanilla-JavaScript navigation controller.

## Design direction

- **Concept:** Engineered Energy — “From one module. To any stage.”
- **Official base palette:** NexGen Teal `#214A4A`, Signal Lime `#DAF450`, Stage White `#FDFFFF`.
- **Derived UI palette:** Backstage Teal `#102F30`, Mid Teal `#2E5D5C`, Mist `#EAF3F0`, Ink `#172E2E`, and restrained Stage Glow `#F1C57D` for atmospheric lighting.
- **Typography:** Barlow Condensed for display headlines; Inter for body copy and UI. Header brand wording follows the supplied logo: NEXGEN / STEELCITY / STAGE MODULES.
- **Visual principle:** nested-square geometry inspired by the NexGen mark, purposeful diagonals, product-first storytelling, and a static large-scale grid in the hero. Main grid lines use Signal Lime at low opacity; a finer secondary grid uses Stage White. The background uses CSS gradients only, with no continuous animation.

## Editing rules

- `index.html` contains semantic page structure and content.
- `styles/tokens.css` contains reusable design values.
- `styles/base.css` contains reset, typography defaults, and accessibility foundations.
- `styles/components.css` contains shared UI patterns and buttons.
- `styles/sections.css` contains section-specific desktop styles.
- `styles/responsive.css` contains breakpoint adjustments.
- `scripts/main.js` contains only the mobile navigation interaction; the desktop “More” menu uses native HTML `<details>` and adds no JavaScript.
- `assets/images/*.svg` are temporary concept illustrations. The customer gallery, storage example and organisation logos currently reference public media already shown on the existing client site; package and optimize approved assets locally before final delivery.

## Technical principles

- No framework, bundler, or third-party JavaScript dependency.
- Keep JavaScript small and add behavior only when native HTML/CSS cannot do the job.
- Preserve semantic HTML, keyboard usability, visible focus, contrast, and reduced-motion preferences.
- The contest brief requires preservation of the live site's SEO. The current meta description is editorial draft copy, not a verified copy of the live value. Before final delivery, compare the prototype against the supplied/live source HTML and preserve the exact title, meta description, canonical, schema, H1–H3 hierarchy, alt text, URLs, and internal links.
- Do not treat prototype copy, illustrative SVGs, or placeholder metadata as verified product claims or production assets.

## Run and validate

Open `index.html` directly for a quick review, or run `python -m http.server 8000` from the repository root and open `http://localhost:8000`.

Run the dependency-free static integrity checks with `python scripts/check_project.py`. GitHub Actions also runs these checks and `node --check scripts/main.js` on pushes and pull requests. The validator checks that the native More menu becomes an in-flow disclosure on mobile. The checks verify local asset references, in-page anchors, unique IDs, CSS design-token use, SVG well-formedness, and essential deployment files.

## Commit policy

Commit complete, testable task batches. Avoid commits for individual styling tweaks or single files unless a fix must be isolated. Check local links, JavaScript syntax, SVG parsing, responsive breakpoints, and keyboard behavior before committing.
