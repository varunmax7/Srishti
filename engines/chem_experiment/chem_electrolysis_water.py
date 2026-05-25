import svgwrite


def render_electrolysis_water(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {})
    w  = canvas.get("width",  900)
    h  = canvas.get("height", 760)
    bg = canvas.get("background", "#ffffff")

    tank_cfg  = spec.get("tank", {})
    mem_cfg   = spec.get("membrane", {})
    el_cfg    = spec.get("electrodes", {})
    ion_cfg   = spec.get("ions", {})
    cir_cfg   = spec.get("circuit", {})

    t_fill  = tank_cfg.get("fill_color",    "#C5DEF5")
    t_ol    = tank_cfg.get("outline_color", "#6B8EAD")
    t_sw    = tank_cfg.get("stroke_width",  3.5)
    t_r     = tank_cfg.get("corner_radius", 18)

    mem_w   = mem_cfg.get("width",   20)
    mem_ol  = mem_cfg.get("outline", "#555555")

    el_fill = el_cfg.get("fill",         "#DCDCDC")
    el_dark = el_cfg.get("fill_dark",    "#B8B8B8")
    el_ol   = el_cfg.get("outline",      "#2E2E2E")
    el_sw   = el_cfg.get("stroke_width", 2)

    cat_c   = ion_cfg.get("cation_color", "#E53030")
    an_c    = ion_cfg.get("anion_color",  "#3060E8")
    ion_r   = ion_cfg.get("radius",       9)

    wire_c  = cir_cfg.get("wire_color",  "#CC2222")
    wire_w  = cir_cfg.get("wire_width",  2.5)
    bat_cols = cir_cfg.get("battery", {}).get("colors", ["#E8882A", "#AAAAAA", "#F0C040"])

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # ── Cross-hatch pattern for membrane ─────────────────────────
    ph = 8
    cross = dwg.defs.add(dwg.pattern(
        id="crosshatch", x=0, y=0, width=ph, height=ph,
        patternUnits="userSpaceOnUse",
    ))
    cross.add(dwg.line(start=(0, 0), end=(ph, ph), stroke="#666", stroke_width=1.5))
    cross.add(dwg.line(start=(ph, 0), end=(0, ph), stroke="#666", stroke_width=1.5))

    # ── Coordinate anchors ────────────────────────────────────────
    t_left, t_right = 162, 772
    t_top,  t_bot   = 282, 698
    mem_cx  = (t_left + t_right) / 2   # 467 — membrane centre
    anode_x  = 318                      # left  electrode (anode  +)
    cathode_x = 616                     # right electrode (cathode −)
    el_rx, el_ry = 28, 11              # electrode half-sizes
    el_top,  el_bot = 242, 672

    # ── Tank fill ────────────────────────────────────────────────
    dwg.add(dwg.rect(
        insert=(t_left, t_top), size=(t_right - t_left, t_bot - t_top),
        rx=t_r, ry=t_r,
        fill=t_fill, stroke=t_ol, stroke_width=t_sw,
    ))

    # ── Membrane ─────────────────────────────────────────────────
    dwg.add(dwg.rect(
        insert=(mem_cx - mem_w/2, t_top + 4), size=(mem_w, t_bot - t_top - 8),
        fill="url(#crosshatch)", stroke=mem_ol, stroke_width=2,
    ))

    # ── Scattered ions ───────────────────────────────────────────
    cations = [
        (205,360),(238,448),(218,512),(252,592),(298,622),
        (340,572),(312,490),(378,438),(282,396),(342,658),
        (382,642),(418,574),(425,432),
    ]
    anions = [
        (512,348),(558,418),(528,482),(514,562),(548,642),
        (592,592),(624,522),(658,468),(662,388),(702,352),
        (697,602),(732,542),(660,662),
    ]
    for x, y in cations:
        dwg.add(dwg.circle(center=(x, y), r=ion_r, fill=cat_c))
    for x, y in anions:
        dwg.add(dwg.circle(center=(x, y), r=ion_r, fill=an_c))

    # ── Helper: draw one cylinder electrode ─────────────────────
    def draw_electrode(ex):
        # body rectangle
        dwg.add(dwg.rect(
            insert=(ex - el_rx, el_top + el_ry),
            size=(el_rx*2, el_bot - el_top - el_ry),
            fill=el_dark, stroke=el_ol, stroke_width=el_sw,
        ))
        # top ellipse cap
        dwg.add(dwg.ellipse(
            center=(ex, el_top + el_ry), r=(el_rx, el_ry),
            fill=el_fill, stroke=el_ol, stroke_width=el_sw,
        ))
        # glass highlight stripe
        dwg.add(dwg.rect(
            insert=(ex - el_rx + 5, el_top + el_ry + 8),
            size=(7, el_bot - el_top - el_ry - 20),
            fill="#F5F5F5", opacity=0.6,
        ))

    draw_electrode(anode_x)
    draw_electrode(cathode_x)

    # ── Tank outline on top ───────────────────────────────────────
    dwg.add(dwg.rect(
        insert=(t_left, t_top), size=(t_right - t_left, t_bot - t_top),
        rx=t_r, ry=t_r,
        fill="none", stroke=t_ol, stroke_width=t_sw,
    ))

    # ── ⊕ / ⊖ symbols beside electrodes ─────────────────────────
    def draw_symbol(cx, cy, plus: bool):
        r_sym = 16
        dwg.add(dwg.circle(
            center=(cx, cy), r=r_sym,
            fill="#ffffff", stroke="#2E2E2E", stroke_width=2,
        ))
        if plus:
            dwg.add(dwg.line(start=(cx-9, cy), end=(cx+9, cy), stroke="#2E2E2E", stroke_width=2))
            dwg.add(dwg.line(start=(cx, cy-9), end=(cx, cy+9), stroke="#2E2E2E", stroke_width=2))
        else:
            dwg.add(dwg.line(start=(cx-9, cy), end=(cx+9, cy), stroke="#2E2E2E", stroke_width=2))

    sym_y = t_top + 55
    draw_symbol(anode_x  + el_rx + 24, sym_y, plus=True)
    draw_symbol(cathode_x - el_rx - 24, sym_y, plus=False)

    # ── Battery / resistor component ─────────────────────────────
    bat_cx, bat_cy = 695, 118
    bat_w,  bat_h  = 188, 44
    bat_x = bat_cx - bat_w / 2
    bat_y = bat_cy - bat_h / 2
    seg_w = bat_w / 3

    for i, col in enumerate(bat_cols):
        dwg.add(dwg.rect(
            insert=(bat_x + i * seg_w, bat_y), size=(seg_w, bat_h),
            fill=col, stroke="#2E2E2E", stroke_width=1.5,
        ))
    dwg.add(dwg.rect(
        insert=(bat_x, bat_y), size=(bat_w, bat_h),
        fill="none", stroke="#2E2E2E", stroke_width=2.2,
    ))

    # ── Red circuit wires ─────────────────────────────────────────
    # Left wire: anode top → up → cubic-curve → battery left terminal
    lx, ly = anode_x, el_top
    dwg.add(dwg.path(
        d=(f"M {lx} {ly} "
           f"L {lx} 168 "
           f"C {lx} 68, {bat_x - 55} 68, {bat_x} {bat_cy}"),
        fill="none", stroke=wire_c, stroke_width=wire_w,
    ))
    # Right wire: cathode top → up → cubic-curve → battery right terminal
    rx, ry = cathode_x, el_top
    bat_rx = bat_x + bat_w
    dwg.add(dwg.path(
        d=(f"M {rx} {ry} "
           f"L {rx} 168 "
           f"C {rx} 68, {bat_rx + 55} 68, {bat_rx} {bat_cy}"),
        fill="none", stroke=wire_c, stroke_width=wire_w,
    ))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
