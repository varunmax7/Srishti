import svgwrite
import random

def render_spray_mechanism(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {"width": 900, "height": 700, "background": "#ffffff"})
    w = canvas.get("width", 900)
    h = canvas.get("height", 700)
    bg = canvas.get("background", "#ffffff")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Config ──────────────────────────────────────────────────────────
    trough_cfg = spec.get("trough", {})
    bjar_cfg = spec.get("bell_jar", {})
    rjar_cfg = spec.get("right_jar", {})
    tube_cfg = spec.get("tube", {})

    t_line = trough_cfg.get("outline_color", "#2E2E2E")
    t_w = trough_cfg.get("outline_width", 3)
    liq_c = trough_cfg.get("liquid_color", "#87CEFA")

    # ── Back Layers (Liquid in back of jars) ─────────────────────────────
    # Right Jar Back Liquid
    rj_cx = 700
    rj_w = 180
    rj_bot_y = 650
    rj_top_y = 250
    rj_liq_y = 350
    
    dwg.add(dwg.path(d=f"M {rj_cx-rj_w/2} {rj_liq_y} L {rj_cx-rj_w/2} {rj_bot_y-20} A {rj_w/2} 20 0 0 0 {rj_cx+rj_w/2} {rj_bot_y-20} L {rj_cx+rj_w/2} {rj_liq_y} Z", fill=liq_c, opacity=0.8))
    dwg.add(dwg.ellipse(center=(rj_cx, rj_liq_y), r=(rj_w/2, 15), fill=liq_c, opacity=0.6))

    # Trough Back Liquid
    tr_cx = 300
    tr_bot_w = 340
    tr_top_w = 400
    tr_bot_y = 680
    tr_top_y = 350
    tr_liq_y = 500
    
    tr_liq_w_half = tr_bot_w/2 + ((tr_top_w - tr_bot_w)/2) * ((tr_bot_y - tr_liq_y)/(tr_bot_y - tr_top_y))
    dwg.add(dwg.path(d=f"M {tr_cx-tr_liq_w_half} {tr_liq_y} L {tr_cx-tr_bot_w/2} {tr_bot_y-20} A {tr_bot_w/2} 20 0 0 0 {tr_cx+tr_bot_w/2} {tr_bot_y-20} L {tr_cx+tr_liq_w_half} {tr_liq_y} Z", fill=liq_c, opacity=0.8))
    dwg.add(dwg.ellipse(center=(tr_cx, tr_liq_y), r=(tr_liq_w_half, 20), fill=liq_c, opacity=0.6))

    # Bell Jar Back Liquid
    bj_cx = tr_cx - 20
    bj_w = 180
    bj_bot_y = 640
    bj_top_y = 250
    bj_liq_y = 530
    
    dwg.add(dwg.path(d=f"M {bj_cx-bj_w/2} {bj_liq_y} L {bj_cx-bj_w/2} {bj_bot_y} A {bj_w/2} 15 0 0 0 {bj_cx+bj_w/2} {bj_bot_y} L {bj_cx+bj_w/2} {bj_liq_y} Z", fill="#E0F7FA", opacity=0.9)) # Slightly lighter inside
    dwg.add(dwg.ellipse(center=(bj_cx, bj_liq_y), r=(bj_w/2, 15), fill="#B2EBF2", opacity=0.8))

    # ── Glass Tube ──────────────────────────────────────────────────────
    tb_c = tube_cfg.get("color", "#E8E8E8")
    tb_e = tube_cfg.get("edge_color", "#2E2E2E")
    tb_w = tube_cfg.get("width", 14)
    
    # Tube path: Starts inside bell jar, goes up, curves right, goes down into right jar
    tb_start_x = bj_cx
    tb_start_y = 380
    tb_out_y = 200
    tb_curve1_x = bj_cx + 100
    tb_curve1_y = 80
    tb_curve2_x = rj_cx - 100
    tb_curve2_y = 400
    tb_end_x = rj_cx - 30
    tb_end_y = 580

    t_path = (
        f"M {tb_start_x} {tb_start_y} "
        f"L {tb_start_x} {tb_out_y} "
        f"C {tb_start_x} {tb_curve1_y}, {tb_curve1_x} {tb_curve1_y}, {tb_curve1_x+50} {tb_curve1_y+50} "
        f"C {tb_curve2_x} {tb_curve2_y}, {tb_curve2_x+20} {tb_curve2_y+50}, {tb_end_x} {tb_end_y}"
    )
    
    dwg.add(dwg.path(d=t_path, fill="none", stroke=tb_e, stroke_width=tb_w+4))
    dwg.add(dwg.path(d=t_path, fill="none", stroke=tb_c, stroke_width=tb_w))
    dwg.add(dwg.path(d=t_path, fill="none", stroke="#ffffff", stroke_width=tb_w-8, opacity=0.6)) # highlight

    # ── Bubbles in Right Jar ────────────────────────────────────────────
    if rjar_cfg.get("bubbles", True):
        random.seed(123)
        for _ in range(8):
            bx = tb_end_x + random.uniform(10, 60)
            by = tb_end_y - random.uniform(10, 150)
            br = random.uniform(4, 12)
            dwg.add(dwg.circle(center=(bx, by), r=br, fill="#E0F7FA", stroke=tb_e, stroke_width=1.5, opacity=0.8))
            dwg.add(dwg.circle(center=(bx-br/3, by-br/3), r=br/4, fill="#ffffff", opacity=0.8)) # Bubble highlight

    # ── Front Outlines (Jars and Trough) ────────────────────────────────
    
    # Bell Jar Front
    stopper_c = bjar_cfg.get("stopper_color", "#45B3A9")
    stopper_e = bjar_cfg.get("stopper_edge", "#2E2E2E")
    
    bj_neck_w = 80
    bj_path = (
        f"M {bj_cx-bj_neck_w/2} {bj_top_y} "
        f"C {bj_cx-bj_w/2} {bj_top_y+20}, {bj_cx-bj_w/2} {bj_top_y+60}, {bj_cx-bj_w/2} {bj_top_y+100} "
        f"L {bj_cx-bj_w/2} {bj_bot_y} "
        f"A {bj_w/2} 15 0 0 0 {bj_cx+bj_w/2} {bj_bot_y} "
        f"L {bj_cx+bj_w/2} {bj_top_y+100} "
        f"C {bj_cx+bj_w/2} {bj_top_y+60}, {bj_cx+bj_neck_w/2} {bj_top_y+20}, {bj_cx+bj_neck_w/2} {bj_top_y}"
    )
    dwg.add(dwg.path(d=bj_path, fill="none", stroke=t_line, stroke_width=t_w))
    # Stopper
    dwg.add(dwg.ellipse(center=(bj_cx, bj_top_y-15), r=(bj_neck_w/2 + 10, 12), fill=stopper_c, stroke=stopper_e, stroke_width=t_w))
    dwg.add(dwg.rect(insert=(bj_cx-bj_neck_w/2-10, bj_top_y-15), size=(bj_neck_w+20, 15), fill=stopper_c, stroke=stopper_e, stroke_width=t_w))
    dwg.add(dwg.ellipse(center=(bj_cx, bj_top_y), r=(bj_neck_w/2 + 10, 12), fill=stopper_c, stroke=stopper_e, stroke_width=t_w))

    # Trough Front
    tr_path = (
        f"M {tr_cx-tr_top_w/2} {tr_top_y} "
        f"L {tr_cx-tr_bot_w/2} {tr_bot_y-20} "
        f"A {tr_bot_w/2} 20 0 0 0 {tr_cx+tr_bot_w/2} {tr_bot_y-20} "
        f"L {tr_cx+tr_top_w/2} {tr_top_y} "
    )
    dwg.add(dwg.path(d=tr_path, fill="none", stroke=t_line, stroke_width=t_w))
    dwg.add(dwg.ellipse(center=(tr_cx, tr_top_y), r=(tr_top_w/2, 25), fill="none", stroke=t_line, stroke_width=t_w))

    # Right Jar Front
    rj_neck_w = 120
    rj_path = (
        f"M {rj_cx-rj_neck_w/2} {rj_top_y} "
        f"C {rj_cx-rj_w/2} {rj_top_y+20}, {rj_cx-rj_w/2} {rj_top_y+50}, {rj_cx-rj_w/2} {rj_top_y+80} "
        f"L {rj_cx-rj_w/2} {rj_bot_y-20} "
        f"A {rj_w/2} 20 0 0 0 {rj_cx+rj_w/2} {rj_bot_y-20} "
        f"L {rj_cx+rj_w/2} {rj_top_y+80} "
        f"C {rj_cx+rj_w/2} {rj_top_y+50}, {rj_cx+rj_neck_w/2} {rj_top_y+20}, {rj_cx+rj_neck_w/2} {rj_top_y}"
    )
    dwg.add(dwg.path(d=rj_path, fill="none", stroke=t_line, stroke_width=t_w))
    # Right jar rim
    dwg.add(dwg.ellipse(center=(rj_cx, rj_top_y), r=(rj_neck_w/2, 10), fill="#ffffff", stroke=t_line, stroke_width=t_w))
    dwg.add(dwg.ellipse(center=(rj_cx, rj_top_y-8), r=(rj_neck_w/2, 10), fill="#ffffff", stroke=t_line, stroke_width=t_w))

    # Jar Highlights (Adding some curved lines on the glass for a 3D effect)
    dwg.add(dwg.path(d=f"M {rj_cx-rj_w/2+15} {rj_top_y+80} L {rj_cx-rj_w/2+15} {rj_bot_y-60}", fill="none", stroke="#ffffff", stroke_width=4, opacity=0.7))
    dwg.add(dwg.path(d=f"M {bj_cx-bj_w/2+15} {bj_top_y+100} L {bj_cx-bj_w/2+15} {bj_bot_y-60}", fill="none", stroke="#ffffff", stroke_width=4, opacity=0.7))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
