# FactoryLM CAD Module

Professional mechanical drawing and schematic generator.

## Features

- **DXF Output**: Industry-standard CAD format
- **Multi-View Drawings**: Side, Top, End views
- **Title Blocks**: Professional formatting
- **Bill of Materials**: Auto-generated BOM
- **Dimensions**: Proper dimensioning
- **Notes**: Construction notes

## Usage

```python
from factorylm_cad.conveyor_full_drawing import generate_conveyor_package

# Generate complete drawing package
dxf_path = generate_conveyor_package(
    job_no="2026-0206-001",
    output_dir="/tmp"
)
```

## Dependencies

- ezdxf (DXF file handling)
- matplotlib (PNG export)
- CadQuery (3D modeling, optional)

## Output Formats

- `.dxf` - Opens in AutoCAD, FreeCAD, any CAD software
- `.png` - Preview images

## Installation

```bash
pip install ezdxf matplotlib
```

## Created

2026-02-06 by Jarvis AI for FactoryLM
