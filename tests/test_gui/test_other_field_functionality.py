"""
Test suite for "Other" field functionality in MetadataPanel.

This test suite validates the Context7-based fixes for dynamic form field handling,
specifically testing Entry widget state management and grid layout positioning.
"""

import pytest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.data.database import DatabaseManager


class TestOtherFieldFunctionality:
    """Test suite for "Other" field functionality with Context7 fixes."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Create a test database manager
        self.db_manager = DatabaseManager(":memory:")
        
        # Create the metadata panel
        self.panel = MetadataPanel(self.root, self.db_manager)
    
    def teardown_method(self):
        """Clean up after each test."""
        if self.root:
            self.root.destroy()
    
    def test_sample_type_other_field_visibility(self):
        """Test that sample type 'Other' field shows/hides correctly."""
        # Initially, the other field should not be in the grid
        assert self.panel.sample_type_other_entry.grid_info() == {}
        
        # Select "other" from sample type dropdown
        self.panel.sample_type_var.set("other")
        self.root.update()  # Process pending events
        
        # Now the other field should be in the grid at the correct position
        grid_info = self.panel.sample_type_other_entry.grid_info()
        assert grid_info != {}
        assert grid_info['row'] == self.panel.sample_type_row
        assert grid_info['column'] == 2
        
        # Select a different option
        self.panel.sample_type_var.set("sample")
        self.root.update()
        
        # Other field should be removed from grid again
        assert self.panel.sample_type_other_entry.grid_info() == {}
    
    def test_sample_type_other_field_state_and_focus(self):
        """Test that sample type 'Other' field is properly editable and focusable."""
        # Select "other" to show the field
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Check that the entry widget is in normal state (editable)
        assert str(self.panel.sample_type_other_entry.cget('state')) == 'normal'
        
        # Check that the entry widget can accept focus (focus_set doesn't fail)
        # Note: We can't test actual focus when root window is withdrawn
        try:
            self.panel.sample_type_other_entry.focus_set()
            focus_set_successful = True
        except Exception:
            focus_set_successful = False
        
        assert focus_set_successful
    
    def test_sample_type_other_field_text_input(self):
        """Test that user can type into the sample type 'Other' field."""
        # Select "other" to show the field
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Clear any existing text
        self.panel.sample_type_other_var.set("")
        
        # Simulate typing into the field
        test_text = "custom_sample_type"
        self.panel.sample_type_other_var.set(test_text)
        
        # Verify the text was set correctly
        assert self.panel.sample_type_other_entry.get() == test_text
        assert self.panel.sample_type_other_var.get() == test_text
    
    def test_sample_other_field_functionality(self):
        """Test sample 'Other' field functionality."""
        # Initially not in grid
        assert self.panel.sample_other_entry.grid_info() == {}
        
        # Show by selecting "other"
        self.panel.sample_var.set("other")
        self.root.update()
        
        # Should be in grid and editable
        assert self.panel.sample_other_entry.grid_info() != {}
        assert str(self.panel.sample_other_entry.cget('state')) == 'normal'
        
        # Test text input
        test_text = "custom_sample"
        self.panel.sample_other_var.set(test_text)
        assert self.panel.sample_other_entry.get() == test_text
    
    def test_plate_name_other_field_functionality(self):
        """Test plate name 'Other' field functionality."""
        # Initially not in grid
        assert self.panel.plate_name_other_entry.grid_info() == {}
        
        # Show by selecting "other"
        self.panel.plate_name_var.set("other")
        self.root.update()
        
        # Should be in grid and editable
        assert self.panel.plate_name_other_entry.grid_info() != {}
        assert str(self.panel.plate_name_other_entry.cget('state')) == 'normal'
        
        # Test text input
        test_text = "custom_plate"
        self.panel.plate_name_other_var.set(test_text)
        assert self.panel.plate_name_other_entry.get() == test_text
    
    def test_grid_layout_positioning(self):
        """Test that 'Other' fields are positioned correctly in the grid."""
        # Test sample type other field positioning
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Get grid info for the sample type other field
        other_grid_info = self.panel.sample_type_other_entry.grid_info()
        
        # Should be positioned in the same row as sample type dropdown, but in column 2
        expected_row = self.panel.sample_type_row
        assert other_grid_info['row'] == expected_row
        assert other_grid_info['column'] == 2
        
        # Test sample other field positioning
        self.panel.sample_var.set("other")
        self.root.update()
        
        sample_other_grid_info = self.panel.sample_other_entry.grid_info()
        assert sample_other_grid_info['row'] == self.panel.sample_row
        assert sample_other_grid_info['column'] == 2
        
        # Test plate name other field positioning
        self.panel.plate_name_var.set("other")
        self.root.update()
        
        plate_other_grid_info = self.panel.plate_name_other_entry.grid_info()
        assert plate_other_grid_info['row'] == self.panel.plate_name_row
        assert plate_other_grid_info['column'] == 2
    
    def test_widget_position_restoration(self):
        """Test that widgets return to original positions when 'Other' field is hidden."""
        # Record original positions
        original_cell_count_row = self.panel.cell_count_row
        original_group1_row = self.panel.group1_row
        
        # Show sample type other field (this should shift other widgets down)
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Hide the other field
        self.panel.sample_type_var.set("sample")
        self.root.update()
        
        # Check that widgets are back in their original positions
        cell_count_grid_info = self.panel.cell_count_entry.grid_info()
        group1_grid_info = self.panel.group1_entry.grid_info()
        
        assert cell_count_grid_info['row'] == original_cell_count_row
        assert group1_grid_info['row'] == original_group1_row
    
    def test_clear_form_hides_other_fields(self):
        """Test that clearing the form properly hides all 'Other' fields."""
        # Show all other fields
        self.panel.sample_var.set("other")
        self.panel.plate_name_var.set("other")
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Verify they are in grid
        assert self.panel.sample_other_entry.grid_info() != {}
        assert self.panel.plate_name_other_entry.grid_info() != {}
        assert self.panel.sample_type_other_entry.grid_info() != {}
        
        # Clear the form
        self.panel.clear_form()
        self.root.update()
        
        # All other fields should be removed from grid
        assert self.panel.sample_other_entry.grid_info() == {}
        assert self.panel.plate_name_other_entry.grid_info() == {}
        assert self.panel.sample_type_other_entry.grid_info() == {}
    
    def test_metadata_retrieval_with_other_fields(self):
        """Test that metadata is correctly retrieved when 'Other' fields are used."""
        # Set up other fields with custom values
        self.panel.sample_var.set("other")
        self.panel.sample_other_var.set("custom_sample")
        
        self.panel.plate_name_var.set("other")
        self.panel.plate_name_other_var.set("custom_plate")
        
        self.panel.sample_type_var.set("other")
        self.panel.sample_type_other_var.set("custom_type")
        
        # Set other required fields
        self.panel.group1_var.set("group1_value")
        
        # Get metadata
        metadata = self.panel.get_metadata()
        
        # Should use the custom values from other fields
        assert metadata['sample'] == "custom_sample"
        assert metadata['plate_name'] == "custom_plate"
        assert metadata['sample_type'] == "custom_type"
        assert metadata['group1'] == "group1_value"
    
    def test_form_validation_with_other_fields(self):
        """Test form validation when 'Other' fields are selected but empty."""
        # Select "other" but leave the text fields empty
        self.panel.sample_var.set("other")
        self.panel.plate_name_var.set("other")
        self.panel.sample_type_var.set("other")
        # Leave other vars empty
        
        # Validation should fail
        is_valid, errors = self.panel.validate_form()
        assert not is_valid
        assert len(errors) > 0
        
        # Should have specific error messages for empty other fields
        error_text = " ".join(errors)
        assert "specify the sample name" in error_text.lower()
        assert "specify the plate name" in error_text.lower()
        assert "specify the sample type" in error_text.lower()
    
    def test_enable_disable_form_affects_other_fields(self):
        """Test that enabling/disabling form affects 'Other' fields."""
        # Show other fields
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        # Disable form
        self.panel.enable_form(False)
        
        # Other field should be disabled
        assert str(self.panel.sample_type_other_entry.cget('state')) == 'disabled'
        
        # Enable form
        self.panel.enable_form(True)
        
        # Other field should be enabled
        assert str(self.panel.sample_type_other_entry.cget('state')) == 'normal'


class TestOtherFieldIntegration:
    """Integration tests for 'Other' field functionality in different modes."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.db_manager = DatabaseManager(":memory:")
        self.panel = MetadataPanel(self.root, self.db_manager)
    
    def teardown_method(self):
        """Clean up after each test."""
        if self.root:
            self.root.destroy()
    
    def test_other_fields_in_single_sample_mode(self):
        """Test 'Other' fields work correctly in single-sample mode."""
        # Configure for single-sample mode
        config = {'sample': 'test_sample', 'plate_name': 'test_plate'}
        self.panel.set_single_sample_defaults(config)
        self.panel.hide_sample_and_plate_fields()
        self.root.update()
        
        # Sample type other field should still work
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        assert self.panel.sample_type_other_entry.grid_info() != {}
        assert str(self.panel.sample_type_other_entry.cget('state')) == 'normal'
        
        # Test typing
        self.panel.sample_type_other_var.set("custom_type")
        assert self.panel.sample_type_other_entry.get() == "custom_type"
    
    def test_other_fields_in_multi_sample_mode(self):
        """Test 'Other' fields work correctly in multi-sample mode."""
        # Configure for multi-sample mode
        config = {'sample_plate_name': 'multi_plate'}
        self.panel.set_multi_sample_defaults(config)
        self.panel.hide_plate_name_field()
        self.root.update()
        
        # Sample and sample type other fields should still work
        self.panel.sample_var.set("other")
        self.panel.sample_type_var.set("other")
        self.root.update()
        
        assert self.panel.sample_other_entry.grid_info() != {}
        assert self.panel.sample_type_other_entry.grid_info() != {}
        
        # Test typing in both fields
        self.panel.sample_other_var.set("custom_sample")
        self.panel.sample_type_other_var.set("custom_type")
        
        assert self.panel.sample_other_entry.get() == "custom_sample"
        assert self.panel.sample_type_other_entry.get() == "custom_type"


if __name__ == "__main__":
    pytest.main([__file__])