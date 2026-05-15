import os
import io
import re
import json
import math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont


def parse_svg_path(d, scale=1.0):
    """Parse SVG path 'd' attribute into a list of points for PIL drawing.
    Supports M, L, Q (quadratic bezier), C (cubic bezier), Z commands.
    Bezier curves are approximated as line segments.
    """
    points = []
    # Split into command + args pairs
    tokens = re.findall(r'([MLQCZmlqcz])\s*([^MLQCZmlqcz]*)', d)
    cx, cy = 0, 0
    start_x, start_y = 0, 0

    for cmd, args in tokens:
        nums = [float(x) * scale for x in re.findall(r'[-+]?\d*\.?\d+', args)]

        if cmd == 'M':
            cx, cy = nums[0], nums[1]
            start_x, start_y = cx, cy
            points.append((cx, cy))
        elif cmd == 'L':
            cx, cy = nums[0], nums[1]
            points.append((cx, cy))
        elif cmd == 'Q':
            # Quadratic bezier
            qx, qy, ex, ey = nums[0], nums[1], nums[2], nums[3]
            for i in range(1, 11):
                t = i / 10.0
                x = (1-t)**2 * cx + 2*(1-t)*t * qx + t**2 * ex
                y = (1-t)**2 * cy + 2*(1-t)*t * qy + t**2 * ey
                points.append((x, y))
            cx, cy = ex, ey
        elif cmd == 'C':
            # Cubic bezier
            c1x, c1y, c2x, c2y, ex, ey = nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]
            for i in range(1, 11):
                t = i / 10.0
                x = (1-t)**3*cx + 3*(1-t)**2*t*c1x + 3*(1-t)*t**2*c2x + t**3*ex
                y = (1-t)**3*cy + 3*(1-t)**2*t*c1y + 3*(1-t)*t**2*c2y + t**3*ey
                points.append((x, y))
            cx, cy = ex, ey
        elif cmd.upper() == 'Z':
            points.append((start_x, start_y))

    return points


def get_font(size=14, bold=False):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def render_svg_to_pil(template: dict, scale: float = 2.0) -> Image.Image:
    """
    Render biology diagram directly from JSON template using PIL.
    No SVG conversion needed — draw shapes directly.
    """
    canvas = template["canvas"]
    w = int(canvas["width"] * scale)
    h = int(canvas["height"] * scale)

    image = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    for part in template["parts"]:
        shape = part["shape"]
        color = part.get("color", "#eeeeee")
        stroke = part.get("stroke", "#333333")
        sw = max(1, int(part.get("stroke_width", 2) * scale))

        # Handle "none" → no fill / no outline (transparent)
        fill_color = None if color.lower() == "none" else color
        stroke_color = None if stroke.lower() == "none" else stroke

        if shape == "rect":
            x = part["x"] * scale
            y = part["y"] * scale
            x2 = x + part["w"] * scale
            y2 = y + part["h"] * scale
            draw.rectangle([x, y, x2, y2], fill=fill_color, outline=stroke_color, width=sw)

        elif shape == "ellipse":
            cx = part["cx"] * scale
            cy = part["cy"] * scale
            rx = part["rx"] * scale
            ry = part["ry"] * scale
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                         fill=fill_color, outline=stroke_color, width=sw)

        elif shape == "path":
            d = part.get("d", "")
            pts = parse_svg_path(d, scale=scale)
            if len(pts) >= 2:
                is_closed = d.strip().upper().endswith('Z')
                if is_closed and fill_color:
                    draw.polygon(pts, fill=fill_color, outline=stroke_color)
                else:
                    draw.line(pts, fill=stroke_color or "#333333", width=sw)

    return image


def draw_arrow(draw, start, end, color="#333333", width=2, head_size=8):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    head_angle = math.radians(25)
    hx1 = x2 - head_size * math.cos(angle - head_angle)
    hy1 = y2 - head_size * math.sin(angle - head_angle)
    hx2 = x2 - head_size * math.cos(angle + head_angle)
    hy2 = y2 - head_size * math.sin(angle + head_angle)
    draw.polygon([(x2, y2), (hx1, hy1), (hx2, hy2)], fill=color)


def add_labels(template_path: str, output_path: str, scale: float = 2.0):
    with open(template_path) as f:
        template = json.load(f)

    # Render shapes directly from JSON
    image = render_svg_to_pil(template, scale=scale)
    draw = ImageDraw.Draw(image)

    font       = get_font(size=int(13 * scale))
    title_font = get_font(size=int(18 * scale), bold=True)

    # Draw title
    title = template.get("title", "")
    if title:
        bbox   = draw.textbbox((0, 0), title, font=title_font)
        text_w = bbox[2] - bbox[0]
        img_w  = image.size[0]
        draw.text(((img_w - text_w) / 2, 8 * scale), title,
                  fill="#222222", font=title_font)

    # Draw labels
    for label in template.get("labels", []):
        lx   = label["lx"] * scale
        ly   = label["ly"] * scale
        tx   = label["tx"] * scale
        ty   = label["ty"] * scale
        text = label["text"]

        bbox   = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        pad = int(5 * scale)
        box = [lx - pad, ly - text_h - pad, lx + text_w + pad, ly + pad]

        # White box behind label
        draw.rounded_rectangle(box, radius=5,
                                fill=(255, 255, 255, 220),
                                outline="#999999", width=1)

        # Arrow from box edge → target part
        box_cx  = (box[0] + box[2]) / 2
        box_cy  = (box[1] + box[3]) / 2
        start_x = box[2] if tx > box_cx else box[0]
        start_y = box_cy

        draw_arrow(draw, (start_x, start_y), (tx, ty),
                   color="#444444",
                   width=max(1, int(1.5 * scale)),
                   head_size=int(7 * scale))

        # Label text
        draw.text((lx, ly - text_h), text, fill="#111111", font=font)

    image.save(output_path, "PNG")
    print(f"Saved: {output_path}")


# ── Test runner ──────────────────────────────────────────────
if __name__ == "__main__":
    diagrams = [
        ("templates/biology/plant_cell.json",       "output/plant_cell_labeled.png"),
        ("templates/biology/animal_cell.json",      "output/animal_cell_labeled.png"),
        ("templates/biology/heart.json",            "output/heart_labeled.png"),
        ("templates/biology/digestive_system.json", "output/digestive_system_labeled.png"),
    ]

    os.makedirs("output", exist_ok=True)

    for template, png in diagrams:
        if os.path.exists(template):
            add_labels(template, png)
        else:
            print(f"❌ Missing: {template}")