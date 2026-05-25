import svgwrite
import math


def render_star_polymer(spec: dict, out_path: str) -> bool:
    canvas = spec.get("canvas", {})
    w = canvas.get("width", 860)
    h = canvas.get("height", 860)
    bg = canvas.get("background", "#ffffff")
    cx, cy = w / 2, h / 2

    core_cfg = spec.get("core", {})
    arm_cfg  = spec.get("arms", {})
    end_cfg  = spec.get("end_groups", {})

    core_r   = core_cfg.get("radius", 30)
    core_fill  = core_cfg.get("fill", "#F5C842")
    core_stroke = core_cfg.get("stroke", "#2E2E2E")
    core_sw  = core_cfg.get("stroke_width", 2.5)

    num_arms  = arm_cfg.get("count", 13)
    arm_len   = arm_cfg.get("length", 230)
    arm_color = arm_cfg.get("color", "#2E2E2E")
    arm_sw    = arm_cfg.get("stroke_width", 2.2)
    amplitude = arm_cfg.get("zigzag_amplitude", 11)
    segments  = arm_cfg.get("zigzag_segments", 16)

    end_r      = end_cfg.get("radius", 30)
    end_fill   = end_cfg.get("fill", "#9EA3C0")
    end_stroke = end_cfg.get("stroke", "#2E2E2E")
    end_sw     = end_cfg.get("stroke_width", 2.5)

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    for i in range(num_arms):
        angle = (2 * math.pi * i) / num_arms - math.pi / 2

        # unit vectors: along arm and perpendicular
        ax, ay = math.cos(angle), math.sin(angle)
        px, py = -ay, ax

        # zigzag polyline points
        t_start = core_r + 4
        t_end   = arm_len
        pts = []
        for j in range(segments + 1):
            t = t_start + (t_end - t_start) * j / segments
            # alternate sides; endpoints land on the centre axis
            if j == 0 or j == segments:
                off = 0.0
            elif j % 2 == 0:
                off = amplitude
            else:
                off = -amplitude
            pts.append((cx + ax * t + px * off, cy + ay * t + py * off))

        dwg.add(dwg.polyline(
            points=pts,
            fill="none",
            stroke=arm_color,
            stroke_width=arm_sw,
            stroke_linejoin="miter",
        ))

        # end-group circle
        ex = cx + ax * (arm_len + end_r + 4)
        ey = cy + ay * (arm_len + end_r + 4)
        dwg.add(dwg.circle(
            center=(ex, ey), r=end_r,
            fill=end_fill, stroke=end_stroke, stroke_width=end_sw,
        ))

    # core on top
    dwg.add(dwg.circle(
        center=(cx, cy), r=core_r,
        fill=core_fill, stroke=core_stroke, stroke_width=core_sw,
    ))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
