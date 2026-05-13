import json
import svgwrite
import os

def render_biology(template_path: str, output_path: str):
    with open(template_path) as f:
        template = json.load(f)

    canvas = template["canvas"]
    width = canvas["width"]
    height = canvas["height"]

    dwg = svgwrite.Drawing(output_path, size=(width, height))

    # White background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="white"))

    # Title
    dwg.add(dwg.text(
        template.get("title", ""),
        insert=(width / 2, 22),
        text_anchor="middle",
        font_size=18,
        font_family="Arial",
        font_weight="bold",
        fill="#333333"
    ))

    # Draw all parts
    for part in template["parts"]:
        shape = part["shape"]
        color = part.get("color", "#eeeeee")
        stroke = part.get("stroke", "#333333")
        sw = part.get("stroke_width", 2)

        if shape == "rect":
            dwg.add(dwg.rect(
                insert=(part["x"], part["y"]),
                size=(part["w"], part["h"]),
                fill=color,
                stroke=stroke,
                stroke_width=sw,
                rx=6, ry=6
            ))

        elif shape == "ellipse":
            dwg.add(dwg.ellipse(
                center=(part["cx"], part["cy"]),
                r=(part["rx"], part["ry"]),
                fill=color,
                stroke=stroke,
                stroke_width=sw
            ))

        elif shape == "path":
            dwg.add(dwg.path(
                d=part["d"],
                fill=part.get("color", "none"),
                stroke=stroke,
                stroke_width=sw
            ))

    # Draw labels with lines
    for label in template.get("labels", []):
        lx = label["lx"]
        ly = label["ly"]
        tx = label["tx"]
        ty = label["ty"]
        text = label["text"]

        # Line from label to part
        dwg.add(dwg.line(
            start=(lx, ly),
            end=(tx, ty),
            stroke="#555555",
            stroke_width=1.2
        ))

        # Small dot at part end
        dwg.add(dwg.circle(
            center=(tx, ty),
            r=3,
            fill="#555555"
        ))

        # Label text background (white box for readability)
        text_len = len(text) * 6.5
        dwg.add(dwg.rect(
            insert=(lx - 3, ly - 13),
            size=(text_len + 6, 16),
            fill="white",
            opacity=0.85,
            rx=3, ry=3
        ))

        # Label text
        dwg.add(dwg.text(
            text,
            insert=(lx, ly),
            font_size=11,
            font_family="Arial",
            fill="#111111"
        ))

    dwg.save()
    print(f"Saved: {output_path}")


# ── Test runner ──────────────────────────────────────────────
if __name__ == "__main__":
    diagrams = [
        ("templates/biology/plant_cell.json",      "output/plant_cell.svg"),
        ("templates/biology/animal_cell.json",     "output/animal_cell.svg"),
        ("templates/biology/heart.json",           "output/heart.svg"),
        ("templates/biology/digestive_system.json","output/digestive_system.svg"),
    ]

    os.makedirs("output", exist_ok=True)

    for template_path, output_path in diagrams:
        if os.path.exists(template_path):
            render_biology(template_path, output_path)
        else:
            print(f"Missing: {template_path}")