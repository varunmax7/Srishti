import svgwrite


def render_evaporation_setup(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {})
    w  = canvas.get("width",  740)
    h  = canvas.get("height", 880)
    bg = canvas.get("background", "#ffffff")

    dish_cfg   = spec.get("dish", {})
    gauze_cfg  = spec.get("gauze", {})
    trip_cfg   = spec.get("tripod", {})
    burn_cfg   = spec.get("burner", {})
    flame_cfg  = spec.get("flame", {})

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Layout anchors ────────────────────────────────────────────
    cx       = 468          # horizontal centre
    gauze_y  = 302          # front edge of wire gauze
    ring_y   = gauze_y + 10 # tripod ring sits just below gauze
    burn_top = 428          # top of burner barrel / flame origin
    burn_bot = 828          # bottom of burner barrel into base
    base_y   = 838          # centre of round base disc

    # ── Wire-gauze SVG pattern ────────────────────────────────────
    gs = gauze_cfg.get("grid_spacing", 18)
    grid_pat = dwg.defs.add(dwg.pattern(
        id="gauzeGrid", x=0, y=0, width=gs, height=gs,
        patternUnits="userSpaceOnUse",
    ))
    grid_pat.add(dwg.line(start=(0, 0), end=(gs, 0), stroke="#888", stroke_width=1))
    grid_pat.add(dwg.line(start=(0, 0), end=(0, gs), stroke="#888", stroke_width=1))

    # ── Tripod legs (drawn first — behind everything) ─────────────
    leg_c = trip_cfg.get("leg_color", "#1A1A1A")
    leg_w = trip_cfg.get("leg_width", 4)

    # Left leg: ring → sweep out to bottom-left
    dwg.add(dwg.path(
        d=f"M {cx} {ring_y} C {cx-80} {550}, {cx-160} {710}, {cx-192} {862}",
        fill="none", stroke=leg_c, stroke_width=leg_w,
        stroke_linecap="round",
    ))
    # Right leg
    dwg.add(dwg.path(
        d=f"M {cx} {ring_y} C {cx+80} {550}, {cx+165} {710}, {cx+195} {862}",
        fill="none", stroke=leg_c, stroke_width=leg_w,
        stroke_linecap="round",
    ))
    # Back/centre leg (slightly thinner, goes mostly straight down)
    dwg.add(dwg.path(
        d=f"M {cx} {ring_y} C {cx-10} {600}, {cx-20} {730}, {cx-22} {862}",
        fill="none", stroke=leg_c, stroke_width=leg_w - 1,
        stroke_linecap="round",
    ))

    # ── Bunsen burner — base disc ─────────────────────────────────
    b_fill = burn_cfg.get("barrel_fill",  "#D8D8D8")
    b_dark = burn_cfg.get("barrel_dark",  "#AAAAAA")
    b_col  = burn_cfg.get("collar_fill",  "#B0B0B0")
    b_sl   = burn_cfg.get("slot_color",   "#3A3A3A")
    b_base = burn_cfg.get("base_fill",    "#C0C0C0")
    b_ol   = burn_cfg.get("outline",      "#2E2E2E")
    b_sw   = burn_cfg.get("stroke_width", 2)

    # Base — two-tier disc
    for (ry_val, y_val, fill_v) in [(22, base_y, b_dark), (16, base_y - 8, b_base)]:
        dwg.add(dwg.ellipse(
            center=(cx, y_val), r=(74, ry_val),
            fill=fill_v, stroke=b_ol, stroke_width=b_sw,
        ))
    # Base body thickness
    dwg.add(dwg.rect(
        insert=(cx - 74, base_y - 8), size=(148, 18),
        fill=b_dark, stroke=b_ol, stroke_width=b_sw,
    ))
    dwg.add(dwg.ellipse(
        center=(cx, base_y + 10), r=(74, 22),
        fill=b_dark, stroke=b_ol, stroke_width=b_sw,
    ))

    # Main barrel
    barrel_w = 34
    dwg.add(dwg.rect(
        insert=(cx - barrel_w/2, burn_top + 28), size=(barrel_w, burn_bot - burn_top - 28),
        fill=b_fill, stroke=b_ol, stroke_width=b_sw,
    ))
    # Barrel highlight
    dwg.add(dwg.rect(
        insert=(cx - barrel_w/2 + 4, burn_top + 38), size=(7, burn_bot - burn_top - 55),
        fill="#F0F0F0", opacity=0.6,
    ))

    # Air-intake collar (mid-barrel, slightly wider, with oval slots)
    col_y, col_h, col_w = 700, 50, 44
    dwg.add(dwg.rect(
        insert=(cx - col_w/2, col_y), size=(col_w, col_h),
        rx=4, ry=4,
        fill=b_col, stroke=b_ol, stroke_width=b_sw,
    ))
    for ox in (-10, 0, 10):
        dwg.add(dwg.ellipse(
            center=(cx + ox, col_y + col_h/2), r=(5, 12),
            fill=b_sl, stroke=b_ol, stroke_width=1,
        ))

    # Gas valve / needle valve connector — horizontal knurled tube to right
    valve_y = 764
    valve_x = cx + barrel_w/2
    dwg.add(dwg.rect(
        insert=(valve_x, valve_y - 8), size=(70, 16),
        rx=4, ry=4,
        fill=b_col, stroke=b_ol, stroke_width=b_sw,
    ))
    # Knurling lines
    for kx in range(int(valve_x) + 6, int(valve_x) + 66, 8):
        dwg.add(dwg.line(
            start=(kx, valve_y - 8), end=(kx, valve_y + 8),
            stroke="#999", stroke_width=1,
        ))
    # End cap of valve
    dwg.add(dwg.ellipse(
        center=(valve_x + 70, valve_y), r=(6, 8),
        fill=b_col, stroke=b_ol, stroke_width=b_sw,
    ))

    # Lower collar connecting barrel to base
    low_col_y, low_col_h, low_col_w = 790, 32, 50
    dwg.add(dwg.rect(
        insert=(cx - low_col_w/2, low_col_y), size=(low_col_w, low_col_h),
        rx=3, ry=3,
        fill=b_dark, stroke=b_ol, stroke_width=b_sw,
    ))

    # Nozzle tip (narrower top of barrel)
    nozzle_w = 24
    dwg.add(dwg.rect(
        insert=(cx - nozzle_w/2, burn_top), size=(nozzle_w, 32),
        fill=b_fill, stroke=b_ol, stroke_width=b_sw,
    ))
    dwg.add(dwg.ellipse(
        center=(cx, burn_top), r=(nozzle_w/2, 6),
        fill=b_fill, stroke=b_ol, stroke_width=b_sw,
    ))

    # ── Flame ────────────────────────────────────────────────────
    f_out  = flame_cfg.get("outer_color", "#FFB300")
    f_inn  = flame_cfg.get("inner_color", "#FF6600")
    f_tip  = flame_cfg.get("tip_color",   "#FFEE55")
    f_base = flame_cfg.get("base_color",  "#4488FF")

    # Outer flame (yellow teardrop)
    dwg.add(dwg.path(
        d=(f"M {cx-22} {burn_top - 2} "
           f"C {cx-32} {burn_top - 55}, {cx-18} {burn_top - 110}, {cx} {burn_top - 128} "
           f"C {cx+18} {burn_top - 110}, {cx+32} {burn_top - 55}, {cx+22} {burn_top - 2} Z"),
        fill=f_out,
    ))
    # Middle flame (orange)
    dwg.add(dwg.path(
        d=(f"M {cx-14} {burn_top - 2} "
           f"C {cx-20} {burn_top - 48}, {cx-10} {burn_top - 90}, {cx} {burn_top - 105} "
           f"C {cx+10} {burn_top - 90}, {cx+20} {burn_top - 48}, {cx+14} {burn_top - 2} Z"),
        fill=f_inn,
    ))
    # Inner bright core (yellow)
    dwg.add(dwg.path(
        d=(f"M {cx-7} {burn_top - 2} "
           f"C {cx-10} {burn_top - 40}, {cx-5} {burn_top - 70}, {cx} {burn_top - 82} "
           f"C {cx+5}  {burn_top - 70}, {cx+10} {burn_top - 40}, {cx+7}  {burn_top - 2} Z"),
        fill=f_tip,
    ))
    # Blue base cone
    dwg.add(dwg.path(
        d=(f"M {cx-10} {burn_top - 2} "
           f"C {cx-8} {burn_top - 20}, {cx+8} {burn_top - 20}, {cx+10} {burn_top - 2} Z"),
        fill=f_base, opacity=0.7,
    ))

    # ── Wire gauze (flat grid, perspective) ───────────────────────
    g_c  = gauze_cfg.get("fill",         "#C8C8C8")
    g_ol = gauze_cfg.get("outline",      "#2E2E2E")
    g_sw = gauze_cfg.get("stroke_width", 1.5)

    # Gauze is a parallelogram: front wider, back slightly narrower
    gfl  = cx - 196   # front-left x
    gfr  = cx + 196   # front-right x
    gbl  = cx - 175   # back-left x
    gbr  = cx + 175   # back-right x
    gfy  = gauze_y         # front y
    gby  = gauze_y - 26    # back y (perspective)

    gauze_poly = [(gfl, gfy), (gfr, gfy), (gbr, gby), (gbl, gby)]
    dwg.add(dwg.polygon(points=gauze_poly, fill=g_c, stroke=g_ol, stroke_width=g_sw))
    # Grid overlay
    dwg.add(dwg.polygon(points=gauze_poly, fill="url(#gauzeGrid)", stroke="none"))
    # Outline again on top
    dwg.add(dwg.polygon(points=gauze_poly, fill="none", stroke=g_ol, stroke_width=g_sw))

    # Tripod ring (drawn over legs but under gauze)
    ring_rx = 185
    ring_ry = 14
    dwg.add(dwg.ellipse(
        center=(cx, ring_y + 6), r=(ring_rx, ring_ry),
        fill="none", stroke=leg_c, stroke_width=trip_cfg.get("ring_width", 4),
    ))

    # ── Evaporating dish ─────────────────────────────────────────
    d_fill  = dish_cfg.get("fill",        "#FFFFFF")
    d_inner = dish_cfg.get("inner_fill",  "#F2F2F2")
    d_res   = dish_cfg.get("residue_fill","#7B4A2D")
    d_ol    = dish_cfg.get("stroke",      "#2E2E2E")
    d_sw    = dish_cfg.get("stroke_width", 2.5)

    dish_cx  = cx
    dish_cy  = gauze_y - 8    # dish rim sits on / just above gauze
    dish_rx  = 192
    dish_ry  = 46             # rim ellipse y-radius
    bowl_depth = 148          # how deep the bowl is

    # Bowl body (curved sides going down)
    bowl_bot_y = dish_cy + bowl_depth
    bowl_d = (
        f"M {dish_cx - dish_rx} {dish_cy} "
        f"Q {dish_cx - dish_rx + 20} {bowl_bot_y + 30}, {dish_cx} {bowl_bot_y + 12} "
        f"Q {dish_cx + dish_rx - 20} {bowl_bot_y + 30}, {dish_cx + dish_rx} {dish_cy}"
    )
    dwg.add(dwg.path(d=bowl_d, fill=d_inner, stroke=d_ol, stroke_width=d_sw))

    # Residue blob (brown deposit at the bottom)
    res_d = (
        f"M {dish_cx - 92} {bowl_bot_y + 22} "
        f"Q {dish_cx - 70} {bowl_bot_y + 5},  {dish_cx - 32} {bowl_bot_y + 18} "
        f"Q {dish_cx}      {bowl_bot_y + 4},   {dish_cx + 42} {bowl_bot_y + 16} "
        f"Q {dish_cx + 78} {bowl_bot_y + 6},   {dish_cx + 92} {bowl_bot_y + 24} "
        f"Q {dish_cx + 55} {bowl_bot_y + 42},  {dish_cx - 55} {bowl_bot_y + 42} Z"
    )
    dwg.add(dwg.path(d=res_d, fill=d_res, stroke="#5A3010", stroke_width=1.2))

    # Rim ellipse on top (draw last so it's clean)
    dwg.add(dwg.ellipse(
        center=(dish_cx, dish_cy), r=(dish_rx, dish_ry),
        fill=d_fill, stroke=d_ol, stroke_width=d_sw,
    ))
    # Inner rim shadow
    dwg.add(dwg.ellipse(
        center=(dish_cx, dish_cy), r=(dish_rx - 14, dish_ry - 6),
        fill="none", stroke="#BBBBBB", stroke_width=1.5,
    ))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
