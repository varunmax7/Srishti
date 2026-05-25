# 🎓 Srishti Shiksha — Scientific Diagram Export Engine

> **Srishti Shiksha** is a Python-based educational diagram generation system that produces high-quality, scientifically accurate diagrams for Biology, Chemistry, Physics, and Lab Experiments — ready for use in textbooks, presentations, and educational applications.

---

## 📸 Sample Outputs

| Biology | Chemistry | Physics | Lab Experiments |
|---|---|---|---|
| Animal & Plant Cells | Benzene & Ethanol | Optics (Lens/Mirrors) | Gas Collection Setup |
| Human Brain & Heart | Molecular Structures | Electric Circuits | Electrolysis of Water |
| Endocrine System | Functional Groups | Force Diagrams | Thermal Decomposition |
| Human Ear & Eye | Complex Molecules | Kinematic Graphs | Conductivity Tests |

---

## 🗂️ Project Structure

```text
srishti/
├── export.py                  # Main export runner — generates all system diagrams
├── engines/
│   ├── label_engine.py        # PIL-based PNG renderer for biology diagrams
│   ├── svg_biology.py         # SVG biology diagram parser & renderer
│   ├── physics_vector.py      # SVG physics diagram generator (vectors, optics, circuits)
│   ├── rdkit_chemistry.py     # RDKit-powered molecular structure renderer
│   ├── svg_chem_experiment.py # Base SVG chemistry experiment setup renderer
│   └── chem_experiment/       # Specialized modules for procedural chemistry setups (e.g. Test Tube Racks, Electrolysis, Flame Tests)
├── templates/
│   ├── biology/               # JSON templates for cells, organ systems, brain, ear, etc. 
│   ├── chemistry/             # JSON definitions containing SMILES strings for molecules
│   ├── physics/               # JSON configuration for physics vectors and optics
│   └── chem_experiment/       # JSON configuration for complex lab experiment diagrams
│
├── scratch/                   # Generator scripts for creating experimental diagram templates
└── output/                    # Generated diagrams saved here (biology, chemistry, physics, chem_experiment)
```

---

## ⚙️ Requirements

- Python **3.8+**
- [RDKit](https://www.rdkit.org/) — for chemistry molecule rendering
- [Pillow](https://pillow.readthedocs.io/) — for biology PNG generation
- [svgwrite](https://svgwrite.readthedocs.io/) — for physics and chemistry experiment SVG diagrams

### Install dependencies

Install all dependencies at once using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note on RDKit:** If `pip install rdkit` fails on your platform, use conda instead:
> ```bash
> conda install -c conda-forge rdkit
> ```

---

## 🚀 How to Run

### Generate all diagrams at once

```bash
python3 export.py
```

This will produce all output files inside the `output/` directory spanning Biology, Chemistry, Physics, and Lab Experiments. 

```text
output/
├── biology/
├── chemistry/
├── physics/
└── chem_experiment/
```

---

## 🧬 Biology Diagrams

Biology diagrams are defined as **JSON templates** in `templates/biology/` and rendered via the `label_engine.py` / `svg_biology.py` renderers.

**Supported systems include:**
- Cellular Level (Plant/Animal Cell)
- Nervous System (Human Brain, Neuron)
- Cardiovascular System (Heart)
- Excretory & Respiratory System (Nephron, Alveoli)
- Endocrine & Reproductive Systems
- Sensory Organs (Eye, Ear)

Each JSON template carefully defines SVG-like anatomical structures and accurate callout labels pointing strictly to the structures.

---

## ⚗️ Chemistry Diagrams & Lab Experiments

### Molecular Structures
Molecular structures are rendered using **RDKit** via `rdkit_chemistry.py`. Small molecules (≤4 heavy atoms) render with explicit hydrogens for pedagogical clarity. Dozens of everyday chemicals and NCERT organic compounds are included.

### Lab Experiments (New!)
A specialized suite under `engines/chem_experiment/` leverages `svgwrite` to build procedural lab setups:
- **Test Tube Racks** & **Flame Tests**
- **Electrolysis of Water** & **Open Circuits**
- **Gas Collection Setups** (Flasks, Delivery Tubes, Troughs)
- **Evaporation** and **Thermal Decomposition** diagrams

Templates in `templates/chem_experiment/` define properties such as equipment types, color configurations, liquid levels, and experimental annotations (like bubble generation for hydrogen gas tests).

---

## 📐 Physics Diagrams

Physics diagrams are generated programmatically as **SVG** via `physics_vector.py`.

### Diagram types
| Diagram | Description |
|---|---|
| `concave_mirror` / `convex_lens` | Ray optics with mathematically accurate image convergence / refraction |
| `circuit` | Closed electric circuit with battery, switch, resistor, bulb |
| `force_diagram` | Free-body diagram with applied force, friction, normal, gravity |

Physics **graphs** include Distance–Time, Velocity–Time, wave motion, and uniform motion represented mathematically.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 About

**Srishti Shiksha** was built to provide high-quality, scientifically accurate educational diagrams for Indian school curriculum (CBSE/NCERT style) that can be directly embedded into learning apps, PDFs, and presentations.
