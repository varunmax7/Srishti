import svgwrite
import math


def render_hydrogen_test(spec: dict, out_path: str) -> bool:
    hints = spec.get("render_hints", {})
    ch    = hints.get("canvas", spec.get("canvas", {}))

    w  = ch.get("width",  900)
    h  = ch.get("height", 820)
    bg = ch.get("background", "#FFFFFF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    OL       = "#1a1a1a"
    GLASS    = "#F8F8F6"
    SPLINT_C = "#C8A870"
    SPLINT_S = "#9A7840"
    FLAME_Y  = "#F5D040"
    FLAME_O  = "#E07820"
    POP_C    = "#F0A0B4"

    # ── TEST TUBE ──────────────────────────────────────────────────
    tilt = math.radians(45)
    dx =  math.cos(tilt)   # 0.707 toward mouth (upper-right)
    dy = -math.sin(tilt)   # -0.707 upward in SVG
    px =  math.sin(tilt)   # 0.707 perpendicular (lower-right side)
    py =  math.cos(tilt)   # 0.707

    t_cx, t_cy = 385, 548
    t_len, t_w = 415, 65
    hw = t_w / 2   # 32.5
    hl = t_len / 2  # 207.5

    mx = t_cx + dx * hl;  my = t_cy + dy * hl   # mouth centre
    bx = t_cx - dx * hl;  by = t_cy - dy * hl   # bottom centre

    # Four corners of tube rectangle
    p1 = (mx + px*hw, my + py*hw)   # mouth right
    p2 = (mx - px*hw, my - py*hw)   # mouth left
    p3 = (bx - px*hw, by - py*hw)   # bottom left
    p4 = (bx + px*hw, by + py*hw)   # bottom right

    # Rounded bottom cap control point (extends away from mouth at 1.4× hw)
    cap_x = bx - dx * hw * 1.4
    cap_y = by - dy * hw * 1.4

    # Single path: mouth-right → bottom-right → (round cap curve) → bottom-left → mouth-left
    tube_d = (f"M {p1[0]:.1f} {p1[1]:.1f} "
              f"L {p4[0]:.1f} {p4[1]:.1f} "
              f"Q {cap_x:.1f} {cap_y:.1f} {p3[0]:.1f} {p3[1]:.1f} "
              f"L {p2[0]:.1f} {p2[1]:.1f}")

    # Glass fill (SVG auto-closes for fill)
    dwg.add(dwg.path(d=tube_d + " Z", fill=GLASS, stroke="none"))

    # ── HYDROGEN GAS BUBBLES ───────────────────────────────────────
    # (frac_from_bottom, perp_offset, r1, along_off2, perp_off2, r2)
    bubble_data = [
        (0.93,  1, 10,  9,  3,  9),
        (0.87, -3, 11, -8,  4,  9),
        (0.81,  3, 10,  8, -4,  9),
        (0.75, -1, 11, -9,  2,  9),
        (0.69,  4, 10,  9,  4, 10),
        (0.63, -4, 11, -8, -3,  9),
        (0.57,  2, 10,  8, -2,  9),
        (0.51, -2, 11, -9,  3,  9),
        (0.45,  4, 10,  8,  4, 10),
        (0.39, -1, 11, -8, -3,  9),
        (0.33,  3, 10,  9, -4,  9),
        (0.27, -3, 11, -8,  3,  9),
        (0.21,  1, 10,  9,  2,  9),
        (0.15, -2, 11, -8, -4,  9),
        (0.08,  2, 10,  8,  3,  9),
    ]
    for frac, po, r1, a2, p2off, r2 in bubble_data:
        cx = bx + dx * t_len * frac + px * po
        cy = by + dy * t_len * frac + py * po
        dwg.add(dwg.circle(center=(cx, cy), r=r1,
                           fill="white", stroke=OL, stroke_width=1.5))
        sx = cx + dx * a2 + px * p2off
        sy = cy + dy * a2 + py * p2off
        dwg.add(dwg.circle(center=(sx, sy), r=r2,
                           fill="white", stroke=OL, stroke_width=1.5))

    # Glass outline (open path — mouth edge intentionally left open)
    dwg.add(dwg.path(d=tube_d, fill="none", stroke=OL, stroke_width=3))
    # Mouth rim line
    dwg.add(dwg.line(start=(p2[0], p2[1]), end=(p1[0], p1[1]),
                     stroke=OL, stroke_width=2.5))

    # Glass highlight stripe on upper-left face
    h1x = mx - px*(hw - 7);  h1y = my - py*(hw - 7)
    h2x = bx - px*(hw - 7);  h2y = by - py*(hw - 7)
    dwg.add(dwg.line(start=(h1x, h1y), end=(h2x, h2y),
                     stroke="#FFFFFF", stroke_width=4, opacity=0.55))

    # ── WOODEN SPLINT ──────────────────────────────────────────────
    sp_ang = math.radians(18)
    sp_dx  =  math.cos(sp_ang)
    sp_dy  = -math.sin(sp_ang)
    sp_ppx =  math.sin(sp_ang)
    sp_ppy =  math.cos(sp_ang)
    sp_hw  = 7

    sp_far_x = mx + sp_dx * 450
    sp_far_y = my + sp_dy * 450

    sp1 = (sp_far_x + sp_ppx*sp_hw, sp_far_y + sp_ppy*sp_hw)
    sp2 = (sp_far_x - sp_ppx*sp_hw, sp_far_y - sp_ppy*sp_hw)
    sp3 = (mx - sp_ppx*sp_hw, my - sp_ppy*sp_hw)
    sp4 = (mx + sp_ppx*sp_hw, my + sp_ppy*sp_hw)

    dwg.add(dwg.polygon(points=[sp1, sp2, sp3, sp4],
                        fill=SPLINT_C, stroke=SPLINT_S, stroke_width=2.5))
    # Highlight along splint
    dwg.add(dwg.line(
        start=(sp_far_x - sp_ppx*3, sp_far_y - sp_ppy*3),
        end=(mx - sp_ppx*3, my - sp_ppy*3),
        stroke="#FFFFFF", stroke_width=2, opacity=0.4,
    ))

    # ── FLAME at tube mouth ────────────────────────────────────────
    fl_x = mx - 2;  fl_y = my - 2
    fh = 48;        fw = 20

    # Outer orange teardrop
    dwg.add(dwg.path(
        d=(f"M {fl_x-fw} {fl_y+5} "
           f"Q {fl_x-fw*1.5} {fl_y-10}, {fl_x-fw*0.2} {fl_y-fh} "
           f"Q {fl_x+fw*0.5} {fl_y-fh*0.4}, {fl_x+fw} {fl_y+3} Z"),
        fill=FLAME_O, stroke="none",
    ))
    # Inner yellow core
    dwg.add(dwg.path(
        d=(f"M {fl_x-fw*0.45} {fl_y+3} "
           f"Q {fl_x-fw*0.85} {fl_y-7}, {fl_x-fw*0.1} {fl_y-fh*0.68} "
           f"Q {fl_x+fw*0.35} {fl_y-fh*0.3}, {fl_x+fw*0.6} {fl_y+2} Z"),
        fill=FLAME_Y, stroke="none",
    ))

    # ── PINK POP MARKS ─────────────────────────────────────────────
    # Tips point toward flame, bases point outward
    # (math angle °, dist to tip, triangle length, half-base width)
    pop_defs = [
        (128, 50, 52, 22),   # upper-left
        (78,  44, 50, 20),   # upper
        (340, 48, 50, 20),   # right (slight downward)
    ]
    for ang_d, dist, length, bw in pop_defs:
        a   = math.radians(ang_d)
        sdx =  math.cos(a)
        sdy = -math.sin(a)   # SVG y-flip
        ppx =  math.sin(a)
        ppy =  math.cos(a)

        tip_x  = fl_x + sdx * dist
        tip_y  = fl_y + sdy * dist
        base_x = fl_x + sdx * (dist + length)
        base_y = fl_y + sdy * (dist + length)

        pts = [
            (tip_x, tip_y),
            (base_x + ppx*bw, base_y + ppy*bw),
            (base_x - ppx*bw, base_y - ppy*bw),
        ]
        dwg.add(dwg.polygon(points=pts, fill=POP_C, stroke=OL, stroke_width=2.5))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
