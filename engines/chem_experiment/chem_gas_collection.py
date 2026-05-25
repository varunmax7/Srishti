import svgwrite
import math


def render_gas_collection(spec: dict, out_path: str) -> bool:
    hints = spec.get("render_hints", {})
    ch    = hints.get("canvas", spec.get("canvas", {}))

    w  = ch.get("width",  900)
    h  = ch.get("height", 1000)
    bg = ch.get("background", "#FFFFFF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Palette ───────────────────────────────────────────────────
    OL     = "#1a1a1a"
    ROD_C  = "#E8E8E8"
    ROD_E  = "#9A9A9A"
    BASE_C = "#EDEDED"
    CLMP_C = "#E0E0E0"
    GLASS  = "#F2F2F0"
    LIQ_C  = "#EDE7C2"
    SOL_C  = "#D8D2C0"
    CORK_C = "#B5731F"
    CORK_S = "#8A5616"
    TUBE_C = "#F5F5F5"
    HAND_C = "#F5C5A0"

    # ── Key positions (calibrated to match reference image) ───────
    rod_x   = 342
    rod_w   = 30
    rod_top = 82
    rod_bot = 882

    base_cx = 435
    base_cy = 924
    base_w  = 334
    base_hv = 58        # height of slab
    foot_h  = 15        # height of feet

    t_cx    = 568       # reaction tube centre x
    t_top   = 298       # tube mouth y
    t_bot   = 836       # end of straight sides
    t_rx    = 51        # half-width
    t_rb    = 51        # round-bottom radius

    ck_h    = 106       # cork height
    ck_w    = 120       # cork width (slightly wider than tube)
    ck_top  = t_top - ck_h      # = 192

    clamp_y = 488       # boss-head y

    # Delivery tube
    dt_w    = 18

    # Collection tube geometry
    ct_cx   = 812
    ct_cy   = 715
    ct_len  = 280
    ct_w    = 90
    ct_tilt = 24        # degrees from vertical

    hand_x  = 882
    hand_y  = 758

    # ── STAND BASE (slab + feet) ───────────────────────────────────
    bx = base_cx - base_w / 2
    by = base_cy - base_hv / 2

    # Main slab
    dwg.add(dwg.rect(insert=(bx, by), size=(base_w, base_hv), rx=5, ry=5,
                     fill=BASE_C, stroke=OL, stroke_width=2.5))
    # Top highlight strip
    dwg.add(dwg.rect(insert=(bx + 6, by + 5), size=(base_w - 12, 10),
                     fill="#FFFFFF", opacity=0.40, rx=3, ry=3))
    # Two feet
    for fx_off in (16, base_w - 72):
        dwg.add(dwg.rect(insert=(bx + fx_off, by + base_hv), size=(56, foot_h), rx=3, ry=3,
                         fill=BASE_C, stroke=OL, stroke_width=2))
    # Rod collar ring on base
    dwg.add(dwg.ellipse(center=(rod_x, base_cy - 6), r=(rod_w / 2 + 4, 10),
                        fill="#CCCCCC", stroke=OL, stroke_width=1.5))

    # ── STAND ROD ─────────────────────────────────────────────────
    dwg.add(dwg.rect(insert=(rod_x - rod_w/2, rod_top), size=(rod_w, rod_bot - rod_top),
                     fill=ROD_C, stroke=ROD_E, stroke_width=2))
    # Highlight
    dwg.add(dwg.rect(insert=(rod_x - rod_w/2 + 5, rod_top + 10),
                     size=(rod_w // 4, rod_bot - rod_top - 20),
                     fill="#FFFFFF", opacity=0.45))

    # ── BOSS HEAD + CLAMP ARM ─────────────────────────────────────
    knob_x = rod_x - 62
    # Knob (sphere)
    dwg.add(dwg.circle(center=(knob_x, clamp_y), r=25,
                       fill=CLMP_C, stroke=OL, stroke_width=2))
    # Cone/trapezoid from rod rightward
    cone_pts = [
        (rod_x - 28, clamp_y - 10),
        (rod_x + 56, clamp_y - 28),
        (rod_x + 56, clamp_y + 28),
        (rod_x - 28, clamp_y + 10),
    ]
    dwg.add(dwg.polygon(points=cone_pts, fill=CLMP_C, stroke=OL, stroke_width=2))
    # Horizontal stub to tube
    arm_end = t_cx - t_rx - 2
    dwg.add(dwg.rect(insert=(rod_x + 54, clamp_y - 9),
                     size=(arm_end - rod_x - 54, 18),
                     fill=CLMP_C, stroke=OL, stroke_width=2))
    # Clamp ears gripping tube on both sides
    for side in (-t_rx - 14, t_rx):
        dwg.add(dwg.rect(insert=(t_cx + side, clamp_y - 17), size=(14, 34),
                         fill=CLMP_C, stroke=OL, stroke_width=2))

    # ── REACTION TUBE — liquid, solid, bubbles, glass outline ─────
    liq_lv = 0.36
    liq_y  = t_bot - liq_lv * (t_bot - t_top)

    # Liquid body
    dwg.add(dwg.path(
        d=(f"M {t_cx - t_rx + 3} {liq_y} "
           f"L {t_cx - t_rx + 3} {t_bot - 5} "
           f"Q {t_cx} {t_bot + t_rb - 5}, {t_cx + t_rx - 3} {t_bot - 5} "
           f"L {t_cx + t_rx - 3} {liq_y} Z"),
        fill=LIQ_C, opacity=0.93,
    ))
    dwg.add(dwg.ellipse(center=(t_cx, liq_y), r=(t_rx - 3, 7),
                        fill=LIQ_C, opacity=0.93, stroke="none"))

    # Solid granules (rough blob at bottom)
    sg = t_bot + 2
    dwg.add(dwg.path(
        d=(f"M {t_cx - 36} {sg + 2} "
           f"Q {t_cx - 16} {sg - 20}, {t_cx - 2} {sg + 1} "
           f"Q {t_cx + 14} {sg - 24}, {t_cx + 32} {sg + 1} "
           f"Q {t_cx + 40} {sg - 8}, {t_cx + 38} {sg + 7} "
           f"Q {t_cx + 16} {sg + 20}, {t_cx - 18} {sg + 16} Z"),
        fill=SOL_C, stroke="#9A9080", stroke_width=1,
    ))
    for rbx, rby, rbr in [(t_cx-20, sg-5, 6), (t_cx+5, sg-9, 7), (t_cx+26, sg-4, 5)]:
        dwg.add(dwg.ellipse(center=(rbx, rby), r=(rbr, rbr * 0.55),
                            fill=SOL_C, stroke="#9A9080", stroke_width=1))

    # Rising bubbles
    for bx_b, by_b, br_b in [
        (t_cx - 4,  t_bot - 62,  6),
        (t_cx + 8,  t_bot - 98,  5),
        (t_cx - 7,  t_bot - 132, 6),
        (t_cx + 5,  t_bot - 164, 5),
        (t_cx - 3,  t_bot - 194, 4),
        (t_cx + 9,  t_bot - 222, 5),
    ]:
        dwg.add(dwg.circle(center=(bx_b, by_b), r=br_b,
                           fill="#FFFFFF", stroke="#AAAAAA", stroke_width=1.2, opacity=0.88))
        dwg.add(dwg.circle(center=(bx_b - br_b*0.3, by_b - br_b*0.3),
                           r=br_b * 0.28, fill="#FFFFFF", opacity=0.7))

    # Tube glass outline
    dwg.add(dwg.path(
        d=(f"M {t_cx - t_rx} {t_top} "
           f"L {t_cx - t_rx} {t_bot - 5} "
           f"Q {t_cx} {t_bot + t_rb - 5}, {t_cx + t_rx} {t_bot - 5} "
           f"L {t_cx + t_rx} {t_top}"),
        fill="none", stroke=OL, stroke_width=2.5,
    ))
    # Glass highlight
    dwg.add(dwg.line(start=(t_cx - t_rx + 9, t_top + 16),
                     end=(t_cx - t_rx + 9, t_bot - 88),
                     stroke="#FFFFFF", stroke_width=6, opacity=0.55))

    # ── CORK (brown cylinder) ─────────────────────────────────────
    ck_cx = t_cx
    ck_x  = ck_cx - ck_w / 2

    # Cork body
    dwg.add(dwg.rect(insert=(ck_x, ck_top), size=(ck_w, ck_h),
                     fill=CORK_C, stroke=OL, stroke_width=2.5))
    # Horizontal ring lines (texture)
    for ky in [ck_top + ck_h*0.27, ck_top + ck_h*0.54, ck_top + ck_h*0.80]:
        dwg.add(dwg.line(start=(ck_x, ky), end=(ck_x + ck_w, ky),
                         stroke=CORK_S, stroke_width=2, opacity=0.50))
    # Top ellipse
    dwg.add(dwg.ellipse(center=(ck_cx, ck_top), r=(ck_w / 2, 12),
                        fill=CORK_C, stroke=OL, stroke_width=2.5))
    # Bottom ellipse (joins tube)
    dwg.add(dwg.ellipse(center=(ck_cx, t_top), r=(ck_w / 2, 12),
                        fill=CORK_S, stroke=OL, stroke_width=2))

    # ── STUB TUBE (short glass tube, left side of cork, ball top) ─
    st_cx  = t_cx - 22
    st_w   = 14
    st_bot = ck_top              # bottom at cork top surface
    st_top = ck_top - 84         # extends upward 84 px

    dwg.add(dwg.rect(insert=(st_cx - st_w/2, st_top), size=(st_w, st_bot - st_top),
                     fill=TUBE_C, stroke=OL, stroke_width=2))
    # Glass ball at very top
    dwg.add(dwg.circle(center=(st_cx, st_top - 1), r=10,
                       fill=TUBE_C, stroke=OL, stroke_width=2))
    # Dark plug where tube enters cork
    dwg.add(dwg.ellipse(center=(st_cx, st_bot), r=(st_w/2, 5),
                        fill="#888", stroke=OL, stroke_width=1))

    # ── DELIVERY TUBE (up → right → down → into collection tube) ──
    # Exit right of stub, at top of cork
    dt_exit_x = t_cx + 24
    dt_exit_y = ck_top

    dt_h_y = ck_top - 18        # horizontal section y
    dt_r_x = 820                # right x of horizontal section

    # Vertical down, then slight angle into collection tube
    dt_path = [
        (dt_exit_x,  dt_exit_y),     # exits cork top (right side)
        (dt_exit_x,  dt_h_y),        # short upward hop
        (dt_r_x,     dt_h_y),        # long horizontal rightward
        (dt_r_x,     550),           # vertical downward
        (796,        624),           # slight angle into collection tube mouth
    ]

    path_d = "M " + " L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in dt_path)
    dwg.add(dwg.path(d=path_d, fill="none", stroke=OL, stroke_width=dt_w + 4,
                     stroke_linejoin="round", stroke_linecap="round"))
    dwg.add(dwg.path(d=path_d, fill="none", stroke=TUBE_C, stroke_width=dt_w,
                     stroke_linejoin="round", stroke_linecap="round"))
    dwg.add(dwg.path(d=path_d, fill="none", stroke="#FFFFFF",
                     stroke_width=dt_w // 3,
                     stroke_linejoin="round", stroke_linecap="round", opacity=0.55))

    # ── COLLECTION TUBE (tilted, glass test tube) ─────────────────
    ta   = math.radians(ct_tilt)
    tax  = math.sin(ta)     # rightward lean
    tay  = math.cos(ta)     # downward component
    tpx  = -tay
    tpy  = tax
    hw   = ct_w / 2
    hl   = ct_len / 2

    # Mouth = upper-left;  sealed bottom = lower-right
    mx    = ct_cx - tax * hl;   my    = ct_cy - tay * hl
    bx_ct = ct_cx + tax * hl;   by_ct = ct_cy + tay * hl

    p1 = (mx - tpx*hw, my - tpy*hw)
    p2 = (mx + tpx*hw, my + tpy*hw)
    p3 = (bx_ct + tpx*hw, by_ct + tpy*hw)
    p4 = (bx_ct - tpx*hw, by_ct - tpy*hw)

    # Faint yellow-tint gas interior
    dwg.add(dwg.polygon(points=[p1, p2, p3, p4],
                        fill="#F0EDD5", opacity=0.38))
    # Glass body
    dwg.add(dwg.polygon(points=[p1, p2, p3, p4],
                        fill=GLASS, stroke=OL, stroke_width=2.5))
    # Rounded sealed bottom end
    dwg.add(dwg.ellipse(center=(bx_ct, by_ct), r=(hw, hw * 0.28),
                        fill=GLASS, stroke=OL, stroke_width=2.5))
    # Open mouth ellipse
    dwg.add(dwg.ellipse(center=(mx, my), r=(hw, hw * 0.28),
                        fill="none", stroke=OL, stroke_width=2.5))
    # Glass highlight stripe
    hl_sx = mx    + tpx*(hw - 10);   hl_sy = my    + tpy*(hw - 10)
    hl_ex = bx_ct + tpx*(hw - 10);   hl_ey = by_ct + tpy*(hw - 10)
    dwg.add(dwg.line(start=(hl_sx, hl_sy), end=(hl_ex, hl_ey),
                     stroke="#FFFFFF", stroke_width=5, opacity=0.55))

    # ── HAND (grips collection tube lower-right) ──────────────────
    dwg.add(dwg.ellipse(center=(hand_x, hand_y), r=(58, 38),
                        fill=HAND_C, stroke="#C8956A", stroke_width=1.5))
    # Thumb (upper-right)
    dwg.add(dwg.ellipse(center=(hand_x + 52, hand_y - 16), r=(18, 11),
                        fill=HAND_C, stroke="#C8956A", stroke_width=1.5))
    # Four finger bumps (pointing downward toward tube)
    for fi in range(4):
        dwg.add(dwg.ellipse(center=(hand_x - 26 + fi*16, hand_y + 30 + fi*3),
                            r=(8, 11), fill=HAND_C, stroke="#C8956A", stroke_width=1.2))
    # Knuckle lines
    for kx in (hand_x - 8, hand_x + 8):
        dwg.add(dwg.line(start=(kx, hand_y + 8), end=(kx, hand_y - 22),
                         stroke="#C8956A", stroke_width=1.2))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
