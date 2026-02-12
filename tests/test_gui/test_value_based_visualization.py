"""
Test suite for value-based color and texture visualization system.

This module tests the new visualization system where:
- Well outlines show sample type colors
- Well fill colors are dynamically assigned based on Group 1 values
- Well fill patterns are dynamically assigned based on Group 2 values
- Group 3 is stored but not displayed
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock

from src.microwell_plate_gui.gui.plate_canvas import PlateCanvas
from src.microwell_plate_gui.gui.main_window import MainWindow


class TestValueBasedVisualization:
    """Test suite for value-based color and texture visualization."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        self.test_frame = ttk.Frame(self.root)
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_dynamic_color_assignment(self):
        """Test that unique Group 1 values get different colors."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply different Group 1 values to different wells
        test_cases = [
            ("A1", "Treatment A"),
            ("A2", "Treatment B"), 
            ("A3", "Treatment A"),  # Same as A1
            ("A4", "Control")
        ]
        
        for well_name, group1_value in test_cases:
            canvas.select_wells({well_name})
            metadata = {
                'sample_type': 'sample',
                'group1': group1_value,
                'group2': '',
                'group3': ''
            }
            canvas.apply_metadata_to_selection(metadata)
        
        # Verify color assignments
        assert len(canvas.group1_colors) == 3  # Three unique Group 1 values
        assert "Treatment A" in canvas.group1_colors
        assert "Treatment B" in canvas.group1_colors
        assert "Control" in canvas.group1_colors
        
        # Verify same values get same colors
        a1_color = canvas.wells["A1"]["fill_color"]
        a3_color = canvas.wells["A3"]["fill_color"]
        assert a1_color == a3_color  # Both have "Treatment A"
        
        # Verify different values get different colors
        a2_color = canvas.wells["A2"]["fill_color"]
        assert a1_color != a2_color  # Different Group 1 values
    
    def test_dynamic_pattern_assignment(self):
        """Test that unique Group 2 values get different patterns."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply different Group 2 values to different wells
        test_cases = [
            ("B1", "Condition X"),
            ("B2", "Condition Y"),
            ("B3", "Condition X"),  # Same as B1
            ("B4", "Baseline")
        ]
        
        for well_name, group2_value in test_cases:
            canvas.select_wells({well_name})
            metadata = {
                'sample_type': 'sample',
                'group1': 'SameGroup',  # Same Group 1 for all
                'group2': group2_value,
                'group3': ''
            }
            canvas.apply_metadata_to_selection(metadata)
        
        # Verify pattern assignments
        assert len(canvas.group2_patterns) == 3  # Three unique Group 2 values
        assert "Condition X" in canvas.group2_patterns
        assert "Condition Y" in canvas.group2_patterns
        assert "Baseline" in canvas.group2_patterns
        
        # Verify same values get same patterns
        b1_pattern = canvas.wells["B1"]["visual_pattern"]
        b3_pattern = canvas.wells["B3"]["visual_pattern"]
        assert b1_pattern == b3_pattern  # Both have "Condition X"
        
        # Verify different values get different patterns
        b2_pattern = canvas.wells["B2"]["visual_pattern"]
        assert b1_pattern != b2_pattern  # Different Group 2 values
    
    def test_combined_color_and_pattern(self):
        """Test wells with both Group 1 and Group 2 values."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        canvas.select_wells({"C1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TreatmentAlpha',
            'group2': 'ConditionBeta',
            'group3': 'ReplicateGamma'  # Stored but not displayed
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify both color and pattern are assigned
        well_info = canvas.wells["C1"]
        assert well_info['group1_value'] == 'TreatmentAlpha'
        assert well_info['group2_value'] == 'ConditionBeta'
        assert well_info['group3_value'] == 'ReplicateGamma'
        assert 'fill_color' in well_info
        assert 'visual_pattern' in well_info
        
        # Verify Group 1 value is mapped to color
        assert 'TreatmentAlpha' in canvas.group1_colors
        assert canvas.group1_colors['TreatmentAlpha'] == well_info['fill_color']
        
        # Verify Group 2 value is mapped to pattern
        assert 'ConditionBeta' in canvas.group2_patterns
        assert canvas.group2_patterns['ConditionBeta'] == well_info['visual_pattern']
    
    def test_empty_group_values(self):
        """Test wells with empty group values."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        canvas.select_wells({"D1"})
        metadata = {
            'sample_type': 'sample',
            'group1': '',  # Empty
            'group2': '',  # Empty
            'group3': ''   # Empty
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify default values are used
        well_info = canvas.wells["D1"]
        assert well_info['fill_color'] == canvas.default_well_color
        assert well_info['visual_pattern'] == ""  # No pattern
    
    def test_clear_all_resets_mappings(self):
        """Test that clearing all metadata resets color and pattern mappings."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply some metadata to create mappings
        canvas.select_wells({"E1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': 'TestGroup2',
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify mappings exist
        assert len(canvas.group1_colors) > 0
        assert len(canvas.group2_patterns) > 0
        
        # Clear all metadata
        canvas.clear_all_metadata()
        
        # Verify mappings are cleared
        assert len(canvas.group1_colors) == 0
        assert len(canvas.group2_patterns) == 0
        assert canvas.color_index == 0
        assert canvas.pattern_index == 0
    
    def test_sample_type_outline_preserved(self):
        """Test that sample type outline colors work with new system."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Test different sample types
        sample_types = ['sample', 'neg_cntrl', 'pos_cntrl', 'unused']
        
        for i, sample_type in enumerate(sample_types):
            well_name = f"F{i+1}"
            canvas.select_wells({well_name})
            
            metadata = {
                'sample_type': sample_type,
                'group1': 'TestGroup',
                'group2': 'TestCondition',
                'group3': ''
            }
            canvas.apply_metadata_to_selection(metadata)
            
            # Verify sample type is stored and outline color is correct
            well_info = canvas.wells[well_name]
            assert well_info['sample_type'] == sample_type
            expected_outline = canvas.sample_type_outline_colors[sample_type]
            assert well_info['outline_color'] == expected_outline


class TestValueBasedIntegration:
    """Test suite for value-based system integration."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_form_clearing_with_value_system(self):
        """Test that form clearing works with value-based system."""
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Select wells and apply metadata
        main_window.plate_canvas.select_wells({"A1", "A2"})
        
        # Fill form with metadata
        main_window.metadata_panel.sample_var.set("TestSample")
        main_window.metadata_panel.plate_name_var.set("TestPlate")
        main_window.metadata_panel.sample_type_var.set("sample")
        main_window.metadata_panel.group1_var.set("UniqueGroup1")
        main_window.metadata_panel.group2_var.set("UniqueGroup2")
        main_window.metadata_panel.group3_var.set("UniqueGroup3")
        
        # Apply metadata
        main_window.metadata_panel._apply_metadata()
        
        # Verify form is cleared
        assert main_window.metadata_panel.sample_var.get() == ""
        assert main_window.metadata_panel.group1_var.get() == ""
        assert main_window.metadata_panel.group2_var.get() == ""
        assert main_window.metadata_panel.group3_var.get() == ""
        
        # Verify wells have the applied colors and patterns
        for well_name in ["A1", "A2"]:
            well_info = main_window.plate_canvas.wells[well_name]
            assert well_info['group1_value'] == 'UniqueGroup1'
            assert well_info['group2_value'] == 'UniqueGroup2'
            assert well_info['group3_value'] == 'UniqueGroup3'
            assert 'fill_color' in well_info
            assert 'visual_pattern' in well_info