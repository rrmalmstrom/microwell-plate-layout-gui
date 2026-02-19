# Microwell Plate GUI - Installation Guide

## Quick Start

### Step 1: Install Conda (if not already installed)
Download and install Miniconda or Anaconda:
- **Intel Macs**: [Miniconda3 macOS Intel x86_64](https://docs.conda.io/en/latest/miniconda.html)
- **Apple Silicon Macs (M1/M2/M3)**: [Miniconda3 macOS Apple M1](https://docs.conda.io/en/latest/miniconda.html)

### Step 2: Create Environment
Choose one of these approaches:

#### Option A: Minimal Environment (Recommended)
```bash
conda env create -f environment.yml
conda activate microwell-plate-gui
```

#### Option B: Conservative Environment (If Option A fails)
```bash
conda env create -f environment_conservative.yml
conda activate microwell-plate-gui-conservative
```

### Step 3: Test Installation
```bash
python test_environment.py
```

### Step 4: Run Application
```bash
python run_app.py
```

## Mac Compatibility Notes

### Intel vs Apple Silicon
Both environment files are designed to work on:
- **Intel Macs** (x86_64 architecture)
- **Apple Silicon Macs** (arm64 architecture - M1, M2, M3 chips)

The environments use **loose version constraints** without build strings to allow conda to select the appropriate packages for your specific Mac architecture.

### Rosetta 2 Compatibility
If you're on Apple Silicon and encounter issues:
1. Some packages may run under Rosetta 2 (Intel emulation)
2. This is handled automatically by conda
3. Performance may be slightly reduced but functionality is preserved

## Troubleshooting

### Environment Creation Fails
If `conda env create` fails with dependency conflicts:

1. **Update conda first**:
   ```bash
   conda update conda
   conda clean --all
   ```

2. **Try the conservative environment**:
   ```bash
   conda env create -f environment_conservative.yml
   ```

3. **Manual installation fallback**:
   ```bash
   conda create -n microwell-plate-gui python>=3.8
   conda activate microwell-plate-gui
   conda install ghostscript -c conda-forge
   ```

### Application Won't Start
If the app fails to start:

1. **Test the environment**:
   ```bash
   python test_environment.py
   ```

2. **Check for missing packages**:
   ```bash
   conda list
   ```

3. **Verify ghostscript**:
   ```bash
   ps2pdf --version
   ```

### PDF Export Issues
If PDF export doesn't work:

1. **Check ghostscript installation**:
   ```bash
   which ps2pdf
   gs --version
   ```

2. **Reinstall ghostscript**:
   ```bash
   conda install ghostscript -c conda-forge --force-reinstall
   ```

### GUI Issues on macOS
If the GUI doesn't appear or looks wrong:

1. **Check tkinter**:
   ```bash
   python -c "import tkinter; print('tkinter works')"
   ```

2. **Install explicit tk support**:
   ```bash
   conda install tk -c conda-forge
   ```

## Architecture Detection

To check your Mac's architecture:
```bash
uname -m
```
- `x86_64` = Intel Mac
- `arm64` = Apple Silicon Mac

To check which conda packages are installed:
```bash
conda list | grep -E "(x86_64|arm64|osx)"
```

## Performance Notes

### Apple Silicon Optimization
- Native arm64 packages provide best performance
- Mixed architectures (some x86_64, some arm64) work but may be slower
- The minimal environment reduces architecture conflicts

### Intel Mac Optimization
- All packages should be x86_64 native
- No emulation overhead
- Full performance expected

## Environment Comparison

| Feature | Minimal | Conservative |
|---------|---------|--------------|
| Download size | ~50MB | ~200MB |
| Install time | 1-2 minutes | 3-5 minutes |
| Compatibility | High | Very High |
| Conflict risk | Low | Very Low |
| Packages | 3-5 | 8-12 |

## Support

### Before Reporting Issues
1. Run `python test_environment.py` and include output
2. Run `conda list` and include output
3. Specify your Mac model and macOS version
4. Include any error messages

### Common Solutions
- **Import errors**: Try conservative environment
- **GUI issues**: Install explicit tk package
- **PDF issues**: Reinstall ghostscript
- **Performance issues**: Check architecture mixing

## Uninstallation

To remove the environment:
```bash
conda env remove -n microwell-plate-gui
# or
conda env remove -n microwell-plate-gui-conservative
```

## Advanced: Custom Installation

If both provided environments fail, you can create a custom environment:

```bash
# Create base environment
conda create -n microwell-plate-gui-custom python=3.11

# Activate and install packages one by one
conda activate microwell-plate-gui-custom
conda install ghostscript -c conda-forge

# Test after each package
python test_environment.py

# Add packages only if tests fail
conda install numpy pandas tk pillow
```

This approach helps identify exactly which packages are needed on your specific system.