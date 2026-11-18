"""Building blocks for documentation diagrams. Every function returns an SVG fragment (str).

Part of the draw-flow-diagram skill. Copyright (c) 2026 nKos. MIT License (see LICENSE).

Copy this file, icons.py, icons_extra.json, fetch_icons.py and render.py into the project's
diagram folder, then write one script per diagram that concatenates fragments and calls
save(). See ../examples/.

Conventions
- Positions are centers (cx, cy) for things and chips, top-left (x, y) for cards and frames.
- Draw order: zones/lanes -> lines -> things and chips (chips cover the lines they label).
- Lines stop G px short of the box they touch.
- Colors: pick one HUES key per place (machine/service) and keep it for the whole set.
- Circled numbers (①..⑳) in any text are made bold automatically (svg_document).

Requires Pillow for exact text widths (falls back to an estimate) and Playwright for PNG.
"""

from __future__ import annotations

import re
from functools import lru_cache
from html import escape
from pathlib import Path

from icons import icon

# ---- style ----
FONT = '"BIZ UDPGothic", "Yu Gothic UI", Meiryo, "Hiragino Sans", "Noto Sans JP", sans-serif'
MONO = 'Consolas, "Cascadia Mono", Menlo, monospace'

INK = "#0f172a"  # names
SUB = "#334155"  # chip labels, roles
MUTED = "#64748b"  # notes, addresses
LINE = "#64748b"  # arrows
REF = "#94a3b8"  # dotted reference lines
MAIN = "#1d4ed8"  # the emphasized main action

# Place colors. stroke = borders, tint = fills, icon = icons and lane labels.
HUES = {
    "blue": {"stroke": "#93c5fd", "tint": "#dbeafe", "icon": "#1d4ed8"},
    "amber": {"stroke": "#fcd34d", "tint": "#fef3c7", "icon": "#b45309"},
    "green": {"stroke": "#6ee7b7", "tint": "#d1fae5", "icon": "#047857"},
    "violet": {"stroke": "#c4b5fd", "tint": "#ede9fe", "icon": "#6d28d9"},
    "rose": {"stroke": "#fda4af", "tint": "#ffe4e6", "icon": "#be123c"},
    "teal": {"stroke": "#5eead4", "tint": "#ccfbf1", "icon": "#0f766e"},
    "gray": {"stroke": "#94a3b8", "tint": "#f1f5f9", "icon": "#475569"},  # outside parties
}
ZONE = {"fill": "#f8fafc", "stroke": "#cbd5e1", "label": "#475569"}

# Tags on action chips: auto/manual (always one of them) and optional (steps that only
# happen when configured). Change "text" for another language.
TAGS = {
    "auto": {"text": "自動", "fill": "#e2e8f0", "ink": "#334155"},
    "manual": {"text": "手動", "fill": "#334155", "ink": "#ffffff"},
    "optional": {"text": "任意", "fill": "#ffffff", "ink": "#475569", "stroke": "#94a3b8"},
}

# ---- sizes ----
G = 6  # gap between a line end and the box it touches
THING_H = 44
CYL_H, CYL_RY = 52, 7
STACK_H, STACK_OFF = 44, 8
TABLE_H = 52
CHIP_H = 24

# Font files used to measure text (first one found wins).
FONT_FILES = {
    False: [("C:/Windows/Fonts/BIZ-UDGothicR.ttc", 1), ("C:/Windows/Fonts/YuGothR.ttc", 0),
            ("C:/Windows/Fonts/meiryo.ttc", 0),
            ("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 0),
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 0)],
    True: [("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 1), ("C:/Windows/Fonts/YuGothB.ttc", 0),
           ("C:/Windows/Fonts/meiryob.ttc", 0),
           ("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 0),
           ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0)],
}


# ---- text ----
def text(x: float, y: float, s: str, *, size: float, color: str = INK, weight: int = 400,
         anchor: str = "start", family: str = FONT, plain: bool = False) -> str:
    """One line of text. y is the baseline. plain=True keeps circled numbers unbolded."""
    attr = ' data-plain="1"' if plain else ""
    return (f'<text{attr} x="{x:g}" y="{y:g}" font-family=\'{family}\' font-size="{size:g}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')


@lru_cache(maxsize=None)
def _font(bold: bool, size: float):
    from PIL import ImageFont

    for path, index in FONT_FILES[bold]:
        if Path(path).exists():
            return ImageFont.truetype(path, round(size * 10), index=index)
    raise FileNotFoundError("no font file for measuring")


def text_width(s: str, size: float, bold: bool = False) -> float:
    """Width of s in px. Size boxes from this so labels never overflow."""
    try:
        return _font(bold, size).getlength(s) / 10
    except Exception:  # no Pillow or no font: estimate
        return sum(size if ord(c) > 0x2000 else size * 0.58 for c in s)


def note(x: float, y: float, lines: list[str], anchor: str = "start") -> str:
    """Small gray text. Use sparingly (rule 1)."""
    return "".join(text(x, y + i * 16, s, size=12, color=MUTED, anchor=anchor)
                   for i, s in enumerate(lines))


def arrow_label(x: float, y: float, lines: list[str], anchor: str = "start") -> str:
    """What moves along an arrow (configuration diagrams). y is the first baseline."""
    return "".join(text(x, y + i * 19, s, size=13.5, color=SUB, anchor=anchor)
                   for i, s in enumerate(lines))


# ---- places ----
def card(x: float, y: float, w: float, h: float, hue: str, icon_name: str, name: str,
         role: str | None = None, addr: str | None = None, *, dashed: bool = False,
         stack: bool = False) -> str:
    """A machine or service: icon circle, name, role, address. stack=True means several."""
    c = HUES[hue]
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    rect = (f'width="{w:g}" height="{h:g}" rx="12" fill="#ffffff" '
            f'stroke="{c["stroke"]}" stroke-width="1.5"{dash}')
    parts = [f'<rect x="{x + d:g}" y="{y + d:g}" {rect}/>' for d in ((10, 5) if stack else ())]
    parts.append(f'<rect x="{x:g}" y="{y:g}" {rect}/>')
    icx, icy = x + 38, y + h / 2
    parts.append(f'<circle cx="{icx:g}" cy="{icy:g}" r="22" fill="{c["tint"]}"/>')
    parts.append(icon(icon_name, icx - 12, icy - 12, 24, c["icon"]))
    lines = [s for s in (role, addr) if s]
    block = 14 + (22 + 20 * (len(lines) - 1) if lines else 0) + 4
    base = y + (h - block) / 2 + 14
    tx = x + 74
    parts.append(text(tx, base, name, size=18, weight=700))
    if role:
        parts.append(text(tx, base + 22, role, size=13.5, color=SUB))
    if addr:
        parts.append(text(tx, base + 22 + (20 if role else 0), addr, size=12.5, color=MUTED,
                          family=MONO))
    return "".join(parts)


def zone(x: float, y: float, w: float, h: float, name: str, icon_name: str = "network") -> str:
    """A boundary such as the company LAN. Outside parties stay outside it."""
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="18" fill="{ZONE["fill"]}" '
        f'stroke="{ZONE["stroke"]}" stroke-width="1.5"/>'
        + icon(icon_name, x + 16, y + 13, 18, ZONE["label"])
        + text(x + 42, y + 28, name, size=15, weight=700, color=ZONE["label"])
    )


def lane(x0: float, y0: float, x1: float, y1: float, hue: str, icon_name: str,
         name: str) -> str:
    """A swimlane for one machine. Label is horizontal at the top-left inside.
    Keep lines away from the label area (about x0..x0+150, y0..y0+30)."""
    c = HUES[hue]
    return (
        f'<rect x="{x0:g}" y="{y0:g}" width="{x1 - x0:g}" height="{y1 - y0:g}" rx="14" '
        f'fill="{c["tint"]}" fill-opacity="0.35" stroke="{c["stroke"]}" stroke-width="1.5"/>'
        + icon(icon_name, x0 + 12, y0 + 9, 17, c["icon"])
        + text(x0 + 35, y0 + 23, name, size=14, weight=700, color=c["icon"])
    )


def scope_frame(x0: float, y0: float, x1: float, y1: float, label: str, hue: str = "blue",
                label_at: str = "right", label_x: float | None = None) -> str:
    """A dashed boundary around the things and chips that run inside one job, environment or
    permission scope. It is a boundary, not a box: enclose every thing and chip of the scope,
    never end an arrow on it, and connect a gating instruction with trigger_line() to its edge.
    The label sits inside the top edge: label_at "left" or "right", or an explicit left x
    (label_x) when lines enter the frame at those places. Keep lines away from the label."""
    c = HUES[hue]
    tw = text_width(label, 12.5, bold=True)
    if label_x is not None:
        lx = label_x
    else:
        lx = x0 + 12 if label_at == "left" else x1 - 12 - tw
    return (
        f'<rect x="{x0:g}" y="{y0:g}" width="{x1 - x0:g}" height="{y1 - y0:g}" rx="10" '
        f'fill="#ffffff" fill-opacity="0.55" stroke="{c["icon"]}" stroke-width="1.3" '
        f'stroke-dasharray="6 4"/>'
        + text(lx, y0 + 18, label, size=12.5, weight=700, color=c["icon"])
    )


def divider(x: float, y0: float, y1: float) -> str:
    """Light dashed vertical divider between columns (side-process diagrams)."""
    return (f'<line x1="{x:g}" y1="{y0:g}" x2="{x:g}" y2="{y1:g}" stroke="#cbd5e1" '
            f'stroke-width="1.2" stroke-dasharray="4 5"/>')


# ---- things ----
def thing_w(label: str) -> float:
    return max(110, text_width(label, 14, bold=True) + 50)


def thing(cx: float, cy: float, hue: str, label: str, icon_name: str = "image") -> str:
    """An image or file: white card with an icon. Width from thing_w(label)."""
    c = HUES[hue]
    w = thing_w(label)
    x, y = cx - w / 2, cy - THING_H / 2
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{THING_H}" rx="8" fill="#ffffff" '
        f'stroke="{c["stroke"]}" stroke-width="1.5"/>'
        + icon(icon_name, x + 12, cy - 8, 16, c["icon"])
        + text(x + 34, cy + 5, label, size=14, weight=700)
    )


def cylinder_w(label: str) -> float:
    return max(100, text_width(label, 14, bold=True) + 36)


def cylinder(cx: float, cy: float, hue: str, label: str) -> str:
    """Records in a database. Height CYL_H."""
    c = HUES[hue]
    w = cylinder_w(label)
    x, y, h, ry = cx - w / 2, cy - CYL_H / 2, CYL_H, CYL_RY
    body = (f"M{x:g},{y + ry:g} A{w / 2:g},{ry} 0 0 0 {x + w:g},{y + ry:g} "
            f"V{y + h - ry:g} A{w / 2:g},{ry} 0 0 1 {x:g},{y + h - ry:g} Z")
    return (
        f'<path d="{body}" fill="{c["tint"]}" stroke="{c["stroke"]}" stroke-width="1.5"/>'
        f'<ellipse cx="{cx:g}" cy="{y + ry:g}" rx="{w / 2:g}" ry="{ry}" fill="#ffffff" '
        f'stroke="{c["stroke"]}" stroke-width="1.5"/>'
        + text(cx, cy + ry / 2 + 5, label, size=14, weight=700, anchor="middle")
    )


def stacked_w(label: str) -> float:
    return max(154, text_width(label, 14, bold=True) + 50)


def stacked(cx: float, cy: float, hue: str, label: str) -> str:
    """A queue / waiting list: stacked cards. The stack sticks out STACK_OFF up and right."""
    c = HUES[hue]
    w = stacked_w(label)
    x, y = cx - w / 2, cy - STACK_H / 2
    rect = (f'width="{w:g}" height="{STACK_H}" rx="6" fill="{c["tint"]}" '
            f'stroke="{c["stroke"]}" stroke-width="1.5"')
    o = STACK_OFF
    return (
        f'<rect x="{x + o:g}" y="{y - o:g}" {rect}/>'
        f'<rect x="{x + o / 2:g}" y="{y - o / 2:g}" {rect}/>'
        f'<rect x="{x:g}" y="{y:g}" {rect}/>'
        + icon("list-ordered", x + 12, cy - 8, 16, c["icon"])
        + text(x + 34, cy + 5, label, size=14, weight=700)
    )


def table_w(label: str) -> float:
    return max(110, text_width(label, 14, bold=True) + 56)


def table_card(cx: float, cy: float, hue: str, label: str) -> str:
    """A list or ledger of items: a table with a header band."""
    c = HUES[hue]
    w, h = table_w(label), TABLE_H
    x, y = cx - w / 2, cy - h / 2
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h}" rx="4" fill="#ffffff" '
        f'stroke="{c["icon"]}" stroke-width="1.5"/>'
        f'<path d="M{x + 0.75:g},{y + 13:g} V{y + 4:g} Q{x + 0.75:g},{y + 0.75:g} '
        f'{x + 4:g},{y + 0.75:g} H{x + w - 4:g} Q{x + w - 0.75:g},{y + 0.75:g} '
        f'{x + w - 0.75:g},{y + 4:g} V{y + 13:g} Z" fill="{c["stroke"]}"/>'
        f'<line x1="{x:g}" y1="{y + 13:g}" x2="{x + w:g}" y2="{y + 13:g}" '
        f'stroke="{c["icon"]}" stroke-width="1"/>'
        + icon("table", x + 16, cy - 1, 16, c["icon"])
        + text(x + 40, cy + 12, label, size=14, weight=700)
    )


# ---- actions ----
def _tag(x: float, cy: float, kind: str, ink: str | None = None,
         fill: str | None = None) -> str:
    t = TAGS[kind]
    stroke = f' stroke="{t["stroke"]}" stroke-width="1"' if "stroke" in t else ""
    return (f'<rect x="{x:g}" y="{cy - 8:g}" width="28" height="16" rx="8" '
            f'fill="{fill or t["fill"]}"{stroke}/>'
            + text(x + 14, cy + 4, t["text"], size=10.5, weight=700, color=ink or t["ink"],
                   anchor="middle"))


OPT_W = 4 + 28  # extra width of the optional tag


def action_w(label: str, optional: bool = False) -> float:
    return 5 + 28 + 5 + text_width(label, 13) + 9 + (OPT_W if optional else 0)


def action(cx: float, cy: float, kind: str, label: str, border: str | None = None,
           optional: bool = False) -> str:
    """An action chip placed on a line: [tag] label [任意]. kind is "auto" or "manual".
    border: give actions started by an actor chip the actor's stroke color.
    optional: the step only happens when configured (adds the 任意 tag)."""
    w = action_w(label, optional)
    x = cx - w / 2
    stroke, bw = (border, 1.6) if border else ("#cbd5e1", 1.2)
    tw = text_width(label, 13)
    return (
        f'<rect x="{x:g}" y="{cy - CHIP_H / 2:g}" width="{w:g}" height="{CHIP_H}" rx="12" '
        f'fill="#ffffff" stroke="{stroke}" stroke-width="{bw}"/>'
        + _tag(x + 5, cy, kind)
        + text(x + 38, cy + 4.5, label, size=13, color=SUB)
        + (_tag(x + 38 + tw + 4, cy, "optional") if optional else "")
    )


def pair_action(x1: float, x2: float, cy: float, kind: str, label: str) -> str:
    """One chip for one action that moves two things along two parallel vertical lines."""
    return (f'<line x1="{x1:g}" y1="{cy:g}" x2="{x2:g}" y2="{cy:g}" stroke="#cbd5e1" '
            f'stroke-width="1.4"/>' + action((x1 + x2) / 2, cy, kind, label))


def main_action_w(label: str) -> float:
    return 9 + 15 + 5 + text_width(label, 14, bold=True) + 7 + 28 + 5


def main_action(cx: float, cy: float, label: str, kind: str = "auto",
                icon_name: str = "sparkles") -> str:
    """The emphasized main processing step (filled blue chip). Use once per flow."""
    tw = text_width(label, 14, bold=True)
    w = main_action_w(label)
    x = cx - w / 2
    tx = x + 29
    return (
        f'<rect x="{x:g}" y="{cy - 15:g}" width="{w:g}" height="30" rx="15" fill="{MAIN}"/>'
        + icon(icon_name, x + 9, cy - 7.5, 15, "#ffffff", brand_color=False)
        + text(tx, cy + 5, label, size=14, weight=700, color="#ffffff", plain=True)
        + _tag(tx + tw + 7, cy, kind, ink=MAIN, fill="#ffffff")
    )


def actor_chip_w(label: str, optional: bool = False) -> float:
    return 8 + 15 + 5 + text_width(label, 13, bold=True) + 6 + 28 + 5 + (OPT_W if optional else 0)


def actor_chip(cx: float, cy: float, hue: str, icon_name: str, label: str,
               kind: str = "manual", optional: bool = False) -> str:
    """An instruction given by a machine or person, in that place's color and icon.
    Connect it to the place with a solid line from dot() at the place's edge. What it starts:
    an arrow to the data it changes, or trigger_line() to the chips or scope frame it starts."""
    c = HUES[hue]
    tw = text_width(label, 13, bold=True)
    w = actor_chip_w(label, optional)
    x = cx - w / 2
    return (
        f'<rect x="{x:g}" y="{cy - 13:g}" width="{w:g}" height="26" rx="13" '
        f'fill="{c["tint"]}" stroke="{c["stroke"]}" stroke-width="1.4"/>'
        + icon(icon_name, x + 8, cy - 7.5, 15, c["icon"])
        + text(x + 28, cy + 4.5, label, size=13, weight=700, color=c["icon"])
        + _tag(x + 28 + tw + 6, cy, kind)
        + (_tag(x + 28 + tw + 6 + OPT_W, cy, "optional") if optional else "")
    )


# ---- lines ----
def arrow(x1: float, y1: float, x2: float, y2: float, *, head: bool = True,
          both: bool = False, color: str = LINE, width: float = 1.6) -> str:
    """A straight line, with an arrow head at the end (and the start if both=True)."""
    end = ' marker-end="url(#arrow)"' if head else ""
    start = ' marker-start="url(#arrow)"' if both else ""
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" '
            f'stroke-width="{width}"{end}{start}/>')


def path_arrow(d: str, color: str = LINE) -> str:
    """A bent arrow. d is SVG path data, e.g. "M10,10 H80 V60"."""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linejoin="round" marker-end="url(#arrow)"/>')


def main_arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    """The thick blue line of the main action."""
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{MAIN}" '
            f'stroke-width="2.8" marker-end="url(#arrow-main)"/>')


def ref_line(d: str, color: str = REF) -> str:
    """A dotted reference line (an action consults this data). End each branch with ref_end."""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-dasharray="3 4" stroke-linecap="round"/>')


def ref_end(x: float, y: float, color: str = REF) -> str:
    """The dot that marks where a reference line reaches its target chip."""
    return f'<circle cx="{x:g}" cy="{y:g}" r="3" fill="{color}"/>'


def trigger_line(d: str, end: tuple[float, float], hue: str) -> str:
    """A dotted line in the actor's color from an actor chip to what it starts (the chips it
    starts, or the edge of a scope frame), with a dot at `end`. Nothing moves along it."""
    color = HUES[hue]["icon"]
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-dasharray="3 4" stroke-linecap="round"/>'
            f'<circle cx="{end[0]:g}" cy="{end[1]:g}" r="3.5" fill="{color}"/>')


def dot(x: float, y: float, color: str = LINE, r: float = 3.5) -> str:
    """A junction, or the point where an actor chip's line leaves its place."""
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{color}"/>'


# ---- document ----
_NUMBER = re.compile("([\u2460-\u2473])")  # ①..⑳
_TEXT = re.compile(r"(<text\b[^>]*>)(.*?)(</text>)", re.S)


def _emphasize_numbers(svg: str) -> str:
    def fix(m: re.Match) -> str:
        if "data-plain" in m.group(1):
            return m.group(0)
        body = _NUMBER.sub(rf'<tspan font-weight="700" fill="{INK}">\1</tspan>', m.group(2))
        return m.group(1) + body + m.group(3)

    return _TEXT.sub(fix, svg)


def svg_document(w: float, h: float, body: str) -> str:
    """Wrap fragments into a complete SVG with a white background and arrow markers."""
    marker = ('<marker id="{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{s}" '
              'markerHeight="{s}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
              'fill="{c}"/></marker>')
    defs = (marker.format(id="arrow", s=6.5, c=LINE)
            + marker.format(id="arrow-main", s=5, c=MAIN))
    return _emphasize_numbers(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" '
        f'viewBox="0 0 {w:g} {h:g}">\n<defs>{defs}</defs>\n'
        f'<rect width="{w:g}" height="{h:g}" fill="#ffffff"/>\n{body}\n</svg>\n'
    )


def save(svg: str, out_dir: Path | str, name: str, png: bool = True, scale: float = 2) -> None:
    """Write out_dir/name.svg and (unless png=False) out_dir/name.png at `scale`."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    svg_path = out / f"{name}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(svg_path)
    if png:
        from render import svg_to_png

        print(svg_to_png(svg_path, scale=scale))
