# 🎓 Srishti Shiksha — Scientific Diagram Export Engine

> **Srishti Shiksha** is a Python-based educational diagram generation system that produces high-quality, scientifically accurate diagrams for Biology, Chemistry, and Physics — ready for use in textbooks, presentations, and educational applications.

---

## 📸 Sample Outputs

| Biology | Chemistry | Physics |
|---|---|---|
| Animal Cell | Benzene | Concave Mirror |
| Plant Cell | Glucose | Electric Circuit |
| Human Heart | Methane | Force Diagram |
| Digestive System | Ethanol | Convex Lens |

---

## 🗂️ Project Structure

```
srishti/
├── export.py                  # Main export runner — generates all 16 diagrams
├── engines/
│   ├── label_engine.py        # PIL-based PNG renderer for biology diagrams
│   ├── svg_biology.py         # SVG biology diagram parser & renderer
│   ├── physics_vector.py      # SVG physics diagram generator (vectors, optics, circuits)
│   └── rdkit_chemistry.py     # RDKit-powered molecular structure renderer
├── templates/
│   ├── biology/
│   │   ├── animal_cell.json   # Animal cell organelle definitions
│   │   ├── plant_cell.json    # Plant cell organelle definitions
│   │   ├── heart.json         # Human heart anatomy template
│   │   └── digestive_system.json  # Digestive system organ template
│   ├── chemistry/
│   │   ├── methane.json
│   │   ├── benzene.json
│   │   └── glucose.json
│   └── physics/
│       ├── circuit.json
│       ├── concave_mirror.json
│       └── force_diagram.json
└── output/                    # Generated diagrams saved here
    ├── biology/
    ├── chemistry/
    └── physics/
```

---

## ⚙️ Requirements

- Python **3.8+**
- [RDKit](https://www.rdkit.org/) — for chemistry molecule rendering
- [Pillow](https://pillow.readthedocs.io/) — for biology PNG generation
- [svgwrite](https://svgwrite.readthedocs.io/) — for physics SVG diagrams

### Install dependencies

Install all dependencies at once using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note on RDKit:** If `pip install rdkit` fails on your platform, use conda instead:
> ```bash
> conda install -c conda-forge rdkit
> ```
> Then install the remaining packages:
> ```bash
> pip install pillow svgwrite
> ```

---

## 🚀 How to Run

### Generate all 16 diagrams at once

```bash
python3 export.py
```

This will produce all output files inside the `output/` directory:

```
output/
├── biology/
│   ├── animal_cell_labeled.png
│   ├── plant_cell_labeled.png
│   ├── heart_labeled.png
│   └── digestive_system_labeled.png
├── chemistry/
│   ├── methane.png
│   ├── benzene.png
│   ├── glucose.png
│   └── ethanol.png
└── physics/
    ├── concave_mirror.svg
    ├── circuit.svg
    ├── force_diagram.svg
    ├── convex_lens.svg
    ├── distance_time.png
    ├── velocity_time.png
    ├── wave.png
    └── motion.png
```

Expected console output:

```
==================================================
  SRISHTI SHIKSHA — Export Layer Test
==================================================
✅  biology            plant_cell           → output/biology/plant_cell_labeled.png
✅  biology            animal_cell          → output/biology/animal_cell_labeled.png
✅  biology            heart                → output/biology/heart_labeled.png
✅  biology            digestive_system     → output/biology/digestive_system_labeled.png
...
==================================================
  16 passed   0 failed
==================================================
```

---

## 🧬 Biology Diagrams

Biology diagrams are defined as **JSON templates** in `templates/biology/` and rendered via the `label_engine.py` PIL renderer.

Each JSON template defines:
- **Parts** — shapes (ellipse, rect, path) with colors and positions
- **Labels** — text annotations with leader lines pointing to parts

### Supported shape types

| Shape | Description |
|---|---|
| `ellipse` | Circle or oval (cx, cy, rx, ry) |
| `rect` | Rectangle (x, y, w, h) |
| `path` | SVG path string (d) — supports M, L, Q, C, Z |

### Scientific accuracy highlights

- **Animal Cell**: Nucleus, nucleolus, mitochondria with cristae, Golgi apparatus (stacked sacs + vesicles), rough ER with attached ribosomes, lysosome, centriole pair, cytoplasm
- **Plant Cell**: Cell wall, cell membrane, tonoplast, central vacuole, chloroplasts, mitochondria with cristae, Golgi, ER, plasmodesmata
- **Human Heart**: 4 chambers (asymmetric LV > RV), aorta arch, pulmonary artery/vein, superior/inferior vena cava, tricuspid, mitral, aortic & pulmonary valves, septum
- **Digestive System**: Mouth → esophagus → J-shaped stomach, liver (overlapping), gallbladder, pancreas, coiled small intestine, U-shaped large intestine, appendix, rectum, anus

---

## ⚗️ Chemistry Diagrams

Molecular structures are rendered using **RDKit** via `rdkit_chemistry.py`.

Each molecule is defined in `templates/chemistry/<name>.json`:

```json
{
  "name": "Benzene",
  "formula": "C₆H₆",
  "smiles": "c1ccccc1"
}
```

- Small molecules (≤4 heavy atoms) render with **explicit hydrogens**
- Carbon labels are force-shown for pedagogical clarity

---

## 📐 Physics Diagrams

Physics diagrams are generated programmatically as **SVG** via `physics_vector.py`.

### Diagram types
| Diagram | Description |
|---|---|
| `concave_mirror` | Ray optics with mathematically accurate image convergence |
| `circuit` | Closed electric circuit with battery, switch, resistor, bulb |
| `force_diagram` | Free-body diagram with applied force, friction, normal, gravity |
| `convex_lens` | Refraction ray diagram |

Physics **graphs** (PNG) include:
- Distance–Time graph
- Velocity–Time graph
- Wave diagram
- Uniform motion

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 About

**Srishti Shiksha** was built to provide high-quality, scientifically accurate educational diagrams for Indian school curriculum (CBSE/NCERT style) that can be directly embedded into learning apps, PDFs, and presentations.
