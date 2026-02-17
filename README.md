# Microwell Plate GUI

A simple tool for designing microwell plate layouts and generating CSV files for molecular biology applications.

## Quick Start (macOS)

### Prerequisites
- macOS computer
- Miniconda or Anaconda installed
  - If not installed: Download from https://docs.conda.io/en/latest/miniconda.html

### One-Time Setup (5 minutes)

1. **Download and extract the package**
   - Extract `microwell-plate-gui.zip` to your desired location
   - Open Terminal and navigate to the extracted folder:
     ```bash
     cd path/to/microwell-plate-gui
     ```

2. **Run the setup script**
   ```bash
   ./setup_microwell_gui.sh
   ```
   
   This script will:
   - Check that conda is installed
   - Create the `microwell-plate-gui` conda environment
   - Install all required dependencies
   - Make the launcher script executable
   - Test that everything works correctly

### Daily Usage

After the one-time setup, simply run:
```bash
./launch_microwell_gui.sh
```

The launcher will automatically:
- Activate the correct conda environment
- Start the application
- Show helpful error messages if something goes wrong

## Features

- Support for 96-well and 384-well plates
- Visual well selection with drag and click
- Metadata management with database integration
- CSV and PDF export functionality
- Value-based well visualization with colors and patterns

## Troubleshooting

### Setup Issues

**"conda: command not found"**
- Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
- Restart Terminal after installation
- Run the setup script again

**"environment.yml not found"**
- Make sure you're running the setup script from the `microwell-plate-gui` directory
- Check that all files were extracted properly

**Setup script fails**
- Check your internet connection (needed to download packages)
- Try running: `conda clean --all` then run setup again
- Make sure you have enough disk space (~500MB needed)

### Daily Usage Issues

**"Environment 'microwell-plate-gui' not found"**
- Run the setup script again: `./setup_microwell_gui.sh`

**"run_app.py not found"**
- Make sure you're running the launcher from the `microwell-plate-gui` directory

**Application won't start**
- Try running: `conda activate microwell-plate-gui && python run_app.py`
- Check Terminal for error messages

## Uninstalling

To remove the application:
```bash
conda env remove -n microwell-plate-gui
```
Then delete the `microwell-plate-gui` folder.

## Support

For issues or questions, contact [Lab Contact Information].

---

## Development Information

### Development Status

- ✅ Phase 1: Core Infrastructure
- ✅ Phase 2: Metadata System
- ✅ Phase 3: Advanced Features
- ✅ Phase 4.1: Core Validation & Testing
- ✅ Phase 4.2: Layout Improvements & Export Features
- ✅ Phase 5.1: Distribution Implementation
- ⏳ Phase 5.2: Distribution Testing

### Project Structure

```
microwell-plate-gui/
├── README.md                    # This file
├── setup_microwell_gui.sh       # One-time setup script
├── launch_microwell_gui.sh      # Daily launcher script
├── environment.yml              # Production conda environment
├── run_app.py                   # Application entry point
├── src/                         # Source code
│   └── microwell_plate_gui/
│       ├── gui/                 # GUI components
│       ├── data/                # Data management
│       ├── utils/               # Utility functions
│       └── main.py              # Application entry point
├── example_database.db          # Sample data
└── example_database.csv         # Sample data
```

### Development Setup

For developers who want to modify the application:

1. Clone this repository
2. Create development environment: `conda env create -f environment-dev.yml`
3. Activate environment: `conda activate microwell-gui-dev`
4. Run application: `python run_app.py`
5. Run tests: `python -m pytest tests/ -v`

### Documentation

See the `plans/` directory for comprehensive design specifications and implementation guidelines.

## License

Laboratory Internal Use