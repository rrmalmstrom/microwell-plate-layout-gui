# User Installation Instructions

## README.md for Distribution Package

```markdown
# Microwell Plate GUI

A simple tool for designing microwell plate layouts and generating CSV files for molecular biology applications.

## Quick Start (macOS)

### Prerequisites
- macOS computer
- Miniconda or Anaconda installed
  - If not installed: Download from https://docs.conda.io/en/latest/miniconda.html

### Installation (5 minutes)

1. **Download the package**
   - Extract `microwell-plate-gui.zip` to your desired location
   - Open Terminal and navigate to the extracted folder:
     ```bash
     cd path/to/microwell-plate-gui
     ```

2. **Create the conda environment**
   ```bash
   conda env create -f environment.yml
   ```
   This creates an environment called `microwell-plate-gui` with all required dependencies.

3. **Make the launcher executable**
   ```bash
   chmod +x launch_microwell_gui.sh
   ```

4. **Launch the application**
   ```bash
   ./launch_microwell_gui.sh
   ```

### Daily Usage

After initial setup, simply run:
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

### "conda: command not found"
- Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
- Restart Terminal after installation

### "Environment 'microwell-plate-gui' not found"
- Run: `conda env create -f environment.yml`
- Make sure you're in the correct directory

### "run_app.py not found"
- Make sure you're running the launcher from the `microwell-plate-gui` directory
- Check that all files were extracted properly

### Application won't start
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
```

## Key Features of Instructions

### Simplicity
- **5-minute setup**: Clear time expectation
- **4 simple steps**: Easy to follow
- **Copy-paste commands**: No typing errors

### User-Focused
- **Prerequisites check**: Ensures conda is available
- **Daily usage**: Simple command for regular use
- **Troubleshooting**: Common issues with solutions

### Lab-Appropriate
- **macOS focus**: Matches your target environment
- **Terminal commands**: Standard for scientific computing
- **Contact info**: Placeholder for lab support

### Error Prevention
- **Step-by-step**: Reduces setup mistakes
- **Verification**: Each step can be confirmed
- **Helpful errors**: Launcher provides guidance

## Installation Flow

1. **Download** → Extract package
2. **Environment** → Create conda environment (one-time)
3. **Permissions** → Make launcher executable (one-time)
4. **Launch** → Run application (daily use)

This approach gives lab colleagues a professional, reliable installation experience while keeping complexity minimal.