"""Icons for diagrams.

Part of the draw-flow-diagram skill. The code is Copyright (c) 2026 nKos, MIT License (see
LICENSE). The icon path data is not: the embedded Lucide icons are ISC (some derived from
Feather, MIT), and icons_extra.json holds Lucide and Simple Icons data under their own terms.
See THIRD_PARTY_NOTICES.md.

- Generic icons: Lucide (ISC License, https://lucide.dev), stroked in the color you pass.
- Product/brand icons: Simple Icons (CC0 data; logos are their owners' trademarks), filled in
  the brand's own color so they are recognized at a glance.

A core set of Lucide icons is embedded below. Everything else lives in icons_extra.json,
filled by fetch_icons.py (e.g. `python fetch_icons.py github notion` or
`python fetch_icons.py --lucide smartphone`). No CDN is used when drawing.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

LUCIDE: dict[str, str] = {
    # places
    "globe": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>'
        '<path d="M2 12h20"/>'
    ),
    "server": (
        '<rect width="20" height="8" x="2" y="2" rx="2" ry="2"/>'
        '<rect width="20" height="8" x="2" y="14" rx="2" ry="2"/>'
        '<line x1="6" x2="6.01" y1="6" y2="6"/>'
        '<line x1="6" x2="6.01" y1="18" y2="18"/>'
    ),
    "hard-drive": (
        '<line x1="22" x2="2" y1="12" y2="12"/>'
        '<path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89'
        'A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>'
        '<line x1="6" x2="6.01" y1="16" y2="16"/>'
        '<line x1="10" x2="10.01" y1="16" y2="16"/>'
    ),
    "monitor-check": (
        '<path d="m9 10 2 2 4-4"/>'
        '<rect width="20" height="14" x="2" y="3" rx="2"/>'
        '<path d="M12 17v4"/>'
        '<path d="M8 21h8"/>'
    ),
    "laptop": (
        '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55'
        'a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>'
    ),
    "network": (
        '<rect x="16" y="16" width="6" height="6" rx="1"/>'
        '<rect x="2" y="16" width="6" height="6" rx="1"/>'
        '<rect x="9" y="2" width="6" height="6" rx="1"/>'
        '<path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/>'
        '<path d="M12 12V8"/>'
    ),
    "store": (
        '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/>'
        '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>'
        '<path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/>'
        '<path d="M2 7h20"/>'
        '<path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0'
        'A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0'
        'A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0'
        'A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0'
        'A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>'
    ),
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    # things
    "image": (
        '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>'
        '<circle cx="9" cy="9" r="2"/>'
        '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>'
    ),
    "file": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5V19A9 3 0 0 0 21 19V5"/>'
        '<path d="M3 12A9 3 0 0 0 21 12"/>'
    ),
    "list-ordered": (
        '<line x1="10" x2="21" y1="6" y2="6"/><line x1="10" x2="21" y1="12" y2="12"/>'
        '<line x1="10" x2="21" y1="18" y2="18"/><path d="M4 6h1v4"/><path d="M4 10h2"/>'
        '<path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"/>'
    ),
    "table": (
        '<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/>'
        '<path d="M3 9h18"/><path d="M3 15h18"/>'
    ),
    "package": (
        '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4'
        'a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/>'
        '<path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/>'
        '<path d="m7.5 4.27 9 5.15"/>'
    ),
    "archive": (
        '<rect width="20" height="5" x="2" y="3" rx="1"/>'
        '<path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>'
    ),
    "git-commit": (
        '<circle cx="12" cy="12" r="3"/>'
        '<line x1="3" x2="9" y1="12" y2="12"/><line x1="15" x2="21" y1="12" y2="12"/>'
    ),
    "key": (
        '<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1'
        'a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586'
        'l.814-.814a6.5 6.5 0 1 0-4-4z"/>'
        '<circle cx="16.5" cy="7.5" r="1"/>'
    ),
    "shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6'
        'a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5'
        'a1 1 0 0 1 1 1z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    # actions
    "sparkles": (
        '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936'
        'A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937'
        'l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135'
        'a.5.5 0 0 1-.963 0z"/>'
        '<path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>'
    ),
}


# Simple Icons brands: slug -> {"title", "hex", "path"} (from icons_extra.json)
BRANDS: dict[str, dict] = {}
BRAND_COLORS = True  # False draws brand icons in the color passed to icon(), like Lucide ones

_EXTRA = Path(__file__).resolve().with_name("icons_extra.json")
if _EXTRA.exists():
    _data = json.loads(_EXTRA.read_text(encoding="utf-8"))
    LUCIDE.update(_data.get("lucide", {}))
    BRANDS.update(_data.get("brands", {}))


def _readable(hex6: str) -> str:
    """The brand color, darkened only when it is too light to see on a white or tinted
    background (e.g. React's cyan, JavaScript's yellow). The hue is kept."""
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    if lum <= 0.45:
        return f"#{hex6}"
    k = 0.62  # keep 62% of each channel
    return "#" + "".join(f"{round(c * 255 * k):02x}" for c in (r, g, b))


def has_icon(name: str) -> bool:
    return name in LUCIDE or name in BRANDS


def icon(name: str, x: float, y: float, size: float, color: str,
         brand_color: bool | None = None) -> str:
    """An icon whose top-left corner is (x, y), size px square.
    Lucide icons are stroked in `color`. Brand icons are filled in the brand color
    (or in `color` when brand_color=False / BRAND_COLORS=False)."""
    scale = size / 24
    if name in LUCIDE:
        return (
            f'<g transform="translate({x:g} {y:g}) scale({scale:g})" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round">{LUCIDE[name]}</g>'
        )
    if name in BRANDS:
        b = BRANDS[name]
        use_brand = BRAND_COLORS if brand_color is None else brand_color
        fill = _readable(b["hex"]) if use_brand else color
        # Brand marks fill the whole 24px box; shrink them to the optical size of Lucide icons.
        return (
            f'<g transform="translate({x:g} {y:g}) scale({scale:g})">'
            f'<g transform="translate(2 2) scale(0.8333)"><title>{escape(b["title"])}</title>'
            f'<path d="{b["path"]}" fill="{fill}"/></g></g>'
        )
    raise KeyError(f"icon '{name}' is not available: run `python fetch_icons.py {name}` "
                   f"(brand) or `python fetch_icons.py --lucide {name}` (generic)")
