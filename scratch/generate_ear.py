import json

data = {
    "diagram": "human_ear",
    "type": "biology",
    "title": "Human Ear Anatomy",
    "canvas": { "width": 900, "height": 700 },
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": r, "ry": r, "color": fill, "stroke": stroke, "stroke_width": w})

# 1. Temporal Bone (Background for the inner sections)
p_bone = (
    "M 350 50 "
    "L 850 50 L 850 650 L 600 650 "
    "C 550 550 500 450 480 450 "
    "C 450 450 420 500 350 500 "
    "C 400 450 400 350 350 350 "
    "C 450 350 500 250 450 150 "
    "C 400 100 350 100 350 50 Z"
)
path("temporal_bone", "Temporal Bone", p_bone, "#EBE3D5", "#111", 3)

# Add some spongy bone texture
for i, (cx, cy) in enumerate([
    (420, 100), (450, 120), (500, 80), (600, 100), (700, 150),
    (750, 80), (800, 180), (650, 120), (550, 70), (780, 120),
    (800, 400), (750, 450), (820, 500), (700, 550), (650, 600),
    (750, 600), (800, 620), (400, 480), (420, 450), (440, 490)
]):
    circle(f"bone_tex_{i}", "Bone Texture", cx, cy, 4, "#D3C8B8", "#B8AA9A", 1)

# 2. Pinna (Outer Ear)
p_pinna = (
    "M 150 350 "
    "C 100 200 150 50 250 50 "
    "C 350 50 350 150 300 250 "
    "C 280 290 320 280 350 280 " # Leads into ear canal
    "L 350 420 "                 # Bottom of canal entrance
    "C 320 420 280 380 250 450 " # Lobule (earlobe)
    "C 250 550 150 500 150 350 Z"
)
path("pinna_base", "Pinna", p_pinna, "#FCE3D2", "#111", 3)

# Pinna cartilage ridges
path("pinna_detail_1", "Cartilage Ridge", "M 200 120 C 150 150 150 250 200 350", "none", "#E5A988", 4)
path("pinna_detail_2", "Cartilage Ridge", "M 250 100 C 200 150 200 200 250 200 C 300 200 250 300 220 350", "none", "#E5A988", 3)
path("pinna_detail_3", "Cartilage Ridge", "M 300 250 C 270 280 270 320 300 350", "none", "#E5A988", 3)

# 3. Ear Canal (External Auditory Meatus)
p_canal = (
    "M 350 280 "
    "C 400 280 450 310 500 310 "
    "L 500 370 "
    "C 450 370 400 420 350 420 "
    "C 380 380 380 320 350 280 Z"
)
path("ear_canal", "Ear Canal", p_canal, "#E5A988", "#111", 2)

# 4. Middle Ear Cavity
p_middle_ear = (
    "M 500 310 "
    "C 520 250 580 250 580 320 "
    "C 580 380 540 400 540 420 "
    "L 500 420 "
    "C 520 380 520 350 500 310 Z"
)
path("middle_ear_cavity", "Middle Ear Cavity", p_middle_ear, "#F9F2F2", "#111", 2)

# 5. Eustachian Tube
p_eustachian = (
    "M 540 420 "
    "C 550 450 600 550 650 650 "
    "L 680 650 "
    "C 620 530 580 480 580 420 Z" # Connects back to middle ear
)
path("eustachian_tube", "Eustachian Tube", p_eustachian, "#F9F2F2", "#111", 2)

# 6. Tympanic Membrane (Eardrum)
path("eardrum", "Tympanic Membrane", "M 500 310 Q 515 340 500 370 Q 495 340 500 310 Z", "#B2DFDB", "#111", 2)

# 7. Ossicles (Malleus, Incus, Stapes)
# Malleus (Hammer) - attached to eardrum
path("malleus", "Malleus", "M 505 340 L 525 280 L 540 280 L 530 310 L 505 340 Z", "#E0E0E0", "#111", 2)
# Incus (Anvil)
path("incus", "Incus", "M 535 280 C 560 270 560 300 550 310 L 540 330 L 530 310 Z", "#E0E0E0", "#111", 2)
# Stapes (Stirrup)
path("stapes", "Stapes", "M 540 330 L 560 320 L 570 330 L 560 340 Z", "none", "#111", 3)
path("stapes_base", "Stapes Footplate", "M 565 315 L 575 345", "none", "#111", 4)

# 8. Inner Ear
# Cochlea (Snail shell)
p_cochlea = (
    "M 570 330 "
    "C 600 400 680 380 660 320 "
    "C 640 260 580 300 600 340 "
    "C 620 370 650 340 630 310 "
    "C 610 290 600 320 620 330 "
)
path("cochlea", "Cochlea", p_cochlea, "#D1C4E9", "#111", 3)

# Semicircular Canals
# Base connection point
path("canal_base", "Vestibule", "M 570 330 C 560 280 600 270 620 300", "#D1C4E9", "none", 0)

# Canal 1 (Superior)
path("sc_canal_1_out", "Canal Outline", "M 570 280 C 550 180 650 180 620 280", "none", "#111", 12)
path("sc_canal_1_in", "Canal Inner", "M 570 280 C 550 180 650 180 620 280", "none", "#D1C4E9", 8)

# Canal 2 (Posterior)
path("sc_canal_2_out", "Canal Outline", "M 590 270 C 650 200 700 250 620 300", "none", "#111", 12)
path("sc_canal_2_in", "Canal Inner", "M 590 270 C 650 200 700 250 620 300", "none", "#D1C4E9", 8)

# Canal 3 (Lateral)
path("sc_canal_3_out", "Canal Outline", "M 575 300 C 600 240 680 250 630 320", "none", "#111", 12)
path("sc_canal_3_in", "Canal Inner", "M 575 300 C 600 240 680 250 630 320", "none", "#D1C4E9", 8)

# 9. Auditory Nerve
p_nerve = (
    "M 650 330 "
    "C 700 350 750 320 800 330 "
    "L 800 370 "
    "C 750 360 700 380 650 360 Z"
)
path("auditory_nerve", "Auditory Nerve", p_nerve, "#FFF59D", "#111", 2)

# Write to file without labels as requested
with open("/Users/ramavathvarun/srishti/templates/biology/human_ear.json", "w") as f:
    json.dump(data, f, indent=4)
