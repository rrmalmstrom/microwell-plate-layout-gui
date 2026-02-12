#!/usr/bin/env python3
"""
Entry point script for the Microwell Plate GUI application.

This script provides a proper entry point that handles Python package imports correctly.
Context7 Reference: Standard Python application entry point patterns
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Now we can import the application
from microwell_plate_gui.main import main

if __name__ == "__main__":
    main()