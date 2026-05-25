import svgwrite


def render_sunlight_exposure(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {})
    w  = canvas.get("width",  900)
    h  = canvas.get("height", 790)
    bg = canvas.get("background", "#ffffff")

    win_cfg  = spec.get("window", {})
    beam_cfg = spec.get("sunlight_beam", {})
    tbl_cfg  = spec.get("table", {})
    dish_cfg = spec.get("dish", {})

    frame_c  = win_cfg.get("frame_color",       "#C8A456")
    frame_ol = win_cfg.get("frame_outline",      "#2E2E2E")
    frame_sw = win_cfg.get("frame_stroke_width", 2.5)
    ft       = win_cfg.get("frame_thickness",    18)
    glass_c  = win_cfg.get("glass_color",        "#F4F8FF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Sunlight beam gradient (drawn first — behind window) ─────────────
    ct   = beam_cfg.get("color_top",      "#FFE533")
    cb   = beam_cfg.get("color_bottom",   "#FFF5AA")
    ot   = beam_cfg.get("opacity_top",    0.92)
    ob   = beam_cfg.get("opacity_bottom", 0.12)

    grad = dwg.defs.add(dwg.linearGradient(id="beamGrad", x1="0", y1="0", x2="0", y2="1"))
    grad.add_stop_color(0, ct, opacity=ot)
    grad.add_stop_color(1, cb, opacity=ob)

    # Beam: narrow at window opening, widens to table
    # Window centre panel bottom at y≈432, table top at y≈598
    bm_top_l, bm_top_r = 406, 582   # width at window bottom
    bm_bot_l, bm_bot_r = 270, 730   # wider spread at table
    bm_top_y, bm_bot_y = 432, 600

    # Also fill inside centre opening
    beam_inside_top_y = 72
    dwg.add(dwg.polygon(
        points=[
            (bm_top_l, beam_inside_top_y),
            (bm_top_r, beam_inside_top_y),
            (bm_top_r, bm_top_y),
            (bm_bot_r, bm_bot_y),
            (bm_bot_l, bm_bot_y),
            (bm_top_l, bm_top_y),
        ],
        fill=ct, opacity=0.25,
    ))

    # Triangle inside window opening (bright wedge, top-right corner)
    dwg.add(dwg.polygon(
        points=[(580, 72), (580, 430), (406, 430)],
        fill=ct, opacity=0.75,
    ))

    # Below-window trapezoid beam with gradient
    dwg.add(dwg.polygon(
        points=[(bm_top_l, bm_top_y), (bm_top_r, bm_top_y),
                (bm_bot_r, bm_bot_y), (bm_bot_l, bm_bot_y)],
        fill="url(#beamGrad)",
    ))

    # ── Helper: draw one window panel (frame + 2×2 panes) ────────────────
    def draw_panel(px, py, pw, ph):
        # Outer frame rect
        dwg.add(dwg.rect(insert=(px, py), size=(pw, ph),
                         fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))
        # Glass area
        gx, gy = px + ft, py + ft
        gw, gh = pw - 2*ft, ph - 2*ft
        dwg.add(dwg.rect(insert=(gx, gy), size=(gw, gh),
                         fill=glass_c, stroke=frame_ol, stroke_width=1.5))
        # Horizontal mid-rail
        mid_y = py + ph / 2
        dwg.add(dwg.rect(insert=(gx, mid_y - ft/2), size=(gw, ft),
                         fill=frame_c, stroke=frame_ol, stroke_width=1.2))
        # Vertical mid-stile
        mid_x = px + pw / 2
        dwg.add(dwg.rect(insert=(mid_x - ft/2, gy), size=(ft, gh),
                         fill=frame_c, stroke=frame_ol, stroke_width=1.2))

    # ── Window layout ─────────────────────────────────────────────────────
    # Left panel: 155–400, Centre opening: 400–587, Right panel: 587–800
    win_top, win_bot = 55, 440
    lp = (155, win_top, 245, win_bot - win_top)   # (x,y,w,h)
    rp = (587, win_top, 213, win_bot - win_top)

    draw_panel(*lp)
    draw_panel(*rp)

    # Centre opening: just frame rails (top/bottom + thin jambs)
    cx0, cy0, cw, ch = 400, win_top, 187, win_bot - win_top
    # top rail
    dwg.add(dwg.rect(insert=(cx0, cy0), size=(cw, ft),
                     fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))
    # bottom rail / sill
    dwg.add(dwg.rect(insert=(cx0, win_bot - ft), size=(cw, ft),
                     fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))
    # jambs
    dwg.add(dwg.rect(insert=(cx0, cy0), size=(10, ch),
                     fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))
    dwg.add(dwg.rect(insert=(cx0 + cw - 10, cy0), size=(10, ch),
                     fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))

    # Full-width outer sill bar
    dwg.add(dwg.rect(insert=(145, win_bot - ft), size=(665, ft + 6),
                     fill=frame_c, stroke=frame_ol, stroke_width=frame_sw))

    # ── Table (3-face 3-D board) ──────────────────────────────────────────
    tbl_top  = tbl_cfg.get("top_color",   "#C8912A")
    tbl_side = tbl_cfg.get("side_color",  "#9A6E1A")
    tbl_ol   = tbl_cfg.get("outline",     "#2E2E2E")
    tbl_sw   = tbl_cfg.get("stroke_width", 2.5)
    tbl_th   = tbl_cfg.get("thickness",   42)

    # Top face (slight parallelogram for perspective)
    tx1, ty1 = 215, 600
    tx2, ty2 = 795, 600
    tx3, ty3 = 845, 648
    tx4, ty4 = 165, 648

    dwg.add(dwg.polygon(
        points=[(tx1, ty1), (tx2, ty2), (tx3, ty3), (tx4, ty4)],
        fill=tbl_top, stroke=tbl_ol, stroke_width=tbl_sw,
    ))
    # Front face
    dwg.add(dwg.polygon(
        points=[(tx4, ty4), (tx3, ty3),
                (tx3, ty3 + tbl_th), (tx4, ty4 + tbl_th)],
        fill=tbl_side, stroke=tbl_ol, stroke_width=tbl_sw,
    ))
    # Left face
    dwg.add(dwg.polygon(
        points=[(tx1, ty1), (tx4, ty4),
                (tx4, ty4 + tbl_th), (tx1, ty1 + tbl_th)],
        fill=tbl_side, stroke=tbl_ol, stroke_width=tbl_sw,
    ))

    # ── Evaporating dish (on table top) ──────────────────────────────────
    df       = dish_cfg.get("fill",        "#FFFFFF")
    di_fill  = dish_cfg.get("inner_fill",  "#EEEEEE")
    dp_fill  = dish_cfg.get("powder_fill", "#AAAAAA")
    d_stroke = dish_cfg.get("stroke",      "#2E2E2E")
    d_sw     = dish_cfg.get("stroke_width", 2.5)

    dcx, dcy = 505, 603   # dish centre on table surface
    drx, dry = 190, 46    # outer rim radii

    # Bowl body (clipped quadratic-bezier profile below rim)
    bowl_depth = 55
    bl = dcx - drx
    br = dcx + drx

    bowl_d = (
        f"M {bl} {dcy} "
        f"Q {dcx - drx + 28} {dcy + bowl_depth + 8}, {dcx} {dcy + bowl_depth} "
        f"Q {dcx + drx - 28} {dcy + bowl_depth + 8}, {br} {dcy}"
    )
    dwg.add(dwg.path(d=bowl_d, fill=di_fill, stroke=d_stroke, stroke_width=d_sw))

    # Inner bottom ellipse (shadow / powder base)
    dwg.add(dwg.ellipse(
        center=(dcx, dcy + bowl_depth - 4),
        r=(drx - 30, dry - 14),
        fill="#DDDDDD", stroke="none", opacity=0.6,
    ))

    # Powder / crystals (irregular blob)
    pd = (
        f"M {dcx - 85} {dcy + bowl_depth + 2} "
        f"Q {dcx - 60} {dcy + bowl_depth - 16}, {dcx - 25} {dcy + bowl_depth + 1} "
        f"Q {dcx}      {dcy + bowl_depth - 14}, {dcx + 45} {dcy + bowl_depth + 0} "
        f"Q {dcx + 72} {dcy + bowl_depth - 12}, {dcx + 85} {dcy + bowl_depth + 6} "
        f"Q {dcx + 45} {dcy + bowl_depth + 20}, {dcx - 45} {dcy + bowl_depth + 18} Z"
    )
    dwg.add(dwg.path(d=pd, fill=dp_fill, stroke="#888888", stroke_width=1.3))

    # Rim (ellipse on top)
    dwg.add(dwg.ellipse(
        center=(dcx, dcy), r=(drx, dry),
        fill=df, stroke=d_stroke, stroke_width=d_sw,
    ))
    # Inner rim shadow
    dwg.add(dwg.ellipse(
        center=(dcx, dcy), r=(drx - 12, dry - 5),
        fill="none", stroke="#AAAAAA", stroke_width=1.2,
    ))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
