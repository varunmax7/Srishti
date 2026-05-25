import json

data = {
    "diagram": "female_reproductive",
    "type": "biology",
    "title": "Female Reproductive System",
    "canvas": {"width": 1000, "height": 700},
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def ellipse(id, name, cx, cy, rx, ry, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#111111", w=2):
    ellipse(id, name, cx, cy, r, r, fill, stroke, w)

# Centre the diagram: uterus body centred at (500, 350)

# ─── 1. BROAD LIGAMENT (background support tissue) ────────────────
path("broad_ligament", "Broad Ligament",
     "M 350 250 C 300 200 250 250 250 300 C 250 380 300 420 350 420 "
     "L 650 420 C 700 420 750 380 750 300 C 750 250 700 200 650 250 Z",
     "#FDE8E8", "#D4A0A0", 1)

# ─── 2. UTERUS (pear/triangular body) ─────────────────────────────
# Outer wall (myometrium)
path("myometrium", "Myometrium",
     "M 420 230 "
     "C 400 230 370 260 370 310 "
     "C 370 380 400 430 430 450 "
     "L 500 480 "
     "L 570 450 "
     "C 600 430 630 380 630 310 "
     "C 630 260 600 230 580 230 Z",
     "#F8BBD0", "#AD1457", 3)

# Inner lining (endometrium)
path("endometrium", "Endometrium",
     "M 440 260 "
     "C 430 265 410 290 410 320 "
     "C 410 370 430 410 450 430 "
     "L 500 450 "
     "L 550 430 "
     "C 570 410 590 370 590 320 "
     "C 590 290 570 265 560 260 Z",
     "#FCE4EC", "#E91E63", 2)

# Uterine cavity (triangular space)
path("uterine_cavity", "Uterine Cavity",
     "M 470 280 L 500 420 L 530 280 Z",
     "#FFFFFF", "#C2185B", 2)

# ─── 3. CERVIX ────────────────────────────────────────────────────
path("cervix", "Cervix",
     "M 475 475 "
     "C 470 490 468 510 470 530 "
     "C 472 545 485 555 500 555 "
     "C 515 555 528 545 530 530 "
     "C 532 510 530 490 525 475 Z",
     "#EF9A9A", "#C62828", 2)

# Cervical os (opening)
ellipse("cervical_os", "Cervical Os", 500, 545, 8, 4, "#FFFFFF", "#C62828", 2)

# ─── 4. VAGINA ────────────────────────────────────────────────────
path("vagina", "Vagina",
     "M 480 555 "
     "L 475 620 L 470 680 "
     "L 530 680 L 525 620 "
     "L 520 555 Z",
     "#FFCDD2", "#E53935", 2)

# Vaginal rugae (folds)
path("rugae_1", "Rugae", "M 478 580 Q 500 575 522 580", "none", "#E57373", 1)
path("rugae_2", "Rugae", "M 476 610 Q 500 605 524 610", "none", "#E57373", 1)
path("rugae_3", "Rugae", "M 474 640 Q 500 635 526 640", "none", "#E57373", 1)
path("rugae_4", "Rugae", "M 472 665 Q 500 660 528 665", "none", "#E57373", 1)

# ─── 5. FALLOPIAN TUBES ──────────────────────────────────────────
# Left fallopian tube (curves upward and outward)
path("fallopian_left", "Fallopian Tube",
     "M 420 250 "
     "C 400 240 370 220 340 210 "
     "C 310 200 280 200 260 210 "
     "C 240 220 225 240 220 260",
     "none", "#AD1457", 3)

# Left tube lumen (inner)
path("fallopian_left_lumen", "Tube Lumen",
     "M 420 255 "
     "C 400 245 370 228 340 218 "
     "C 310 208 280 208 262 218 "
     "C 245 225 232 242 228 258",
     "none", "#F48FB1", 2)

# Right fallopian tube
path("fallopian_right", "Fallopian Tube",
     "M 580 250 "
     "C 600 240 630 220 660 210 "
     "C 690 200 720 200 740 210 "
     "C 760 220 775 240 780 260",
     "none", "#AD1457", 3)

# Right tube lumen
path("fallopian_right_lumen", "Tube Lumen",
     "M 580 255 "
     "C 600 245 630 228 660 218 "
     "C 690 208 720 208 738 218 "
     "C 755 225 768 242 772 258",
     "none", "#F48FB1", 2)

# ─── 6. FIMBRIAE (finger-like projections at tube ends) ──────────
# Left fimbriae
for i, (dx, dy, angle) in enumerate([
    (-8, -15, 0), (-15, -8, 1), (-18, 2, 2), (-15, 12, 3), (-8, 18, 4), (0, 20, 5)
]):
    bx, by = 220 + dx, 260 + dy
    path(f"fimbria_l_{i}", "Fimbriae",
         f"M 220 260 C {220+dx//2} {260+dy//2} {bx} {by} {bx+dx//3} {by+dy//3}",
         "none", "#AD1457", 2)

# Right fimbriae
for i, (dx, dy) in enumerate([
    (8, -15), (15, -8), (18, 2), (15, 12), (8, 18), (0, 20)
]):
    bx, by = 780 + dx, 260 + dy
    path(f"fimbria_r_{i}", "Fimbriae",
         f"M 780 260 C {780+dx//2} {260+dy//2} {bx} {by} {bx+dx//3} {by+dy//3}",
         "none", "#AD1457", 2)

# ─── 7. OVARIES ──────────────────────────────────────────────────
# Left ovary (almond shape)
ellipse("ovary_left", "Ovary", 210, 310, 40, 25, "#CE93D8", "#6A1B9A", 3)

# Follicles inside left ovary
circle("follicle_l1", "Follicle", 195, 300, 6, "#E1BEE7", "#8E24AA", 1)
circle("follicle_l2", "Follicle", 215, 295, 8, "#E1BEE7", "#8E24AA", 1)
circle("follicle_l3", "Follicle", 225, 315, 5, "#E1BEE7", "#8E24AA", 1)
circle("follicle_l4", "Follicle", 200, 320, 7, "#E1BEE7", "#8E24AA", 1)

# Right ovary
ellipse("ovary_right", "Ovary", 790, 310, 40, 25, "#CE93D8", "#6A1B9A", 3)

# Follicles inside right ovary
circle("follicle_r1", "Follicle", 775, 300, 6, "#E1BEE7", "#8E24AA", 1)
circle("follicle_r2", "Follicle", 795, 295, 8, "#E1BEE7", "#8E24AA", 1)
circle("follicle_r3", "Follicle", 805, 315, 5, "#E1BEE7", "#8E24AA", 1)
circle("follicle_r4", "Follicle", 780, 320, 7, "#E1BEE7", "#8E24AA", 1)

# ─── 8. OVARIAN LIGAMENT (connects ovary to uterus) ─────────────
path("ovarian_lig_l", "Ovarian Ligament",
     "M 250 310 C 280 310 320 290 370 280",
     "none", "#AD1457", 2)
path("ovarian_lig_r", "Ovarian Ligament",
     "M 750 310 C 720 310 680 290 630 280",
     "none", "#AD1457", 2)

# ─── 9. ROUND LIGAMENT ──────────────────────────────────────────
path("round_lig_l", "Round Ligament",
     "M 400 260 C 350 250 300 280 270 340",
     "none", "#999", 2)
path("round_lig_r", "Round Ligament",
     "M 600 260 C 650 250 700 280 730 340",
     "none", "#999", 2)

# ─── LABELS ──────────────────────────────────────────────────────
# lx,ly = text box position; tx,ty = arrow target on structure
data["labels"] = [
    # LEFT SIDE labels
    {"part_id": "ovary_left",      "text": "Ovary",              "lx": 30, "ly": 260, "tx": 210, "ty": 310},
    {"part_id": "fimbria_l_0",     "text": "Fimbriae",           "lx": 30, "ly": 210, "tx": 215, "ty": 255},
    {"part_id": "fallopian_left",  "text": "Fallopian Tube",     "lx": 30, "ly": 160, "tx": 340, "ty": 215},
    {"part_id": "ovarian_lig_l",   "text": "Ovarian Ligament",   "lx": 30, "ly": 310, "tx": 300, "ty": 300},
    {"part_id": "vagina",          "text": "Vagina",             "lx": 30, "ly": 620, "tx": 475, "ty": 640},
    {"part_id": "cervix",          "text": "Cervix",             "lx": 30, "ly": 530, "tx": 472, "ty": 530},

    # RIGHT SIDE labels
    {"part_id": "myometrium",      "text": "Myometrium",         "lx": 750, "ly": 240, "tx": 630, "ty": 310},
    {"part_id": "endometrium",     "text": "Endometrium",        "lx": 750, "ly": 290, "tx": 590, "ty": 320},
    {"part_id": "uterine_cavity",  "text": "Uterine Cavity",    "lx": 750, "ly": 340, "tx": 530, "ty": 350},
    {"part_id": "fallopian_right", "text": "Fallopian Tube",     "lx": 750, "ly": 160, "tx": 660, "ty": 215},
    {"part_id": "ovary_right",     "text": "Ovary",              "lx": 750, "ly": 390, "tx": 790, "ty": 310},
    {"part_id": "follicle_r2",     "text": "Follicles",          "lx": 750, "ly": 440, "tx": 795, "ty": 295},
    {"part_id": "cervical_os",     "text": "Cervical Os",        "lx": 750, "ly": 540, "tx": 530, "ty": 545},
    {"part_id": "broad_ligament",  "text": "Broad Ligament",     "lx": 750, "ly": 490, "tx": 680, "ty": 400},
]

with open("/Users/ramavathvarun/srishti/templates/biology/female_reproductive.json", "w") as f:
    json.dump(data, f, indent=4)

print("female_reproductive.json created successfully")
