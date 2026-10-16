#!/usr/bin/env python3
"""Dependency-free integrity checks for the NexGen static homepage."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
HTML_FILE = ROOT / "index.html"
TOKEN_FILE = ROOT / "styles" / "tokens.css"
CSS_FILES = [
    ROOT / "styles" / "tokens.css",
    ROOT / "styles" / "base.css",
    ROOT / "styles" / "components.css",
    ROOT / "styles" / "sections.css",
    ROOT / "styles" / "responsive.css",
]
WORKFLOW_FILES = [
    ROOT / ".github" / "workflows" / "static.yml",
    ROOT / ".github" / "workflows" / "validate.yml",
]


class PageAuditParser(HTMLParser):
    """Collect IDs, links, source paths, headings, and essential accessibility hooks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[str] = []
        self.h1_count = 0
        self.title_open = False
        self.title_text: list[str] = []
        self.meta_description = ""
        self.nav_toggle_found = False
        self.nav_target = ""
        self.nav_found = False
        self.main_found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        for key in ("href", "src"):
            value = attributes.get(key)
            if value:
                self.references.append(value)

        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_open = True
        if tag == "meta" and attributes.get("name", "").lower() == "description":
            self.meta_description = attributes.get("content") or ""
        if "data-nav-toggle" in attributes:
            self.nav_toggle_found = True
            self.nav_target = attributes.get("aria-controls") or ""
        if "data-site-nav" in attributes:
            self.nav_found = True
        if tag == "main" and element_id == "main":
            self.main_found = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_open = False

    def handle_data(self, data: str) -> None:
        if self.title_open:
            self.title_text.append(data)


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    raise SystemExit(1)


def main() -> int:
    if not HTML_FILE.is_file():
        fail("index.html is missing")

    for path in CSS_FILES:
        if not path.is_file():
            fail(f"required stylesheet is missing: {path.relative_to(ROOT)}")

    for path in WORKFLOW_FILES:
        if not path.is_file():
            fail(f"required workflow is missing: {path.relative_to(ROOT)}")

    parser = PageAuditParser()
    parser.feed(HTML_FILE.read_text(encoding="utf-8"))
    parser.close()

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        fail(f"duplicate HTML id(s): {', '.join(duplicate_ids)}")

    id_set = set(parser.ids)
    missing_anchors = sorted({
        fragment
        for ref in parser.references
        if ref.startswith("#")
        for fragment in [urlparse(ref).fragment]
        if fragment and fragment not in id_set
    })
    if missing_anchors:
        fail(f"broken in-page anchor(s): {', '.join(missing_anchors)}")

    missing_paths: list[str] = []
    for reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local_path = (ROOT / parsed.path.lstrip("/")).resolve()
        if not local_path.is_file():
            missing_paths.append(reference)
    if missing_paths:
        fail(f"missing local asset/page reference(s): {', '.join(sorted(set(missing_paths)))}")

    if parser.h1_count != 1:
        fail(f"expected one H1 in the prototype, found {parser.h1_count}")
    if not parser.main_found:
        fail("semantic <main id='main'> landmark is missing")
    if not parser.nav_toggle_found or not parser.nav_target:
        fail("mobile navigation toggle or aria-controls target is missing")
    if parser.nav_target not in id_set or not parser.nav_found:
        fail("mobile navigation toggle points to a missing navigation element")
    if not parser.meta_description or "prototype description" in parser.meta_description.lower():
        fail("meta description is blank or contains an internal prototype warning")

    tokens = TOKEN_FILE.read_text(encoding="utf-8").lower()
    if "--brand-teal: #214a4a" not in tokens or "--brand-lime: #daf450" not in tokens or "--brand-white: #fdffff" not in tokens:
        fail("official NexGen brand colours have changed or are missing")

    page_html = HTML_FILE.read_text(encoding="utf-8")
    hero_css = (ROOT / "styles" / "sections.css").read_text(encoding="utf-8")
    if 'class="hero__grid"' not in page_html or 'class="hero__grid cyber-pattern"' in page_html:
        fail("the hero should use the static grid layer without animation classes")
    if ".hero__grid {" not in hero_css or "@keyframes cyber-move" in hero_css or "animation: cyber-move" in hero_css:
        fail("the hero grid must remain static and CSS-only")
    if "110px 110px" not in hero_css:
        fail("the main hero grid scale should remain large and calm")
    if "--grid-line: rgb(218 244 80 / 9%)" not in tokens or "--fine-grid-line: rgb(253 255 255 / 3%)" not in tokens:
        fail("hero grid lines must use the official lime and white palette")
    if "3 233 244" in hero_css or "217 3 244" in hero_css:
        fail("old cyan/magenta grid colours must not return")
    if "rgb(33 74 74) / 28%" in hero_css:
        fail("invalid RGB alpha syntax in the hero backdrop")
    if 'src="assets/images/nexgen-steelcity-wordmark.svg"' not in page_html:
        fail("official NexGen SteelCity SVG wordmark is missing from the header")
    if 'class="brand__mark"' not in page_html or "brand__mark-outer" not in page_html:
        fail("animated geometric logo mark is missing from the header")

    if not (ROOT / "scripts" / "main.js").is_file():
        fail("scripts/main.js is missing")
    js = (ROOT / "scripts" / "main.js").read_text(encoding="utf-8")
    responsive = (ROOT / "styles" / "responsive.css").read_text(encoding="utf-8")
    if "classList.add('has-js')" not in js or ".has-js .site-nav" not in responsive:
        fail("progressive-enhancement navigation fallback is missing")
    if "closeNavigation(true)" not in js:
        fail("Escape key should restore focus to the navigation toggle")
    if ".site-nav__dropdown { position: static" not in responsive:
        fail("the mobile Explore mega menu must stay in normal navigation flow")
    if 'class="site-nav__dropdown site-nav__dropdown--mega"' not in page_html or 'class="mega-menu__links"' not in page_html:
        fail("the desktop Explore mega menu structure is missing")
    for required_link in ('href="#ranges"', 'href="#system"', 'href="tel:+441143992978"', 'href="https://www.portablestage.co.uk/quote-me/"'):
        if required_link not in page_html:
            fail(f"primary navigation destination is missing: {required_link}")
    if "details[open]" not in js or "openDropdown.querySelector('summary')?.focus()" not in js:
        fail("the Explore menu must close accessibly on Escape and navigation")

    css = "\n".join(path.read_text(encoding="utf-8") for path in CSS_FILES)
    token_css = TOKEN_FILE.read_text(encoding="utf-8")
    defined_tokens = set(re.findall(r"(--[\w-]+)\s*:", token_css))
    used_tokens = set(re.findall(r"var\(\s*(--[\w-]+)", css))
    undefined_tokens = sorted(used_tokens - defined_tokens)
    if undefined_tokens:
        fail(f"undefined CSS token(s): {', '.join(undefined_tokens)}")

    svg_files = sorted((ROOT / "assets" / "images").glob("*.svg"))
    if not svg_files:
        fail("no local SVG assets found")
    for svg_path in svg_files:
        try:
            ET.parse(svg_path)
        except ET.ParseError as error:
            fail(f"invalid SVG {svg_path.relative_to(ROOT)}: {error}")

    pages_workflow = (ROOT / ".github" / "workflows" / "static.yml").read_text(encoding="utf-8")
    if "actions/deploy-pages@" not in pages_workflow or 'branches: ["main"]' not in pages_workflow:
        fail("GitHub Pages deploy workflow no longer deploys on main")

    print("PASS  unique HTML IDs and valid in-page anchors")
    print("PASS  official NexGen palette, SVG wordmark, and animated mark")
    print("PASS  large-scale static NexGen hero grid")
    print("PASS  local CSS, script, and image references")
    print("PASS  one H1, main landmark, and accessible mobile-nav wiring")
    print("PASS  CSS custom properties are defined")
    print(f"PASS  {len(svg_files)} SVG assets parse successfully")
    print("PASS  GitHub Pages deployment workflow is present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
