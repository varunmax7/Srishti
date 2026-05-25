import json
import math

data = {
    "diagram": "brain_cross_section",
    "type": "biology",
    "title": "Brain Cross-Section",
    "canvas": { "width": 900, "height": 800 },
    "parts": [],
    "labels": []
}

def path(id, name, d, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "path", "d": d, "color": fill, "stroke": stroke, "stroke_width": w})

def circle(id, name, cx, cy, r, fill="#FFFFFF", stroke="#111111", w=2):
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": r, "ry": r, "color": fill, "stroke": stroke, "stroke_width": w})

def ellipse(id, name, cx, cy, rx, ry, fill="#FFFFFF", stroke="#111111", w=2, angle=0):
    # label_engine might not support rotation directly, so we just use axis-aligned
    data["parts"].append({"id": id, "name": name, "shape": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "color": fill, "stroke": stroke, "stroke_width": w})

# The brain is facing left.
# 1. Outer covering (Meninges/Skull)
# Leftmost point ~200, 500. Top ~450, 100. Rightmost ~800, 400. Bottom right ~700, 600.
p_outer = (
    "M 300 550 "
    "C 280 400 350 200 500 120 "
    "C 700 80 850 250 850 450 "
    "C 850 600 750 650 650 650 "
    "C 550 650 500 550 450 550 "
    "C 350 550 320 570 300 550 Z"
)
path("outer_layer", "Meninges", p_outer, "#FCFBE3", "#111", 3)

# 2. Outer Cortex (Cerebrum)
p_cortex = (
    "M 320 500 "
    "C 300 380 370 220 500 150 "
    "C 680 120 810 270 810 440 "
    "C 810 560 730 610 650 610 "
    "C 580 610 550 520 480 500 "
    "C 400 480 350 520 320 500 Z"
)
path("cerebrum", "Cerebrum", p_cortex, "#FCE9D8", "#111", 3)

# 3. Brain Stem and Thalamus
# Starts from middle (480, 450), goes down to 600, 800
p_stem = (
    "M 450 420 "
    "C 450 380 500 380 550 400 " # Thalamus upper
    "C 580 420 580 480 550 500 " # Midbrain
    "C 550 550 580 580 550 620 " # Pons (bulge leftwards)
    "C 580 680 650 780 650 850 " # Medulla / Spinal cord
    "L 700 850 "
    "C 700 780 620 680 620 620 "
    "C 620 580 650 520 650 480 "
    "C 650 400 600 350 500 350 "
    "C 450 350 420 380 450 420 Z"
)
path("brain_stem", "Brain Stem", p_stem, "#FCD0A1", "#111", 3)

# 4. Corpus Callosum
p_corpus = (
    "M 420 380 "
    "C 400 350 420 300 500 280 "
    "C 600 270 650 320 650 350 "
    "C 650 380 620 380 620 350 "
    "C 620 320 550 300 500 310 "
    "C 450 320 440 360 450 380 "
    "C 460 390 420 400 420 380 Z"
)
path("corpus_callosum", "Corpus Callosum", p_corpus, "#F9B8B1", "#111", 2)

# 5. Cerebellum (Leafy structure at bottom right)
p_cerebellum = (
    "M 600 500 "
    "C 650 450 750 450 780 500 "
    "C 800 550 780 620 700 650 "
    "C 650 650 600 600 580 550 "
    "C 560 520 580 500 600 500 Z"
)
path("cerebellum", "Cerebellum", p_cerebellum, "#FCD0A1", "#111", 3)

# Arbor Vitae (Tree of life inside cerebellum)
path("arbor_vitae_1", "Arbor Vitae", "M 600 550 L 680 550 L 730 520", "none", "#333", 3)
path("arbor_vitae_2", "Arbor Vitae", "M 680 550 L 730 580", "none", "#333", 3)
path("arbor_vitae_3", "Arbor Vitae", "M 650 550 L 680 500", "none", "#333", 3)
path("arbor_vitae_4", "Arbor Vitae", "M 650 550 L 680 600", "none", "#333", 3)

# 6. Cortex Folds (Gyri and Sulci)
# Let's add some squiggly lines to simulate folds
folds = [
    "M 350 450 Q 380 400 370 350 T 420 280",
    "M 400 220 Q 420 250 450 220 T 500 250",
    "M 550 180 Q 580 200 600 180 T 650 250",
    "M 700 200 Q 680 250 720 300 T 750 350",
    "M 780 400 Q 750 420 730 400 T 700 480",
    "M 380 350 Q 420 380 450 350",
    "M 450 280 Q 500 260 550 300",
    "M 600 250 Q 620 300 580 320",
    "M 650 320 Q 700 350 680 400",
    "M 330 400 Q 360 420 380 450"
]
for i, d in enumerate(folds):
    path(f"fold_{i}", "Fold", d, "none", "#111", 2)

# 7. Pituitary Gland & Olfactory bulb
# Small orange bean at front of brain stem
p_pituitary = "M 460 460 C 440 450 440 480 460 490 C 470 480 470 460 460 460 Z"
path("pituitary", "Pituitary Gland", p_pituitary, "#FA9D7A", "#111", 2)

# Olfactory area (small orange spot at front bottom of meninges)
path("olfactory", "Olfactory Bulb", "M 320 540 C 310 520 330 510 340 520 C 350 530 340 550 320 540 Z", "#FA9D7A", "#111", 2)

# Save the JSON (no labels initially, as requested for the previous one, or wait, user says "exact like that image and I should able to see it in output". The image has no labels. So I won't add labels!)
with open("/Users/ramavathvarun/srishti/templates/biology/brain_cross_section.json", "w") as f:
    json.dump(data, f, indent=4)
