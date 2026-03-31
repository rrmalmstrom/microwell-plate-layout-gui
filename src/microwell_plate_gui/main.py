"""
Main entry point for the Microwell Plate GUI application.

This module provides the main function to launch the GUI application.
Context7 Reference: Tkinter application architecture with proper main loop setup
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microwell_plate_gui.gui.main_window import MainWindow


def _check_ghostscript():
    """
    Check whether Ghostscript (gs / ps2pdf) is available and return its version string.

    Returns:
        str: Version string (e.g. "10.06.0") if found, or None if not available.
    """
    for cmd in (['gs', '--version'], ['ps2pdf', '--version']):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                return version
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
            continue
    return None


def main(project_directory=None):
    """
    Main entry point for the application.
    
    Args:
        project_directory (str, optional): Path to the project directory where data files are located.
                                         If None, uses current working directory.
    
    Context7 Reference: Standard Tkinter application startup pattern
    - Create root window
    - Initialize main window
    - Show startup dialog
    - Start main loop
    """
    try:
        # Set the project directory (where user data files are located)
        if project_directory is None:
            project_directory = os.getcwd()
        
        # Ensure the project directory exists
        if not os.path.isdir(project_directory):
            raise ValueError(f"Project directory does not exist: {project_directory}")
        
        print(f"  📁 Project directory: {project_directory}")
        
        # Create root window
        root = tk.Tk()

        # Check Ghostscript availability and warn early if missing
        gs_version = _check_ghostscript()
        if gs_version:
            print(f"  ✅ Ghostscript {gs_version} detected — PDF export available")
        else:
            print("  ⚠️  Ghostscript not found — PDF export will not work")
            messagebox.showwarning(
                "PDF Export Unavailable",
                "Ghostscript is not installed or not on PATH.\n\n"
                "You can still use the app and export CSV files, "
                "but PDF export will not work.\n\n"
                "To fix, run in Terminal:\n"
                "  conda install ghostscript -c conda-forge\n\n"
                f"(Ghostscript 10.x required, tested on 10.06.0)"
            )

        # Create main window with project directory
        app = MainWindow(root, project_directory)
        
        # Show startup dialog
        if not app.show_startup_dialog():
            # User cancelled, exit application
            root.destroy()
            return
        
        # Update window title with selected configuration
        app.on_plate_type_selected(app.plate_type, app.sample_mode)
        
        # Start main event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()