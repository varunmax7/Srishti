import svgwrite

def render_heat_conduction(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {"width": 800, "height": 700, "background": "#ffffff"})
    w = canvas.get("width", 800)
    h = canvas.get("height", 700)
    bg = canvas.get("background", "#ffffff")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    stn_cfg = spec.get("stand", {})
    rod_cfg = spec.get("metal_rod", {})
    bun_cfg = spec.get("bunsen_burner", {})
    wax_cfg = spec.get("wax_pin", {})

    stn_base = stn_cfg.get("base_color", "#E0E0E0")
    stn_edge = stn_cfg.get("base_edge", "#333333")
    rod_c = stn_cfg.get("rod_color", "#D0D0D0")
    rod_edge = stn_cfg.get("rod_edge", "#555555")
    clamp_c = stn_cfg.get("clamp_color", "#2A2A2A")

    h_rod_c = rod_cfg.get("color", "#C4CFCF")
    h_rod_e = rod_cfg.get("edge_color", "#333333")
    h_rod_w = rod_cfg.get("width", 400)
    h_rod_h = rod_cfg.get("height", 16)

    # ── 1. Stand Base (Left side) ───────────────────────────────────────
    base_cx = 250
    base_bot_y = 650
    
    # 3D block base (Trapezoid front/top)
    b_top_w = 100
    b_bot_w = 140
    b_h = 40
    
    # Top face of base
    b_top_pts = [
        (base_cx - b_top_w/2, base_bot_y - b_h - 20),
        (base_cx + b_top_w/2, base_bot_y - b_h - 20),
        (base_cx + b_bot_w/2, base_bot_y - b_h),
        (base_cx - b_bot_w/2, base_bot_y - b_h)
    ]
    dwg.add(dwg.polygon(b_top_pts, fill=stn_base, stroke=stn_edge, stroke_width=2))
    
    # Front face of base
    b_front_pts = [
        (base_cx - b_bot_w/2, base_bot_y - b_h),
        (base_cx + b_bot_w/2, base_bot_y - b_h),
        (base_cx + b_bot_w/2 - 10, base_bot_y),
        (base_cx - b_bot_w/2 + 10, base_bot_y)
    ]
    dwg.add(dwg.polygon(b_front_pts, fill="#CCCCCC", stroke=stn_edge, stroke_width=2))
    
    # Little feet
    dwg.add(dwg.rect(insert=(base_cx - b_bot_w/2 + 15, base_bot_y), size=(15, 8), fill="#999", stroke=stn_edge, stroke_width=2))
    dwg.add(dwg.rect(insert=(base_cx + b_bot_w/2 - 30, base_bot_y), size=(15, 8), fill="#999", stroke=stn_edge, stroke_width=2))

    # ── 2. Stand Vertical Rod ───────────────────────────────────────────
    v_rod_w = 22
    v_rod_top = 100
    v_rod_bot = base_bot_y - b_h - 10
    
    # Rod shadow/gradient effect
    dwg.add(dwg.rect(insert=(base_cx - v_rod_w/2, v_rod_top), size=(v_rod_w, v_rod_bot - v_rod_top), 
                     fill=rod_c, stroke=rod_edge, stroke_width=2, rx=10, ry=10))
    # Rod base ring
    dwg.add(dwg.ellipse(center=(base_cx, v_rod_bot), r=(20, 8), fill=stn_base, stroke=stn_edge, stroke_width=2))

    # ── 3. Horizontal Metal Rod & Clamp ─────────────────────────────────
    h_rod_y = 300
    
    # Clamp back piece
    clamp_h = 36
    clamp_w = 46
    dwg.add(dwg.rect(insert=(base_cx - clamp_w/2, h_rod_y - clamp_h/2), size=(clamp_w, clamp_h), 
                     fill=clamp_c, stroke=stn_edge, stroke_width=2, rx=4, ry=4))
    
    # Horizontal rod
    h_rod_left = base_cx - 40
    h_rod_right = h_rod_left + h_rod_w
    dwg.add(dwg.rect(insert=(h_rod_left, h_rod_y - h_rod_h/2), size=(h_rod_w, h_rod_h), 
                     fill=h_rod_c, stroke=h_rod_e, stroke_width=2))
    
    # Clamp front piece
    dwg.add(dwg.rect(insert=(base_cx - clamp_w/2 - 4, h_rod_y - h_rod_h/2 - 4), size=(clamp_w + 8, h_rod_h + 8), 
                     fill=clamp_c, stroke=stn_edge, stroke_width=2, rx=2, ry=2))

    # ── 4. Bunsen Burner ────────────────────────────────────────────────
    bun_x = base_cx + bun_cfg.get("offset_x", 150)
    bb_bot = 640
    bb_top = h_rod_y + h_rod_h/2 + 50 # Flame gap
    
    b_tube = bun_cfg.get("tube_color", "#C0C0C0")
    b_edge = bun_cfg.get("tube_edge", "#333333")
    b_base = bun_cfg.get("base_color", "#808080")
    b_hole = bun_cfg.get("air_hole_color", "#444444")
    
    # Base
    dwg.add(dwg.ellipse(center=(bun_x, bb_bot), r=(60, 15), fill="#666", stroke=b_edge, stroke_width=2))
    dwg.add(dwg.ellipse(center=(bun_x, bb_bot - 8), r=(55, 12), fill=b_base, stroke=b_edge, stroke_width=2))
    dwg.add(dwg.path(d=f"M {bun_x-55} {bb_bot-8} L {bun_x-60} {bb_bot} A 60 15 0 0 0 {bun_x+60} {bb_bot} L {bun_x+55} {bb_bot-8} Z", fill="#555"))
    # Base neck
    dwg.add(dwg.rect(insert=(bun_x - 15, bb_bot - 25), size=(30, 17), fill=b_tube, stroke=b_edge, stroke_width=2))
    
    # Tube
    tube_w = 20
    dwg.add(dwg.rect(insert=(bun_x - tube_w/2, bb_top), size=(tube_w, bb_bot - 25 - bb_top), fill=b_tube, stroke=b_edge, stroke_width=2))
    
    # Collar & Airhole
    collar_y = bb_bot - 55
    dwg.add(dwg.rect(insert=(bun_x - tube_w/2 - 2, collar_y), size=(tube_w + 4, 30), fill=b_tube, stroke=b_edge, stroke_width=2))
    dwg.add(dwg.rect(insert=(bun_x - 4, collar_y + 6), size=(8, 18), fill=b_hole, rx=4, ry=4))
    
    # Side inlet pipe
    dwg.add(dwg.rect(insert=(bun_x + tube_w/2 + 2, bb_bot - 20), size=(40, 8), fill=b_tube, stroke=b_edge, stroke_width=2, rx=3, ry=3))

    # Flame (reaching the rod)
    f_out = bun_cfg.get("flame_outer", "#FF9800")
    f_inn = bun_cfg.get("flame_inner", "#FFC107")
    f_core = bun_cfg.get("flame_core", "#FFEE58")
    
    flame_tip_y = h_rod_y + h_rod_h/2
    # Outer flame
    dwg.add(dwg.path(d=f"M {bun_x-12} {bb_top} Q {bun_x-20} {bb_top-30} {bun_x-10} {flame_tip_y} Q {bun_x} {flame_tip_y+10} {bun_x+5} {flame_tip_y} Q {bun_x+20} {bb_top-30} {bun_x+12} {bb_top} Z", fill=f_out))
    # Inner flame
    dwg.add(dwg.path(d=f"M {bun_x-8} {bb_top} Q {bun_x-12} {bb_top-20} {bun_x-5} {flame_tip_y+15} Q {bun_x+12} {bb_top-20} {bun_x+8} {bb_top} Z", fill=f_inn))
    # Core
    dwg.add(dwg.path(d=f"M {bun_x-4} {bb_top} Q {bun_x-6} {bb_top-10} {bun_x} {flame_tip_y+30} Q {bun_x+6} {bb_top-10} {bun_x+4} {bb_top} Z", fill=f_core))

    # ── 5. Wax and Pin (Far right) ──────────────────────────────────────
    wax_c = wax_cfg.get("wax_color", "#F5DEB3")
    wax_e = wax_cfg.get("wax_edge", "#D2B48C")
    pin_c = wax_cfg.get("pin_color", "#888888")
    pin_e = wax_cfg.get("pin_edge", "#222222")

    pin_x = h_rod_right - 25
    pin_y = h_rod_y + h_rod_h/2
    
    # Wax blob under the rod
    dwg.add(dwg.ellipse(center=(pin_x, pin_y + 4), r=(12, 6), fill=wax_c, stroke=wax_e, stroke_width=1.5))
    
    # Pin hanging down
    dwg.add(dwg.path(d=f"M {pin_x-2} {pin_y+8} L {pin_x+2} {pin_y+8} L {pin_x} {pin_y+35} Z", fill=pin_c, stroke=pin_e, stroke_width=1))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
