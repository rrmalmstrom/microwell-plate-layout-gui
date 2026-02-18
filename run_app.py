#!/usr/bin/env python3
"""
Entry point script for the Microwell Plate GUI application.

This script provides a proper entry point that handles Python package imports correctly.
Context7 Reference: Standard Python application entry point patterns
"""

import sys
import os
import argparse

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Now we can import the application
from microwell_plate_gui.main import main

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Microwell Plate GUI Application')
    parser.add_argument('project_directory', nargs='?', default=None,
                       help='Path to project directory containing database files')
    
    args = parser.parse_args()
    
    # Call main with project directory
    main(args.project_directory)