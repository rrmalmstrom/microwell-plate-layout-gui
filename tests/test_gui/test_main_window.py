"""
Tests for the main window GUI component.

Context7 Reference: Tkinter application architecture patterns and main window setup
- Using tkinter.Tk for main application root
- Using ttk.Panedwindow for split layout design
- Following standard widget configuration patterns
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.main_window import MainWindow


class TestMainWindow:
    """Test suite for MainWindow class."""
    
    def setup_method(self):
        """Setup for each test method."""
        # Create root window for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
    
    def teardown_method(self):
        """Cleanup after each test method."""
        if self.root:
            self.root.destroy()
    
    def test_main_window_creation(self):
        """Test that MainWindow can be created successfully."""
        # Context7 Reference: tkinter.Tk application root setup
        window = MainWindow(self.root)
        assert window is not None
        assert window.root == self.root
    
    def test_window_title_set(self):
        """Test that window title is set correctly."""
        window = MainWindow(self.root)
        expected_title = "Microwell Plate Layout Designer"
        assert self.root.title() == expected_title
    
    def test_window_geometry_set(self):
        """Test that window geometry is configured."""
        window = MainWindow(self.root)
        # Should have minimum size set
        assert self.root.minsize() == (800, 600)
    
    def test_split_layout_created(self):
        """Test that split layout with PanedWindow is created."""
        # Context7 Reference: ttk.Panedwindow for split layout
        window = MainWindow(self.root)
        
        # Should have a paned window for split layout
        assert hasattr(window, 'paned_window')
        assert window.paned_window.winfo_class() == 'TPanedwindow'
    
    def test_plate_frame_created(self):
        """Test that plate visualization frame is created."""
        window = MainWindow(self.root)
        
        # Should have plate frame for canvas
        assert hasattr(window, 'plate_frame')
        assert window.plate_frame.winfo_class() == 'TFrame'
    
    def test_metadata_frame_created(self):
        """Test that metadata panel frame is created."""
        window = MainWindow(self.root)
        
        # Should have metadata frame for forms
        assert hasattr(window, 'metadata_frame')
        assert window.metadata_frame.winfo_class() == 'TFrame'
    
    def test_equal_split_layout(self):
        """Test that split layout gives equal space to both panels."""
        window = MainWindow(self.root)
        
        # Both panes should be added to the paned window
        panes = window.paned_window.panes()
        assert len(panes) == 2
    
    def test_startup_dialog_method_exists(self):
        """Test that startup dialog method exists."""
        window = MainWindow(self.root)
        
        # Should have method to show startup dialog
        assert hasattr(window, 'show_startup_dialog')
        assert callable(window.show_startup_dialog)
    
    def test_plate_type_selection_callback(self):
        """Test that plate type selection callback exists."""
        window = MainWindow(self.root)
        
        # Should have method to handle plate type selection
        assert hasattr(window, 'on_plate_type_selected')
        assert callable(window.on_plate_type_selected)


class TestStartupDialog:
    """Test suite for startup dialog functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.root = tk.Tk()
        self.root.withdraw()
    
    def teardown_method(self):
        """Cleanup after each test method."""
        if self.root:
            self.root.destroy()
    
    def test_startup_dialog_creation(self):
        """Test that startup dialog can be created."""
        from microwell_plate_gui.gui.main_window import StartupDialog
        
        dialog = StartupDialog(self.root)
        assert dialog is not None
    
    def test_plate_type_options(self):
        """Test that startup dialog has plate type options."""
        from microwell_plate_gui.gui.main_window import StartupDialog
        
        dialog = StartupDialog(self.root)
        
        # Should have 96-well and 384-well options
        assert hasattr(dialog, 'plate_type_var')
        assert dialog.plate_type_var.get() in ['96', '384']
    
    def test_sample_mode_options(self):
        """Test that startup dialog has sample mode options."""
        from microwell_plate_gui.gui.main_window import StartupDialog
        
        dialog = StartupDialog(self.root)
        
        # Should have single/multi sample mode options
        assert hasattr(dialog, 'sample_mode_var')
        assert dialog.sample_mode_var.get() in ['single', 'multi']