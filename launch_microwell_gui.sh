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