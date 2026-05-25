import json

data = {
    "diagram": "female_endocrine",
    "type": "biology",
    "title": "Female Endocrine System",
    "canvas": {"width": 600, "height": 900},
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def ellipse(id, name, cx, cy, rx, ry, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": r, "ry": r, "color": fill, "stroke": stroke, "stroke_width": w})

# ─── BODY SILHOUETTE ────────────────────────────────────────────────────────
# Head
circle("head", "Head", 300, 75, 60, "#FDDBB4", "#C8956C", 3)

# Neck
path("neck", "Neck",
     "M 275 128 L 275 170 L 325 170 L 325 128 Z",
     "#FDDBB4", "#C8956C", 2)

# Torso (female shape)
path("torso", "Torso",
     "M 210 170 "        # left shoulder
     "C 190 200 180 240 185 290 "   # left side upper
     "C 182 330 188 360 195 390 "   # waist in
     "C 188 420 185 450 195 490 "   # hip out
     "C 200 520 210 540 220 560 "   # thigh start
     "L 265 560 "
     "L 265 490 "        # inner thigh
     "C 260 460 258 430 260 400 "   # inner body
     "L 340 400 "
     "C 342 430 340 460 335 490 "
     "L 335 560 "
     "L 380 560 "
     "C 390 540 400 520 405 490 "
     "C 415 450 412 420 405 390 "
     "C 412 360 418 330 415 290 "
     "C 420 240 410 200 390 170 Z", # right shoulder
     "#FDDBB4", "#C8956C", 3)

# Arms (simple)
path("left_arm", "Left Arm",
     "M 210 170 C 185 200 170 280 175 360 L 195 360 C 192 280 205 200 230 175 Z",
     "#FDDBB4", "#C8956C", 2)
path("right_arm", "Right Arm",
     "M 390 170 C 415 200 430 280 425 360 L 405 360 C 408 280 395 200 370 175 Z",
     "#FDDBB4", "#C8956C", 2)

# Legs
path("left_leg", "Left Leg",
     "M 220 560 L 220 800 L 265 800 L 265 560 Z",
     "#FDDBB4", "#C8956C", 2)
path("right_leg", "Right Leg",
     "M 335 560 L 335 800 L 380 800 L 380 560 Z",
     "#FDDBB4", "#C8956C", 2)

# ─── GLANDS ─────────────────────────────────────────────────────────────────

# 1. Pineal Gland (deep in brain, top-centre)
circle("pineal_gland", "Pineal Gland", 300, 60, 7, "#CE93D8", "#7B1FA2", 2)

# 2. Hypothalamus (base of brain)
ellipse("hypothalamus", "Hypothalamus", 300, 82, 18, 9, "#9FA8DA", "#3949AB", 2)

# 3. Pituitary Gland (hangs below hypothalamus)
circle("pituitary_gland", "Pituitary Gland", 300, 100, 8, "#EF9A9A", "#C62828", 2)

# 4. Thyroid Gland (butterfly shape at base of neck)
path("thyroid_left", "Thyroid Gland",
     "M 275 158 C 263 155 255 162 257 172 C 259 182 270 185 280 180 C 288 175 285 162 275 158 Z",
     "#80CBC4", "#00695C", 2)
path("thyroid_right", "Thyroid Gland",
     "M 325 158 C 337 155 345 162 343 172 C 341 182 330 185 320 180 C 312 175 315 162 325 158 Z",
     "#80CBC4", "#00695C", 2)
path("thyroid_isthmus", "Thyroid Isthmus",
     "M 280 170 L 320 170 L 320 175 L 280 175 Z",
     "#80CBC4", "#00695C", 1)

# 5. Parathyroid Glands (4 tiny dots behind thyroid)
circle("parathyroid_1", "Parathyroid", 268, 163, 4, "#FFE082", "#F57F17", 1)
circle("parathyroid_2", "Parathyroid", 268, 175, 4, "#FFE082", "#F57F17", 1)
circle("parathyroid_3", "Parathyroid", 332, 163, 4, "#FFE082", "#F57F17", 1)
circle("parathyroid_4", "Parathyroid", 332, 175, 4, "#FFE082", "#F57F17", 1)

# 6. Thymus (behind sternum, upper chest — two lobes)
ellipse("thymus_left", "Thymus", 288, 225, 15, 25, "#A5D6A7", "#2E7D32", 2)
ellipse("thymus_right", "Thymus", 312, 225, 15, 25, "#A5D6A7", "#2E7D32", 2)

# 7. Heart (for orientation — light outline only)
path("heart_outline", "Heart",
     "M 300 260 C 280 240 255 250 255 270 C 255 290 275 310 300 330 C 325 310 345 290 345 270 C 345 250 320 240 300 260 Z",
     "#FFCDD2", "#EF9A9A", 1)

# 8. Adrenal Glands (triangular hats on kidneys, mid-back region ~y=340)
path("adrenal_left", "Adrenal Gland",
     "M 240 330 C 230 320 225 330 230 345 C 235 355 248 355 252 345 C 256 335 248 322 240 330 Z",
     "#FFCC80", "#E65100", 2)
path("adrenal_right", "Adrenal Gland",
     "M 360 330 C 370 320 375 330 370 345 C 365 355 352 355 348 345 C 344 335 352 322 360 330 Z",
     "#FFCC80", "#E65100", 2)

# 9. Kidneys (under adrenals, for context)
ellipse("kidney_left", "Kidney", 238, 360, 18, 28, "#FFCCBC", "#BF360C", 2)
ellipse("kidney_right", "Kidney", 362, 360, 18, 28, "#FFCCBC", "#BF360C", 2)

# 10. Pancreas (horizontal, behind stomach ~y=310)
path("pancreas", "Pancreas",
     "M 255 310 C 265 305 300 305 340 308 C 350 310 355 318 345 322 C 310 325 270 325 258 320 C 252 318 252 312 255 310 Z",
     "#FFF59D", "#F9A825", 2)

# 11. Ovaries (lower abdomen, two almond shapes)
ellipse("ovary_left", "Ovary", 262, 470, 20, 15, "#F48FB1", "#AD1457", 2)
ellipse("ovary_right", "Ovary", 338, 470, 20, 15, "#F48FB1", "#AD1457", 2)

# Uterus (pear shape)
path("uterus", "Uterus",
     "M 300 445 C 280 445 268 455 268 468 C 268 490 280 505 300 508 C 320 505 332 490 332 468 C 332 455 320 445 300 445 Z",
     "#F06292", "#880E4F", 2)

# ─── LABELS ──────────────────────────────────────────────────────────────────
data["labels"] = [
    {"part_id": "pineal_gland",    "text": "Pineal Gland",        "lx": 300, "ly": 55,  "tx": 430, "ty": 30},
    {"part_id": "hypothalamus",    "text": "Hypothalamus",        "lx": 300, "ly": 82,  "tx": 430, "ty": 70},
    {"part_id": "pituitary_gland", "text": "Pituitary Gland",     "lx": 300, "ly": 100, "tx": 430, "ty": 110},
    {"part_id": "thyroid_left",    "text": "Thyroid Gland",       "lx": 266, "ly": 170, "tx": 130, "ty": 155},
    {"part_id": "parathyroid_1",   "text": "Parathyroid Glands",  "lx": 268, "ly": 163, "tx": 130, "ty": 195},
    {"part_id": "thymus_left",     "text": "Thymus",              "lx": 300, "ly": 225, "tx": 430, "ty": 200},
    {"part_id": "adrenal_left",    "text": "Adrenal Glands",      "lx": 240, "ly": 338, "tx": 130, "ty": 320},
    {"part_id": "kidney_left",     "text": "Kidneys",             "lx": 238, "ly": 360, "tx": 130, "ty": 360},
    {"part_id": "pancreas",        "text": "Pancreas",            "lx": 300, "ly": 315, "tx": 430, "ty": 295},
    {"part_id": "ovary_left",      "text": "Ovaries",             "lx": 262, "ly": 470, "tx": 130, "ty": 470},
    {"part_id": "uterus",          "text": "Uterus",              "lx": 300, "ly": 475, "tx": 430, "ty": 470},
]

with open("/Users/ramavathvarun/srishti/templates/biology/female_endocrine.json", "w") as f:
    json.dump(data, f, indent=4)

print("female_endocrine.json created successfully")
