import json

data = {
    "diagram": "male_reproductive",
    "type": "biology",
    "title": "Male Reproductive System (Frontal View)",
    "canvas": {"width": 1000, "height": 800},
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def ellipse(id, name, cx, cy, rx, ry, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#111111", w=2):
    ellipse(id, name, cx, cy, r, r, fill, stroke, w)

# ─── 1. BLADDER (context) ────────────────────────────────────────
ellipse("bladder", "Urinary Bladder", 500, 250, 70, 50, "#FFCCBC", "#BF360C", 2)

# ─── 2. SEMINAL VESICLES ─────────────────────────────────────────
path("seminal_vesicle_left", "Seminal Vesicle",
     "M 430 250 C 400 230 380 270 410 300 C 420 310 440 280 445 280 Z",
     "#FFF59D", "#F9A825", 2)
path("seminal_vesicle_right", "Seminal Vesicle",
     "M 570 250 C 600 230 620 270 590 300 C 580 310 560 280 555 280 Z",
     "#FFF59D", "#F9A825", 2)

# ─── 3. PROSTATE GLAND ───────────────────────────────────────────
ellipse("prostate", "Prostate Gland", 500, 320, 45, 35, "#E1BEE7", "#6A1B9A", 2)

# ─── 4. BULBOURETHRAL GLANDS ─────────────────────────────────────
circle("bulbourethral_left", "Bulbourethral Gland", 480, 370, 6, "#C5E1A5", "#558B2F", 2)
circle("bulbourethral_right", "Bulbourethral Gland", 520, 370, 6, "#C5E1A5", "#558B2F", 2)

# ─── 5. URETHRA ──────────────────────────────────────────────────
path("urethra", "Urethra",
     "M 500 295 L 500 620",
     "none", "#F44336", 4)

# ─── 6. PENIS ────────────────────────────────────────────────────
# Corpus cavernosum and spongiosum silhouette
path("penis", "Penis",
     "M 470 380 C 465 450 470 550 480 600 C 485 625 515 625 520 600 C 530 550 535 450 530 380 Z",
     "#F8BBD0", "#AD1457", 2)
# Glans penis
path("glans_penis", "Glans Penis",
     "M 475 600 C 460 620 485 650 500 650 C 515 650 540 620 525 600 Z",
     "#F48FB1", "#880E4F", 2)

# ─── 7. SCROTUM ──────────────────────────────────────────────────
path("scrotum", "Scrotum",
     "M 460 450 C 370 480 380 640 430 660 C 480 670 500 650 500 650 C 500 650 520 670 570 660 C 620 640 630 480 540 450 Z",
     "#FDDBB4", "#C8956C", 2)

# ─── 8. TESTES ───────────────────────────────────────────────────
ellipse("testis_left", "Testis", 430, 580, 35, 50, "#CE93D8", "#4A148C", 2)
ellipse("testis_right", "Testis", 570, 580, 35, 50, "#CE93D8", "#4A148C", 2)

# ─── 9. EPIDIDYMIS ───────────────────────────────────────────────
path("epididymis_left", "Epididymis",
     "M 400 580 C 385 530 420 510 440 520 C 460 530 460 550 460 550",
     "none", "#4DB6AC", 8)
path("epididymis_right", "Epididymis",
     "M 600 580 C 615 530 580 510 560 520 C 540 530 540 550 540 550",
     "none", "#4DB6AC", 8)

# ─── 10. VAS DEFERENS ────────────────────────────────────────────
path("vas_deferens_left", "Vas Deferens",
     "M 440 520 C 440 450 350 400 350 300 C 350 200 450 200 480 280",
     "none", "#FFB74D", 3)
path("vas_deferens_right", "Vas Deferens",
     "M 560 520 C 560 450 650 400 650 300 C 650 200 550 200 520 280",
     "none", "#FFB74D", 3)

# ─── LABELS ──────────────────────────────────────────────────────
# lx, ly: text box in margins
# tx, ty: arrow tip pointing to part
data["labels"] = [
    # LEFT SIDE
    {"part_id": "bladder",            "text": "Urinary Bladder",     "lx": 50, "ly": 250, "tx": 450, "ty": 250},
    {"part_id": "vas_deferens_left",  "text": "Vas Deferens",        "lx": 50, "ly": 300, "tx": 350, "ty": 300},
    {"part_id": "penis",              "text": "Penis",               "lx": 50, "ly": 450, "tx": 472, "ty": 450},
    {"part_id": "urethra",            "text": "Urethra",             "lx": 50, "ly": 520, "tx": 500, "ty": 520},
    {"part_id": "glans_penis",        "text": "Glans Penis",         "lx": 50, "ly": 620, "tx": 485, "ty": 620},
    
    # RIGHT SIDE
    {"part_id": "seminal_vesicle_right", "text": "Seminal Vesicle",  "lx": 800, "ly": 260, "tx": 580, "ty": 270},
    {"part_id": "prostate",           "text": "Prostate Gland",      "lx": 800, "ly": 320, "tx": 540, "ty": 320},
    {"part_id": "bulbourethral_right", "text": "Bulbourethral Gland","lx": 800, "ly": 370, "tx": 525, "ty": 370},
    {"part_id": "epididymis_right",   "text": "Epididymis",          "lx": 800, "ly": 520, "tx": 585, "ty": 525},
    {"part_id": "testis_right",       "text": "Testis",              "lx": 800, "ly": 580, "tx": 590, "ty": 580},
    {"part_id": "scrotum",            "text": "Scrotum",             "lx": 800, "ly": 650, "tx": 550, "ty": 655},
]

with open("/Users/ramavathvarun/srishti/templates/biology/male_reproductive.json", "w") as f:
    json.dump(data, f, indent=4)

print("male_reproductive.json created successfully")
