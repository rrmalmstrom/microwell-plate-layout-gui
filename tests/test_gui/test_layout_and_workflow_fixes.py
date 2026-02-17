"""
Test suite for layout and workflow fixes in Phase 3.

This module tests the fixes implemented for:
1. Multi-sample mode sample dropdown visibility
2. Layout improvements with proper PanedWindow sizing
3. Plate canvas sizing improvements
4. Title display with plate name information
"""

import pytest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.data.database import DatabaseManager


class TestLayoutAndWorkflowFixes:
    """Test suite for layout and workflow fixes."""
    
    def setup_method(self):
        """Setup test environment."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Create test database
        self.db_path = "test_layout_fixes.db"
        self.db_manager = DatabaseManager(self.db_path)
        
        # Create main window
        self.main_window = MainWindow(self.root, self.db_path)
    
    def teardown_method(self):
        """Cleanup test environment."""
        if hasattr(self, 'root'):
            self.root.destroy()
        
        # Clean up test database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_multi_sample_mode_metadata_panel_configuration(self):
        """Test that multi-sample mode shows sample dropdown in metadata panel."""
        # Simulate multi-sample mode configuration
        self.main_window.sample_mode = "multi"
        self.main_window.plate_type = "96"
        self.main_window.multi_sample_config = {'sample_plate_name': 'TestPlate'}
        
        # Initialize the plate interface
        self.main_window._initialize_plate_interface()
        
        # Check that metadata panel exists
        assert self.main_window.metadata_panel is not None
        
        # Check that sample dropdown is visible (not removed from grid)
        sample_combo_info = self.main_window.metadata_panel.sample_combo.grid_info()
        assert sample_combo_info != {}, "Sample dropdown should be visible in multi-sample mode"
        
        # Check that plate name dropdown is hidden (removed from grid)
        plate_name_combo_info = self.main_window.metadata_panel.plate_name_combo.grid_info()
        assert plate_name_combo_info == {}, "Plate name dropdown should be hidden in multi-sample mode"
        
        # Check that sample label is visible
        sample_label_info = self.main_window.metadata_panel.sample_label.grid_info()
        assert sample_label_info != {}, "Sample label should be visible in multi-sample mode"
    
    def test_single_sample_mode_metadata_panel_configuration(self):
        """Test that single-sample mode hides both sample and plate dropdowns."""
        # Simulate single-sample mode configuration
        self.main_window.sample_mode = "single"
        self.main_window.plate_type = "96"
        self.main_window.single_sample_config = {
            'sample': 'TestSample',
            'plate_name': 'TestPlate'
        }
        
        # Initialize the plate interface
        self.main_window._initialize_plate_interface()
        
        # Check that metadata panel exists
        assert self.main_window.metadata_panel is not None
        
        # Check that both sample and plate name dropdowns are hidden
        sample_combo_info = self.main_window.metadata_panel.sample_combo.grid_info()
        assert sample_combo_info == {}, "Sample dropdown should be hidden in single-sample mode"
        
        plate_name_combo_info = self.main_window.metadata_panel.plate_name_combo.grid_info()
        assert plate_name_combo_info == {}, "Plate name dropdown should be hidden in single-sample mode"
    
    def test_window_title_includes_plate_information(self):
        """Test that window title includes plate name information."""
        # Test single-sample mode title
        self.main_window.sample_mode = "single"
        self.main_window.plate_type = "96"
        self.main_window.single_sample_config = {
            'sample': 'TestSample',
            'plate_name': 'TestPlate'
        }
        
        self.main_window._initialize_plate_interface()
        
        title = self.root.title()
        assert "96-well" in title, "Title should include plate type"
        assert "single sample" in title, "Title should include sample mode"
        assert "TestSample" in title, "Title should include sample name"
        
        # Test multi-sample mode title
        self.main_window.sample_mode = "multi"
        self.main_window.plate_type = "384"
        self.main_window.multi_sample_config = {'sample_plate_name': 'MultiTestPlate'}
        
        self.main_window._initialize_plate_interface()
        
        title = self.root.title()
        assert "384-well" in title, "Title should include plate type"
        assert "multi sample" in title, "Title should include sample mode"
        assert "MultiTestPlate" in title, "Title should include plate name"
    
    def test_paned_window_layout_configuration(self):
        """Test that PanedWindow layout has proper weight distribution."""
        # Check main horizontal paned window
        assert hasattr(self.main_window, 'paned_window')
        assert isinstance(self.main_window.paned_window, ttk.Panedwindow)
        
        # Check that frames are added to paned window
        panes = self.main_window.paned_window.panes()
        assert len(panes) == 2, "Should have two panes (plate and right panel)"
        
        # Check right panel vertical paned window
        assert hasattr(self.main_window, 'right_paned_window')
        assert isinstance(self.main_window.right_paned_window, ttk.Panedwindow)
        
        right_panes = self.main_window.right_paned_window.panes()
        assert len(right_panes) == 2, "Should have two right panes (metadata and legend)"
    
    def test_plate_canvas_sizing_improvements(self):
        """Test that plate canvas uses improved sizing parameters."""
        # Simulate plate creation
        self.main_window.sample_mode = "single"
        self.main_window.plate_type = "96"
        self.main_window.single_sample_config = {
            'sample': 'TestSample',
            'plate_name': 'TestPlate'
        }
        
        self.main_window._initialize_plate_interface()
        
        # Check that plate canvas was created
        assert self.main_window.plate_canvas is not None
        
        # Check that canvas has reasonable dimensions (should be larger than default)
        canvas = self.main_window.plate_canvas.canvas
        canvas_width = canvas.winfo_reqwidth()
        canvas_height = canvas.winfo_reqheight()
        
        # For 96-well plate with well_size=25, should be larger than old default (well_size=20)
        assert canvas_width > 300, f"Canvas width {canvas_width} should be reasonable for 96-well plate"
        assert canvas_height > 200, f"Canvas height {canvas_height} should be reasonable for 96-well plate"
    
    def test_configuration_display_panel(self):
        """Test that configuration display panel shows correct information."""
        # Test single-sample mode configuration display
        self.main_window.sample_mode = "single"
        self.main_window.plate_type = "96"
        self.main_window.single_sample_config = {
            'sample': 'TestSample',
            'plate_name': 'TestPlate'
        }
        
        self.main_window._initialize_plate_interface()
        
        # Check that configuration display frame was created
        assert hasattr(self.main_window, 'config_display_frame')
        assert self.main_window.config_display_frame is not None
        
        # Test multi-sample mode configuration display
        self.main_window.sample_mode = "multi"
        self.main_window.multi_sample_config = {'sample_plate_name': 'MultiTestPlate'}
        
        self.main_window._initialize_plate_interface()
        
        # Configuration display should still exist
        assert self.main_window.config_display_frame is not None
    
    def test_metadata_panel_grid_layout_for_multi_sample(self):
        """Test that metadata panel grid layout is correct for multi-sample mode."""
        # Create a standalone metadata panel for testing
        test_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(test_frame, self.db_manager)
        
        # Simulate multi-sample mode configuration
        metadata_panel.hide_plate_name_field()
        
        # Check that sample widgets are positioned correctly
        sample_label_info = metadata_panel.sample_label.grid_info()
        sample_combo_info = metadata_panel.sample_combo.grid_info()
        
        assert sample_label_info['row'] == 1, "Sample label should be in row 1"
        assert sample_combo_info['row'] == 1, "Sample combo should be in row 1"
        
        # Check that sample type is positioned correctly (should be in row 2)
        sample_type_label_info = metadata_panel.sample_type_label.grid_info()
        sample_type_combo_info = metadata_panel.sample_type_combo.grid_info()
        
        assert sample_type_label_info['row'] == 2, "Sample type label should be in row 2"
        assert sample_type_combo_info['row'] == 2, "Sample type combo should be in row 2"
    
    def test_metadata_panel_other_field_functionality_in_multi_sample(self):
        """Test that 'Other' fields work correctly in multi-sample mode."""
        # Create a standalone metadata panel for testing
        test_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(test_frame, self.db_manager)
        
        # Configure for multi-sample mode
        metadata_panel.hide_plate_name_field()
        
        # Test sample "Other" field
        metadata_panel.sample_var.set("other")
        
        # Check that sample other field is visible
        sample_other_info = metadata_panel.sample_other_entry.grid_info()
        assert sample_other_info != {}, "Sample other field should be visible when 'other' is selected"
        assert sample_other_info['column'] == 2, "Sample other field should be in column 2"
        
        # Test sample type "Other" field
        metadata_panel.sample_type_var.set("other")
        
        # Check that sample type other field is visible
        sample_type_other_info = metadata_panel.sample_type_other_entry.grid_info()
        assert sample_type_other_info != {}, "Sample type other field should be visible when 'other' is selected"
        assert sample_type_other_info['column'] == 2, "Sample type other field should be in column 2"


class TestMetadataPanelMultiSampleMode:
    """Focused tests for metadata panel multi-sample mode functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Create test database
        self.db_path = "test_metadata_multi.db"
        self.db_manager = DatabaseManager(self.db_path)
        
        # Create test frame and metadata panel
        self.test_frame = ttk.Frame(self.root)
        self.metadata_panel = MetadataPanel(self.test_frame, self.db_manager)
    
    def teardown_method(self):
        """Cleanup test environment."""
        if hasattr(self, 'root'):
            self.root.destroy()
        
        # Clean up test database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_adjust_grid_layout_for_multi_sample_mode(self):
        """Test the new _adjust_grid_layout_for_multi_sample_mode method."""
        # Call the new method
        self.metadata_panel._adjust_grid_layout_for_multi_sample_mode()
        
        # Check that sample widgets are visible and positioned correctly
        sample_label_info = self.metadata_panel.sample_label.grid_info()
        sample_combo_info = self.metadata_panel.sample_combo.grid_info()
        
        assert sample_label_info != {}, "Sample label should be visible"
        assert sample_combo_info != {}, "Sample combo should be visible"
        assert sample_label_info['row'] == 1, "Sample label should be in row 1"
        assert sample_combo_info['row'] == 1, "Sample combo should be in row 1"
        
        # Check that sample type follows sample
        sample_type_label_info = self.metadata_panel.sample_type_label.grid_info()
        sample_type_combo_info = self.metadata_panel.sample_type_combo.grid_info()
        
        assert sample_type_label_info['row'] == 2, "Sample type should be in row 2"
        assert sample_type_combo_info['row'] == 2, "Sample type combo should be in row 2"
    
    def test_hide_plate_name_field_calls_correct_layout_method(self):
        """Test that hide_plate_name_field calls the multi-sample layout method."""
        # Initially, plate name widgets should be visible
        plate_name_label_info = self.metadata_panel.plate_name_label.grid_info()
        plate_name_combo_info = self.metadata_panel.plate_name_combo.grid_info()
        
        assert plate_name_label_info != {}, "Plate name label should initially be visible"
        assert plate_name_combo_info != {}, "Plate name combo should initially be visible"
        
        # Call hide_plate_name_field
        self.metadata_panel.hide_plate_name_field()
        
        # Check that plate name widgets are now hidden
        plate_name_label_info = self.metadata_panel.plate_name_label.grid_info()
        plate_name_combo_info = self.metadata_panel.plate_name_combo.grid_info()
        
        assert plate_name_label_info == {}, "Plate name label should be hidden"
        assert plate_name_combo_info == {}, "Plate name combo should be hidden"
        
        # Check that sample widgets are still visible (multi-sample mode)
        sample_label_info = self.metadata_panel.sample_label.grid_info()
        sample_combo_info = self.metadata_panel.sample_combo.grid_info()
        
        assert sample_label_info != {}, "Sample label should remain visible in multi-sample mode"
        assert sample_combo_info != {}, "Sample combo should remain visible in multi-sample mode"