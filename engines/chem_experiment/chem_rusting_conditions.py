import svgwrite
import random

def render_rusting_conditions(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {"width": 800, "height": 700, "background": "#ffffff"})
    w = canvas.get("width", 800)
    h = canvas.get("height", 700)
    bg = canvas.get("background", "#ffffff")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    tubes_cfg = spec.get("test_tubes", {})
    t_w = tubes_cfg.get("width", 50)
    t_h = tubes_cfg.get("height", 400)
    gap = tubes_cfg.get("gap", 150)
    t_out = tubes_cfg.get("outline_color", "#404040")
    cork_c = tubes_cfg.get("cork_color", "#DDBE8F")
    cork_e = tubes_cfg.get("cork_edge", "#5A3A22")

    tube_configs = [
        spec.get("tube_A", {}),
        spec.get("tube_B", {}),
        spec.get("tube_C", {})
    ]

    # Layout: center the three tubes
    total_w = 3 * t_w + 2 * gap
    start_x = (w - total_w) / 2 + t_w / 2
    t_y = 150
    t_bot_y = t_y + t_h

    # Helper function to draw nails
    def draw_nails(cx, bot_y, nail_cfg):
        count = nail_cfg.get("count", 2)
        rusted = nail_cfg.get("rusted", False)
        n_color = nail_cfg.get("color", "#C0C0C0")
        r_spots = nail_cfg.get("rust_spots", "#8B4513")
        
        n_len = 160
        n_w = 6
        head_w = 16
        
        # We draw them crossing slightly
        angles = [-5, 5] if count == 2 else [0]
        
        for i, angle in enumerate(angles):
            g = dwg.g(transform=f"rotate({angle}, {cx}, {bot_y})")
            nx = cx - n_w/2
            ny = bot_y - n_len
            
            # Shaft
            shaft_path = f"M {nx} {ny} L {nx+n_w} {ny} L {cx+1} {bot_y} L {cx-1} {bot_y} Z"
            g.add(dwg.path(d=shaft_path, fill=n_color, stroke=t_out, stroke_width=1.5))
            
            # Rust spots
            if rusted:
                # Add random small polygons for rust
                random.seed(42 + i) # deterministic
                for _ in range(8):
                    ry = random.uniform(ny + 10, bot_y - 20)
                    rx = random.uniform(nx, nx + n_w)
                    g.add(dwg.circle(center=(rx, ry), r=1.5, fill=r_spots))
                    
            # Head
            g.add(dwg.ellipse(center=(cx, ny), r=(head_w/2, 3), fill=n_color, stroke=t_out, stroke_width=1.5))
            dwg.add(g)

    # ── Draw Tubes ──────────────────────────────────────────────────────
    for i in range(3):
        cx = start_x + i * (t_w + gap)
        cfg = tube_configs[i]
        
        # 1. Back outline and content
        
        # Liquid
        liq_lvl = cfg.get("liquid_level", 0)
        liq_c = cfg.get("liquid_color", "none")
        if liq_lvl > 0 and liq_c != "none":
            l_h = liq_lvl * t_h
            l_y = t_bot_y - l_h
            l_path = (
                f"M {cx-t_w/2} {l_y} "
                f"L {cx-t_w/2} {t_bot_y - t_w/2} "
                f"A {t_w/2} {t_w/2} 0 0 0 {cx+t_w/2} {t_bot_y - t_w/2} "
                f"L {cx+t_w/2} {l_y} Z"
            )
            dwg.add(dwg.path(d=l_path, fill=liq_c, opacity=0.7))
            dwg.add(dwg.ellipse(center=(cx, l_y), r=(t_w/2, 6), fill=liq_c, opacity=0.8))

        # Oil Layer
        if cfg.get("oil_layer", False):
            oil_c = cfg.get("oil_color", "#FFF59D")
            oil_thk = cfg.get("oil_thickness", 30)
            o_bot_y = t_bot_y - (liq_lvl * t_h)
            o_top_y = o_bot_y - oil_thk
            dwg.add(dwg.rect(insert=(cx - t_w/2, o_top_y), size=(t_w, oil_thk), fill=oil_c, opacity=0.8))
            dwg.add(dwg.ellipse(center=(cx, o_top_y), r=(t_w/2, 6), fill=oil_c, stroke=t_out, stroke_width=0.5))

        # Pellets
        if cfg.get("pellets", False):
            p_c = cfg.get("pellets_color", "#FFFFFF")
            p_e = cfg.get("pellets_edge", "#808080")
            # Draw a pile of small circles at the bottom
            random.seed(99)
            for _ in range(45):
                px = random.uniform(cx - t_w/2 + 5, cx + t_w/2 - 5)
                py = random.uniform(t_bot_y - t_w/2, t_bot_y - 5)
                # Ensure they stay somewhat in the curved bottom
                if (px-cx)**2 + (py-(t_bot_y-t_w/2))**2 <= (t_w/2 - 4)**2 or py < t_bot_y - t_w/2:
                    dwg.add(dwg.circle(center=(px, py), r=4, fill=p_c, stroke=p_e, stroke_width=1))

        # 2. Nails
        draw_nails(cx, t_bot_y - 10 if not cfg.get("pellets") else t_bot_y - 25, cfg.get("nails", {}))

        # 3. Test Tube Outline (Front)
        tube_path = (
            f"M {cx-t_w/2} {t_y} "
            f"L {cx-t_w/2} {t_bot_y - t_w/2} "
            f"A {t_w/2} {t_w/2} 0 0 0 {cx+t_w/2} {t_bot_y - t_w/2} "
            f"L {cx+t_w/2} {t_y}"
        )
        dwg.add(dwg.path(d=tube_path, fill="none", stroke=t_out, stroke_width=2))
        
        # 4. Cork
        c_top_w = t_w + 10
        c_bot_w = t_w - 6
        c_h = 35
        c_pts = [
            (cx - c_bot_w/2, t_y + 10),
            (cx + c_bot_w/2, t_y + 10),
            (cx + c_top_w/2, t_y - c_h),
            (cx - c_top_w/2, t_y - c_h)
        ]
        dwg.add(dwg.polygon(c_pts, fill=cork_c, stroke=cork_e, stroke_width=2))
        dwg.add(dwg.ellipse(center=(cx, t_y - c_h), r=(c_top_w/2, 6), fill=cork_c, stroke=cork_e, stroke_width=2))
        # Tube rim over cork
        dwg.add(dwg.ellipse(center=(cx, t_y), r=(t_w/2, 6), fill="none", stroke=t_out, stroke_width=2))
        
        # Label (A, B, C)
        lbl = cfg.get("label", "")
        if lbl:
            dwg.add(dwg.text(lbl, insert=(cx, t_bot_y + 40), text_anchor="middle", font_size=24, font_family="Arial", font_weight="bold", fill="#1a1a2e"))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
