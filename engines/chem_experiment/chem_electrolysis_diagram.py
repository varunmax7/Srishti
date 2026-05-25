import svgwrite


def render_electrolysis_diagram(spec: dict, out_path: str) -> bool:
    """Render an electrolysis diagram with a U-shaped tank, plate electrodes,
    blue gradient liquid, reddish-brown deposit, and battery + switch circuit."""

    canvas = spec.get("canvas", {"width": 800, "height": 700, "background": "#f5f5f5"})
    w = canvas.get("width", 800)
    h = canvas.get("height", 700)
    bg = canvas.get("background", "#f5f5f5")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    tank_cfg = spec.get("tank", {})
    liq_cfg = spec.get("liquid", {})
    el_cfg = spec.get("electrodes", {})
    dep_cfg = spec.get("deposit", {})
    circ_cfg = spec.get("circuit", {})

    wall_color = tank_cfg.get("wall_color", "#B8A98C")
    wall_edge = tank_cfg.get("wall_edge_color", "#1a1a2e")
    wall_t = tank_cfg.get("wall_thickness", 26)

    wire_color = circ_cfg.get("wire_color", "#1a1a2e")
    wire_w = circ_cfg.get("wire_width", 2.5)

    # ── Title ───────────────────────────────────────────────────────────
    title = spec.get("title", "")
    if title:
        dwg.add(dwg.text(title, insert=(w / 2, 35), text_anchor="middle",
                         font_size=22, font_family="Arial", font_weight="bold",
                         fill="#1a1a2e"))

    # ── Geometry ────────────────────────────────────────────────────────
    cx = w / 2                    # 400
    tank_outer_w = 420
    tank_outer_h = 380
    tank_bot_y = 620
    tank_top_y = tank_bot_y - tank_outer_h   # 240
    tank_left = cx - tank_outer_w / 2        # 190
    tank_right = cx + tank_outer_w / 2       # 610

    inner_left = tank_left + wall_t          # 216
    inner_right = tank_right - wall_t        # 584
    inner_w = inner_right - inner_left       # 368
    inner_bot_y = tank_bot_y - wall_t        # 594
    corner_r = 30                            # rounded bottom radius

    # ── 1. Tank outer shell (U-shape) ───────────────────────────────────
    # Outer U-path: left wall down, rounded bottom, right wall up
    outer_u = (
        f"M {tank_left} {tank_top_y} "
        f"L {tank_left} {tank_bot_y - corner_r} "
        f"Q {tank_left} {tank_bot_y} {tank_left + corner_r} {tank_bot_y} "
        f"L {tank_right - corner_r} {tank_bot_y} "
        f"Q {tank_right} {tank_bot_y} {tank_right} {tank_bot_y - corner_r} "
        f"L {tank_right} {tank_top_y}"
    )
    # Inner U-path (reverse direction for fill)
    inner_u = (
        f"L {inner_right} {tank_top_y} "
        f"L {inner_right} {inner_bot_y - corner_r} "
        f"Q {inner_right} {inner_bot_y} {inner_right - corner_r} {inner_bot_y} "
        f"L {inner_left + corner_r} {inner_bot_y} "
        f"Q {inner_left} {inner_bot_y} {inner_left} {inner_bot_y - corner_r} "
        f"L {inner_left} {tank_top_y} Z"
    )
    dwg.add(dwg.path(d=outer_u + " " + inner_u, fill=wall_color,
                     stroke=wall_edge, stroke_width=2))

    # ── 2. Liquid (blue gradient) inside the tank ───────────────────────
    fill_level = liq_cfg.get("fill_level", 0.82)
    top_c = liq_cfg.get("top_color", "#E8F4FB")
    bot_c = liq_cfg.get("bottom_color", "#AEDCF0")

    liquid_inner_h = inner_bot_y - tank_top_y       # available inner height
    liquid_h = fill_level * liquid_inner_h
    liquid_top_y = inner_bot_y - liquid_h

    # Define a vertical gradient
    grad = dwg.defs.add(dwg.linearGradient(id="liqGrad", x1="0%", y1="0%",
                                           x2="0%", y2="100%"))
    grad.add_stop_color(offset="0%", color=top_c)
    grad.add_stop_color(offset="100%", color=bot_c)

    liquid_path = (
        f"M {inner_left} {liquid_top_y} "
        f"L {inner_left} {inner_bot_y - corner_r} "
        f"Q {inner_left} {inner_bot_y} {inner_left + corner_r} {inner_bot_y} "
        f"L {inner_right - corner_r} {inner_bot_y} "
        f"Q {inner_right} {inner_bot_y} {inner_right} {inner_bot_y - corner_r} "
        f"L {inner_right} {liquid_top_y} Z"
    )
    dwg.add(dwg.path(d=liquid_path, fill="url(#liqGrad)"))

    # Liquid surface line
    dwg.add(dwg.line((inner_left, liquid_top_y), (inner_right, liquid_top_y),
                     stroke="#9DCAE0", stroke_width=1.5))

    # ── 3. Deposit on the floor ─────────────────────────────────────────
    if dep_cfg.get("show", True):
        dep_color = dep_cfg.get("color", "#A8451E")
        dep_shade = dep_cfg.get("shade_color", "#7A2F10")
        # A small mound toward the right side of the floor
        dep_cx = cx + 40
        dep_w = 120
        dep_h = 30
        dep_path = (
            f"M {dep_cx - dep_w/2} {inner_bot_y} "
            f"Q {dep_cx - dep_w/4} {inner_bot_y - dep_h} {dep_cx} {inner_bot_y - dep_h} "
            f"Q {dep_cx + dep_w/4} {inner_bot_y - dep_h} {dep_cx + dep_w/2} {inner_bot_y} Z"
        )
        dwg.add(dwg.path(d=dep_path, fill=dep_color, stroke=dep_shade,
                         stroke_width=1))

    # ── 4. Plate Electrodes ─────────────────────────────────────────────
    plate_w = el_cfg.get("plate_width", 50)
    plate_color = el_cfg.get("plate_color", "#C9CDD2")
    plate_edge = el_cfg.get("edge_color", "#888888")
    highlight = el_cfg.get("highlight_color", "#E8EAEC")
    gap = el_cfg.get("gap", 220)
    depth_ratio = el_cfg.get("bottom_into_liquid", 0.70)
    bracket_color = el_cfg.get("bracket_color", "#6B5B3E")

    plate_top_y = liquid_top_y - 40            # plates stick above liquid
    plate_bot_y = liquid_top_y + depth_ratio * liquid_h

    plate_xs = [cx - gap / 2, cx + gap / 2]   # center-x of each plate

    for px in plate_xs:
        # Main plate body
        dwg.add(dwg.rect(insert=(px - plate_w / 2, plate_top_y),
                         size=(plate_w, plate_bot_y - plate_top_y),
                         fill=plate_color, stroke=plate_edge, stroke_width=2))
        # Highlight strip (left 30% width, lighter shade)
        hl_w = plate_w * 0.28
        dwg.add(dwg.rect(insert=(px - plate_w / 2 + 2, plate_top_y + 2),
                         size=(hl_w, plate_bot_y - plate_top_y - 4),
                         fill=highlight, opacity=0.55))
        # Small bracket/clamp at top
        br_h = 8
        br_w = plate_w + 16
        dwg.add(dwg.rect(insert=(px - br_w / 2, plate_top_y - br_h),
                         size=(br_w, br_h),
                         fill=bracket_color, stroke=wall_edge, stroke_width=1.5,
                         rx=2, ry=2))

    # ── 5. Circuit (switch left, battery right) ─────────────────────────
    circ_y = 110                               # horizontal rail y

    left_px, right_px = plate_xs[0], plate_xs[1]

    # Wires down from circuit rail to each plate bracket top
    bracket_top_y = plate_top_y - 8
    dwg.add(dwg.line((left_px, circ_y), (left_px, bracket_top_y),
                     stroke=wire_color, stroke_width=wire_w))
    dwg.add(dwg.line((right_px, circ_y), (right_px, bracket_top_y),
                     stroke=wire_color, stroke_width=wire_w))

    # Horizontal rail
    sw_cfg = circ_cfg.get("switch", {})
    bat_cfg = circ_cfg.get("battery", {})

    # --- Switch (left side) ---
    sw_left_x = left_px - 10
    sw_right_x = left_px + 50
    sw_closed = sw_cfg.get("closed", False)

    # Wire from left electrode up to switch left terminal
    dwg.add(dwg.line((left_px, circ_y), (sw_left_x, circ_y),
                     stroke=wire_color, stroke_width=wire_w))

    # Switch terminals
    dwg.add(dwg.circle(center=(sw_left_x, circ_y), r=4, fill="none",
                       stroke=wire_color, stroke_width=2))
    dwg.add(dwg.circle(center=(sw_right_x, circ_y), r=4, fill="none",
                       stroke=wire_color, stroke_width=2))

    if sw_closed:
        dwg.add(dwg.line((sw_left_x, circ_y), (sw_right_x, circ_y),
                         stroke=wire_color, stroke_width=wire_w))
    else:
        # Open lever slanted upward
        dwg.add(dwg.line((sw_left_x, circ_y), (sw_right_x - 5, circ_y - 20),
                         stroke=wire_color, stroke_width=wire_w))

    # Wire from switch right terminal to battery left
    bat_start_x = right_px - 40
    dwg.add(dwg.line((sw_right_x, circ_y), (bat_start_x, circ_y),
                     stroke=wire_color, stroke_width=wire_w))

    # --- Battery (right side) ---
    cells = bat_cfg.get("cells", 2)
    bx = bat_start_x
    for i in range(cells):
        offset = i * 14
        # Long thin line (positive)
        dwg.add(dwg.line((bx + offset, circ_y - 20), (bx + offset, circ_y + 20),
                         stroke=wire_color, stroke_width=1.5))
        # Short thick line (negative)
        dwg.add(dwg.line((bx + offset + 7, circ_y - 11), (bx + offset + 7, circ_y + 11),
                         stroke=wire_color, stroke_width=4))
        if i < cells - 1:
            dwg.add(dwg.line((bx + offset + 7, circ_y), (bx + offset + 14, circ_y),
                             stroke=wire_color, stroke_width=wire_w))

    bat_end_x = bx + (cells - 1) * 14 + 7
    # Wire from battery to right electrode
    dwg.add(dwg.line((bat_end_x, circ_y), (right_px, circ_y),
                     stroke=wire_color, stroke_width=wire_w))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
