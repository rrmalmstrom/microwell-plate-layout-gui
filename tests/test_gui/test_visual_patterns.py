"""
Test suite for visual pattern functionality in PlateCanvas.

This module tests that Group 2 values are correctly mapped to visual patterns
and that the patterns are applied as overlay shapes on canvas items.
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch

from src.microwell_plate_gui.gui.plate_canvas import PlateCanvas


class TestVisualPatterns:
    """Test suite for visual pattern functionality."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        self.test_frame = ttk.Frame(self.root)
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_visual_pattern_assignment(self):
        """Test that Group 2 values get assigned visual patterns."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply metadata with Group 2 values
        test_cases = [
            ("A1", "Pattern1"),
            ("A2", "Pattern2"),
            ("A3", "Pattern1"),  # Same as A1
            ("A4", "Pattern3")
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
        assert "Pattern1" in canvas.group2_patterns
        assert "Pattern2" in canvas.group2_patterns
        assert "Pattern3" in canvas.group2_patterns
        
        # Verify same values get same patterns
        pattern1 = canvas.group2_patterns["Pattern1"]
        pattern2 = canvas.group2_patterns["Pattern2"]
        pattern3 = canvas.group2_patterns["Pattern3"]
        
        # All patterns should be different
        assert pattern1 != pattern2
        assert pattern1 != pattern3
        assert pattern2 != pattern3
        
        # Verify patterns are from available list
        assert pattern1 in canvas.available_patterns
        assert pattern2 in canvas.available_patterns
        assert pattern3 in canvas.available_patterns
    
    def test_visual_pattern_storage_in_wells(self):
        """Test that visual patterns are stored in well metadata."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        canvas.select_wells({"B1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': 'TestPattern',
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify pattern is stored in well info
        well_info = canvas.wells["B1"]
        assert 'visual_pattern' in well_info
        assert well_info['visual_pattern'] in canvas.available_patterns
        assert well_info['group2_value'] == 'TestPattern'
    
    def test_pattern_overlay_creation(self):
        """Test that pattern overlays are created on canvas."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Get initial canvas item count
        initial_items = len(canvas.canvas.find_all())
        
        canvas.select_wells({"C1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': 'TestPattern',
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify additional canvas items were created for pattern overlay
        final_items = len(canvas.canvas.find_all())
        assert final_items > initial_items, "Pattern overlay should create additional canvas items"
        
        # Verify pattern overlay items are stored
        well_info = canvas.wells["C1"]
        assert 'pattern_overlays' in well_info
        assert len(well_info['pattern_overlays']) > 0
    
    def test_empty_group2_no_pattern(self):
        """Test that empty Group 2 values result in no visual pattern."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        canvas.select_wells({"D1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': '',  # Empty Group 2
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify no pattern is assigned
        well_info = canvas.wells["D1"]
        assert well_info.get('visual_pattern', '') == ""
        assert well_info.get('pattern_overlays', []) == []
    
    def test_available_patterns_are_valid(self):
        """Test that available patterns are valid visual pattern types."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Expected visual pattern types
        expected_patterns = ["dots", "lines", "cross", "grid", "circles", "squares", "triangles", "stars", "diamond", "zigzag"]
        
        # Verify available patterns match expected types
        assert len(canvas.available_patterns) == len(expected_patterns)
        for pattern in expected_patterns:
            assert pattern in canvas.available_patterns
    
    def test_pattern_index_increments(self):
        """Test that pattern index increments for each new Group 2 value."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        initial_index = canvas.pattern_index
        
        # Apply different Group 2 values
        group2_values = ["Pattern1", "Pattern2", "Pattern3"]
        
        for i, group2_value in enumerate(group2_values):
            canvas.select_wells({f"E{i+1}"})
            metadata = {
                'sample_type': 'sample',
                'group1': 'TestGroup1',
                'group2': group2_value,
                'group3': ''
            }
            canvas.apply_metadata_to_selection(metadata)
            
            # Verify pattern index has incremented
            expected_index = initial_index + i + 1
            assert canvas.pattern_index == expected_index
    
    def test_clear_all_resets_patterns(self):
        """Test that clearing all metadata resets pattern mappings."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply some metadata to create pattern mappings
        canvas.select_wells({"F1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': 'TestPattern',
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify pattern mapping exists
        assert len(canvas.group2_patterns) > 0
        assert canvas.pattern_index > 0
        
        # Clear all metadata
        canvas.clear_all_metadata()
        
        # Verify pattern mappings are cleared
        assert len(canvas.group2_patterns) == 0
        assert canvas.pattern_index == 0
    
    def test_pattern_overlay_removal(self):
        """Test that pattern overlays are properly removed when wells are cleared."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Apply pattern to well
        canvas.select_wells({"G1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'TestGroup1',
            'group2': 'TestPattern',
            'group3': ''
        }
        canvas.apply_metadata_to_selection(metadata)
        
        # Verify pattern overlay exists
        well_info = canvas.wells["G1"]
        overlay_items = well_info.get('pattern_overlays', [])
        assert len(overlay_items) > 0
        
        # Clear the well
        canvas.select_wells({"G1"})
        canvas.apply_metadata_to_selection({
            'sample_type': 'unused',
            'group1': '',
            'group2': '',
            'group3': ''
        })
        
        # Verify pattern overlay is removed
        well_info = canvas.wells["G1"]
        assert well_info.get('pattern_overlays', []) == []


class TestVisualPatternsIntegration:
    """Integration tests for visual patterns with other components."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_visual_patterns_with_colors(self):
        """Test that visual patterns work together with Group 1 colors."""
        from src.microwell_plate_gui.gui.main_window import MainWindow
        
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Apply metadata with both Group 1 and Group 2 values
        main_window.plate_canvas.select_wells({"A1"})
        metadata = {
            'sample_type': 'sample',
            'group1': 'ColorGroup',
            'group2': 'PatternGroup',
            'group3': ''
        }
        main_window.plate_canvas.apply_metadata_to_selection(metadata)
        
        # Verify both color and pattern are assigned
        well_info = main_window.plate_canvas.wells["A1"]
        assert 'fill_color' in well_info
        assert 'visual_pattern' in well_info
        assert well_info['fill_color'] != main_window.plate_canvas.default_well_color
        assert well_info['visual_pattern'] in main_window.plate_canvas.available_patterns
        
        # Verify mappings exist
        assert 'ColorGroup' in main_window.plate_canvas.group1_colors
        assert 'PatternGroup' in main_window.plate_canvas.group2_patterns