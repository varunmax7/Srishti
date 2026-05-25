import svgwrite

def render_thermal_decomposition(spec: dict, out_path: str) -> bool:
    hints = spec.get("render_hints", {})
    ch    = hints.get("canvas", spec.get("canvas", {}))

    w  = ch.get("width",  900)
    h  = ch.get("height", 800)
    bg = ch.get("background", "#FFFFFF")

    dwg = svgwrite.Drawing(out_path, size=(w, h))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bg))

    # Delivery Tube (draw first so it goes behind glass)
    dt_path = "M 470 300 L 630 300 Q 650 300 650 320 L 650 650"
    dwg.add(dwg.path(d=dt_path, fill="none", stroke="#1a1a1a", stroke_width=10))
    dwg.add(dwg.path(d=dt_path, fill="none", stroke="#F5F8FF", stroke_width=6))

    # Vertical Test Tube Liquid
    dwg.add(dwg.rect(insert=(630, 600), size=(40, 100), fill="#FFFACD", opacity=0.85))
    dwg.add(dwg.path(d="M 630 700 A 20 20 0 0 0 670 700 Z", fill="#FFFACD", opacity=0.85))

    # Vertical Test Tube Glass
    dwg.add(dwg.path(d="M 630 450 L 630 700 A 20 20 0 0 0 670 700 L 670 450", fill="none", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.path(d="M 635 460 L 635 690 A 15 15 0 0 0 645 700", fill="none", stroke="#FFFFFF", stroke_width=4, opacity=0.6))
    dwg.add(dwg.ellipse(center=(650, 450), r=(20, 6), fill="none", stroke="#1a1a1a", stroke_width=2))

    # Horizontal Test Tube Glass (Back/Fill)
    dwg.add(dwg.rect(insert=(300, 280), size=(180, 40), fill="#F0F8FF", opacity=0.4))
    dwg.add(dwg.path(d="M 300 280 A 20 20 0 0 0 300 320 Z", fill="#F0F8FF", opacity=0.4))

    # Powder
    dwg.add(dwg.path(d="M 302 312 Q 315 295, 340 315 L 340 318 L 302 318 Z", fill="#D0D0D0", stroke="#999999", stroke_width=1))

    # Horizontal Test Tube Glass (Outline)
    dwg.add(dwg.path(d="M 480 280 L 300 280 A 20 20 0 0 0 300 320 L 480 320", fill="none", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.ellipse(center=(480, 300), r=(6, 20), fill="none", stroke="#1a1a1a", stroke_width=2))

    # Stopper
    dwg.add(dwg.polygon(points=[(480, 282), (500, 286), (500, 314), (480, 318)], fill="#8C5C3B", stroke="#1a1a1a", stroke_width=2))

    # Stand Base & Rod
    dwg.add(dwg.rect(insert=(430, 710), size=(150, 30), rx=5, ry=5, fill="#D8D8D8", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(430, 740), size=(150, 10), fill="#A0A0A0", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(530, 150), size=(16, 560), fill="#E8E8E8", stroke="#1a1a1a", stroke_width=2))

    # Bunsen Burner
    dwg.add(dwg.polygon(points=[(300, 710), (380, 710), (360, 690), (320, 690)], fill="#D0D0D0", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(370, 695), size=(30, 10), rx=3, ry=3, fill="#77BBFF", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(332, 500), size=(16, 190), fill="#E0E0E0", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(328, 650), size=(24, 20), rx=2, ry=2, fill="#B0B0B0", stroke="#1a1a1a", stroke_width=2))

    # Flame
    dwg.add(dwg.path(d="M 340 500 Q 315 460, 340 380 Q 365 460, 340 500 Z", fill="#4DB8FF", stroke="#1a1a1a", stroke_width=1.5))
    dwg.add(dwg.path(d="M 340 500 Q 325 470, 340 410 Q 355 470, 340 500 Z", fill="#99D6FF", stroke="none"))

    # Clamp Boss
    dwg.add(dwg.rect(insert=(460, 275), size=(80, 50), rx=6, ry=6, fill="#7A7A7A", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(460, 280), size=(80, 5), fill="#FFFFFF", opacity=0.3))
    dwg.add(dwg.line(start=(520, 275), end=(520, 325), stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(500, 265), size=(20, 10), rx=2, ry=2, fill="#B0B0B0", stroke="#1a1a1a", stroke_width=2))
    dwg.add(dwg.rect(insert=(506, 255), size=(8, 10), fill="#909090", stroke="#1a1a1a", stroke_width=2))

    dwg.save()
    print(f"✅ Saved: {out_path}")
    return True
