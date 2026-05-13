import os
import json
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image, ImageDraw, ImageFont
import io


# ── Molecule library ─────────────────────────────────────────
MOLECULES = {
    # Class 9-10 NCERT
    "methane":       {"smiles": "C",                                      "formula": "CH₄",     "name": "Methane"},
    "ethane":        {"smiles": "CC",                                     "formula": "C₂H₆",    "name": "Ethane"},
    "ethene":        {"smiles": "C=C",                                    "formula": "C₂H₄",    "name": "Ethene"},
    "ethyne":        {"smiles": "C#C",                                    "formula": "C₂H₂",    "name": "Ethyne"},
    "ethanol":       {"smiles": "CCO",                                    "formula": "C₂H₅OH",  "name": "Ethanol"},
    "acetic_acid":   {"smiles": "CC(=O)O",                               "formula": "CH₃COOH", "name": "Acetic Acid"},
    "benzene":       {"smiles": "c1ccccc1",                               "formula": "C₆H₆",    "name": "Benzene"},
    "glucose":       {"smiles": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O","formula": "C₆H₁₂O₆","name": "Glucose"},
    "water":         {"smiles": "O",                                      "formula": "H₂O",     "name": "Water"},
    "ammonia":       {"smiles": "N",                                      "formula": "NH₃",     "name": "Ammonia"},
    "co2":           {"smiles": "O=C=O",                                  "formula": "CO₂",     "name": "Carbon Dioxide"},
    "hcl":           {"smiles": "Cl",                                     "formula": "HCl",     "name": "Hydrochloric Acid"},
    "nacl":          {"smiles": "[Na+].[Cl-]",                            "formula": "NaCl",    "name": "Sodium Chloride"},
    "methanol":      {"smiles": "CO",                                     "formula": "CH₃OH",   "name": "Methanol"},
    "propane":       {"smiles": "CCC",                                    "formula": "C₃H₈",    "name": "Propane"},
    "butane":        {"smiles": "CCCC",                                   "formula": "C₄H₁₀",   "name": "Butane"},
    "acetone":       {"smiles": "CC(=O)C",                               "formula": "C₃H₆O",   "name": "Acetone"},
    "sulfuric_acid": {"smiles": "OS(=O)(=O)O",                           "formula": "H₂SO₄",   "name": "Sulfuric Acid"},
    "nitric_acid":   {"smiles": "O[N+](=O)[O-]",                         "formula": "HNO₃",    "name": "Nitric Acid"},
    "urea":          {"smiles": "NC(=O)N",                               "formula": "CH₄N₂O",  "name": "Urea"},
}


def get_font(size=16, bold=False):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def render_molecule(name: str, output_path: str, size=(500, 400)):
    """
    Render a molecule by name → saves PNG with title and formula.
    """
    name = name.lower().strip().replace(" ", "_")

    if name not in MOLECULES:
        print(f"❌ Molecule '{name}' not found. Available: {', '.join(MOLECULES.keys())}")
        return False

    mol_data = MOLECULES[name]
    smiles   = mol_data["smiles"]
    title    = mol_data["name"]
    formula  = mol_data["formula"]

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"❌ Could not parse SMILES for {name}")
        return False

    # For small molecules (≤4 heavy atoms), add explicit hydrogens
    # so that atoms like C and H are drawn instead of just skeletal bond lines.
    # This fixes ethene (H₂C=CH₂), ethyne (HC≡CH), methane, water, etc.
    num_heavy = mol.GetNumHeavyAtoms()
    if num_heavy <= 4:
        mol = Chem.AddHs(mol)

    # Compute 2D coordinates (must be done AFTER adding H atoms)
    AllChem.Compute2DCoords(mol)

    # Draw molecule using RDKit drawer (high quality)
    mol_w, mol_h = size
    drawer = rdMolDraw2D.MolDraw2DCairo(mol_w, mol_h) if hasattr(rdMolDraw2D, 'MolDraw2DCairo') else None

    if drawer:
        opts = drawer.drawOptions()
        opts.addStereoAnnotation = True
        if num_heavy <= 4:
            # Force ALL atom symbols to be visible (including C) for small molecules.
            # By default RDKit hides C labels in skeletal notation — useless for
            # tiny molecules like ethene (H₂C=CH₂) and ethyne (HC≡CH).
            for atom in mol.GetAtoms():
                atom.SetProp("atomLabel", atom.GetSymbol())
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        mol_img = Image.open(io.BytesIO(drawer.GetDrawingText())).convert("RGBA")
    else:
        # Fallback: use Draw.MolToImage
        mol_img = Draw.MolToImage(mol, size=size, kekulize=True)
        mol_img = mol_img.convert("RGBA")

    # Build final image with title + formula banner
    padding   = 70
    final_w   = mol_w
    final_h   = mol_h + padding
    final_img = Image.new("RGBA", (final_w, final_h), (255, 255, 255, 255))

    # White background for molecule area
    final_img.paste(mol_img, (0, padding))

    draw = ImageDraw.Draw(final_img)

    # Top banner
    draw.rectangle([0, 0, final_w, padding], fill="#F3F4F6")
    draw.line([0, padding, final_w, padding], fill="#CCCCCC", width=2)

    # Title
    title_font   = get_font(size=22, bold=True)
    formula_font = get_font(size=16)

    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w    = title_bbox[2] - title_bbox[0]
    draw.text(((final_w - title_w) / 2, 8), title, fill="#1a1a2e", font=title_font)

    # Formula
    formula_bbox = draw.textbbox((0, 0), formula, font=formula_font)
    formula_w    = formula_bbox[2] - formula_bbox[0]
    draw.text(((final_w - formula_w) / 2, 38), formula, fill="#555555", font=formula_font)

    # Save
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    final_img.save(output_path, "PNG")
    print(f"Saved: {output_path}  ({title} — {formula})")
    return True


def render_all(output_dir: str = "output/chemistry"):
    """Render all molecules in the library."""
    os.makedirs(output_dir, exist_ok=True)
    for name in MOLECULES:
        render_molecule(name, os.path.join(output_dir, f"{name}.png"))


# ── Test runner ──────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("output/chemistry", exist_ok=True)

    # Test the 3 key ones first
    test_molecules = [
        "methane",
        "benzene",
        "glucose",
        "ethanol",
        "co2",
        "water",
        "ammonia",
        "ethene",
        "ethyne",
        "acetic_acid",
    ]

    print("Rendering molecules...\n")
    for mol in test_molecules:
        render_molecule(mol, f"output/chemistry/{mol}.png")

    print(f"\nDone. Open output/chemistry/ to view all molecules.")