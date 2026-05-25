import json

data = {
    "diagram": "alveoli",
    "type": "biology",
    "title": "Alveoli",
    "canvas": {
        "width": 900,
        "height": 800
    },
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#333333", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#333333", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": r, "ry": r, "color": fill, "stroke": stroke, "stroke_width": w})

# 1. Background blobs for right exterior cluster
cx, cy = 720, 600
for i, (dx, dy, r) in enumerate([
    (0, -50, 45), (45, -30, 40), (60, 20, 40), (35, 65, 40),
    (-10, 80, 45), (-55, 55, 40), (-70, 10, 40), (-45, -35, 45),
    (-10, -10, 45), (20, 20, 45), (-10, 40, 45)
]):
    circle(f"r_ext_{i}", "Alveolar Sac", cx+dx, cy+dy, r, "#F9F9F9", "#111", 2)

# 2. Main cross-section cluster (Left)
# First draw outer bubbles
cx, cy = 350, 450
for i, (dx, dy, r) in enumerate([
    (0, -70, 50), (60, -50, 50), (90, 0, 50), (70, 60, 50),
    (10, 90, 50), (-60, 60, 50), (-90, 0, 50), (-60, -50, 50),
    (-20, -20, 50), (30, 20, 50), (-20, 40, 50)
]):
    circle(f"l_ext_{i}", "Alveolar Sac", cx+dx, cy+dy, r, "#F9F9F9", "#111", 2)

# Now draw the thick white overlay for the cross section
# This is a large white blob that covers the inner area
path("l_cs_base", "Cross Section", 
     "M 280 400 C 320 350 400 350 430 400 C 470 450 450 520 400 540 C 350 560 280 540 260 480 C 240 430 250 410 280 400 Z",
     "#FFFFFF", "none", 0)

# Inner cavities (grey)
for i, (cx_c, cy_c, r) in enumerate([
    (310, 410, 25), (370, 405, 30), (410, 440, 25), 
    (400, 500, 28), (340, 510, 30), (280, 470, 25), 
    (340, 450, 22), (300, 440, 15)
]):
    circle(f"l_cav_{i}", "Alveolar Cavity", cx_c, cy_c, r, "#E0E0E0", "#111", 2)
    # A small highlight/shadow in the cavity
    path(f"l_cav_sh_{i}", "Shadow", f"M {cx_c-10} {cy_c} Q {cx_c} {cy_c-10} {cx_c+10} {cy_c}", "none", "#999", 2)

# 3. Bottom cross-section cluster
cx, cy = 520, 620
for i, (dx, dy, r) in enumerate([
    (0, -60, 45), (50, -40, 45), (70, 10, 45), (40, 60, 45),
    (-10, 70, 45), (-60, 40, 45), (-70, -10, 45), (-40, -50, 45),
    (-10, -10, 45), (20, 20, 45), (-10, 30, 45)
]):
    circle(f"b_ext_{i}", "Alveolar Sac", cx+dx, cy+dy, r, "#F9F9F9", "#111", 2)

# Overlay
path("b_cs_base", "Cross Section", 
     "M 470 580 C 500 550 560 550 580 580 C 600 620 580 680 540 690 C 490 700 450 670 440 630 C 430 590 450 580 470 580 Z",
     "#FFFFFF", "none", 0)

# Cavities
for i, (cx_c, cy_c, r) in enumerate([
    (480, 580, 20), (530, 570, 25), (570, 610, 22), 
    (560, 660, 20), (510, 670, 25), (460, 640, 20), 
    (510, 620, 25)
]):
    circle(f"b_cav_{i}", "Alveolar Cavity", cx_c, cy_c, r, "#E0E0E0", "#111", 2)
    path(f"b_cav_sh_{i}", "Shadow", f"M {cx_c-8} {cy_c} Q {cx_c} {cy_c-8} {cx_c+8} {cy_c}", "none", "#999", 2)

# 4. Bronchiole tubes
# Main tube from top right
path("tube_main_outline", "Bronchiole",
     "M 700 150 C 700 350 650 450 580 500 L 630 520 C 720 450 750 350 750 150 Z",
     "#F4F4F4", "#111", 2)

# Branch to left cluster
path("tube_branch_l", "Alveolar Duct",
     "M 590 480 C 520 480 450 480 410 440 L 420 410 C 460 450 520 450 600 450 Z",
     "#F4F4F4", "#111", 2)

# Branch to bottom cluster
path("tube_branch_b", "Alveolar Duct",
     "M 600 500 C 580 540 550 560 530 570 L 510 550 C 530 540 560 520 580 480 Z",
     "#F4F4F4", "#111", 2)

# Open end of right tube (showing it's cut)
path("tube_main_cut", "Opening",
     "M 700 150 Q 725 160 750 150",
     "none", "#111", 2)

# 5. Some open cutaways on the tubes like the image
circle("tube_pore_1", "Pore", 550, 465, 8, "#E0E0E0", "#111", 1)
circle("tube_pore_2", "Pore", 470, 440, 6, "#E0E0E0", "#111", 1)
circle("tube_pore_3", "Pore", 540, 520, 7, "#E0E0E0", "#111", 1)

# Labels
data["labels"] = [
    {
        "part_id": "tube_main_outline",
        "text": "Terminal Bronchiole",
        "lx": 730, "ly": 250,
        "tx": 820, "ty": 200
    },
    {
        "part_id": "tube_branch_l",
        "text": "Alveolar Duct",
        "lx": 500, "ly": 450,
        "tx": 550, "ty": 380
    },
    {
        "part_id": "r_ext_0",
        "text": "Alveoli (Exterior View)",
        "lx": 760, "ly": 600,
        "tx": 820, "ty": 650
    },
    {
        "part_id": "l_cav_0",
        "text": "Alveolar Sac (Cross-Section)",
        "lx": 310, "ly": 410,
        "tx": 150, "ty": 350
    },
    {
        "part_id": "l_cav_3",
        "text": "Alveolar Cavity",
        "lx": 400, "ly": 500,
        "tx": 200, "ty": 550
    }
]

with open("/Users/ramavathvarun/srishti/templates/biology/alveoli.json", "w") as f:
    json.dump(data, f, indent=4)
