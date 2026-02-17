# Microwell Plate Layout GUI

A Python-based GUI tool for designing microwell plate layouts and generating standardized CSV files for molecular biology applications.

## Features

- Support for 96-well and 384-well plates
- Visual well selection with drag and click
- Metadata management with database integration
- Value-based well visualization with 12 colors and 10 visual patterns
- Combined CSV & PDF image export functionality
- Exit application with confirmation dialog
- Optimized layout with improved panel visibility
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

- ✅ Phase 1: Core Infrastructure
- ✅ Phase 2: Metadata System
- ✅ Phase 3: Advanced Features
- ✅ Phase 4.1: Core Validation & Testing
- ✅ Phase 4.2: Layout Improvements & Export Features
- 🔄 Phase 4.3: Advanced Polish (Next)
- ⏳ Phase 5: Distribution

### Recent Completion: Phase 4.2 Features
- **Layout Improvements**: Optimized panel weight ratios and button organization
- **Exit Application**: Safe application closure with confirmation dialog
- **Image Export**: Combined CSV & PDF image export functionality
- **Enhanced UX**: Better button styling and responsive layout design

## Project Structure

```
src/microwell_plate_gui/
├── gui/          # GUI components (main_window, plate_canvas, metadata_panel, legend_panel)
├── data/         # Data management (database, validation)
├── utils/        # Utility functions (csv_export, image_export)
└── main.py       # Application entry point

tests/            # Comprehensive test suite
├── test_gui/     # GUI component tests
├── test_data/    # Data management tests
└── test_utils/   # Utility function tests

plans/            # Design documentation and specifications
```

## Documentation

See the `plans/` directory for comprehensive design specifications and implementation guidelines.

## License

Laboratory Internal Use