import svgwrite
import math

def render_gas_collection_spoon(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {"width": 700, "height": 800, "background": "#C8E6C9"})
    w = canvas.get("width", 700)
    h = canvas.get("height", 800)
    bg = canvas.get("background", "#C8E6C9")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    bun_cfg = spec.get("bunsen_burner", {})
    jar_cfg = spec.get("gas_jar", {})
    spn_cfg = spec.get("spoon", {})
    tng_cfg = spec.get("tongs", {})
    hnd_cfg = spec.get("hands", {})

    # Colors
    b_tube = bun_cfg.get("tube_color", "#A8A8A8")
    b_edge = bun_cfg.get("tube_edge", "#707070")
    b_base = bun_cfg.get("base_color", "#B0B0B0")
    b_hole = bun_cfg.get("air_hole_color", "#505050")
    
    jar_line = jar_cfg.get("outline_color", "#555555")
    jar_w = jar_cfg.get("outline_width", 2.5)
    fume_col = jar_cfg.get("fume_color", "#D4A0B0")

    sp_hndl = spn_cfg.get("handle_color", "#777777")
    sp_edge = spn_cfg.get("handle_edge", "#555555")
    sp_cup = spn_cfg.get("cup_color", "#888888")
    sub_col = spn_cfg.get("substance_color", "#F9A825")
    
    skin = hnd_cfg.get("skin_color", "#F5D0B0")
    skin_edge = hnd_cfg.get("skin_edge", "#D4A882")

    tongs_c = tng_cfg.get("color", "#444444")
    tongs_edge = tng_cfg.get("edge_color", "#222222")

    cx = w / 2

    # ── 1. Bunsen Burner (bottom center) ──────────────────────────────
    bb_bot_y = 700
    bb_top_y = 520
    bb_w = 26
    
    # Base
    dwg.add(dwg.path(d=f"M {cx-45} {bb_bot_y} Q {cx} {bb_bot_y-25} {cx+45} {bb_bot_y} Z", fill=b_base, stroke=b_edge, stroke_width=2))
    dwg.add(dwg.rect(insert=(cx-10, bb_bot_y-30), size=(20, 10), fill=b_tube, stroke=b_edge, stroke_width=2))
    # Gas inlet pipe
    dwg.add(dwg.rect(insert=(cx+8, bb_bot_y-26), size=(35, 6), fill=b_tube, stroke=b_edge, stroke_width=2))
    
    # Main Tube
    dwg.add(dwg.rect(insert=(cx-bb_w/2, bb_top_y), size=(bb_w, bb_bot_y-30-bb_top_y), fill=b_tube, stroke=b_edge, stroke_width=2))
    
    # Collar & Air Hole
    collar_y = bb_bot_y - 65
    dwg.add(dwg.rect(insert=(cx-bb_w/2-2, collar_y), size=(bb_w+4, 25), fill=b_tube, stroke=b_edge, stroke_width=2))
    dwg.add(dwg.rect(insert=(cx-4, collar_y+5), size=(8, 15), fill=b_hole, rx=3))

    # Flame
    f_out = bun_cfg.get("flame_outer", "#FFD54F")
    f_inn = bun_cfg.get("flame_inner", "#FF8F00")
    f_core = bun_cfg.get("flame_core", "#FFF9C4")
    dwg.add(dwg.path(d=f"M {cx-15} {bb_top_y} Q {cx-20} {bb_top_y-30} {cx} {bb_top_y-60} Q {cx+20} {bb_top_y-30} {cx+15} {bb_top_y} Z", fill=f_out))
    dwg.add(dwg.path(d=f"M {cx-10} {bb_top_y} Q {cx-12} {bb_top_y-20} {cx} {bb_top_y-45} Q {cx+12} {bb_top_y-20} {cx+10} {bb_top_y} Z", fill=f_inn))
    dwg.add(dwg.path(d=f"M {cx-5} {bb_top_y} Q {cx-5} {bb_top_y-15} {cx} {bb_top_y-25} Q {cx+5} {bb_top_y-15} {cx+5} {bb_top_y} Z", fill=f_core))

    # ── 2. Spoon inside jar ───────────────────────────────────────────
    sp_y = bb_top_y - 20 # 500
    sp_cx = cx + 8 # slightly offset to right inside jar
    
    # Handle
    handle_len = 160
    dwg.add(dwg.rect(insert=(sp_cx - handle_len, sp_y - 4), size=(handle_len, 8), fill=sp_hndl, stroke=sp_edge, stroke_width=1.5))
    
    # Handle grip
    dwg.add(dwg.rect(insert=(sp_cx - handle_len - 30, sp_y - 6), size=(30, 12), fill="#cccccc", stroke=sp_edge, stroke_width=1.5))

    # Cup
    cup_r = 18
    dwg.add(dwg.path(d=f"M {sp_cx-cup_r} {sp_y} A {cup_r} {cup_r/2} 0 0 0 {sp_cx+cup_r} {sp_y} Z", fill=sp_cup, stroke=sp_edge, stroke_width=2))
    
    # Substance (Burning yellow powder)
    dwg.add(dwg.path(d=f"M {sp_cx-12} {sp_y} Q {sp_cx} {sp_y-10} {sp_cx+12} {sp_y} Z", fill=sub_col))
    
    if spn_cfg.get("burning", True):
        sf = spn_cfg.get("flame_color", "#FFEB3B")
        dwg.add(dwg.path(d=f"M {sp_cx-8} {sp_y-5} Q {sp_cx-10} {sp_y-20} {sp_cx} {sp_y-30} Q {sp_cx+10} {sp_y-20} {sp_cx+8} {sp_y-5} Z", fill=sf, opacity=0.8))

    # Fumes rising
    for i in range(3):
        ox = sp_cx - 10 + i*10
        f_path = f"M {ox} {sp_y-35} Q {ox-15} {sp_y-80} {ox+5} {sp_y-130} T {ox-5} {sp_y-200}"
        dwg.add(dwg.path(d=f_path, fill="none", stroke=fume_col, stroke_width=2, opacity=0.6))

    # ── 3. Gas Jar (Inverted over flame) ──────────────────────────────
    jar_w_val = 80
    jar_h = 320
    jar_bot_y = bb_top_y - 5 # 515
    jar_top_y = jar_bot_y - jar_h
    jar_lx = cx - jar_w_val/2
    jar_rx = cx + jar_w_val/2
    
    # Jar path
    jar_path = (
        f"M {jar_lx-10} {jar_bot_y} L {jar_lx} {jar_bot_y} L {jar_lx} {jar_top_y + jar_w_val/2} "
        f"A {jar_w_val/2} {jar_w_val/2} 0 0 1 {jar_rx} {jar_top_y + jar_w_val/2} "
        f"L {jar_rx} {jar_bot_y} L {jar_rx+10} {jar_bot_y}"
    )
    # Background fill
    fill_col = jar_cfg.get("fill_color", "#ffffff")
    fill_op = jar_cfg.get("fill_opacity", 0.15)
    dwg.add(dwg.path(d=jar_path, fill=fill_col, opacity=fill_op))
    
    # Outline
    dwg.add(dwg.path(d=jar_path, fill="none", stroke=jar_line, stroke_width=jar_w))
    dwg.add(dwg.line((jar_lx-10, jar_bot_y-2), (jar_lx, jar_bot_y-2), stroke=jar_line, stroke_width=jar_w/2))
    dwg.add(dwg.line((jar_rx+10, jar_bot_y-2), (jar_rx, jar_bot_y-2), stroke=jar_line, stroke_width=jar_w/2))

    # Highlight
    dwg.add(dwg.line((jar_lx+8, jar_bot_y-10), (jar_lx+8, jar_top_y + jar_w_val/2), stroke="#ffffff", stroke_width=3, opacity=0.6))

    # ── 4. Tongs holding Jar (Right side) ─────────────────────────────
    t_cx = jar_rx - 5
    t_cy = jar_top_y + 100
    
    # Tongs gripping jar
    dwg.add(dwg.path(d=f"M {jar_lx-15} {t_cy-5} Q {cx} {t_cy-20} {jar_rx+10} {t_cy}", fill="none", stroke=tongs_c, stroke_width=6))
    dwg.add(dwg.path(d=f"M {jar_lx-15} {t_cy+25} Q {cx} {t_cy+40} {jar_rx+10} {t_cy+15}", fill="none", stroke=tongs_c, stroke_width=6))
    
    # Tong handles crossing
    dwg.add(dwg.line((jar_rx+10, t_cy), (jar_rx+110, t_cy-20), stroke=tongs_c, stroke_width=8, stroke_linecap="round"))
    dwg.add(dwg.line((jar_rx+10, t_cy+15), (jar_rx+120, t_cy-10), stroke=tongs_c, stroke_width=8, stroke_linecap="round"))
    # Pivot
    dwg.add(dwg.circle(center=(jar_rx+30, t_cy+4), r=3, fill="#888"))

    # ── 5. Hands ──────────────────────────────────────────────────────
    if hnd_cfg.get("show", True):
        # Left hand holding spoon
        lh_x = sp_cx - handle_len - 30
        lh_y = sp_y
        lh_path = f"M {lh_x} {lh_y-10} Q {lh_x-30} {lh_y-40} {lh_x-60} {lh_y+20} Q {lh_x-40} {lh_y+60} {lh_x-20} {lh_y+40} Q {lh_x-10} {lh_y+10} {lh_x} {lh_y+15} Z"
        dwg.add(dwg.path(d=lh_path, fill=skin, stroke=skin_edge, stroke_width=2, stroke_linejoin="round"))
        # Left Thumb
        dwg.add(dwg.path(d=f"M {lh_x-20} {lh_y-10} Q {lh_x+5} {lh_y-25} {lh_x+10} {lh_y-5} Q {lh_x-5} {lh_y+5} {lh_x-20} {lh_y-5}", fill=skin, stroke=skin_edge, stroke_width=2))
        
        # Right hand holding tongs
        rh_x = jar_rx + 80
        rh_y = t_cy - 15
        rh_path = f"M {rh_x} {rh_y+10} Q {rh_x+40} {rh_y-20} {rh_x+80} {rh_y-20} L {rh_x+80} {rh_y+30} Q {rh_x+40} {rh_y+50} {rh_x-10} {rh_y+30} Z"
        dwg.add(dwg.path(d=rh_path, fill=skin, stroke=skin_edge, stroke_width=2, stroke_linejoin="round"))
        # Right Thumb
        dwg.add(dwg.path(d=f"M {rh_x+20} {rh_y} Q {rh_x-10} {rh_y+20} {rh_x-20} {rh_y+35} Q {rh_x} {rh_y+40} {rh_x+15} {rh_y+20}", fill=skin, stroke=skin_edge, stroke_width=2))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
