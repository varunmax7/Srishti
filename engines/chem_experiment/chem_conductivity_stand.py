import svgwrite


def render_conductivity_stand(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {})
    w  = canvas.get("width",  720)
    h  = canvas.get("height", 840)
    bg = canvas.get("background", "#ffffff")

    stand_cfg    = spec.get("stand", {})
    tube_cfg     = spec.get("tube", {})
    liquid_cfg   = spec.get("liquid", {})
    el_cfg       = spec.get("electrodes", {})

    rod_c   = stand_cfg.get("rod_color",       "#DDB876")
    rod_hl  = stand_cfg.get("rod_highlight",   "#EDD090")
    base_c  = stand_cfg.get("base_color",      "#C8912A")
    base_s  = stand_cfg.get("base_side_color", "#9A6E1A")
    s_ol    = stand_cfg.get("outline",         "#2E2E2E")
    s_sw    = stand_cfg.get("stroke_width",    2.5)

    t_ol    = tube_cfg.get("outline_color", "#2E2E2E")
    t_sw    = tube_cfg.get("stroke_width",  2.5)

    liq_c   = liquid_cfg.get("fill_color", "#5BB8E8")
    liq_lv  = liquid_cfg.get("fill_level", 0.73)
    liq_op  = liquid_cfg.get("opacity",    0.88)

    el_fill = el_cfg.get("fill",       "#C8C8C8")
    el_st   = el_cfg.get("stroke",     "#888888")
    el_w    = el_cfg.get("width",      13)
    el_gap  = el_cfg.get("gap",        38)
    w_col   = el_cfg.get("wire_color", "#1A1A1A")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Layout constants ─────────────────────────────────────────
    rod_cx   = 295
    rod_w    = 27
    rod_top  = 42
    rod_bot  = 762      # disappears into base

    tube_cx  = 560
    tube_rx  = 72       # half-width of tube
    tube_top = 188
    tube_bot = 726      # bottom of straight sides (before round cap)
    tube_ry_bot = 72    # round-bottom radius
    tube_ry_top = 12    # rim ellipse y-radius

    arm_y    = 420      # height of boss/clamp arm
    clamp_y  = 430      # tube clamp position (≈ arm_y)

    # ── Vertical rod ────────────────────────────────────────────
    dwg.add(dwg.rect(
        insert=(rod_cx - rod_w/2, rod_top), size=(rod_w, rod_bot - rod_top),
        fill=rod_c, stroke=s_ol, stroke_width=s_sw,
    ))
    dwg.add(dwg.rect(
        insert=(rod_cx - rod_w/2 + 5, rod_top + 12),
        size=(rod_w // 3, rod_bot - rod_top - 24),
        fill=rod_hl, opacity=0.55,
    ))

    # ── Base — 3-face perspective slab ─────────────────────────
    bx1, by1 = 252, 748
    bx2, by2 = 688, 748
    bx3, by3 = 712, 786
    bx4, by4 = 228, 786
    bth = 34  # board thickness

    # top face
    dwg.add(dwg.polygon(
        points=[(bx1, by1), (bx2, by2), (bx3, by3), (bx4, by4)],
        fill=base_c, stroke=s_ol, stroke_width=s_sw,
    ))
    # front face
    dwg.add(dwg.polygon(
        points=[(bx4, by4), (bx3, by3), (bx3, by3+bth), (bx4, by4+bth)],
        fill=base_s, stroke=s_ol, stroke_width=s_sw,
    ))
    # left face
    dwg.add(dwg.polygon(
        points=[(bx1, by1), (bx4, by4), (bx4, by4+bth), (bx1, by1+bth)],
        fill=base_s, stroke=s_ol, stroke_width=s_sw,
    ))
    # rod collar hole
    dwg.add(dwg.ellipse(
        center=(rod_cx, by1 + 8), r=(rod_w/2 + 2, 7),
        fill="#7A5010", stroke=s_ol, stroke_width=1.5,
    ))

    # ── Boss head — horizontal arm ────────────────────────────
    knob_r   = 23
    knob_cx  = 186
    arm_h    = 16

    # left decorative ball
    dwg.add(dwg.circle(
        center=(knob_cx, arm_y), r=knob_r,
        fill=rod_c, stroke=s_ol, stroke_width=s_sw,
    ))
    # arm from ball to rod
    dwg.add(dwg.rect(
        insert=(knob_cx, arm_y - arm_h/2),
        size=(rod_cx - knob_cx, arm_h),
        fill=rod_c, stroke=s_ol, stroke_width=s_sw,
    ))
    # boss square around rod
    boss_w, boss_h = 24, 32
    dwg.add(dwg.rect(
        insert=(rod_cx - boss_w/2, arm_y - boss_h/2), size=(boss_w, boss_h),
        fill=rod_c, stroke=s_ol, stroke_width=s_sw,
    ))
    # arm continues right to tube
    arm2_end = tube_cx - tube_rx - 2
    dwg.add(dwg.rect(
        insert=(rod_cx + boss_w/2, arm_y - arm_h/2),
        size=(arm2_end - rod_cx - boss_w/2, arm_h),
        fill=rod_c, stroke=s_ol, stroke_width=s_sw,
    ))
    # small right-side clamp ears on tube
    cl_w, cl_h = 13, 32
    dwg.add(dwg.rect(
        insert=(tube_cx - tube_rx - cl_w, clamp_y - cl_h/2), size=(cl_w, cl_h),
        fill=rod_c, stroke=s_ol, stroke_width=2,
    ))
    dwg.add(dwg.rect(
        insert=(tube_cx + tube_rx, clamp_y - cl_h/2), size=(cl_w, cl_h),
        fill=rod_c, stroke=s_ol, stroke_width=2,
    ))

    # ── Liquid fill (draw before tube walls) ───────────────────
    liq_surface_y = tube_top + (1 - liq_lv) * (tube_bot - tube_top)

    liq_d = (
        f"M {tube_cx - tube_rx + 3} {liq_surface_y} "
        f"L {tube_cx - tube_rx + 3} {tube_bot} "
        f"Q {tube_cx} {tube_bot + tube_ry_bot - 5}, "
        f"  {tube_cx + tube_rx - 3} {tube_bot} "
        f"L {tube_cx + tube_rx - 3} {liq_surface_y} Z"
    )
    dwg.add(dwg.path(d=liq_d, fill=liq_c, opacity=liq_op))
    dwg.add(dwg.ellipse(
        center=(tube_cx, liq_surface_y), r=(tube_rx - 3, 8),
        fill=liq_c, opacity=liq_op, stroke="none",
    ))

    # ── Electrodes (pencil/carbon rods) ────────────────────────
    el1x = tube_cx - el_gap / 2
    el2x = tube_cx + el_gap / 2
    el_top_y = liq_surface_y - 18
    el_bot_y = tube_bot - 55

    for ex in (el1x, el2x):
        # body
        dwg.add(dwg.rect(
            insert=(ex - el_w/2, el_top_y), size=(el_w, el_bot_y - el_top_y),
            fill=el_fill, stroke=el_st, stroke_width=1.5,
        ))
        # tip triangle
        dwg.add(dwg.polygon(
            points=[(ex - el_w/2, el_bot_y), (ex + el_w/2, el_bot_y), (ex, el_bot_y + 15)],
            fill=el_fill, stroke=el_st, stroke_width=1.5,
        ))
        # highlight stripe
        dwg.add(dwg.rect(
            insert=(ex - el_w/2 + 2, el_top_y + 6), size=(3, el_bot_y - el_top_y - 12),
            fill="#E8E8E8", opacity=0.7,
        ))

    # ── Wire from electrodes looping over rim ───────────────────
    # each electrode wire goes up and converges over the rim
    rim_left  = tube_cx - 12
    rim_right = tube_cx + 18
    w_top     = tube_top + t_sw + 2

    dwg.add(dwg.path(
        d=(f"M {el1x} {el_top_y} "
           f"C {el1x - 18} {liq_surface_y - 40}, "
           f"  {rim_left - 10} {w_top + 40}, "
           f"  {rim_left} {w_top}"),
        fill="none", stroke=w_col, stroke_width=2,
    ))
    dwg.add(dwg.path(
        d=(f"M {el2x} {el_top_y} "
           f"C {el2x + 10} {liq_surface_y - 35}, "
           f"  {rim_right + 8} {w_top + 40}, "
           f"  {rim_right} {w_top}"),
        fill="none", stroke=w_col, stroke_width=2,
    ))
    # arc over the rim
    dwg.add(dwg.path(
        d=(f"M {rim_left} {w_top} "
           f"Q {tube_cx + 3} {tube_top - 22}, "
           f"  {rim_right} {w_top}"),
        fill="none", stroke=w_col, stroke_width=2,
    ))

    # ── Test tube outline (on top of liquid & electrodes) ──────
    tube_d = (
        f"M {tube_cx - tube_rx} {tube_top} "
        f"L {tube_cx - tube_rx} {tube_bot} "
        f"Q {tube_cx} {tube_bot + tube_ry_bot}, "
        f"  {tube_cx + tube_rx} {tube_bot} "
        f"L {tube_cx + tube_rx} {tube_top}"
    )
    dwg.add(dwg.path(d=tube_d, fill="none", stroke=t_ol, stroke_width=t_sw))
    # rim ellipse
    dwg.add(dwg.ellipse(
        center=(tube_cx, tube_top), r=(tube_rx, tube_ry_top),
        fill="none", stroke=t_ol, stroke_width=t_sw,
    ))
    # glass highlight
    dwg.add(dwg.line(
        start=(tube_cx - tube_rx + 11, tube_top + 22),
        end=(tube_cx - tube_rx + 11, tube_bot - 50),
        stroke="#ffffff", stroke_width=6, opacity=0.65,
    ))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
