"""Fetch icons into icons_extra.json (next to this script), which icons.py loads at import.

Part of the draw-flow-diagram skill. Copyright (c) 2026 nKos. MIT License (see LICENSE).
The fetched icon data keeps its own license (see THIRD_PARTY_NOTICES.md).

    python fetch_icons.py github notion cloudflare python react   # product/brand icons
    python fetch_icons.py --lucide smartphone monitor mail          # generic icons
    python fetch_icons.py --list                                    # what the cache holds

Brand icons come from Simple Icons (CC0 data; the logos remain their owners' trademarks — use
them only to identify the product) and keep the brand color. Slugs are on https://simpleicons.org
(e.g. "nodedotjs", "githubactions"). Generic icons come from Lucide (ISC), https://lucide.dev.

Some brand icons carry their own license (e.g. CC-BY-3.0 needs attribution). The license, source
and brand-guidelines URL of each brand are stored in the cache, and a warning is printed for
licensed icons: add the required notice wherever you publish diagrams or the cache file.

The versions are pinned so a rebuild draws the same icons. The cache file is part of the
diagram code: keep it in the repository so builds need no network.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

SIMPLE_ICONS = "16.36.0"
LUCIDE_STATIC = "1.67.0"
CDN = "https://cdn.jsdelivr.net/npm"
CACHE = Path(__file__).resolve().with_name("icons_extra.json")


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "diagram-icon-fetcher"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def load_cache(path: Path = CACHE) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"versions": {}, "lucide": {}, "brands": {}}


def fetch_brands(slugs: list[str], cache: dict) -> list[str]:
    """Add Simple Icons brands. Returns the slugs that do not exist."""
    data = json.loads(_get(f"{CDN}/simple-icons@{SIMPLE_ICONS}/data/simple-icons.json"))
    by_title = {e["title"]: e for e in data}
    missing = []
    for slug in slugs:
        try:
            svg = _get(f"{CDN}/simple-icons@{SIMPLE_ICONS}/icons/{slug}.svg")
        except urllib.error.HTTPError:
            missing.append(slug)
            continue
        title = re.search(r"<title>(.*?)</title>", svg).group(1)
        title = (title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                 .replace("&quot;", '"').replace("&#39;", "'"))
        path = re.search(r'<path d="([^"]+)"', svg).group(1)
        entry = by_title.get(title, {})
        item = {"title": title, "hex": entry.get("hex", "475569"), "path": path,
                "source": entry.get("source", "")}
        if entry.get("guidelines"):
            item["guidelines"] = entry["guidelines"]
        if entry.get("license"):
            item["license"] = entry["license"]
            print(f"note: {slug} has its own license {entry['license']} - add the notice it "
                  f"requires (source: {item['source']})", file=sys.stderr)
        cache["brands"][slug] = item
    cache["versions"]["simple-icons"] = SIMPLE_ICONS
    return missing


def fetch_lucide(names: list[str], cache: dict) -> list[str]:
    """Add Lucide icons (inner elements only). Returns the names that do not exist."""
    missing = []
    for name in names:
        try:
            svg = _get(f"{CDN}/lucide-static@{LUCIDE_STATIC}/icons/{name}.svg")
        except urllib.error.HTTPError:
            missing.append(name)
            continue
        inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
        inner = re.sub(r"\s*\n\s*", "", inner).replace(" />", "/>")
        cache["lucide"][name] = inner
    cache["versions"]["lucide-static"] = LUCIDE_STATIC
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="Simple Icons slugs (or Lucide names with --lucide)")
    parser.add_argument("--lucide", action="store_true", help="the names are Lucide icons")
    parser.add_argument("--list", action="store_true", help="list the cached icons")
    args = parser.parse_args()
    cache = load_cache()
    if args.list or not args.names:
        print("brands:", " ".join(sorted(cache["brands"])) or "-")
        print("lucide:", " ".join(sorted(cache["lucide"])) or "-")
        return
    missing = (fetch_lucide if args.lucide else fetch_brands)(args.names, cache)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                     encoding="utf-8")
    print(f"saved {CACHE}")
    if missing:
        print("not found:", " ".join(missing), file=sys.stderr)
        sys.exit(1 if len(missing) == len(args.names) else 0)


if __name__ == "__main__":
    main()
