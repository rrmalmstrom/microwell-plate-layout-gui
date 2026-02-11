# Conda Distribution and Environment Setup

## Automated Environment Management

### Environment Configuration Files

#### environment.yml (Deterministic Build)
```yaml
name: microwell-plate-gui
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11.5
  - tkinter=8.6.12
  - sqlite=3.42.0
  - pytest=7.4.0
  - pytest-cov=4.1.0
  - pandas=2.0.3
  - pip=23.2.1
  - pip:
    - pytest-mock==3.11.1
    - pytest-qt==4.2.0
prefix: /path/to/conda/envs/microwell-plate-gui
```

#### environment-lock.yml (Exact Version Lock)
```yaml
# This file may be used to create an environment using:
# $ conda env create --file environment-lock.yml
name: microwell-plate-gui
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11.5=h2755cc3_0
  - tkinter=8.6.12=py311h2755cc3_0
  - sqlite=3.42.0=h2bbff1b_0
  - pytest=7.4.0=py311haa95532_0
  - pytest-cov=4.1.0=py311haa95532_0
  - pandas=2.0.3=py311hf62ec03_0
  - pip=23.2.1=py311haa95532_0
  - pip:
    - pytest-mock==3.11.1
    - pytest-qt==4.2.0
```

### Automated Launcher Scripts

#### Windows Launcher (microwell-gui.bat)
```batch
@echo off
REM Microwell Plate GUI Launcher for Windows
REM This script automatically activates the conda environment and runs the application

echo Starting Microwell Plate GUI...

REM Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Miniconda or Anaconda first
    pause
    exit /b 1
)

REM Check if environment exists
conda env list | findstr "microwell-plate-gui" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Environment 'microwell-plate-gui' not found
    echo Creating environment from environment.yml...
    conda env create -f environment.yml
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create conda environment
        pause
        exit /b 1
    )
)

REM Activate environment and run application
echo Activating conda environment...
call conda activate microwell-plate-gui
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate conda environment
    pause
    exit /b 1
)

echo Starting application...
python -m microwell_plate_gui.main
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Application failed to start
    pause
    exit /b 1
)

echo Application closed successfully
pause
```

#### macOS/Linux Launcher (microwell-gui.sh)
```bash
#!/bin/bash
# Microwell Plate GUI Launcher for macOS/Linux
# This script automatically activates the conda environment and runs the application

set -e  # Exit on any error

echo "Starting Microwell Plate GUI..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH"
    echo "Please install Miniconda or Anaconda first"
    exit 1
fi

# Initialize conda for bash
eval "$(conda shell.bash hook)"

# Check if environment exists
if ! conda env list | grep -q "microwell-plate-gui"; then
    echo "Environment 'microwell-plate-gui' not found"
    echo "Creating environment from environment.yml..."
    conda env create -f environment.yml
fi

# Activate environment
echo "Activating conda environment..."
conda activate microwell-plate-gui

# Run application
echo "Starting application..."
python -m microwell_plate_gui.main

echo "Application closed successfully"
```

### Package Structure for Distribution

```
microwell-plate-gui-package/
├── README.md
├── INSTALL.md
├── LICENSE
├── environment.yml
├── environment-lock.yml
├── microwell-gui.bat          # Windows launcher
├── microwell-gui.sh           # macOS/Linux launcher
├── setup.py
├── pyproject.toml
├── src/
│   └── microwell_plate_gui/
│       ├── __init__.py
│       ├── main.py
│       ├── gui/
│       ├── data/
│       └── utils/
├── tests/
├── docs/
├── examples/
│   ├── example_database.db
│   ├── example_database.csv
│   └── sample_layouts/
└── scripts/
    ├── install.py
    ├── verify_installation.py
    └── create_desktop_shortcut.py
```

### Installation Script (install.py)

```python
#!/usr/bin/env python3
"""
Automated installation script for Microwell Plate GUI
This script sets up the conda environment and creates shortcuts
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_conda():
    """Check if conda is available"""
    try:
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Found conda: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Conda not found in PATH")
    print("Please install Miniconda or Anaconda:")
    print("  https://docs.conda.io/en/latest/miniconda.html")
    return False

def create_environment():
    """Create the conda environment"""
    print("Creating conda environment...")
    
    # Use lock file for exact reproducibility
    env_file = "environment-lock.yml" if Path("environment-lock.yml").exists() else "environment.yml"
    
    cmd = ['conda', 'env', 'create', '-f', env_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Environment created successfully")
        return True
    else:
        print(f"✗ Failed to create environment: {result.stderr}")
        return False

def verify_installation():
    """Verify the installation works"""
    print("Verifying installation...")
    
    # Test import in the new environment
    cmd = ['conda', 'run', '-n', 'microwell-plate-gui', 
           'python', '-c', 'import microwell_plate_gui; print("Import successful")']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Installation verified successfully")
        return True
    else:
        print(f"✗ Installation verification failed: {result.stderr}")
        return False

def create_shortcuts():
    """Create desktop shortcuts and start menu entries"""
    system = platform.system()
    
    if system == "Windows":
        create_windows_shortcuts()
    elif system == "Darwin":  # macOS
        create_macos_shortcuts()
    elif system == "Linux":
        create_linux_shortcuts()

def create_windows_shortcuts():
    """Create Windows shortcuts"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Microwell Plate GUI.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.abspath("microwell-gui.bat")
        shortcut.WorkingDirectory = os.path.abspath(".")
        shortcut.IconLocation = os.path.abspath("icon.ico") if os.path.exists("icon.ico") else ""
        shortcut.save()
        
        print("✓ Desktop shortcut created")
    except ImportError:
        print("! Could not create desktop shortcut (winshell not available)")
    except Exception as e:
        print(f"! Could not create desktop shortcut: {e}")

def create_macos_shortcuts():
    """Create macOS application bundle"""
    app_name = "Microwell Plate GUI.app"
    app_path = Path.home() / "Applications" / app_name
    
    try:
        # Create basic app bundle structure
        app_path.mkdir(parents=True, exist_ok=True)
        (app_path / "Contents").mkdir(exist_ok=True)
        (app_path / "Contents" / "MacOS").mkdir(exist_ok=True)
        
        # Create Info.plist
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>microwell-gui</string>
    <key>CFBundleIdentifier</key>
    <string>com.lab.microwell-plate-gui</string>
    <key>CFBundleName</key>
    <string>Microwell Plate GUI</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>"""
        
        with open(app_path / "Contents" / "Info.plist", "w") as f:
            f.write(plist_content)
        
        # Create executable script
        script_content = f"""#!/bin/bash
cd "{os.path.abspath('.')}"
./microwell-gui.sh
"""
        
        script_path = app_path / "Contents" / "MacOS" / "microwell-gui"
        with open(script_path, "w") as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print("✓ macOS application bundle created")
        
    except Exception as e:
        print(f"! Could not create macOS app bundle: {e}")

def create_linux_shortcuts():
    """Create Linux desktop entry"""
    try:
        desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Microwell Plate GUI
Comment=GUI tool for designing microwell plate layouts
Exec={os.path.abspath('microwell-gui.sh')}
Icon={os.path.abspath('icon.png') if os.path.exists('icon.png') else 'applications-science'}
Path={os.path.abspath('.')}
Terminal=false
Categories=Science;Education;
"""
        
        # Create desktop file
        desktop_path = Path.home() / ".local" / "share" / "applications"
        desktop_path.mkdir(parents=True, exist_ok=True)
        
        with open(desktop_path / "microwell-plate-gui.desktop", "w") as f:
            f.write(desktop_entry)
        
        print("✓ Linux desktop entry created")
        
    except Exception as e:
        print(f"! Could not create Linux desktop entry: {e}")

def main():
    """Main installation function"""
    print("Microwell Plate GUI Installation")
    print("=" * 40)
    
    # Check prerequisites
    if not check_conda():
        sys.exit(1)
    
    # Create environment
    if not create_environment():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        sys.exit(1)
    
    # Create shortcuts
    create_shortcuts()
    
    print("\n" + "=" * 40)
    print("✓ Installation completed successfully!")
    print("\nTo run the application:")
    
    system = platform.system()
    if system == "Windows":
        print("  - Double-click the desktop shortcut")
        print("  - Or run: microwell-gui.bat")
    else:
        print("  - Use the application launcher")
        print("  - Or run: ./microwell-gui.sh")
    
    print("\nFor help and documentation, see README.md")

if __name__ == "__main__":
    main()
```

### User Installation Instructions (INSTALL.md)

```markdown
# Installation Instructions

## Quick Start

### Option 1: Automated Installation (Recommended)
1. Download and extract the microwell-plate-gui package
2. Open terminal/command prompt in the extracted folder
3. Run the installation script:
   ```bash
   python install.py
   ```
4. Follow the on-screen instructions

### Option 2: Manual Installation
1. Install Miniconda or Anaconda if not already installed
2. Create the environment:
   ```bash
   conda env create -f environment.yml
   ```
3. Make launcher scripts executable (macOS/Linux):
   ```bash
   chmod +x microwell-gui.sh
   ```

## Running the Application

### Windows
- Double-click `microwell-gui.bat`
- Or from command prompt: `microwell-gui.bat`

### macOS/Linux
- Run: `./microwell-gui.sh`
- Or use the application launcher if shortcuts were created

## Troubleshooting

### Conda Not Found
If you get "conda not found" errors:
1. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
2. Restart your terminal/command prompt
3. Try the installation again

### Environment Creation Fails
If environment creation fails:
1. Update conda: `conda update conda`
2. Clear conda cache: `conda clean --all`
3. Try creating environment manually:
   ```bash
   conda env create -f environment-lock.yml
   ```

### Application Won't Start
If the application fails to start:
1. Verify environment is activated: `conda activate microwell-plate-gui`
2. Test import: `python -c "import microwell_plate_gui"`
3. Check for error messages in the terminal

### Database File Issues
If you get database-related errors:
1. Ensure `example_database.db` is in the same folder as the application
2. Check file permissions (should be readable)
3. Try running from the correct working directory

## Uninstallation

To remove the application:
1. Remove the conda environment:
   ```bash
   conda env remove -n microwell-plate-gui
   ```
2. Delete the application folder
3. Remove any desktop shortcuts created

## Support

For issues not covered here:
1. Check the README.md file
2. Review the user documentation in the docs/ folder
3. Contact your system administrator
```

### Verification Script (verify_installation.py)

```python
#!/usr/bin/env python3
"""
Installation verification script for Microwell Plate GUI
"""

import sys
import subprocess
import os
from pathlib import Path

def test_conda_environment():
    """Test that the conda environment exists and works"""
    print("Testing conda environment...")
    
    # Check if environment exists
    result = subprocess.run(['conda', 'env', 'list'], 
                          capture_output=True, text=True)
    
    if 'microwell-plate-gui' not in result.stdout:
        print("✗ Conda environment 'microwell-plate-gui' not found")
        return False
    
    print("✓ Conda environment found")
    
    # Test activation and import
    cmd = ['conda', 'run', '-n', 'microwell-plate-gui', 
           'python', '-c', 'import microwell_plate_gui; print("Import successful")']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Package import successful")
        return True
    else:
        print(f"✗ Package import failed: {result.stderr}")
        return False

def test_database_file():
    """Test that the database file exists and is readable"""
    print("Testing database file...")
    
    db_file = Path("example_database.db")
    if not db_file.exists():
        print("✗ Database file 'example_database.db' not found")
        return False
    
    if not os.access(db_file, os.R_OK):
        print("✗ Database file is not readable")
        return False
    
    print("✓ Database file found and readable")
    return True

def test_launcher_scripts():
    """Test that launcher scripts exist and are executable"""
    print("Testing launcher scripts...")
    
    import platform
    system = platform.system()
    
    if system == "Windows":
        script = Path("microwell-gui.bat")
    else:
        script = Path("microwell-gui.sh")
    
    if not script.exists():
        print(f"✗ Launcher script '{script}' not found")
        return False
    
    if system != "Windows" and not os.access(script, os.X_OK):
        print(f"✗ Launcher script '{script}' is not executable")
        print(f"  Run: chmod +x {script}")
        return False
    
    print("✓ Launcher script found and executable")
    return True

def main():
    """Run all verification tests"""
    print("Microwell Plate GUI Installation Verification")
    print("=" * 50)
    
    tests = [
        test_conda_environment,
        test_database_file,
        test_launcher_scripts
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    if all(results):
        print("✓ All tests passed! Installation is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

This setup ensures that users can easily install and run the application with the correct conda environment automatically activated, providing a seamless user experience while maintaining deterministic builds.