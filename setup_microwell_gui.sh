#!/bin/bash
# Microwell Plate GUI Setup Script for macOS
# One-time setup for lab colleagues

set -e  # Exit on any error

echo "🧬 Setting up Microwell Plate GUI..."
echo "This is a one-time setup process that should take about 5 minutes."
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda is not installed or not in PATH"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    echo "Then restart your terminal and run this setup script again."
    exit 1
fi

# Initialize conda for bash (required for conda activate)
eval "$(conda shell.bash hook)"

# Check if environment.yml exists
if [ ! -f "environment.yml" ]; then
    echo "❌ Error: environment.yml not found in current directory"
    echo "Please run this script from the microwell-plate-gui directory"
    exit 1
fi

# Check if the environment already exists
if conda env list | grep -q "microwell-gui-dev"; then
    echo "⚠️  Environment 'microwell-gui-dev' already exists."
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing environment..."
        conda env remove -n microwell-gui-dev -y
    else
        echo "✅ Using existing environment."
        echo "Setup complete! You can now run: ./launch_microwell_gui.sh"
        exit 0
    fi
fi

# Create the conda environment
echo "📦 Creating conda environment 'microwell-gui-dev'..."
echo "This may take a few minutes to download and install packages..."
conda env create -f environment.yml

# Make the launcher executable
if [ -f "launch_microwell_gui.sh" ]; then
    echo "🔧 Making launcher script executable..."
    chmod +x launch_microwell_gui.sh
else
    echo "⚠️  Warning: launch_microwell_gui.sh not found"
fi

# Test that the environment works
echo "🧪 Testing the environment..."
conda activate microwell-gui-dev

# Check if we can import the main modules
python -c "import tkinter; import sqlite3; import pandas; import numpy; print('✅ All required modules available')" || {
    echo "❌ Error: Some required modules are missing"
    exit 1
}

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application daily, simply use:"
echo "  ./launch_microwell_gui.sh"
echo ""
echo "The setup created a conda environment called 'microwell-gui-dev'"
echo "that contains all the required dependencies."
echo ""