import svgwrite
import os

def render_zinc_reaction(spec: dict, out_path: str) -> bool:
    hints = spec.get("render_hints", {})
    ch    = hints.get("canvas", spec.get("canvas", {}))

    w  = ch.get("width",  900)
    h  = ch.get("height", 800)
    bg = ch.get("background", "#FFFFFF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # 1. Flask Back Base & Neck curves
    dwg.add(dwg.path(d="M 270 670 A 180 30 0 0 1 630 670", fill="none", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.path(d="M 380 240 A 70 15 0 0 1 520 240", fill="none", stroke="#1a1a1a", stroke_width=2))

    # 2. Delivery Tube
    dwg.add(dwg.rect(insert=(444, 80), size=(12, 320), fill="#F0F8FF", opacity=0.8))
    dwg.add(dwg.path(d="M 444 80 L 444 400", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.path(d="M 456 80 L 456 400", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.ellipse(center=(450, 80), r=(6, 2), fill="#E6E6E6", stroke="#1a1a1a", stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(450, 400), r=(6, 2), fill="#D0D0D0", stroke="#1a1a1a", stroke_width=1.5))

    # 3. Stopper
    stopper_path = "M 398 180 L 405 320 A 45 10 0 0 0 495 320 L 502 180 Z"
    dwg.add(dwg.path(d=stopper_path, fill="#C48A5A", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.path(d="M 415 180 L 420 318", fill="none", stroke="#E8C090", stroke_width=10, opacity=0.5))
    dwg.add(dwg.path(d="M 485 180 L 480 318", fill="none", stroke="#8A5A30", stroke_width=8, opacity=0.4))
    dwg.add(dwg.ellipse(center=(450, 180), r=(52, 12), fill="#D4A070", stroke="#1a1a1a", stroke_width=2))

    # 4. Zinc Granules
    granules = [
        (310, 670), (330, 665), (345, 680), (360, 660), (375, 675),
        (400, 685), (420, 665), (435, 675), (455, 660), (470, 685),
        (490, 670), (510, 680), (530, 660), (550, 675), (570, 665),
        (590, 670), (440, 685), (390, 670), (410, 675), (520, 670),
        (320, 680), (600, 680), (480, 665), (500, 685), (380, 685)
    ]
    for gx, gy in granules:
        dwg.add(dwg.ellipse(center=(gx, gy), r=(11, 7), fill="#999999", stroke="#1a1a1a", stroke_width=1.5))
        dwg.add(dwg.circle(center=(gx-3, gy-1), r=1, fill="#333333"))
        dwg.add(dwg.circle(center=(gx+3, gy+1), r=1.5, fill="#333333"))
        dwg.add(dwg.circle(center=(gx+1, gy-2), r=1, fill="#333333"))

    # 5. Liquid
    liq_body = "M 320 550 A 130 20 0 0 1 580 550 L 630 670 A 180 30 0 0 1 270 670 Z"
    dwg.add(dwg.path(d=liq_body, fill="#FFF599", opacity=0.4))
    dwg.add(dwg.ellipse(center=(450, 550), r=(130, 20), fill="#FFF066", opacity=0.5, stroke="#D4C850", stroke_width=1))

    # 6. Bubbles
    bubbles = [
        (320, 640), (330, 620), (340, 580), (360, 650), (365, 600), (370, 570),
        (390, 630), (410, 610), (420, 660), (440, 580), (455, 640), (470, 600),
        (490, 630), (510, 590), (530, 650), (550, 610), (560, 570), (580, 630),
        (350, 610), (380, 590), (430, 620), (460, 580), (480, 650), (500, 610),
        (520, 640), (540, 580), (570, 600), (590, 650), (400, 580), (450, 660)
    ]
    for bx, by in bubbles:
        dwg.add(dwg.circle(center=(bx, by), r=3.5, fill="#FFFFFF", stroke="#888888", stroke_width=1, opacity=0.85))

    # 7. Flask Glass Front
    flask_front = (
        "M 380 240 "
        "A 70 15 0 0 0 520 240 "  
        "L 500 260 "
        "L 500 360 "
        "L 630 670 "
        "A 180 30 0 0 1 270 670 " 
        "L 400 360 "
        "L 400 260 "
        "Z"
    )
    dwg.add(dwg.path(d=flask_front, fill="#EAF4FC", opacity=0.25, stroke="#1a1a1a", stroke_width=2.5, stroke_linejoin="round"))

    dwg.add(dwg.path(d="M 406 360 L 285 660", fill="none", stroke="#FFFFFF", stroke_width=6, opacity=0.6, stroke_linecap="round"))
    dwg.add(dwg.path(d="M 494 360 L 615 660", fill="none", stroke="#FFFFFF", stroke_width=3, opacity=0.3, stroke_linecap="round"))
    dwg.add(dwg.path(d="M 406 265 L 406 350", fill="none", stroke="#FFFFFF", stroke_width=4, opacity=0.6, stroke_linecap="round"))

    # 8. Text label
    dwg.add(dwg.text("Zinc granules", insert=(550, 750), font_family="serif", font_size="28px", fill="#1a1a1a"))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
