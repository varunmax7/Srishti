"""
SVG Chemistry Experiment Renderer (Shim)
─────────────────────────────────
This module has been refactored into the `engines.chem_experiment` package.
This file serves as a shim to maintain backward compatibility for `export.py`.
"""

from engines.chem_experiment import render_experiment, render_all, RENDERERS

if __name__ == "__main__":
    render_all()
