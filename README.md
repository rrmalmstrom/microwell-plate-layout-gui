# Microwell Plate Layout GUI

A Python-based GUI tool for designing microwell plate layouts and generating standardized CSV files for molecular biology applications.

## Features

- Support for 96-well and 384-well plates
- Visual well selection with drag and click
- Metadata management with database integration
- Tri-color well visualization for grouping levels
- CSV export matching laboratory standards
- Accessibility features for colorblind users

## Installation

### Prerequisites
- Python 3.11+
- Conda package manager

### Setup
1. Clone this repository
2. Create conda environment: `conda env create -f environment.yml`
3. Activate environment: `conda activate microwell-gui`
4. Run application: `python -m microwell_plate_gui.main`

## Development Status

- ✅ Phase 0: Development Environment Setup
- 🔄 Phase 1: Core Infrastructure (In Progress)
- ⏳ Phase 2: Metadata System
- ⏳ Phase 3: Advanced Features
- ⏳ Phase 4: Validation & Polish
- ⏳ Phase 5: Export & Distribution

## Project Structure

```
src/microwell_plate_gui/
├── gui/          # GUI components
├── data/         # Data management
├── utils/        # Utility functions
└── main.py       # Application entry point

tests/            # Test suite
plans/            # Design documentation
```

## Documentation

See the `plans/` directory for comprehensive design specifications and implementation guidelines.

## License

Laboratory Internal Use