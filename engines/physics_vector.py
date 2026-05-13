import os
import math
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
import svgwrite
from PIL import Image, ImageDraw, ImageFont


# ═══════════════════════════════════════════════════════════════
# SECTION 1 — MATPLOTLIB GRAPHS
# ═══════════════════════════════════════════════════════════════

GRAPH_STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor":   "#F8F9FA",
    "axes.grid":        True,
    "grid.color":       "#DDDDDD",
    "grid.linestyle":   "--",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "font.family":      "sans-serif",
}


def apply_style():
    plt.rcParams.update(GRAPH_STYLE)


def render_distance_time_graph(
    times, distances,
    output_path,
    title="Distance-Time Graph",
    xlabel="Time (s)", ylabel="Distance (m)",
    color="#1565C0", label="Object"
):
    apply_style()
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(times, distances, color=color, linewidth=2.5,
            marker="o", markersize=5, label=label)

    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=13)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {output_path}")


def render_velocity_time_graph(
    times, velocities,
    output_path,
    title="Velocity-Time Graph",
    color="#C62828", label="Object"
):
    apply_style()
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(times, velocities, color=color, linewidth=2.5,
            marker="s", markersize=5, label=label)

    # Shade area under curve (displacement)
    ax.fill_between(times, velocities, alpha=0.15, color=color, label="Displacement area")

    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Time (s)", fontsize=13)
    ax.set_ylabel("Velocity (m/s)", fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {output_path}")


def render_wave_diagram(
    output_path,
    title="Wave Diagram",
    wavelength=2.0, amplitude=1.0, num_waves=3
):
    apply_style()
    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.linspace(0, num_waves * wavelength, 500)
    y = amplitude * np.sin(2 * np.pi * x / wavelength)

    ax.plot(x, y, color="#6A1B9A", linewidth=2.5)
    ax.axhline(0, color="#333333", linewidth=1, linestyle="--")

    # Labels
    ax.annotate("", xy=(wavelength, amplitude * 0.5),
                xytext=(0, amplitude * 0.5),
                arrowprops=dict(arrowstyle="<->", color="#1565C0", lw=1.5))
    ax.text(wavelength / 2, amplitude * 0.6, "λ (wavelength)",
            ha="center", fontsize=11, color="#1565C0")

    ax.annotate("", xy=(wavelength * 0.25, amplitude),
                xytext=(wavelength * 0.25, 0),
                arrowprops=dict(arrowstyle="<->", color="#C62828", lw=1.5))
    ax.text(wavelength * 0.25 + 0.15, amplitude / 2, "A",
            fontsize=11, color="#C62828")

    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Distance", fontsize=13)
    ax.set_ylabel("Displacement", fontsize=13)
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {output_path}")


def render_motion_graphs(output_path, title="Uniformly Accelerated Motion"):
    """Renders distance-time and velocity-time side by side."""
    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    t = np.linspace(0, 5, 50)
    a = 2.0  # acceleration
    u = 0.0  # initial velocity

    s = u * t + 0.5 * a * t ** 2
    v = u + a * t

    # Distance-time
    ax1.plot(t, s, color="#1565C0", linewidth=2.5, marker="o", markersize=3)
    ax1.set_title("Distance-Time", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Time (s)", fontsize=12)
    ax1.set_ylabel("Distance (m)", fontsize=12)
    ax1.set_xlim(left=0); ax1.set_ylim(bottom=0)

    # Velocity-time
    ax2.plot(t, v, color="#C62828", linewidth=2.5, marker="s", markersize=3)
    ax2.fill_between(t, v, alpha=0.15, color="#C62828")
    ax2.set_title("Velocity-Time", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Time (s)", fontsize=12)
    ax2.set_ylabel("Velocity (m/s)", fontsize=12)
    ax2.set_xlim(left=0); ax2.set_ylim(bottom=0)

    fig.suptitle(title, fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {output_path}")


# ═══════════════════════════════════════════════════════════════
# SECTION 2 — SVG STRUCTURAL DIAGRAMS
# ═══════════════════════════════════════════════════════════════

def render_concave_mirror(output_path):
    dwg = svgwrite.Drawing(output_path, size=(700, 420))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    # ── Geometry (all derived from these constants) ───────────────
    # Mirror pole P, Focus F, Centre of curvature C (all on y=220 axis)
    Py = 220          # principal axis y
    Px = 570          # pole x
    Fx = 500          # focus x  (focal length = Px-Fx = 70px)
    Cx = 430          # centre x (radius  = Px-Cx = 140px = 2f)
    obj_x, obj_y_tip = 200, 120   # object base on axis, tip 100px above

    # Image position via mirror formula: 1/v = 1/f − 1/u
    u = Px - obj_x       # 370
    f = Px - Fx          # 70
    v = (f * u) / (u - f)          # ≈ 86.3 px from pole
    img_x = round(Px - v)          # ≈ 484
    # Magnification m = −v/u  →  image height (downward = inverted)
    img_h = round(abs(v / u) * (Py - obj_y_tip))   # ≈ 23 px below axis
    img_y_tip = Py + img_h         # ≈ 243

    # ── Title ────────────────────────────────────────────────────
    dwg.add(dwg.text("Concave Mirror — Ray Diagram",
                     insert=(350, 28), text_anchor="middle",
                     font_size=18, font_family="Arial",
                     font_weight="bold", fill="#1a1a2e"))

    # ── Principal axis ───────────────────────────────────────────
    dwg.add(dwg.line((30, Py), (670, Py),
                     stroke="#555", stroke_width=1.5,
                     **{"stroke-dasharray": "6,4"}))
    dwg.add(dwg.text("Principal Axis", insert=(35, Py - 6),
                     font_size=11, fill="#555", font_family="Arial"))

    # ── Mirror arc (concave — opening left) ──────────────────────
    dwg.add(dwg.path(
        d=f"M {Px} 90 Q {Px-50} {Py} {Px} 350",
        stroke="#1565C0", stroke_width=5, fill="none"
    ))
    dwg.add(dwg.text("Concave Mirror", insert=(Px+5, Py),
                     font_size=12, fill="#1565C0", font_family="Arial"))

    # ── Reference points F and C ──────────────────────────────────
    for x, lbl in [(Cx, "C"), (Fx, "F")]:
        dwg.add(dwg.line((x, Py-6), (x, Py+6), stroke="#333", stroke_width=1.5))
        dwg.add(dwg.text(lbl, insert=(x - 5, Py + 20),
                         font_size=13, font_family="Arial", fill="#333"))
    dwg.add(dwg.text("P", insert=(Px - 4, Py + 20),
                     font_size=13, font_family="Arial", fill="#333"))

    # ── Object arrow (orange) ─────────────────────────────────────
    dwg.add(dwg.line((obj_x, Py), (obj_x, obj_y_tip),
                     stroke="#FF6F00", stroke_width=3))
    dwg.add(dwg.polygon(
        [(obj_x, obj_y_tip - 10), (obj_x - 6, obj_y_tip + 8), (obj_x + 6, obj_y_tip + 8)],
        fill="#FF6F00"))
    dwg.add(dwg.text("Object", insert=(obj_x - 40, obj_y_tip - 5),
                     font_size=12, fill="#FF6F00", font_family="Arial"))

    # ─────────────────────────────────────────────────────────────
    # RAY 1 (red): Parallel to axis → hits mirror → reflects through F
    # Incident ray travels at y = obj_y_tip from left to mirror pole x
    # Reflected ray: line through (Px, obj_y_tip) and F(Fx, Py)
    #   slope = (Py - obj_y_tip) / (Fx - Px)
    # ─────────────────────────────────────────────────────────────
    r1_hit_x, r1_hit_y = Px, obj_y_tip    # hits mirror at pole height
    # reflected: continue through F and on to image
    dwg.add(dwg.line((50, obj_y_tip), (r1_hit_x, r1_hit_y),
                     stroke="#E53935", stroke_width=2))    # incident
    dwg.add(dwg.line((r1_hit_x, r1_hit_y), (Fx, Py),
                     stroke="#E53935", stroke_width=2))    # reflected (to F)
    dwg.add(dwg.line((Fx, Py), (img_x - 20, img_y_tip + 5),
                     stroke="#E53935", stroke_width=2))    # continues past image

    # ─────────────────────────────────────────────────────────────
    # RAY 2 (green): From object tip → through F → hits mirror
    #   → reflects PARALLEL to principal axis → meets Ray 1 at image
    # Line through obj tip (obj_x, obj_y_tip) and F (Fx, Py):
    #   slope = (Py - obj_y_tip)/(Fx - obj_x)
    #   At x=Px: y_hit = obj_y_tip + slope*(Px - obj_x)
    # Reflected: horizontal at y=y_hit going left until x=img_x
    # ─────────────────────────────────────────────────────────────
    r2_slope = (Py - obj_y_tip) / (Fx - obj_x)   # 100/300 ≈ 0.333
    r2_hit_y = round(obj_y_tip + r2_slope * (Px - obj_x))  # y where ray hits mirror
    # Extended start of ray 2 (before object, at x=50)
    r2_start_y = round(obj_y_tip - r2_slope * (obj_x - 50))
    dwg.add(dwg.line((50, r2_start_y), (Px, r2_hit_y),
                     stroke="#2E7D32", stroke_width=2))    # incident through F
    dwg.add(dwg.line((Px, r2_hit_y), (img_x - 20, r2_hit_y),
                     stroke="#2E7D32", stroke_width=2))    # reflected parallel to axis

    # ── Image arrow (purple, inverted) ────────────────────────────
    dwg.add(dwg.line((img_x, Py), (img_x, img_y_tip),
                     stroke="#6A1B9A", stroke_width=3))
    dwg.add(dwg.polygon(
        [(img_x, img_y_tip + 10), (img_x - 6, img_y_tip - 8), (img_x + 6, img_y_tip - 8)],
        fill="#6A1B9A"))
    dwg.add(dwg.text("Image", insert=(img_x + 6, img_y_tip + 14),
                     font_size=12, fill="#6A1B9A", font_family="Arial"))

    # ── Legend ────────────────────────────────────────────────────
    for i, (col, lbl) in enumerate([
        ("#E53935", "Ray 1: parallel to axis → reflects through F"),
        ("#2E7D32", "Ray 2: through F → reflects parallel to axis"),
        ("#FF6F00", "Object (beyond C)"),
        ("#6A1B9A", "Image (real, inverted, diminished)"),
    ]):
        y = 345 + i * 18
        dwg.add(dwg.line((30, y), (60, y), stroke=col, stroke_width=2))
        dwg.add(dwg.text(lbl, insert=(65, y + 4),
                         font_size=11, fill="#333", font_family="Arial"))

    dwg.save()
    print(f"✅ Saved: {output_path}")


def render_circuit(output_path):
    dwg = svgwrite.Drawing(output_path, size=(640, 420))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    dwg.add(dwg.text("Simple Electric Circuit",
                     insert=(320, 28), text_anchor="middle",
                     font_size=18, font_weight="bold",
                     font_family="Arial", fill="#1a1a2e"))

    # Wires — rectangle loop
    wire_color = "#333333"
    wire_w = 3
    # Top
    dwg.add(dwg.line((100, 100), (540, 100), stroke=wire_color, stroke_width=wire_w))
    # Bottom
    dwg.add(dwg.line((100, 320), (540, 320), stroke=wire_color, stroke_width=wire_w))
    # Left
    dwg.add(dwg.line((100, 100), (100, 320), stroke=wire_color, stroke_width=wire_w))
    # Right
    dwg.add(dwg.line((540, 100), (540, 320), stroke=wire_color, stroke_width=wire_w))

    # Battery (left side) — long + short lines
    for y, thick in [(175, True), (195, False), (220, True), (240, False), (265, True)]:
        w = 30 if thick else 18
        dwg.add(dwg.line((100 - w // 2, y), (100 + w // 2, y),
                         stroke="#E53935", stroke_width=4 if thick else 2))
    dwg.add(dwg.text("Battery", insert=(20, 225),
                     font_size=12, fill="#E53935", font_family="Arial"))
    dwg.add(dwg.text("6V", insert=(28, 242),
                     font_size=11, fill="#E53935", font_family="Arial"))
    dwg.add(dwg.text("+", insert=(108, 178),
                     font_size=14, fill="#E53935", font_family="Arial"))
    dwg.add(dwg.text("−", insert=(108, 275),
                     font_size=16, fill="#E53935", font_family="Arial"))

    # Bulb (top wire, center)
    bx, by = 320, 100
    dwg.add(dwg.circle(center=(bx, by), r=22,
                       fill="#FFF9C4", stroke="#F57F17", stroke_width=3))
    dwg.add(dwg.line((bx - 10, by + 10), (bx + 10, by - 10),
                     stroke="#F57F17", stroke_width=2))
    dwg.add(dwg.line((bx - 10, by - 10), (bx + 10, by + 10),
                     stroke="#F57F17", stroke_width=2))
    dwg.add(dwg.text("Bulb", insert=(305, 68),
                     font_size=12, fill="#F57F17", font_family="Arial"))

    # Resistor (right side)
    rx, ry = 540, 210
    dwg.add(dwg.rect(insert=(rx - 18, ry - 40), size=(36, 80),
                     fill="#E8EAF6", stroke="#3949AB", stroke_width=3, rx=4))
    for i in range(4):
        y = ry - 30 + i * 18
        dwg.add(dwg.line((rx - 14, y), (rx + 14, y),
                         stroke="#3949AB", stroke_width=1.5))
    dwg.add(dwg.text("Resistor", insert=(548, 205),
                     font_size=12, fill="#3949AB", font_family="Arial"))
    dwg.add(dwg.text("10 Ω", insert=(550, 222),
                     font_size=11, fill="#3949AB", font_family="Arial"))

    # Switch (bottom wire) — CLOSED: lever connects the two contact points
    dwg.add(dwg.line((260, 320), (290, 320), stroke=wire_color, stroke_width=wire_w))
    dwg.add(dwg.line((370, 320), (400, 320), stroke=wire_color, stroke_width=wire_w))
    dwg.add(dwg.line((290, 320), (370, 320),
                     stroke=wire_color, stroke_width=wire_w))  # closed switch lever
    dwg.add(dwg.circle(center=(290, 320), r=4, fill=wire_color))
    dwg.add(dwg.circle(center=(370, 320), r=4, fill=wire_color))
    dwg.add(dwg.text("Switch (closed)", insert=(278, 345),
                     font_size=12, fill="#333", font_family="Arial"))

    # Current direction arrows on top wire (valid because switch is CLOSED)
    for x in [160, 240, 400, 470]:
        dwg.add(dwg.polygon(
            [(x + 8, 100), (x - 4, 94), (x - 4, 106)],
            fill="#555"))
    dwg.add(dwg.text("I →", insert=(195, 90),
                     font_size=12, fill="#555", font_family="Arial"))

    # Properties box
    dwg.add(dwg.rect(insert=(30, 340), size=(220, 60),
                     fill="#F3F4F6", stroke="#CCC", stroke_width=1, rx=6))
    dwg.add(dwg.text("V = 6V   |   R = 10Ω   |   I = 0.6A",
                     insert=(40, 365), font_size=11, fill="#333", font_family="Arial"))
    dwg.add(dwg.text("Circuit Type: Series",
                     insert=(40, 385), font_size=11, fill="#555", font_family="Arial"))

    dwg.save()
    print(f"✅ Saved: {output_path}")


def render_force_diagram(output_path):
    dwg = svgwrite.Drawing(output_path, size=(540, 520))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    dwg.add(dwg.text("Free Body Diagram",
                     insert=(270, 28), text_anchor="middle",
                     font_size=18, font_weight="bold",
                     font_family="Arial", fill="#1a1a2e"))

    # Ground
    dwg.add(dwg.line((60, 320), (480, 320),
                     stroke="#4E342E", stroke_width=4))
    for i in range(20):
        x = 65 + i * 22
        dwg.add(dwg.line((x, 320), (x - 8, 336),
                         stroke="#4E342E", stroke_width=1.5))
    dwg.add(dwg.text("Ground", insert=(60, 355),
                     font_size=12, fill="#4E342E", font_family="Arial"))

    # Object box
    dwg.add(dwg.rect(insert=(200, 220), size=(140, 100),
                     fill="#BBDEFB", stroke="#1565C0", stroke_width=3, rx=6))
    dwg.add(dwg.text("m = 5 kg", insert=(220, 278),
                     font_size=13, fill="#1565C0", font_family="Arial"))

    def arrow(x1, y1, x2, y2, color, label, lx, ly):
        dwg.add(dwg.line((x1, y1), (x2, y2),
                         stroke=color, stroke_width=3))
        # Arrowhead
        angle = math.atan2(y2 - y1, x2 - x1)
        ha = math.radians(25)
        hs = 12
        hx1 = x2 - hs * math.cos(angle - ha)
        hy1 = y2 - hs * math.sin(angle - ha)
        hx2 = x2 - hs * math.cos(angle + ha)
        hy2 = y2 - hs * math.sin(angle + ha)
        dwg.add(dwg.polygon([(x2, y2), (hx1, hy1), (hx2, hy2)], fill=color))
        dwg.add(dwg.text(label, insert=(lx, ly),
                         font_size=12, fill=color, font_family="Arial"))

    # Normal Force ↑
    arrow(270, 220, 270, 100, "#2E7D32", "Normal (N = 49N)", 280, 95)
    # Weight ↓
    arrow(270, 320, 270, 430, "#C62828", "Weight (mg = 49N)", 280, 445)
    # Applied Force → (pushes RIGHT: from left side toward object)
    arrow(80, 270, 200, 270, "#FF6F00", "Applied F = 20N", 20, 255)
    # Friction ← (opposes motion, points LEFT: from right side toward object)
    arrow(460, 270, 340, 270, "#6A1B9A", "Friction f = 14.7N", 345, 255)

    # Net force label — points RIGHT (same direction as applied force)
    dwg.add(dwg.rect(insert=(170, 370), size=(200, 36),
                     fill="#F3F4F6", stroke="#CCC", stroke_width=1, rx=6))
    dwg.add(dwg.text("Net Force = 5.3 N →",
                     insert=(185, 393), font_size=12, fill="#333", font_family="Arial"))

    dwg.save()
    print(f"✅ Saved: {output_path}")


def render_ray_optics_convex(output_path):
    """Convex lens ray diagram."""
    dwg = svgwrite.Drawing(output_path, size=(700, 400))
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    dwg.add(dwg.text("Convex Lens — Ray Diagram",
                     insert=(350, 28), text_anchor="middle",
                     font_size=18, font_weight="bold",
                     font_family="Arial", fill="#1a1a2e"))

    # Principal axis
    dwg.add(dwg.line((30, 210), (670, 210),
                     stroke="#555", stroke_width=1.5,
                     **{"stroke-dasharray": "6,4"}))

    # Lens (vertical line with arrowheads at both ends)
    dwg.add(dwg.line((350, 80), (350, 340),
                     stroke="#1565C0", stroke_width=3))
    dwg.add(dwg.polygon([(350, 70), (343, 90), (357, 90)], fill="#1565C0"))
    dwg.add(dwg.polygon([(350, 350), (343, 330), (357, 330)], fill="#1565C0"))
    dwg.add(dwg.text("Convex Lens", insert=(355, 370),
                     font_size=12, fill="#1565C0", font_family="Arial"))

    # Focal points F and F'
    for x, lbl in [(210, "F"), (490, "F'")]:
        dwg.add(dwg.circle(center=(x, 210), r=4, fill="#333"))
        dwg.add(dwg.text(lbl, insert=(x - 5, 228),
                         font_size=13, font_family="Arial", fill="#333"))

    # Object
    dwg.add(dwg.line((150, 210), (150, 120),
                     stroke="#FF6F00", stroke_width=3))
    dwg.add(dwg.polygon([(150, 110), (144, 128), (156, 128)], fill="#FF6F00"))
    dwg.add(dwg.text("Object", insert=(100, 118),
                     font_size=12, fill="#FF6F00", font_family="Arial"))

    # Ray 1 — parallel → through F' (red)
    dwg.add(dwg.line((100, 120), (350, 120), stroke="#E53935", stroke_width=2))
    dwg.add(dwg.line((350, 120), (490, 210), stroke="#E53935", stroke_width=2))
    dwg.add(dwg.line((490, 210), (560, 265), stroke="#E53935", stroke_width=2))

    # Ray 2 — through centre, no bending (green)
    dwg.add(dwg.line((100, 120), (560, 265), stroke="#2E7D32", stroke_width=2))

    # Image
    dwg.add(dwg.line((560, 210), (560, 265),
                     stroke="#6A1B9A", stroke_width=3))
    dwg.add(dwg.polygon([(560, 275), (554, 257), (566, 257)], fill="#6A1B9A"))
    dwg.add(dwg.text("Image", insert=(565, 285),
                     font_size=12, fill="#6A1B9A", font_family="Arial"))

    dwg.save()
    print(f"✅ Saved: {output_path}")


# ═══════════════════════════════════════════════════════════════
# SECTION 3 — TEMPLATE-BASED RENDERER (reads physics JSON)
# ═══════════════════════════════════════════════════════════════

def render_from_template(template_path: str, output_path: str):
    """Render physics diagram from JSON template."""
    with open(template_path) as f:
        template = json.load(f)

    diagram = template["diagram"]

    if diagram == "concave_mirror":
        render_concave_mirror(output_path)
    elif diagram == "circuit":
        render_circuit(output_path)
    elif diagram == "force_diagram":
        render_force_diagram(output_path)
    else:
        print(f"❌ No renderer found for: {diagram}")


# ═══════════════════════════════════════════════════════════════
# TEST RUNNER
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs("output/physics", exist_ok=True)

    print("── Graphs ──────────────────────────────")

    # Distance-time (uniform motion)
    render_distance_time_graph(
        times=[0, 1, 2, 3, 4, 5],
        distances=[0, 10, 20, 30, 40, 50],
        output_path="output/physics/distance_time.png",
        title="Distance-Time Graph (Uniform Motion)"
    )

    # Velocity-time (uniform acceleration)
    render_velocity_time_graph(
        times=[0, 1, 2, 3, 4, 5],
        velocities=[0, 4, 8, 12, 16, 20],
        output_path="output/physics/velocity_time.png",
        title="Velocity-Time Graph (Uniform Acceleration)"
    )

    # Wave diagram
    render_wave_diagram(
        output_path="output/physics/wave_diagram.png"
    )

    # Combined motion graphs
    render_motion_graphs(
        output_path="output/physics/motion_graphs.png"
    )

    print("\n── Structural Diagrams ─────────────────")

    render_concave_mirror("output/physics/concave_mirror.svg")
    render_circuit("output/physics/circuit.svg")
    render_force_diagram("output/physics/force_diagram.svg")
    render_ray_optics_convex("output/physics/convex_lens.svg")

    print("\nDone. Open output/physics/ to view all diagrams.")