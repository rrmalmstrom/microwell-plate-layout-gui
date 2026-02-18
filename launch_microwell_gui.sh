#!/bin/bash
# Microwell Plate GUI Launcher for macOS
# Simple launcher script for lab colleagues
#
# Usage:
#   ./launch_microwell_gui.sh [project_directory]
#
# If no project_directory is provided, uses current directory

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

# Check if the environment exists (suppress conda warnings)
if ! conda env list 2>/dev/null | grep -q "microwell-gui-dev"; then
    echo "❌ Error: Environment 'microwell-gui-dev' not found"
    echo "Please create the environment first:"
    echo "  conda env create -f environment.yml"
    exit 1
fi

# Activate the environment
echo "🔧 Activating conda environment..."
conda activate microwell-gui-dev 2>/dev/null

# Determine the project directory (where user data files are)
if [ $# -eq 0 ]; then
    # No argument provided, prompt user for project directory
    echo ""
    echo "📁 Please specify your project directory (where your data files are located):"
    echo ""
    echo "Options:"
    echo "  1. Press ENTER to use current directory: $(pwd)"
    echo "  2. Type the full path to your project directory"
    echo "  3. Drag and drop your project folder here and press ENTER"
    echo ""
    read -p "Project directory [current: $(pwd)]: " user_input
    
    if [ -z "$user_input" ]; then
        # User pressed enter without input, use current directory
        PROJECT_DIR="$(pwd)"
        echo "📁 Using current directory as project directory: $PROJECT_DIR"
    else
        # User provided input, validate it
        # Remove any trailing whitespace and quotes that might come from drag-drop
        user_input=$(echo "$user_input" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;s/^"//;s/"$//')
        
        if [ -d "$user_input" ]; then
            PROJECT_DIR="$(cd "$user_input" && pwd 2>/dev/null)" || {
                echo "❌ Error: Cannot access project directory: $user_input"
                exit 1
            }
            echo "📁 Using specified project directory: $PROJECT_DIR"
        else
            echo "❌ Error: Directory does not exist: $user_input"
            exit 1
        fi
    fi
elif [ $# -eq 1 ]; then
    # Project directory provided as argument
    PROJECT_DIR="$(cd "$1" && pwd 2>/dev/null)" || {
        echo "❌ Error: Cannot access project directory: $1"
        exit 1
    }
    echo "📁 Using specified project directory: $PROJECT_DIR"
else
    echo "❌ Error: Too many arguments"
    echo "Usage: $0 [project_directory]"
    exit 1
fi

# Find the installation directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we can find run_app.py in the installation directory
if [ ! -f "$SCRIPT_DIR/run_app.py" ]; then
    echo "❌ Error: run_app.py not found in installation directory: $SCRIPT_DIR"
    echo "Please ensure the microwell-plate-gui installation is complete"
    exit 1
fi

# Launch the application
echo "🚀 Launching application..."
echo "📦 Installation directory: $SCRIPT_DIR"
echo "📁 Project directory: $PROJECT_DIR"

# Run the app from installation directory, passing project directory as argument
python "$SCRIPT_DIR/run_app.py" "$PROJECT_DIR"

echo "✅ Application closed successfully"