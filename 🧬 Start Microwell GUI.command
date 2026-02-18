#!/bin/bash
# Microwell Plate GUI Launcher - Double-clickable from Finder
# This .command file can be double-clicked to launch the application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the launch script
./_internal_launcher.sh

# Keep terminal open after execution (optional)
echo ""
echo "Press any key to close this window..."
read -n 1 -s