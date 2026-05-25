import svgwrite

def render_open_circuit(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {"width": 800, "height": 600, "background": "#ffffff"})
    w = canvas.get("width", 800)
    h = canvas.get("height", 600)
    bg = canvas.get("background", "#ffffff")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    circ_cfg = spec.get("circuit", {})
    wire_c = circ_cfg.get("wire_color", "#000000")
    wire_w = circ_cfg.get("wire_width", 4)
    rect_w = circ_cfg.get("rect_width", 500)
    rect_h = circ_cfg.get("rect_height", 300)

    bulb_cfg = spec.get("bulb", {})
    bulb_glass = bulb_cfg.get("glass_color", "#FEE12B")
    bulb_base = bulb_cfg.get("base_color", "#CCCCCC")
    bulb_edge = bulb_cfg.get("edge_color", "#000000")

    bat_cfg = spec.get("battery", {})
    cells = bat_cfg.get("cells", 3)

    sw_cfg = spec.get("switch", {})
    sw_closed = sw_cfg.get("closed", False)

    res_cfg = spec.get("resistor", {})
    zigzags = res_cfg.get("zigzags", 3)

    cx, cy = w / 2, h / 2
    left_x = cx - rect_w / 2
    right_x = cx + rect_w / 2
    top_y = cy - rect_h / 2
    bot_y = cy + rect_h / 2

    # ── 1. Top Edge (Battery) ───────────────────────────────────────────
    # We want the battery centered.
    # A single cell has a long positive and short negative.
    cell_w = 16
    bat_total_w = cells * cell_w
    bat_start = cx - bat_total_w / 2

    # Left wire
    dwg.add(dwg.line((left_x, top_y), (bat_start, top_y), stroke=wire_c, stroke_width=wire_w))

    bx = bat_start
    for i in range(cells):
        # Long positive
        dwg.add(dwg.line((bx, top_y - 25), (bx, top_y + 25), stroke=wire_c, stroke_width=wire_w))
        # Short negative
        dwg.add(dwg.line((bx + 8, top_y - 12), (bx + 8, top_y + 12), stroke=wire_c, stroke_width=wire_w * 1.5))
        if i < cells - 1:
            # Wire connecting cells
            dwg.add(dwg.line((bx + 8, top_y), (bx + 16, top_y), stroke=wire_c, stroke_width=wire_w))
        bx += cell_w

    # Right wire
    dwg.add(dwg.line((bx - 8, top_y), (right_x, top_y), stroke=wire_c, stroke_width=wire_w))

    # ── 2. Left Edge (Bulb) ─────────────────────────────────────────────
    # Bulb centered vertically on the left edge. Pointing left.
    bulb_h_space = 40
    # Wire from top
    dwg.add(dwg.line((left_x, top_y), (left_x, cy - bulb_h_space / 2), stroke=wire_c, stroke_width=wire_w))
    # Wire from bottom
    dwg.add(dwg.line((left_x, bot_y), (left_x, cy + bulb_h_space / 2), stroke=wire_c, stroke_width=wire_w))

    # Draw Bulb (oriented leftwards)
    # The screw base attaches to the wire
    base_w = 20
    base_h = 36
    b_left = left_x - base_w
    b_top = cy - base_h/2
    # Base outline
    dwg.add(dwg.rect(insert=(b_left, b_top), size=(base_w, base_h), fill=bulb_base, stroke=bulb_edge, stroke_width=2, rx=4, ry=4))
    # Screw threads
    for t in [-10, 0, 10]:
        dwg.add(dwg.line((b_left, cy + t), (b_left + base_w, cy + t + 3), stroke=bulb_edge, stroke_width=2))

    # Glass bulb
    glass_r = 30
    dwg.add(dwg.path(d=f"M {b_left} {b_top} C {b_left-40} {b_top-40}, {b_left-80} {cy}, {b_left-40} {b_top+base_h+40} C {b_left-20} {b_top+base_h+10}, {b_left} {b_top+base_h}, {b_left} {b_top+base_h} Z", 
                     fill=bulb_glass, stroke=bulb_edge, stroke_width=2))
    
    # Filament
    dwg.add(dwg.path(d=f"M {b_left} {cy-6} L {b_left-15} {cy-10} L {b_left-20} {cy-4} L {b_left-25} {cy-10} L {b_left-30} {cy} L {b_left-25} {cy+10} L {b_left-20} {cy+4} L {b_left-15} {cy+10} L {b_left} {cy+6}", 
                     fill="none", stroke=bulb_edge, stroke_width=1.5))

    # ── 3. Bottom Edge (Resistor) ───────────────────────────────────────
    # Resistor centered horizontally.
    z_width = 16
    z_height = 25
    res_w = zigzags * z_width * 2
    res_start = cx - res_w / 2

    # Left wire
    dwg.add(dwg.line((left_x, bot_y), (res_start, bot_y), stroke=wire_c, stroke_width=wire_w))

    # Zigzags
    z_pts = [(res_start, bot_y)]
    zx = res_start
    for i in range(zigzags):
        z_pts.append((zx + z_width, bot_y - z_height))
        z_pts.append((zx + z_width * 2, bot_y + z_height))
        zx += z_width * 2
    z_pts.append((zx + z_width, bot_y))
    dwg.add(dwg.polyline(z_pts, fill="none", stroke=wire_c, stroke_width=wire_w, stroke_linejoin="miter"))

    # Right wire
    dwg.add(dwg.line((zx + z_width, bot_y), (right_x, bot_y), stroke=wire_c, stroke_width=wire_w))

    # ── 4. Right Edge (Switch) ──────────────────────────────────────────
    sw_space = 60
    sw_top = cy - sw_space / 2
    sw_bot = cy + sw_space / 2

    # Wire from top
    dwg.add(dwg.line((right_x, top_y), (right_x, sw_top), stroke=wire_c, stroke_width=wire_w))
    # Wire from bottom
    dwg.add(dwg.line((right_x, bot_y), (right_x, sw_bot), stroke=wire_c, stroke_width=wire_w))

    # Switch terminals
    dwg.add(dwg.circle(center=(right_x, sw_top), r=5, fill=wire_c))
    dwg.add(dwg.circle(center=(right_x, sw_bot), r=5, fill=wire_c))

    # Switch Lever
    if sw_closed:
        dwg.add(dwg.line((right_x, sw_bot), (right_x, sw_top), stroke=wire_c, stroke_width=wire_w))
    else:
        # Open pointing upwards and outwards
        dwg.add(dwg.line((right_x, sw_bot), (right_x + 30, sw_bot - 50), stroke=wire_c, stroke_width=wire_w, stroke_linecap="round"))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
