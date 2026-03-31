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
if conda env list | grep -q "microwell-gui"; then
    echo "⚠️  Environment 'microwell-gui' already exists."
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing environment..."
        conda env remove -n microwell-gui -y
    else
        echo "✅ Using existing environment."
        echo "Setup complete! You can now double-click: 🧬 Start Microwell GUI.command"
        exit 0
    fi
fi

# Create the conda environment with smart fallback strategy
echo "📦 Creating conda environment 'microwell-gui'..."
echo "This may take a few minutes to download and install packages..."

# Try the minimal environment.yml first (most likely to succeed)
if conda env create -f environment.yml; then
    echo "✅ Environment created successfully with minimal configuration"
    echo "   Only essential packages installed (python + ghostscript + pip)"
elif [ -f "environment_conservative.yml" ]; then
    echo "⚠️  Minimal environment failed, trying conservative configuration..."
    conda env create -f environment_conservative.yml
    if [ $? -eq 0 ]; then
        echo "✅ Environment created successfully with conservative configuration"
        echo "   Additional packages included for maximum compatibility"
    else
        echo "❌ Both validated environment configurations failed"
        echo "Trying manual installation approach..."
        
        # Create environment with just Python and essential packages
        conda create -n microwell-gui "python>=3.11,<3.13" pip -y
        eval "$(conda shell.bash hook)"
        conda activate microwell-gui
        
        # Install ghostscript (essential for PDF export)
        echo "Installing essential packages individually..."
        conda install ghostscript -c conda-forge -y || {
            echo "⚠️  Ghostscript installation failed - PDF export may not work"
        }
        
        # Install optional packages that might be needed
        conda install numpy pandas -c conda-forge -y || {
            echo "⚠️  Some optional packages failed, trying pip installation..."
            pip install numpy pandas
        }
        
        echo "✅ Manual environment created with fallback packages"
    fi
else
    echo "❌ Environment creation failed and no conservative configuration found"
    echo "Please check your conda installation and internet connection"
    exit 1
fi

# Make the launcher executable
if [ -f "_internal_launcher.sh" ]; then
    echo "🔧 Making launcher script executable..."
    chmod +x _internal_launcher.sh
else
    echo "⚠️  Warning: _internal_launcher.sh not found"
fi

# Test that the environment works
echo "🧪 Testing the environment..."
conda activate microwell-gui

# Run comprehensive validation if test script exists
if [ -f "tests/test_environment.py" ]; then
    echo "Running comprehensive environment validation..."
    python tests/test_environment.py || {
        echo "❌ Error: Environment validation failed"
        echo "Some functionality may not work properly"
        echo "Consider using the conservative environment instead"
    }
else
    # Fallback to basic import test
    echo "Running basic import test..."
    python -c "
import sys
try:
    import tkinter
    print('✅ tkinter (GUI framework) available')
    import sqlite3
    print('✅ sqlite3 (database) available')
    import os, csv, logging, subprocess
    print('✅ Standard library modules available')
    
    # Test ghostscript availability
    import subprocess
    result = subprocess.run(['gs', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ ghostscript available for PDF export')
    else:
        print('⚠️  ghostscript may not be available - PDF export might not work')
    
    print('✅ Core functionality should work')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'⚠️  Warning: {e}')
" || {
        echo "❌ Error: Basic environment test failed"
        exit 1
    }
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application daily, simply double-click:"
echo "  🧬 Start Microwell GUI.command"
echo ""
echo "The setup created a conda environment called 'microwell-gui'"
echo "that contains all the required dependencies."
echo ""