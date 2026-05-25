import svgwrite

def render_conductivity_test(spec: dict, out_path: str) -> bool:
    canvas_cfg = spec.get("canvas", {"width": 800, "height": 1000, "background": "#ffffff"})
    w = canvas_cfg.get("width", 800)
    h = canvas_cfg.get("height", 1000)
    bg = canvas_cfg.get("background", "#ffffff")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # Draw Title
    title = spec.get("title", "")
    if title:
        dwg.add(dwg.text(title,
                         insert=(w / 2, 50), text_anchor="middle",
                         font_size=24, font_family="Arial, Helvetica, sans-serif",
                         font_weight="bold", fill="#1a1a1a"))

    # Geometry & placement
    cx = w / 2  # 400
    beaker_w = 440
    beaker_h = 360
    beaker_bottom_y = 800
    beaker_top_y = beaker_bottom_y - beaker_h  # 440
    beaker_left_x = cx - beaker_w / 2  # 180
    beaker_right_x = cx + beaker_w / 2  # 620

    beaker_cfg = spec.get("beaker", {})
    beaker_outline = beaker_cfg.get("outline_color", "#1a1a1a")
    beaker_width = beaker_cfg.get("outline_width", 3)
    rim_ellipse_ry = beaker_cfg.get("rim_ellipse_ry", 28)

    # Liquid Configuration
    liquid_cfg = spec.get("liquid", {})
    fill_color = liquid_cfg.get("fill_color", "#bfe6f5")
    fill_opacity = liquid_cfg.get("fill_opacity", 1.0)
    fill_level = liquid_cfg.get("fill_level", 0.45)
    surface_color = liquid_cfg.get("surface_color", "#1a1a1a")

    liquid_h = fill_level * beaker_h
    liquid_surface_y = beaker_bottom_y - liquid_h

    # ── 1. Draw Liquid Background ──────────────────────────────────────────
    # The liquid shape consists of:
    # - Top surface: ellipse at liquid_surface_y
    # - Body: rect/path down to beaker_bottom_y with elliptical bottom
    liquid_path_d = (
        f"M {beaker_left_x} {liquid_surface_y} "
        f"A {beaker_w/2} {rim_ellipse_ry} 0 0 0 {beaker_right_x} {liquid_surface_y} "
        f"L {beaker_right_x} {beaker_bottom_y} "
        f"A {beaker_w/2} {rim_ellipse_ry} 0 0 1 {beaker_left_x} {beaker_bottom_y} "
        f"Z"
    )
    dwg.add(dwg.path(d=liquid_path_d, fill=fill_color, opacity=fill_opacity))

    # Liquid top surface ellipse
    dwg.add(dwg.ellipse(center=(cx, liquid_surface_y), r=(beaker_w / 2, rim_ellipse_ry),
                        fill=fill_color, stroke=surface_color, stroke_width=1.5, opacity=fill_opacity))

    # ── 2. Draw Electrodes ──────────────────────────────────────────────
    electrodes_cfg = spec.get("electrodes", {})
    el_count = electrodes_cfg.get("count", 2)
    el_color = electrodes_cfg.get("color", "#9e9e9e")
    el_edge = electrodes_cfg.get("edge_color", "#6e6e6e")
    el_w = electrodes_cfg.get("width", 24)
    el_gap = electrodes_cfg.get("gap", 320)
    el_top_ratio = electrodes_cfg.get("top_y_ratio", 0.27)
    el_depth_ratio = electrodes_cfg.get("depth_into_liquid", 0.78)

    el_top_y = el_top_ratio * h  # 270
    el_bottom_y = liquid_surface_y + el_depth_ratio * liquid_h  # 638 + 0.78 * 162 = 764.36

    el_xs = []
    if el_count == 2:
        el_xs = [cx - el_gap / 2, cx + el_gap / 2]
    else:
        el_xs = [cx]

    for el_x in el_xs:
        # Electrode is a vertical rectangle
        dwg.add(dwg.rect(insert=(el_x - el_w / 2, el_top_y), size=(el_w, el_bottom_y - el_top_y),
                         fill=el_color, stroke=el_edge, stroke_width=2))

    # ── 3. Draw Beaker Outline (drawn after liquid & electrodes for correct layering) ──
    beaker_path_d = (
        f"M {beaker_left_x} {beaker_top_y} "
        f"L {beaker_left_x} {beaker_bottom_y} "
        f"A {beaker_w/2} {rim_ellipse_ry} 0 0 0 {beaker_right_x} {beaker_bottom_y} "
        f"L {beaker_right_x} {beaker_top_y}"
    )
    dwg.add(dwg.path(d=beaker_path_d, fill="none", stroke=beaker_outline, stroke_width=beaker_width))
    # Beaker top rim ellipse
    dwg.add(dwg.ellipse(center=(cx, beaker_top_y), r=(beaker_w / 2, rim_ellipse_ry),
                        fill="none", stroke=beaker_outline, stroke_width=beaker_width))

    # ── 4. Draw Circuit ─────────────────────────────────────────────────
    circuit_cfg = spec.get("circuit", {})
    wire_color = circuit_cfg.get("wire_color", "#1a1a1a")
    wire_width = circuit_cfg.get("wire_width", 3)
    circ_top_ratio = circuit_cfg.get("top_y_ratio", 0.22)
    circ_top_y = circ_top_ratio * h  # 220

    # We assume 2 electrodes
    if len(el_xs) == 2:
        left_el_x, right_el_x = el_xs[0], el_xs[1]

        # Draw wire from left electrode top center vertically up to circ_top_y, then right to Battery left terminal
        dwg.add(dwg.line((left_el_x, el_top_y), (left_el_x, circ_top_y),
                         stroke=wire_color, stroke_width=wire_width))
        dwg.add(dwg.line((left_el_x, circ_top_y), (290, circ_top_y),
                         stroke=wire_color, stroke_width=wire_width))

        # Battery (between 290 and 320)
        battery_cfg = circuit_cfg.get("battery", {})
        cells = battery_cfg.get("cells", 2)
        # Connect left wire to first plate
        dwg.add(dwg.line((290, circ_top_y), (295, circ_top_y), stroke=wire_color, stroke_width=wire_width))
        # Draw cells
        for idx in range(cells):
            offset = idx * 12
            # Long thin line (positive)
            dwg.add(dwg.line((295 + offset, circ_top_y - 25), (295 + offset, circ_top_y + 25),
                             stroke=wire_color, stroke_width=1.5))
            # Short thick line (negative)
            dwg.add(dwg.line((301 + offset, circ_top_y - 15), (301 + offset, circ_top_y + 15),
                             stroke=wire_color, stroke_width=4))
            # Wire connecting the plates of the same cell / to next cell
            if idx < cells - 1:
                dwg.add(dwg.line((301 + offset, circ_top_y), (295 + offset + 12, circ_top_y),
                                 stroke=wire_color, stroke_width=wire_width))
        
        # Connect last negative plate to wire segment 2
        last_neg_x = 295 + (cells - 1) * 12 + 6  # e.g., for cells=2: 295 + 12 + 6 = 313
        dwg.add(dwg.line((last_neg_x, circ_top_y), (320, circ_top_y), stroke=wire_color, stroke_width=wire_width))
        
        # Labels for battery (+ and -)
        dwg.add(dwg.text("+", insert=(280, circ_top_y - 10), font_size=20, font_family="Arial", font_weight="bold", fill=wire_color))
        dwg.add(dwg.text("−", insert=(last_neg_x + 8, circ_top_y - 10), font_size=20, font_family="Arial", font_weight="bold", fill=wire_color))

        # Label battery if requested
        if battery_cfg.get("show_label", False):
            dwg.add(dwg.text(battery_cfg.get("label", "Battery"), insert=(305, circ_top_y - 35),
                             text_anchor="middle", font_size=14, font_family="Arial", fill=wire_color))

        # Wire segment 2 (Battery to Bulb)
        dwg.add(dwg.line((320, circ_top_y), (390, circ_top_y),
                         stroke=wire_color, stroke_width=wire_width))

        # Bulb (centered at 410)
        bulb_cfg = circuit_cfg.get("bulb", {})
        glowing = bulb_cfg.get("glowing", True)
        glow_color = bulb_cfg.get("glow_color", "#ffb300")
        bulb_r = 20

        # Bulb circle
        bulb_bg = glow_color if glowing else "#ffffff"
        dwg.add(dwg.circle(center=(410, circ_top_y), r=bulb_r,
                           fill=bulb_bg, stroke=wire_color, stroke_width=wire_width))
        
        # Inside filament (loop)
        filament_path_adjusted = f"M 402 {circ_top_y + 10} C 402 {circ_top_y - 5}, 410 {circ_top_y - 15}, 410 {circ_top_y - 5} C 410 {circ_top_y - 15}, 418 {circ_top_y - 5}, 418 {circ_top_y + 10}"
        dwg.add(dwg.path(d=filament_path_adjusted, fill="none", stroke=wire_color, stroke_width=1.5))

        # Rays if glowing
        if glowing:
            ray_len = 10
            rays = [
                ((410, circ_top_y - bulb_r - 2), (410, circ_top_y - bulb_r - ray_len)),
                ((410, circ_top_y + bulb_r + 2), (410, circ_top_y + bulb_r + ray_len)),
                ((410 - bulb_r - 2, circ_top_y), (410 - bulb_r - ray_len, circ_top_y)),
                ((410 + bulb_r + 2, circ_top_y), (410 + bulb_r + ray_len, circ_top_y)),
                ((410 - 14, circ_top_y - 14), (410 - 21, circ_top_y - 21)),
                ((410 + 14, circ_top_y - 14), (410 + 21, circ_top_y - 21)),
                ((410 - 14, circ_top_y + 14), (410 - 21, circ_top_y + 21)),
                ((410 + 14, circ_top_y + 14), (410 + 21, circ_top_y + 21))
            ]
            for start, end in rays:
                dwg.add(dwg.line(start, end, stroke=glow_color, stroke_width=2.5))

        # Label bulb if requested
        if bulb_cfg.get("show_label", False):
            dwg.add(dwg.text(bulb_cfg.get("label", "Bulb"), insert=(410, circ_top_y - 35),
                             text_anchor="middle", font_size=14, font_family="Arial", fill=wire_color))

        # Wire segment 3 (Bulb to Switch)
        dwg.add(dwg.line((430, circ_top_y), (480, circ_top_y),
                         stroke=wire_color, stroke_width=wire_width))

        # Switch (between 480 and 510)
        switch_cfg = circuit_cfg.get("switch", {})
        switch_closed = switch_cfg.get("closed", True)
        
        # Switch contact dots
        dwg.add(dwg.circle(center=(480, circ_top_y), r=4, fill=wire_color))
        dwg.add(dwg.circle(center=(510, circ_top_y), r=4, fill=wire_color))

        if switch_closed:
            # Closed lever connects them
            dwg.add(dwg.line((480, circ_top_y), (510, circ_top_y), stroke=wire_color, stroke_width=wire_width))
        else:
            # Open lever slanted up
            dwg.add(dwg.line((480, circ_top_y), (505, circ_top_y - 15), stroke=wire_color, stroke_width=wire_width))

        # Label switch if requested
        if switch_cfg.get("show_label", False):
            dwg.add(dwg.text(switch_cfg.get("label", "Switch"), insert=(495, circ_top_y - 35),
                             text_anchor="middle", font_size=14, font_family="Arial", fill=wire_color))

        # Wire segment 4 (Switch to right electrode)
        dwg.add(dwg.line((510, circ_top_y), (right_el_x, circ_top_y),
                         stroke=wire_color, stroke_width=wire_width))
        dwg.add(dwg.line((right_el_x, circ_top_y), (right_el_x, el_top_y),
                         stroke=wire_color, stroke_width=wire_width))

    # ── 5. Render Labels if enabled ─────────────────────────────────────
    labels_cfg = spec.get("labels", {})
    if labels_cfg.get("show", False):
        font_family = labels_cfg.get("font_family", "Arial, Helvetica, sans-serif")
        font_size = labels_cfg.get("font_size", 18)
        lbl_color = labels_cfg.get("color", "#1a1a1a")

        if beaker_cfg.get("label"):
            dwg.add(dwg.text(beaker_cfg.get("label"), insert=(beaker_right_x + 15, beaker_top_y + beaker_h / 2),
                             font_size=font_size, font_family=font_family, fill=lbl_color))
        if liquid_cfg.get("label"):
            dwg.add(dwg.text(liquid_cfg.get("label"), insert=(beaker_right_x + 15, liquid_surface_y + liquid_h / 2),
                             font_size=font_size, font_family=font_family, fill=lbl_color))
        if electrodes_cfg.get("label"):
            dwg.add(dwg.text(electrodes_cfg.get("label"), insert=(cx, el_top_y + (el_bottom_y - el_top_y) / 2),
                             text_anchor="middle", font_size=font_size, font_family=font_family, fill=lbl_color))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
