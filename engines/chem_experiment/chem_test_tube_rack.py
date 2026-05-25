import svgwrite


def render_test_tube_rack(spec: dict, out_path: str) -> bool:
    hints = spec.get("render_hints", {})
    ch    = hints.get("canvas", spec.get("canvas", {}))

    w  = ch.get("width",  900)
    h  = ch.get("height", 800)
    bg = ch.get("background", "#FFFFFF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    OL     = "#1a1a1a"
    WOOD_F = "#EBC99A"   # main face wood
    WOOD_T = "#F5DFB8"   # top / inner lighter face
    WOOD_D = "#C8956A"   # right-side darker face
    WOOD_I = "#EDD5A0"   # inner back / side walls

    # ── RACK GEOMETRY ─────────────────────────────────────────────
    fl, fr, ft, fb = 185, 788, 362, 758   # outer front face
    board = 42                             # board thickness
    dx, dy = 62, 54                        # 3-D depth offset (right, up)

    il = fl + board   # 227  inner opening left
    ir = fr - board   # 746  inner opening right
    it = ft + board   # 404  inner opening top
    ib = fb - board   # 716  inner opening bottom

    # Corners of the back wall (inner opening projected by depth)
    bl, br, bt, bb = il+dx, ir+dx, it-dy, ib-dy
    # = 289, 808, 350, 662

    # ── 1. INNER BACK WALL ─────────────────────────────────────────
    dwg.add(dwg.rect(insert=(bl, bt), size=(br-bl, bb-bt),
                     fill=WOOD_I, stroke=OL, stroke_width=1.5))

    # ── 2. INNER FLOOR (trapezoid front→back) ─────────────────────
    dwg.add(dwg.polygon(
        points=[(il, ib), (ir, ib), (br, bb), (bl, bb)],
        fill=WOOD_T, stroke=OL, stroke_width=1.5,
    ))

    # ── 3. INNER LEFT WALL (trapezoid) ───────────────────────────
    dwg.add(dwg.polygon(
        points=[(il, it), (il, ib), (bl, bb), (bl, bt)],
        fill=WOOD_I, stroke=OL, stroke_width=1.5,
    ))

    # ── 4. TEST TUBES (liquid + glass, inside rack) ───────────────
    tube_rx  = 46
    tube_ry  = 11    # top-ellipse minor radius
    tube_top = 192   # visible tube top (above rack)
    tube_bot = 704   # rounded bottom y (inside rack)

    # Left tube: deep blue gradient; Right tube: very light blue
    TUBES = [
        (415, "gL", "#90D0F5", "#3AAAE8", "#1882D0"),
        (620, "gR", "#D8EFFC", "#AADAF5", "#85C4EC"),
    ]

    for cx, gid, c0, c1, c2 in TUBES:
        # Gradient for liquid
        g = dwg.defs.add(dwg.linearGradient(id=gid, x1="0", y1="0", x2="0", y2="1"))
        g.add_stop_color(0,   c0, opacity=0.80)
        g.add_stop_color(0.5, c1, opacity=0.95)
        g.add_stop_color(1,   c2, opacity=1.0)

        liq_y1 = it + 6
        liq_y2 = tube_bot - 8

        # Liquid body
        dwg.add(dwg.rect(
            insert=(cx - tube_rx + 3, liq_y1),
            size=(tube_rx*2 - 6, liq_y2 - liq_y1),
            fill=f"url(#{gid})", stroke="none",
        ))
        # Liquid bottom ellipse
        dwg.add(dwg.ellipse(center=(cx, liq_y2), r=(tube_rx-3, tube_ry),
                            fill=c2, stroke="none"))

        # Glass tube outline (inside-rack section only)
        dwg.add(dwg.line(start=(cx-tube_rx, it), end=(cx-tube_rx, tube_bot),
                         stroke=OL, stroke_width=2.5))
        dwg.add(dwg.line(start=(cx+tube_rx, it), end=(cx+tube_rx, tube_bot),
                         stroke=OL, stroke_width=2.5))
        # Rounded bottom arc
        dwg.add(dwg.path(
            d=(f"M {cx-tube_rx} {tube_bot} "
               f"Q {cx} {tube_bot + int(tube_rx*0.88)}, {cx+tube_rx} {tube_bot}"),
            fill="none", stroke=OL, stroke_width=2.5,
        ))
        # Inner glass highlight
        dwg.add(dwg.line(
            start=(cx-tube_rx+8, it+20), end=(cx-tube_rx+8, tube_bot-55),
            stroke="#FFFFFF", stroke_width=5, opacity=0.55,
        ))

    # ── 5. FRONT FRAME (four border boards) ───────────────────────
    # Top board
    dwg.add(dwg.rect(insert=(fl, ft), size=(fr-fl, board),
                     fill=WOOD_F, stroke=OL, stroke_width=2.5))
    # Bottom board
    dwg.add(dwg.rect(insert=(fl, fb-board), size=(fr-fl, board),
                     fill=WOOD_F, stroke=OL, stroke_width=2.5))
    # Left board
    dwg.add(dwg.rect(insert=(fl, ft), size=(board, fb-ft),
                     fill=WOOD_F, stroke=OL, stroke_width=2.5))
    # Right board
    dwg.add(dwg.rect(insert=(fr-board, ft), size=(board, fb-ft),
                     fill=WOOD_F, stroke=OL, stroke_width=2.5))

    # ── 6. RIGHT SIDE FACE ────────────────────────────────────────
    dwg.add(dwg.polygon(
        points=[(fr, ft), (fr, fb), (fr+dx, fb-dy), (fr+dx, ft-dy)],
        fill=WOOD_D, stroke=OL, stroke_width=2.5,
    ))

    # ── 7. TOP SURFACE PARALLELOGRAM ─────────────────────────────
    top_pts = [(fl, ft), (fr, ft), (fr+dx, ft-dy), (fl+dx, ft-dy)]
    dwg.add(dwg.polygon(points=top_pts, fill=WOOD_T, stroke=OL, stroke_width=2.5))

    # Holes in top surface where tubes pass through
    for cx, gid, c0, c1, c2 in TUBES:
        hx = cx + int(dx * 0.35)
        hy = ft - int(dy * 0.35)
        dwg.add(dwg.ellipse(center=(hx, hy), r=(tube_rx, tube_ry),
                            fill="#C8B888", stroke=OL, stroke_width=2))
        dwg.add(dwg.ellipse(center=(hx, hy), r=(tube_rx, tube_ry),
                            fill="none", stroke=OL, stroke_width=2.5))

    # ── 8. TUBE BODIES ABOVE RACK ─────────────────────────────────
    for cx, gid, c0, c1, c2 in TUBES:
        hx = cx + int(dx * 0.35)
        hy = ft - int(dy * 0.35)

        # Semi-transparent glass body above rack
        dwg.add(dwg.rect(
            insert=(cx-tube_rx, tube_top),
            size=(tube_rx*2, hy - tube_top),
            fill="#F5F5FF", opacity=0.55, stroke="none",
        ))
        # Left / right outlines
        dwg.add(dwg.line(start=(cx-tube_rx, tube_top), end=(cx-tube_rx, hy),
                         stroke=OL, stroke_width=2.5))
        dwg.add(dwg.line(start=(cx+tube_rx, tube_top), end=(cx+tube_rx, hy),
                         stroke=OL, stroke_width=2.5))
        # Highlight
        dwg.add(dwg.line(
            start=(cx-tube_rx+8, tube_top+tube_ry+5), end=(cx-tube_rx+8, hy-5),
            stroke="#FFFFFF", stroke_width=4, opacity=0.50,
        ))
        # Open top rim
        dwg.add(dwg.ellipse(center=(cx, tube_top), r=(tube_rx, tube_ry),
                            fill="#ECECEC", stroke=OL, stroke_width=2.5))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
