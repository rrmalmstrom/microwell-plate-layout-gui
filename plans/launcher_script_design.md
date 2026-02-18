# Launcher Script Design

## Simple macOS Launcher (`launch_microwell_gui.sh`)

```bash
#!/bin/bash
# Microwell Plate GUI Launcher for macOS
# Simple launcher script for lab colleagues

set -e  # Exit on any error

echo "🧬 Starting Microwell Plate GUI..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda is not installed or not in PATH"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Initialize conda for bash (required for conda activate)
eval "$(conda shell.bash hook)"

# Check if the environment exists
if ! conda env list | grep -q "microwell-plate-gui"; then
    echo "❌ Error: Environment 'microwell-plate-gui' not found"
    echo "Please create the environment first:"
    echo "  conda env create -f environment.yml"
    exit 1
fi

# Activate the environment
echo "🔧 Activating conda environment..."
conda activate microwell-plate-gui

# Check if we're in the right directory (look for run_app.py)
if [ ! -f "run_app.py" ]; then
    echo "❌ Error: run_app.py not found in current directory"
    echo "Please run this script from the microwell-plate-gui directory"
    exit 1
fi

# Launch the application
echo "🚀 Launching application..."
python run_app.py

echo "✅ Application closed successfully"
```

## Key Features

### Simplicity
- Single shell script for macOS
- No cross-platform complexity
- Clear error messages with helpful instructions

### Error Handling
- Checks for conda installation
- Verifies environment exists
- Confirms correct working directory
- Provides actionable error messages

### User Experience
- Friendly emoji indicators
- Clear status messages
- Helpful error instructions
- Automatic environment activation

### Reliability
- Uses `set -e` for fail-fast behavior
- Proper conda shell initialization
- Directory validation before launch

## Usage Instructions

1. Make executable: `chmod +x launch_microwell_gui.sh`
2. Run: `./launch_microwell_gui.sh`

## Error Scenarios Handled

1. **Conda not installed**: Provides installation link
2. **Environment missing**: Shows creation command
3. **Wrong directory**: Explains where to run from
4. **Application failure**: Exits cleanly with error code

This launcher eliminates the need for users to remember conda commands or worry about environment activation.