# Distribution Package Structure

## Minimal Package Layout

```
microwell-plate-gui/
├── README.md                           # Simple installation & usage instructions
├── environment.yml                     # Production conda environment (pinned versions)
├── launch_microwell_gui.sh            # Simple launcher script for macOS
├── run_app.py                         # Application entry point
├── src/                               # Source code directory
│   └── microwell_plate_gui/
│       ├── __init__.py
│       ├── main.py
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── plate_canvas.py
│       │   ├── metadata_panel.py
│       │   └── legend_panel.py
│       ├── data/
│       │   ├── __init__.py
│       │   └── database.py
│       └── utils/
│           ├── __init__.py
│           ├── csv_export.py
│           └── image_export.py
├── example_database.db                # Sample database file
└── example_database.csv               # Sample CSV data
```

## Files to Include

### Essential Files
- **Source code**: Complete `src/` directory
- **Entry point**: `run_app.py` (already configured)
- **Sample data**: `example_database.db` and `example_database.csv`

### Distribution Files
- **Environment**: `environment.yml` (production version)
- **Launcher**: `launch_microwell_gui.sh` (executable script)
- **Documentation**: `README.md` (installation instructions)

## Files to Exclude

### Development Files (Not Needed)
- `environment-dev.yml` (development environment)
- `tests/` directory (testing code)
- `.benchmarks/` directory (performance data)
- `plans/` directory (design documentation)
- Debug scripts (`debug_*.py`, `simple_debug.py`)
- Git files (`.gitignore`)
- Development CSV files (`RM5097_layout.csv`)

### Rationale
- **Minimal size**: Only include runtime essentials
- **User focus**: Remove developer-specific files
- **Simplicity**: Clear structure for lab users

## Package Creation Process

1. **Create clean directory**: `microwell-plate-gui/`
2. **Copy source code**: `src/` directory
3. **Copy entry point**: `run_app.py`
4. **Copy sample data**: Database and CSV files
5. **Add distribution files**: Environment, launcher, README
6. **Set permissions**: Make launcher executable

## Distribution Method

### For Lab Colleagues
- **Git clone**: Clone repository and package for distribution
- **Archive**: Create `.zip` or `.tar.gz` for easy sharing
- **Shared drive**: Place package on lab shared storage

### Package Size
- Estimated size: ~500KB (source code + sample data)
- No large dependencies included (handled by conda)
- Fast download/transfer for lab network