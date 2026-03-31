# Microwell Plate GUI - Distribution Package

## What's Included

This distribution package contains everything needed to run the Microwell Plate GUI application on macOS systems.

### Files Overview

```
microwell-plate-layout-gui/
├── docs/
│   ├── README_DISTRIBUTION.md     # This file
│   ├── INSTALLATION.md            # Detailed installation instructions
│   └── VALIDATION_REPORT.md       # Environment validation results
├── src/microwell_plate_gui/       # Application source code
├── tests/                         # Test suite
├── environment.yml                # Minimal conda environment (recommended)
├── environment_conservative.yml   # Conservative environment (backup)
├── run_app.py                     # Application entry point
├── setup_microwell_gui.sh         # One-time setup script
├── _internal_launcher.sh          # Internal launcher (called by .command file)
└── 🧬 Start Microwell GUI.command # Double-click launcher for daily use
```

## Quick Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rrmalmstrom/microwell-plate-layout-gui.git
cd microwell-plate-layout-gui

# 2. Run one-time setup
./setup_microwell_gui.sh

# 3. Launch daily by double-clicking:
#    🧬 Start Microwell GUI.command
```

The app auto-updates on every launch via `git pull`.

## Manual Environment Setup (if setup script fails)

### Minimal Environment (Recommended)
```bash
conda env create -f environment.yml
conda activate microwell-gui
python tests/test_environment.py
python run_app.py
```

### Conservative Environment (If minimal fails)
```bash
conda env create -f environment_conservative.yml
conda activate microwell-gui
python tests/test_environment.py
python run_app.py
```

## System Requirements

- **macOS**: 10.14 (Mojave) or later
- **Architecture**: Intel (x86_64) or Apple Silicon (M1/M2/M3)
- **Conda**: Miniconda or Anaconda installed
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space

## Key Features

- **Minimal Dependencies**: Only requires Python + Ghostscript
- **Cross-Platform**: Works on Intel and Apple Silicon Macs
- **Self-Testing**: Automated validation without manual GUI testing
- **Fallback Options**: Multiple environment configurations
- **PDF Export**: Full PostScript to PDF conversion support

## Environment Strategy

### Why Two Environment Files?

1. **environment.yml (Minimal)**
   - Contains only essential packages
   - Fastest installation
   - Lowest conflict risk
   - Based on actual code analysis

2. **environment_conservative.yml (Backup)**
   - Includes additional common packages
   - Better compatibility with diverse systems
   - Larger but more robust

### Dependency Analysis Results

Your application was analyzed and found to use:
- **Python Standard Library**: tkinter, sqlite3, os, sys, csv, logging, subprocess, etc.
- **External Dependencies**: Only ghostscript (for PDF export)
- **Test Dependencies**: pytest, pillow (development only)

This minimal dependency footprint eliminates the conflicts you experienced with your 80+ package development environment.

## Troubleshooting

### Common Issues

1. **"Conda not found"**
   - Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
   - Restart terminal after installation

2. **Environment creation fails**
   - Try: `conda update conda && conda clean --all`
   - Use conservative environment: `environment_conservative.yml`

3. **Application won't start**
   - Run: `python test_environment.py`
   - Check output for specific missing packages

4. **PDF export doesn't work**
   - Test: `ps2pdf --version`
   - Reinstall: `conda install ghostscript -c conda-forge`

### Getting Help

1. Run the test suite: `python test_environment.py`
2. Check the detailed installation guide: `INSTALLATION.md`
3. Include test output when reporting issues

## Technical Notes

### Architecture Compatibility
- Uses pinned version ranges (Python 3.11.x, Ghostscript 10.x) tested on Intel and Apple Silicon
- No platform-specific build strings — conda selects the right binary for your Mac automatically
- Supports both Intel (x86_64) and Apple Silicon (arm64) architectures

### Performance
- Minimal environment: ~50MB download, 1-2 minute install
- Conservative environment: ~200MB download, 3-5 minute install
- Native performance on both Intel and Apple Silicon

### Security
- All packages from trusted conda-forge and defaults channels
- No custom or third-party repositories
- Minimal attack surface with few dependencies

## Development Notes

If you need to modify or extend this application:

1. **Development Environment**:
   ```bash
   conda env create -f environment_conservative.yml
   conda activate microwell-gui
   conda install pytest pillow  # Add development tools
   ```

2. **Testing**:
   ```bash
   python tests/test_environment.py  # Environment validation
   pytest tests/                     # Full test suite
   ```

3. **Code Notes**:
   - Application uses only Python standard library (no numpy, pandas, etc. in production code)
   - Ghostscript (10.x) required for PDF export — tested on 10.06.0
   - Python 3.11.x required — tested on 3.11.14