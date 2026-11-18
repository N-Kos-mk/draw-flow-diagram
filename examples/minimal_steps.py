"""A small step flow (swimlane) built with diagram_kit. Use it as a starting template.

    python minimal_steps.py [--out DIR] [--no-png]

Shows: an outside party, two lanes, a list (table), a file (thing), a database (cylinder),
auto/manual action chips, the emphasized main action, a dotted reference, and an actor chip.
The system is fictional. For a larger example with product icons, a scope frame and a
side-column card, see pypi_trusted_publishing.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from diagram_kit import (CYL_H, G, HUES, TABLE_H, THING_H, action, actor_chip, arrow, card,  # noqa: E402
                         cylinder, dot, lane, main_action, main_arrow, ref_end, ref_line, save,
                         svg_document, table_card, table_w, thing, thing_w)

# ---- layout (named constants, so groups move together) ----
W = 760
X1, X2 = 200, 540  # columns: order list / slip PDF
EXT_Y, EXT_H = 20, 64
A_TOP = EXT_Y + EXT_H + 56  # server lane
R1 = A_TOP + 80
R2 = R1 + 110
A_BOTTOM = R2 + 50
W_TOP = A_BOTTOM + 64  # staff lane
WR = W_TOP + 52
W_BOTTOM = WR + 40
H = W_BOTTOM + 20
GAP_MID = (A_BOTTOM + W_TOP) / 2

XA = X1 + table_w("注文一覧") / 2 + G  # main arrow start / end
XB = X2 - thing_w("伝票PDF") / 2 - G
XM = (XA + XB) / 2  # main chip, rule database, actor chip


def background() -> str:
    return (lane(20, A_TOP, W - 20, A_BOTTOM, "blue", "server", "処理サーバー")
            + lane(20, W_TOP, W - 20, W_BOTTOM, "violet", "laptop", "担当者PC"))


def lines() -> str:
    staff = HUES["violet"]["icon"]
    return "".join([
        # ① fetch from the outside party
        arrow(X1, EXT_Y + EXT_H + G, X1, R1 - TABLE_H / 2 - G),
        action(X1, (EXT_Y + EXT_H + A_TOP) / 2, "auto", "① 取得"),
        # ② convert: the main action (the list really becomes PDFs)
        main_arrow(XA, R1, XB, R1),
        main_action(XM, R1, "② 変換"),
        # the conversion consults the rules (dotted, ends at the chip with a dot)
        ref_line(f"M{XM:g},{R2 - CYL_H / 2 - 2:g} V{R1 + 15:g}"),
        ref_end(XM, R1 + 15),
        # ③ download to the staff PC
        arrow(X2, R1 + THING_H / 2 + G, X2, WR - THING_H / 2 - G),
        action(X2, GAP_MID, "manual", "③ ダウンロード"),
        # an instruction from the staff PC changes the rules
        dot(XM, W_TOP, color=staff, r=4),
        arrow(XM, W_TOP, XM, GAP_MID + 13, head=False, color=staff),
        arrow(XM, GAP_MID - 13, XM, R2 + CYL_H / 2 + G),
        actor_chip(XM, GAP_MID, "violet", "laptop", "ルール更新"),
    ])


def things() -> str:
    return "".join([
        card(X1 - 110, EXT_Y, 220, EXT_H, "gray", "globe", "取引先サイト", "社外", dashed=True),
        table_card(X1, R1, "blue", "注文一覧"),
        thing(X2, R1, "blue", "伝票PDF", icon_name="file"),
        cylinder(XM, R2, "blue", "変換ルール"),
        thing(X2, WR, "violet", "伝票PDF", icon_name="file"),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(Path(__file__).resolve().parent / "out"),
                        help="output folder (default: examples/out)")
    parser.add_argument("--no-png", action="store_true", help="write the SVG only")
    args = parser.parse_args()
    body = f"{background()}\n{lines()}\n{things()}"  # lanes -> lines -> boxes
    save(svg_document(W, H, body), args.out, "minimal_steps", png=not args.no_png)


if __name__ == "__main__":
    main()
