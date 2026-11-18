"""Step flow (swimlane): publishing a Python package to PyPI from GitHub Actions with
Trusted Publishing. A full example of the skill's patterns.

    python pypi_trusted_publishing.py [--out DIR] [--no-png]

Patterns shown:
- product icons (GitHub, PyPI, Python, OpenID) next to generic ones
- a service that only supplies one thing to one step (the OIDC provider) as a side-column card,
  so the main line (⑨ upload) crosses no other lane
- a scope frame (the publish job) enclosing all of its chips, released by an optional approval
  through a trigger line
- actor chips (the maintainer's registration and approval), dotted references (⑧, ⑨)
- the main column on the left, so no empty block is left under the tagged commit

Facts were checked against the official documentation:
- https://docs.pypi.org/trusted-publishers/ (short-lived API token)
- https://docs.pypi.org/trusted-publishers/adding-a-publisher/ (owner, repository, workflow
  required; environment optional but strongly recommended)
- https://docs.pypi.org/trusted-publishers/using-a-publisher/ (id-token: write; OIDC token is
  exchanged at PyPI for an API token; the pypa action does the exchange)
- https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
  (publish on tag pushes; build job uploads an artifact; publish job in the "pypi" environment
  downloads it)
- https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/reviewing-deployments
  (approval of a protected environment)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from diagram_kit import (CYL_H, G, HUES, THING_H, action, action_w, actor_chip,  # noqa: E402
                         actor_chip_w, arrow, card, cylinder, cylinder_w, dot, lane,
                         main_action, main_action_w, main_arrow, path_arrow, ref_end, ref_line,
                         save, scope_frame, svg_document, text_width, thing, thing_w,
                         trigger_line)

# ---- labels ----
L_TAG, L_DIST, L_ART = "タグ付きコミット", "配布物", "アーティファクト"
L_API, L_OIDC, L_CFG = "API トークン", "OIDC トークン", "信頼する発行元の設定"
C1, C2, C3, C4 = "① 信頼する発行元を登録", "② タグを push", "③ ビルド", "④ 保存"
C5, C6, C7, C8, C9 = "⑤ 承認", "⑥ 取り出し", "⑦ 取得", "⑧ PyPI で交換", "⑨ アップロード"
FRAME_LABEL = "公開のジョブ（pypi 環境）"
OIDC_NAME, OIDC_ROLE = "OIDC プロバイダー", "GitHub"

# ---- columns ----
# The main column (distributions -> artifact -> job -> PyPI) is on the left, so the build (③)
# runs right to left from the tagged commit. This leaves no empty block under the commit.
GAP = 14  # clear space between a chip and the box beside it
X2 = 140  # main column
XT = X2 + thing_w(L_DIST) / 2 + G + GAP + action_w(C3) + GAP + G + thing_w(L_TAG) / 2  # commit
X3 = max(XT,  # tokens, aligned with the commit
         X2 + main_action_w(C9) / 2 + 36 + thing_w(L_API) / 2,  # room for the ⑨ reference
         X2 + thing_w(L_DIST) / 2 + 40 + thing_w(L_OIDC) / 2)
X7 = X3 + thing_w(L_OIDC) / 2 + G + GAP + action_w(C7) / 2  # ⑦ chip
FL = X2 - main_action_w(C9) / 2 - 18  # publish-job frame
FR = X7 + action_w(C7) / 2 + GAP
XS = X3 + thing_w(L_OIDC) / 2 + 30  # settings (its reference line rises here)
LANE_R = max(FR, XS + cylinder_w(L_CFG) / 2 + 12) + 20
XR = LANE_R + 28  # side column: ① route
CARD_W = text_width(OIDC_NAME, 18, bold=True) + 74 + 20
CARD_X = XR + 26
XA = XT + action_w(C2) / 2 + 18 + actor_chip_w(C5, True) / 2  # ⑤ approval, right of ②
FRAME_LABEL_X = X2 + action_w(C6) / 2 + 16  # right of the ⑥ line, left of the ⑤ trigger
W = CARD_X + CARD_W + 20

# ---- rows ----
M_TOP = 20
RM = M_TOP + 62
M_BOTTOM = RM + THING_H / 2 + 18
A_TOP = M_BOTTOM + 66
GAP1 = (M_BOTTOM + A_TOP) / 2
R1 = A_TOP + 62  # tagged commit -> distributions
R2 = R1 + 110  # artifact
FT = R2 + THING_H / 2 + 22  # frame top
Y6 = FT + 30  # ⑥ chip (inside the frame)
R3 = FT + 82  # distributions / OIDC token
R4 = R3 + 110  # ⑨ chip / API token
FB = R4 + THING_H / 2 + 16
A_BOTTOM = FB + 14
P_TOP = A_BOTTOM + 60
RP = P_TOP + 62
P_BOTTOM = RP + CYL_H / 2 + 18
H = P_BOTTOM + 20
GAP2 = (A_BOTTOM + P_TOP) / 2  # ① chip (side column, between GitHub and PyPI)


def background() -> str:
    return "".join([
        lane(20, M_TOP, LANE_R, M_BOTTOM, "violet", "user", "メンテナー"),
        lane(20, A_TOP, LANE_R, A_BOTTOM, "blue", "github", "GitHub"),
        lane(20, P_TOP, LANE_R, P_BOTTOM, "amber", "pypi", "PyPI"),
        scope_frame(FL, FT, FR, FB, FRAME_LABEL, "blue", label_x=FRAME_LABEL_X),
    ])


def lines() -> str:
    dev = HUES["violet"]["icon"]
    h = THING_H / 2
    y8 = (R3 + R4) / 2
    return "".join([
        # ① registration: maintainer -> settings, routed down the side column
        dot(LANE_R, RM, color=dev, r=4),
        f'<path d="M{LANE_R:g},{RM:g} H{XR:g} V{GAP2 - 13:g}" fill="none" stroke="{dev}" '
        f'stroke-width="1.6" stroke-linejoin="round"/>',
        path_arrow(f"M{XR:g},{GAP2 + 13:g} V{RP:g} H{XS + cylinder_w(L_CFG) / 2 + G:g}"),
        # ② push the tag
        arrow(XT, RM + h + G, XT, R1 - h - G),
        # ③ build: the tagged commit becomes distributions (right to left)
        arrow(XT - thing_w(L_TAG) / 2 - G, R1, X2 + thing_w(L_DIST) / 2 + G, R1),
        # ④ save as an artifact
        arrow(X2, R1 + h + G, X2, R2 - h - G),
        # ⑤ approval (optional) releases the publish job: trigger line to the frame's edge
        dot(XA, M_BOTTOM, color=dev, r=4),
        arrow(XA, M_BOTTOM, XA, GAP1 - 13, head=False, color=dev),
        trigger_line(f"M{XA:g},{GAP1 + 13:g} V{FT:g}", (XA, FT), "violet"),
        # ⑥ download inside the job
        arrow(X2, R2 + h + G, X2, R3 - h - G),
        # ⑦ OIDC token from the provider (side column) to the job
        arrow(CARD_X - G, R3, X3 + thing_w(L_OIDC) / 2 + G, R3),
        # ⑧ exchange at PyPI, checked against the settings
        arrow(X3, R3 + h + G, X3, R4 - h - G),
        ref_line(f"M{XS:g},{RP - CYL_H / 2 - 2:g} V{y8:g} H{X3 + action_w(C8) / 2:g}"),
        ref_end(X3 + action_w(C8) / 2, y8),
        # ⑨ upload with the API token (main action)
        main_arrow(X2, R3 + h + G, X2, RP - h - G),
        ref_line(f"M{X3 - thing_w(L_API) / 2 - 2:g},{R4:g} H{X2 + main_action_w(C9) / 2:g}"),
        ref_end(X2 + main_action_w(C9) / 2, R4),
    ])


def things() -> str:
    return "".join([
        thing(XT, RM, "violet", L_TAG, icon_name="git-commit"),
        thing(XT, R1, "blue", L_TAG, icon_name="git-commit"),
        thing(X2, R1, "blue", L_DIST, icon_name="python"),
        thing(X2, R2, "blue", L_ART, icon_name="archive"),
        thing(X2, R3, "blue", L_DIST, icon_name="python"),
        thing(X3, R3, "blue", L_OIDC, icon_name="key"),
        thing(X3, R4, "blue", L_API, icon_name="key"),
        thing(X2, RP, "amber", L_DIST, icon_name="python"),
        cylinder(XS, RP, "amber", L_CFG),
        card(CARD_X, R3 - 32, CARD_W, 64, "teal", "openid", OIDC_NAME, OIDC_ROLE),
    ])


def chips() -> str:
    return "".join([
        actor_chip(XR, GAP2, "violet", "user", C1),
        action(XT, GAP1, "manual", C2),
        action((X2 + thing_w(L_DIST) / 2 + XT - thing_w(L_TAG) / 2) / 2, R1, "auto", C3),
        action(X2, (R1 + R2) / 2, "auto", C4),
        actor_chip(XA, GAP1, "violet", "user", C5, optional=True),
        action(X2, Y6, "auto", C6),
        action(X7, R3, "auto", C7),
        action(X3, (R3 + R4) / 2, "auto", C8),
        main_action(X2, R4, C9, icon_name="cloud-upload"),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(Path(__file__).resolve().parent / "out"),
                        help="output folder (default: examples/out)")
    parser.add_argument("--no-png", action="store_true")
    args = parser.parse_args()
    body = f"{background()}\n{lines()}\n{things()}\n{chips()}"
    save(svg_document(W, H, body), args.out, "pypi_trusted_publishing", png=not args.no_png)


if __name__ == "__main__":
    main()
