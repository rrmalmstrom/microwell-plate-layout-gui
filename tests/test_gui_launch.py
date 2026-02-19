#!/usr/bin/env python3
"""
Test script to verify GUI launches in minimal environment
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add src to path
src_path = Path.cwd() / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def test_gui_launch():
    """Test that the GUI can be created and destroyed quickly"""
    try:
        print("Testing GUI launch...")
        
        # Import the main application
        from microwell_plate_gui.gui.main_window import MainWindow
        
        # Create root window
        root = tk.Tk()
        root.withdraw()  # Hide initially
        
        # Create main window
        app = MainWindow(root)
        print("✅ GUI created successfully")
        
        # Schedule window to close after 1 second
        root.after(1000, root.quit)
        
        # Show window briefly
        root.deiconify()
        print("✅ GUI displayed")
        
        # Run for 1 second then quit
        root.mainloop()
        
        # Clean up
        root.destroy()
        print("✅ GUI closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gui_launch()
    print(f"\nGUI Launch Test: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)