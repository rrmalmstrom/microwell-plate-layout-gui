"""
Test suite for metadata panel callback functionality.

Tests the "Other" field toggle callbacks and clear all metadata functionality.
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.gui.plate_canvas import PlateCanvas
from microwell_plate_gui.data.database import DatabaseManager


class TestMetadataCallbacks:
    """Test suite for metadata panel callback functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        
        # Create mock database manager
        self.mock_db = Mock(spec=DatabaseManager)
        self.mock_db.get_existing_samples.return_value = ["Sample1", "Sample2"]
        self.mock_db.generate_plate_names.return_value = ["Test.Sample1.1", "Test.Sample1.2"]
        
        # Create metadata panel
        self.metadata_panel = MetadataPanel(self.root, self.mock_db)
        
    def teardown_method(self):
        """Cleanup after tests."""
        if self.root:
            self.root.destroy()
    
    def test_sample_other_field_toggle_callback_signature(self):
        """Test that sample other field toggle accepts callback arguments."""
        # This should not raise an exception
        self.metadata_panel._toggle_sample_other_field("var", "index", "mode")
        
        # Verify the field is not shown when sample is not "other"
        assert not self.metadata_panel.sample_other_entry.winfo_viewable()
    
    def test_plate_name_other_field_toggle_callback_signature(self):
        """Test that plate name other field toggle accepts callback arguments."""
        # This should not raise an exception
        self.metadata_panel._toggle_plate_name_other_field("var", "index", "mode")
        
        # Verify the field is not shown when plate name is not "other"
        assert not self.metadata_panel.plate_name_other_entry.winfo_viewable()
    
    def test_sample_type_other_field_toggle_callback_signature(self):
        """Test that sample type other field toggle accepts callback arguments."""
        # This should not raise an exception
        self.metadata_panel._toggle_sample_type_other_field("var", "index", "mode")
        
        # Verify the field is not shown when sample type is not "other"
        assert not self.metadata_panel.sample_type_other_entry.winfo_viewable()
    
    def test_sample_other_field_shows_when_other_selected(self):
        """Test that sample other field appears when 'other' is selected."""
        # Ensure the main frame is properly configured
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Set sample to "other"
        self.metadata_panel.sample_var.set("other")
        
        # Trigger the callback
        self.metadata_panel._toggle_sample_other_field()
        
        # Update the GUI
        self.root.update_idletasks()
        self.root.update()
        
        # Check if the widget is managed by the grid manager
        grid_info = self.metadata_panel.sample_other_entry.grid_info()
        assert grid_info != {}, f"Widget not managed by grid: {grid_info}"
        
        # Check if the widget exists and is mapped
        assert self.metadata_panel.sample_other_entry.winfo_exists()
        assert self.metadata_panel.sample_other_entry.winfo_ismapped()
    
    def test_plate_name_other_field_shows_when_other_selected(self):
        """Test that plate name other field appears when 'other' is selected."""
        # Set plate name to "other"
        self.metadata_panel.plate_name_var.set("other")
        
        # Trigger the callback
        self.metadata_panel._toggle_plate_name_other_field()
        
        # Update the GUI
        self.root.update()
        
        # Verify the other field is now visible
        assert self.metadata_panel.plate_name_other_entry.winfo_viewable()
    
    def test_sample_type_other_field_shows_when_other_selected(self):
        """Test that sample type other field appears when 'other' is selected."""
        # Set sample type to "other"
        self.metadata_panel.sample_type_var.set("other")
        
        # Trigger the callback
        self.metadata_panel._toggle_sample_type_other_field()
        
        # Update the GUI
        self.root.update()
        
        # Verify the other field is now visible
        assert self.metadata_panel.sample_type_other_entry.winfo_viewable()
    
    def test_clear_all_metadata_button_exists(self):
        """Test that clear all metadata button exists."""
        assert hasattr(self.metadata_panel, 'clear_all_button')
        assert self.metadata_panel.clear_all_button.winfo_exists()
    
    def test_clear_all_metadata_callback_setup(self):
        """Test that clear all metadata callback can be set."""
        mock_callback = Mock()
        
        # Set the callback
        self.metadata_panel.set_clear_all_metadata_callback(mock_callback)
        
        # Verify it was set
        assert self.metadata_panel.clear_all_metadata_callback == mock_callback
    
    def test_clear_all_metadata_calls_callback(self):
        """Test that clear all metadata button calls the callback."""
        mock_callback = Mock()
        
        # Set the callback
        self.metadata_panel.set_clear_all_metadata_callback(mock_callback)
        
        # Trigger clear all metadata
        self.metadata_panel._clear_all_metadata()
        
        # Verify callback was called
        mock_callback.assert_called_once()
    
    def test_clear_all_metadata_without_callback(self):
        """Test that clear all metadata works without callback set."""
        # This should not raise an exception
        self.metadata_panel._clear_all_metadata()


class TestPlateCanvasClearMetadata:
    """Test suite for plate canvas clear all metadata functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        
        # Create plate canvas
        self.plate_canvas = PlateCanvas(self.root, "96-well")
        
    def teardown_method(self):
        """Cleanup after tests."""
        if self.root:
            self.root.destroy()
    
    def test_clear_all_metadata_method_exists(self):
        """Test that clear all metadata method exists."""
        assert hasattr(self.plate_canvas, 'clear_all_metadata')
        assert callable(self.plate_canvas.clear_all_metadata)
    
    def test_clear_all_metadata_clears_storage(self):
        """Test that clear all metadata clears the metadata storage."""
        # Add some test metadata
        test_metadata = {'sample': 'Test', 'sample_type': 'sample'}
        self.plate_canvas.well_metadata['A1'] = test_metadata
        self.plate_canvas.well_metadata['B2'] = test_metadata
        
        # Verify metadata exists
        assert len(self.plate_canvas.well_metadata) == 2
        
        # Clear all metadata
        self.plate_canvas.clear_all_metadata()
        
        # Verify metadata is cleared
        assert len(self.plate_canvas.well_metadata) == 0
    
    def test_clear_all_metadata_resets_well_colors(self):
        """Test that clear all metadata resets well colors to default."""
        # Apply metadata to a well first
        test_metadata = {'sample': 'Test', 'sample_type': 'pos_cntrl'}
        self.plate_canvas.well_metadata['A1'] = test_metadata
        self.plate_canvas._update_well_color('A1', 'pos_cntrl')
        
        # Verify well has metadata color
        well_info = self.plate_canvas.wells['A1']
        canvas_id = well_info['canvas_id']
        current_color = self.plate_canvas.canvas.itemcget(canvas_id, 'fill')
        assert current_color == self.plate_canvas.metadata_colors['pos_cntrl']
        
        # Clear all metadata
        self.plate_canvas.clear_all_metadata()
        
        # Verify well color is reset to default
        new_color = self.plate_canvas.canvas.itemcget(canvas_id, 'fill')
        assert new_color == self.plate_canvas.default_well_color
    
    def test_clear_all_metadata_preserves_selection_colors(self):
        """Test that clear all metadata preserves selection colors for selected wells."""
        # Select a well
        self.plate_canvas._select_well('A1')
        
        # Add metadata to the selected well
        test_metadata = {'sample': 'Test', 'sample_type': 'sample'}
        self.plate_canvas.well_metadata['A1'] = test_metadata
        
        # Clear all metadata
        self.plate_canvas.clear_all_metadata()
        
        # Verify selected well still has selection color
        well_info = self.plate_canvas.wells['A1']
        canvas_id = well_info['canvas_id']
        current_color = self.plate_canvas.canvas.itemcget(canvas_id, 'fill')
        assert current_color == self.plate_canvas.selection_color
    
    def test_clear_all_metadata_removes_well_metadata_attributes(self):
        """Test that clear all metadata removes metadata attributes from wells."""
        # Add metadata attributes to a well
        well_info = self.plate_canvas.wells['A1']
        well_info['metadata_color'] = '#90EE90'
        well_info['sample_type'] = 'sample'
        
        # Clear all metadata
        self.plate_canvas.clear_all_metadata()
        
        # Verify metadata attributes are removed
        assert 'metadata_color' not in well_info
        assert 'sample_type' not in well_info