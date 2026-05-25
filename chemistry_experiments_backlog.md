# Chemistry Experiments Backlog

Use this file to document the chemistry experiments you want to add. For each experiment, please provide the JSON configuration and any specific rendering/design instructions.

---

## 1. chem_electrolysis_setup

### JSON Template
```json
{
  "diagram": "chem_electrolysis_setup",
  "title": "Electrolysis Setup",
  "canvas": {
    "width": 800,
    "height": 1000,
    "background": "#ffffff",
    "padding": 40
  },
  "beaker": {
    "label": "Beaker",
    "show_label": false,
    "outline_color": "#1a1a1a",
    "outline_width": 3,
    "has_spout": true,
    "rim_ellipse_ry": 30
  },
  "liquid": {
    "label": "Electrolyte",
    "show_label": false,
    "fill_color": "#f5edb3",
    "fill_opacity": 1.0,
    "fill_level": 0.30,
    "surface_color": "#1a1a1a"
  },
  "solid_block": {
    "label": "Solid block",
    "show_label": false,
    "shape": "trapezoid",
    "fill_color": "#b5731f",
    "edge_color": "#8a5616",
    "top_width": 160,
    "bottom_width": 260,
    "height": 220,
    "sits_on_bottom": true
  },
  "electrodes": {
    "count": 2,
    "type": "nail",
    "label": "Iron nails",
    "show_label": false,
    "color": "#b8b8b8",
    "edge_color": "#7a7a7a",
    "head_radius": 14,
    "shaft_width": 10,
    "gap": 110,
    "embedded_in_block": true,
    "tip_into_block": 0.5
  },
  "circuit": {
    "wire_color": "#1a1a1a",
    "wire_width": 3,
    "top_y_ratio": 0.18,
    "battery": {
      "label": "Battery (3 cells)",
      "show_label": false,
      "cells": 3
    },
    "bulb": {
      "label": "Bulb",
      "show_label": false,
      "glowing": false,
      "glow_color": "#ffb300"
    },
    "switch": {
      "label": "Switch",
      "show_label": false,
      "closed": false,
      "style": "open_gap"
    }
  },
  "labels": {
    "font_family": "Arial, Helvetica, sans-serif",
    "font_size": 18,
    "color": "#1a1a1a",
    "show": false
  }
}
```

### Rendering Notes
- Solid block: Trapezoid at the bottom of the beaker.
- Electrodes: Iron nails (with head, shaft, tip) embedded in the solid block.
- Circuit: Battery with 3 cells, open switch (style: open_gap), non-glowing bulb.
