import svgwrite
import math


def render_flame_test(spec: dict, out_path: str) -> bool:
    hints   = spec.get("render_hints", {})
    ch      = hints.get("canvas",          spec.get("canvas", {}))
    board_h = hints.get("board",           {})
    torch_h = hints.get("torch",           {})
    flame_h = hints.get("flame",           {})
    tong_h  = hints.get("tongs",           {})
    part_h  = hints.get("particle_stream", {})
    dish_h  = hints.get("dish",            {})
    hands_h = hints.get("hands",           {})

    w  = ch.get("width",  900)
    h  = ch.get("height", 720)
    bg = ch.get("background", "#ffffff")
    hand_c = hands_h.get("skin_color", "#F5C5A0")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Rotated-rectangle helper ──────────────────────────────────
    def rrect(cx, cy, length, width, angle_deg):
        a  = math.radians(angle_deg)
        ax_, ay_ = math.cos(a), math.sin(a)
        px_, py_ = -ay_, ax_
        hl, hw   = length / 2, width / 2
        return [
            (cx - ax_*hl - px_*hw, cy - ay_*hl - py_*hw),
            (cx + ax_*hl - px_*hw, cy + ay_*hl - py_*hw),
            (cx + ax_*hl + px_*hw, cy + ay_*hl + py_*hw),
            (cx - ax_*hl + px_*hw, cy - ay_*hl + py_*hw),
        ]

    # ── Board (wooden slab, 3-face perspective) ───────────────────
    b_ty  = board_h.get("top_y",            470)
    b_lx  = board_h.get("left_x",           120)
    b_rx  = board_h.get("right_x",          840)
    b_sk  = board_h.get("perspective_skew",  28)
    b_th  = board_h.get("thickness",         52)
    b_tc  = board_h.get("top_color",   "#D4A030")
    b_sc  = board_h.get("side_color",  "#A87820")
    b_hl  = board_h.get("highlight",   "#F0C860")
    b_ol  = board_h.get("outline",     "#2E2E2E")
    b_sw  = board_h.get("stroke_width",    2.5)

    shift = b_sk // 2     # vertical lift of back edge = 14 px

    # top face
    dwg.add(dwg.polygon(
        points=[(b_lx, b_ty), (b_rx, b_ty),
                (b_rx - b_sk, b_ty - shift), (b_lx + b_sk, b_ty - shift)],
        fill=b_tc, stroke=b_ol, stroke_width=b_sw,
    ))
    # highlight stripe on top face
    dwg.add(dwg.polygon(
        points=[(b_lx + 80, b_ty), (b_rx - 130, b_ty),
                (b_rx - 130 - b_sk, b_ty - shift), (b_lx + 80 + b_sk, b_ty - shift)],
        fill=b_hl, opacity=0.32,
    ))
    # front face
    dwg.add(dwg.polygon(
        points=[(b_lx, b_ty), (b_rx, b_ty),
                (b_rx, b_ty + b_th), (b_lx, b_ty + b_th)],
        fill=b_sc, stroke=b_ol, stroke_width=b_sw,
    ))
    # right side face
    dwg.add(dwg.polygon(
        points=[(b_rx, b_ty), (b_rx - b_sk, b_ty - shift),
                (b_rx - b_sk, b_ty - shift + b_th), (b_rx, b_ty + b_th)],
        fill=b_sc, stroke=b_ol, stroke_width=b_sw,
    ))

    # ── Evaporating dish / watch glass ────────────────────────────
    d_cx, d_cy = dish_h.get("center", [560, 460])
    d_rx  = dish_h.get("rx",           150)
    d_ry  = dish_h.get("ry",            48)
    d_fill  = dish_h.get("fill",        "#FFFFFF")
    d_inner = dish_h.get("inner_fill",  "#F0F0F0")
    d_pow   = dish_h.get("powder_fill", "#D8D8D8")
    d_ol    = dish_h.get("stroke",      "#2E2E2E")
    d_dsw   = dish_h.get("stroke_width", 2.5)
    bd      = 44   # bowl depth

    # bowl curve
    dwg.add(dwg.path(
        d=(f"M {d_cx - d_rx} {d_cy} "
           f"Q {d_cx - d_rx + 22} {d_cy + bd + 8}, {d_cx} {d_cy + bd} "
           f"Q {d_cx + d_rx - 22} {d_cy + bd + 8}, {d_cx + d_rx} {d_cy}"),
        fill=d_inner, stroke=d_ol, stroke_width=d_dsw,
    ))
    # powder blob
    dwg.add(dwg.path(
        d=(f"M {d_cx - 86} {d_cy + bd + 2} "
           f"Q {d_cx - 52} {d_cy + bd - 11}, {d_cx} {d_cy + bd + 1} "
           f"Q {d_cx + 56} {d_cy + bd - 11}, {d_cx + 86} {d_cy + bd + 4} "
           f"Q {d_cx + 52} {d_cy + bd + 20}, {d_cx - 52} {d_cy + bd + 18} Z"),
        fill=d_pow, stroke="#AAAAAA", stroke_width=1.2,
    ))
    # rim
    dwg.add(dwg.ellipse(center=(d_cx, d_cy), r=(d_rx, d_ry),
                        fill=d_fill, stroke=d_ol, stroke_width=d_dsw))
    dwg.add(dwg.ellipse(center=(d_cx, d_cy), r=(d_rx - 14, d_ry - 6),
                        fill="none", stroke="#BBBBBB", stroke_width=1.3))

    # ── Torch base disc ───────────────────────────────────────────
    s_cx, s_cy = torch_h.get("stand_center", [310, 480])
    s_r    = torch_h.get("stand_radius",     70)
    noz_x, noz_y = torch_h.get("nozzle_at", [430, 250])

    t_fill = torch_h.get("barrel_fill",  "#D0D0D0")
    t_dark = torch_h.get("barrel_dark",  "#AAAAAA")
    t_col  = torch_h.get("collar_fill",  "#B8B8B8")
    t_base = torch_h.get("base_fill",    "#C8C8C8")
    t_ol   = torch_h.get("outline",      "#2E2E2E")
    t_sw   = torch_h.get("stroke_width", 2)

    # lower disc shadow
    dwg.add(dwg.ellipse(center=(s_cx, s_cy + 5), r=(s_r, s_r // 5),
                        fill=t_dark, stroke=t_ol, stroke_width=t_sw))
    # disc body sides
    dwg.add(dwg.polygon(
        points=[(s_cx - s_r, s_cy - 4), (s_cx + s_r, s_cy - 4),
                (s_cx + s_r, s_cy + 5), (s_cx - s_r, s_cy + 5)],
        fill=t_dark, stroke=t_ol, stroke_width=t_sw,
    ))
    # top of disc
    dwg.add(dwg.ellipse(center=(s_cx, s_cy - 4), r=(s_r, s_r // 5),
                        fill=t_base, stroke=t_ol, stroke_width=t_sw))

    # ── Barrel ────────────────────────────────────────────────────
    brl_sx, brl_sy = s_cx, s_cy - s_r // 5
    brl_ex, brl_ey = noz_x, noz_y
    brl_len   = math.hypot(brl_ex - brl_sx, brl_ey - brl_sy)
    brl_angle = math.degrees(math.atan2(brl_ey - brl_sy, brl_ex - brl_sx))
    brl_mcx   = (brl_sx + brl_ex) / 2
    brl_mcy   = (brl_sy + brl_ey) / 2

    dwg.add(dwg.polygon(
        points=rrect(brl_mcx, brl_mcy, brl_len, 30, brl_angle),
        fill=t_dark, stroke=t_ol, stroke_width=t_sw,
    ))
    # highlight stripe
    dwg.add(dwg.polygon(
        points=rrect(brl_mcx - 5, brl_mcy - 5, brl_len - 12, 8, brl_angle),
        fill="#EEEEEE", opacity=0.65,
    ))
    # collar band at ~28 % along barrel
    c_t   = 0.28
    c_cx  = brl_sx + c_t * (brl_ex - brl_sx)
    c_cy  = brl_sy + c_t * (brl_ey - brl_sy)
    dwg.add(dwg.polygon(
        points=rrect(c_cx, c_cy, 28, 46, brl_angle),
        fill=t_col, stroke=t_ol, stroke_width=t_sw,
    ))
    # nozzle cap
    dwg.add(dwg.polygon(
        points=rrect(noz_x, noz_y, 20, 24, brl_angle),
        fill=t_fill, stroke=t_ol, stroke_width=t_sw,
    ))

    # ── Left hand (grips barrel collar) ──────────────────────────
    lh_x, lh_y = hands_h.get("left_hand", {}).get("at", [300, 360])

    dwg.add(dwg.ellipse(center=(lh_x, lh_y), r=(56, 34),
                        fill=hand_c, stroke="#C8956A", stroke_width=1.5))
    # thumb
    dwg.add(dwg.ellipse(center=(lh_x - 44, lh_y + 8), r=(18, 11),
                        fill=hand_c, stroke="#C8956A", stroke_width=1.5))
    # four finger bumps (top of palm)
    for fi in range(4):
        dwg.add(dwg.ellipse(center=(lh_x - 22 + fi * 16, lh_y - 30), r=(8, 11),
                            fill=hand_c, stroke="#C8956A", stroke_width=1.2))
    # knuckle lines
    for kx in (lh_x - 6, lh_x + 10):
        dwg.add(dwg.line(start=(kx, lh_y + 8), end=(kx, lh_y - 22),
                         stroke="#C8956A", stroke_width=1.2))

    # ── Flame (non-luminous, blue) ────────────────────────────────
    f_ox, f_oy = flame_h.get("origin",       [435, 245])
    f_dir      = flame_h.get("direction_deg", 38)
    f_len      = flame_h.get("length",        150)
    f_bc       = flame_h.get("base_color",   "#3366FF")
    f_oc       = flame_h.get("outer_color",  "#66AAFF")
    f_ic       = flame_h.get("inner_color",  "#99CCFF")
    f_tc       = flame_h.get("tip_color",    "#FFFFFF")

    fa   = math.radians(f_dir)
    fax  = math.cos(fa)
    fay  = -math.sin(fa)   # SVG y is inverted — positive angle goes UP
    fpx, fpy = -fay, fax

    def flame_path(ox, oy, length, width):
        return (
            f"M {ox + fpx*width/2:.1f} {oy + fpy*width/2:.1f} "
            f"Q {ox + fax*length*0.45 + fpx*width*0.65:.1f} "
            f"  {oy + fay*length*0.45 + fpy*width*0.65:.1f}, "
            f"  {ox + fax*length:.1f} {oy + fay*length:.1f} "
            f"Q {ox + fax*length*0.45 - fpx*width*0.65:.1f} "
            f"  {oy + fay*length*0.45 - fpy*width*0.65:.1f}, "
            f"  {ox - fpx*width/2:.1f} {oy - fpy*width/2:.1f} Z"
        )

    dwg.add(dwg.path(d=flame_path(f_ox, f_oy, f_len,            44), fill=f_oc))
    dwg.add(dwg.path(d=flame_path(f_ox, f_oy, int(f_len*0.72),  30), fill=f_ic))
    dwg.add(dwg.path(d=flame_path(f_ox, f_oy, int(f_len*0.46),  18), fill=f_tc, opacity=0.9))
    # deep-blue base cone
    dwg.add(dwg.path(
        d=(f"M {f_ox + fpx*16:.1f} {f_oy + fpy*16:.1f} "
           f"Q {f_ox + fax*34:.1f} {f_oy + fay*34:.1f}, "
           f"  {f_ox - fpx*16:.1f} {f_oy - fpy*16:.1f} Z"),
        fill=f_bc, opacity=0.88,
    ))

    # ── Particle / vapour stream (flame tip → dish) ───────────────
    p_from   = part_h.get("from",   [470, 240])
    p_to     = part_h.get("to",     [510, 470])
    p_count  = part_h.get("count",   18)
    p_col    = part_h.get("color",   "#CCCCCC")
    p_spread = part_h.get("spread",   26)

    for i in range(p_count):
        t    = i / (p_count - 1)
        ptx  = p_from[0] + t * (p_to[0] - p_from[0])
        pty  = p_from[1] + t * (p_to[1] - p_from[1])
        side = (t - 0.5) * p_spread * 0.5
        r    = max(1.4, 3.5 - 1.8 * t)
        dwg.add(dwg.circle(center=(ptx + side, pty), r=r, fill=p_col, opacity=0.82))

    # ── Tongs (brass, two-arm scissor) ───────────────────────────
    rh_x, rh_y  = hands_h.get("right_hand", {}).get("at", [690, 150])
    t_tip_x, t_tip_y = tong_h.get("tip_at", [560, 200])

    t_c  = tong_h.get("color",        "#B8A020")
    t_hl = tong_h.get("highlight",    "#E8D040")
    t_to = tong_h.get("stroke",       "#2E2E2E")
    t_ts = tong_h.get("stroke_width", 2)

    tong_len   = math.hypot(rh_x - t_tip_x, rh_y - t_tip_y) + 22
    tong_angle = math.degrees(math.atan2(rh_y - t_tip_y, rh_x - t_tip_x))
    t_mcx      = (t_tip_x + rh_x) / 2
    t_mcy      = (t_tip_y + rh_y) / 2

    ta_r = math.radians(tong_angle)
    tpx, tpy = -math.sin(ta_r), math.cos(ta_r)
    sep = 7

    # arm 1 (one side)
    dwg.add(dwg.polygon(
        points=rrect(t_mcx + tpx*sep, t_mcy + tpy*sep, tong_len, 7, tong_angle),
        fill=t_c, stroke=t_to, stroke_width=t_ts,
    ))
    # arm 2 (other side)
    dwg.add(dwg.polygon(
        points=rrect(t_mcx - tpx*sep, t_mcy - tpy*sep, tong_len, 7, tong_angle),
        fill=t_hl, stroke=t_to, stroke_width=t_ts,
    ))
    # wire loop at tip
    dwg.add(dwg.ellipse(center=(t_tip_x - 4, t_tip_y + 6), r=(14, 9),
                        fill="none", stroke=t_c,  stroke_width=3))
    dwg.add(dwg.ellipse(center=(t_tip_x - 4, t_tip_y + 6), r=(8,  5),
                        fill="none", stroke=t_hl, stroke_width=2))

    # ── Right hand (holds tong handles) ──────────────────────────
    dwg.add(dwg.ellipse(center=(rh_x, rh_y), r=(60, 40),
                        fill=hand_c, stroke="#C8956A", stroke_width=1.5))
    # thumb
    dwg.add(dwg.ellipse(center=(rh_x + 50, rh_y - 12), r=(18, 11),
                        fill=hand_c, stroke="#C8956A", stroke_width=1.5))
    # four finger bumps (pointing downward-left toward tong handle)
    for fi in range(4):
        dwg.add(dwg.ellipse(center=(rh_x - 26 + fi * 16, rh_y + 30 + fi * 3), r=(8, 11),
                            fill=hand_c, stroke="#C8956A", stroke_width=1.2))
    # knuckle lines
    for kx in (rh_x - 8, rh_x + 8):
        dwg.add(dwg.line(start=(kx, rh_y + 8), end=(kx, rh_y - 22),
                         stroke="#C8956A", stroke_width=1.2))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
