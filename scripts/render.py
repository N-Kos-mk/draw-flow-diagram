"""Render an SVG to PNG with Playwright's Chromium (fonts render as in a browser).

Part of the draw-flow-diagram skill. Copyright (c) 2026 nKos. MIT License (see LICENSE).

    python render.py out/diagram.svg [--scale 2]

Needs: pip install playwright && playwright install chromium
"""

from __future__ import annotations

import argparse
from pathlib import Path

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>html, body {{ margin: 0; background: #ffffff; }} svg {{ display: block; }}</style>
</head><body>{svg}</body></html>"""


def svg_to_png(svg_path: Path, png_path: Path | None = None, scale: float = 2) -> Path:
    """Write a PNG at `scale` times the SVG size. Default output: same path, .png."""
    from playwright.sync_api import sync_playwright

    svg_path = Path(svg_path)
    png_path = Path(png_path) if png_path else svg_path.with_suffix(".png")
    svg = svg_path.read_text(encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=scale)
        page.set_content(PAGE.format(svg=svg))
        page.evaluate("document.fonts.ready")
        page.locator("svg").first.screenshot(path=str(png_path))
        browser.close()
    return png_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--scale", type=float, default=2)
    args = parser.parse_args()
    print(svg_to_png(args.svg, scale=args.scale))


if __name__ == "__main__":
    main()
