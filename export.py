import os
import json


# ── Import all engines ───────────────────────────────────────
from engines.svg_biology    import render_biology
from engines.label_engine   import add_labels
from engines.rdkit_chemistry import render_molecule
from engines.physics_vector import (
    render_distance_time_graph,
    render_velocity_time_graph,
    render_wave_diagram,
    render_motion_graphs,
    render_concave_mirror,
    render_circuit,
    render_force_diagram,
    render_ray_optics_convex,
    render_from_template,
)


# ── Output directory ─────────────────────────────────────────
OUTPUT_DIR = "output"


def export_diagram(request: dict) -> dict:
    """
    Single entry point your friend's router calls.

    Request format:
    {
        "type":     "biology" | "chemistry" | "physics_graph" | "physics_diagram",
        "name":     "plant_cell" | "methane" | "concave_mirror" | ...,
        "format":   "png" | "svg"   (optional, default: png),
        "output":   "custom/path/file.png"  (optional)
    }

    Returns:
    {
        "success": True | False,
        "path":    "output/path/to/file.png",
        "error":   "error message if failed"
    }
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    req_type   = request.get("type", "").lower().strip()
    name       = request.get("name", "").lower().strip().replace(" ", "_")
    fmt        = request.get("format", "png").lower()
    custom_out = request.get("output", None)

    # ── BIOLOGY ─────────────────────────────────────────────
    if req_type == "biology":

        BIOLOGY_TEMPLATES = {
            "plant_cell":        "templates/biology/plant_cell.json",
            "animal_cell":       "templates/biology/animal_cell.json",
            "heart":             "templates/biology/heart.json",
            "digestive_system":  "templates/biology/digestive_system.json",
        }

        if name not in BIOLOGY_TEMPLATES:
            return {
                "success": False,
                "error":   f"Unknown biology diagram '{name}'. "
                           f"Available: {', '.join(BIOLOGY_TEMPLATES.keys())}"
            }

        template_path = BIOLOGY_TEMPLATES[name]

        if not os.path.exists(template_path):
            return {"success": False, "error": f"Template file missing: {template_path}"}

        os.makedirs(f"{OUTPUT_DIR}/biology", exist_ok=True)
        out_path = custom_out or f"{OUTPUT_DIR}/biology/{name}_labeled.png"

        try:
            add_labels(template_path, out_path)
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}


    # ── CHEMISTRY ───────────────────────────────────────────
    elif req_type == "chemistry":

        os.makedirs(f"{OUTPUT_DIR}/chemistry", exist_ok=True)
        out_path = custom_out or f"{OUTPUT_DIR}/chemistry/{name}.png"

        try:
            success = render_molecule(name, out_path)
            if success:
                return {"success": True, "path": out_path}
            else:
                return {"success": False, "error": f"Molecule '{name}' not found in library"}
        except Exception as e:
            return {"success": False, "error": str(e)}


    # ── PHYSICS GRAPHS ──────────────────────────────────────
    elif req_type == "physics_graph":

        os.makedirs(f"{OUTPUT_DIR}/physics", exist_ok=True)
        out_path = custom_out or f"{OUTPUT_DIR}/physics/{name}.png"

        try:
            if name in ("distance_time", "distance-time"):
                render_distance_time_graph(
                    times=request.get("times", [0, 1, 2, 3, 4, 5]),
                    distances=request.get("values", [0, 10, 20, 30, 40, 50]),
                    output_path=out_path,
                    title=request.get("title", "Distance-Time Graph")
                )

            elif name in ("velocity_time", "velocity-time"):
                render_velocity_time_graph(
                    times=request.get("times", [0, 1, 2, 3, 4, 5]),
                    velocities=request.get("values", [0, 4, 8, 12, 16, 20]),
                    output_path=out_path,
                    title=request.get("title", "Velocity-Time Graph")
                )

            elif name == "wave":
                render_wave_diagram(output_path=out_path)

            elif name == "motion":
                render_motion_graphs(output_path=out_path)

            else:
                return {
                    "success": False,
                    "error":   f"Unknown graph '{name}'. "
                               f"Available: distance_time, velocity_time, wave, motion"
                }

            return {"success": True, "path": out_path}

        except Exception as e:
            return {"success": False, "error": str(e)}


    # ── PHYSICS DIAGRAMS ────────────────────────────────────
    elif req_type == "physics_diagram":

        os.makedirs(f"{OUTPUT_DIR}/physics", exist_ok=True)
        out_fmt  = "svg"
        out_path = custom_out or f"{OUTPUT_DIR}/physics/{name}.{out_fmt}"

        PHYSICS_RENDERERS = {
            "concave_mirror": render_concave_mirror,
            "circuit":        render_circuit,
            "force_diagram":  render_force_diagram,
            "convex_lens":    render_ray_optics_convex,
        }

        if name not in PHYSICS_RENDERERS:
            # Try rendering from template file
            template_path = f"templates/physics/{name}.json"
            if os.path.exists(template_path):
                try:
                    render_from_template(template_path, out_path)
                    return {"success": True, "path": out_path}
                except Exception as e:
                    return {"success": False, "error": str(e)}
            else:
                return {
                    "success": False,
                    "error":   f"Unknown diagram '{name}'. "
                               f"Available: {', '.join(PHYSICS_RENDERERS.keys())}"
                }

        try:
            PHYSICS_RENDERERS[name](out_path)
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}


    # ── UNKNOWN TYPE ─────────────────────────────────────────
    else:
        return {
            "success": False,
            "error":   f"Unknown type '{req_type}'. "
                       f"Use: biology, chemistry, physics_graph, physics_diagram"
        }


# ═══════════════════════════════════════════════════════════════
# TEST RUNNER — tests every engine through the export layer
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    tests = [
        # Biology
        {"type": "biology",          "name": "plant_cell"},
        {"type": "biology",          "name": "animal_cell"},
        {"type": "biology",          "name": "heart"},
        {"type": "biology",          "name": "digestive_system"},

        # Chemistry
        {"type": "chemistry",        "name": "methane"},
        {"type": "chemistry",        "name": "benzene"},
        {"type": "chemistry",        "name": "glucose"},
        {"type": "chemistry",        "name": "ethanol"},

        # Physics graphs
        {"type": "physics_graph",    "name": "distance_time"},
        {"type": "physics_graph",    "name": "velocity_time"},
        {"type": "physics_graph",    "name": "wave"},
        {"type": "physics_graph",    "name": "motion"},

        # Physics diagrams
        {"type": "physics_diagram",  "name": "concave_mirror"},
        {"type": "physics_diagram",  "name": "circuit"},
        {"type": "physics_diagram",  "name": "force_diagram"},
        {"type": "physics_diagram",  "name": "convex_lens"},
    ]

    print("=" * 50)
    print("  SRISHTI SHIKSHA — Export Layer Test")
    print("=" * 50)

    passed = 0
    failed = 0

    for test in tests:
        result = export_diagram(test)
        if result["success"]:
            print(f"✅  {test['type']:<18} {test['name']:<20} → {result['path']}")
            passed += 1
        else:
            print(f"❌  {test['type']:<18} {test['name']:<20} → {result['error']}")
            failed += 1

    print("=" * 50)
    print(f"  {passed} passed   {failed} failed")
    print("=" * 50)