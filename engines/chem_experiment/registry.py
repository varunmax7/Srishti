import os
import json

from .chem_conductivity_test import render_conductivity_test
from .chem_electrolysis_diagram import render_electrolysis_diagram
from .chem_gas_collection_spoon import render_gas_collection_spoon
from .chem_heat_conduction import render_heat_conduction
from .chem_open_circuit import render_open_circuit
from .chem_rusting_conditions import render_rusting_conditions
from .chem_spray_mechanism import render_spray_mechanism
from .chem_star_polymer import render_star_polymer
from .chem_sunlight_exposure import render_sunlight_exposure
from .chem_conductivity_stand import render_conductivity_stand
from .chem_electrolysis_water import render_electrolysis_water
from .chem_evaporation_setup import render_evaporation_setup
from .chem_flame_test import render_flame_test
from .chem_gas_collection import render_gas_collection
from .chem_hydrogen_test import render_hydrogen_test
from .chem_test_tube_rack import render_test_tube_rack
from .chem_thermal_decomposition import render_thermal_decomposition
from .chem_zinc_reaction import render_zinc_reaction

RENDERERS = {
    "chem_conductivity_test": render_conductivity_test,
    "chem_electrolysis_diagram": render_electrolysis_diagram,
    "chem_gas_collection_spoon": render_gas_collection_spoon,
    "chem_heat_conduction": render_heat_conduction,
    "chem_open_circuit": render_open_circuit,
    "chem_rusting_conditions": render_rusting_conditions,
    "chem_spray_mechanism": render_spray_mechanism,
    "chem_star_polymer": render_star_polymer,
    "chem_sunlight_exposure": render_sunlight_exposure,
    "chem_conductivity_stand": render_conductivity_stand,
    "chem_electrolysis_water": render_electrolysis_water,
    "chem_evaporation_setup": render_evaporation_setup,
    "chem_flame_test": render_flame_test,
    "chem_gas_collection": render_gas_collection,
    "chem_hydrogen_test": render_hydrogen_test,
    "chem_test_tube_rack": render_test_tube_rack,
    "chem_thermal_decomposition": render_thermal_decomposition,
    "chem_zinc_reaction": render_zinc_reaction,
}

def render_experiment(spec_path: str, output_dir: str = "output/chem_experiment") -> bool:
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    diagram = spec.get("diagram")
    if diagram not in RENDERERS:
        print(f"❌ No renderer found for: {diagram}")
        return False

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{diagram}.svg")
    return RENDERERS[diagram](spec, out_path)

def render_all(template_dir: str = "templates/chem_experiment",
               output_dir:   str = "output/chem_experiment") -> None:
    if not os.path.isdir(template_dir):
        print(f"❌ Template directory not found: {template_dir}")
        return
    for fname in sorted(os.listdir(template_dir)):
        if fname.endswith(".json"):
            render_experiment(os.path.join(template_dir, fname), output_dir)
