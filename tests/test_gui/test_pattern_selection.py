"""
Test pattern selection functionality for microwell plate GUI.

This module tests the four pattern selection buttons that automatically select wells
based on odd/even row and column patterns.
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.plate_canvas import PlateCanvas
from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.data.database import DatabaseManager


class TestPatternSelection(unittest.TestCase):
    """Test pattern selection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Create a test database manager
        self.db_manager = DatabaseManager(":memory:")
        
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def test_plate_canvas_pattern_methods_exist(self):
        """Test that pattern selection methods exist in PlateCanvas."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Check that all pattern selection methods exist
        self.assertTrue(hasattr(plate_canvas, 'select_pattern_upper_left'))
        self.assertTrue(hasattr(plate_canvas, 'select_pattern_lower_left'))
        self.assertTrue(hasattr(plate_canvas, 'select_pattern_upper_right'))
        self.assertTrue(hasattr(plate_canvas, 'select_pattern_lower_right'))
        self.assertTrue(hasattr(plate_canvas, 'add_pattern_to_selection'))
    
    def test_upper_left_pattern_96_well(self):
        """Test upper left pattern selection for 96-well plate."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_upper_left()
        
        # Get selected wells
        selected_wells = plate_canvas.get_selected_wells()
        
        # Verify pattern: odd rows (A,C,E,G) and odd columns (1,3,5,7,9,11)
        expected_wells = set()
        for row_idx in [0, 2, 4, 6]:  # A, C, E, G (0-based)
            for col_idx in [0, 2, 4, 6, 8, 10]:  # 1, 3, 5, 7, 9, 11 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(selected_wells, expected_wells)
        print(f"Upper left pattern selected {len(selected_wells)} wells: {sorted(selected_wells)}")
    
    def test_lower_left_pattern_96_well(self):
        """Test lower left pattern selection for 96-well plate."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_lower_left()
        
        # Get selected wells
        selected_wells = plate_canvas.get_selected_wells()
        
        # Verify pattern: even rows (B,D,F,H) and odd columns (1,3,5,7,9,11)
        expected_wells = set()
        for row_idx in [1, 3, 5, 7]:  # B, D, F, H (0-based)
            for col_idx in [0, 2, 4, 6, 8, 10]:  # 1, 3, 5, 7, 9, 11 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(selected_wells, expected_wells)
        print(f"Lower left pattern selected {len(selected_wells)} wells: {sorted(selected_wells)}")
    
    def test_upper_right_pattern_96_well(self):
        """Test upper right pattern selection for 96-well plate."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_upper_right()
        
        # Get selected wells
        selected_wells = plate_canvas.get_selected_wells()
        
        # Verify pattern: odd rows (A,C,E,G) and even columns (2,4,6,8,10,12)
        expected_wells = set()
        for row_idx in [0, 2, 4, 6]:  # A, C, E, G (0-based)
            for col_idx in [1, 3, 5, 7, 9, 11]:  # 2, 4, 6, 8, 10, 12 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(selected_wells, expected_wells)
        print(f"Upper right pattern selected {len(selected_wells)} wells: {sorted(selected_wells)}")
    
    def test_lower_right_pattern_96_well(self):
        """Test lower right pattern selection for 96-well plate."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_lower_right()
        
        # Get selected wells
        selected_wells = plate_canvas.get_selected_wells()
        
        # Verify pattern: even rows (B,D,F,H) and even columns (2,4,6,8,10,12)
        expected_wells = set()
        for row_idx in [1, 3, 5, 7]:  # B, D, F, H (0-based)
            for col_idx in [1, 3, 5, 7, 9, 11]:  # 2, 4, 6, 8, 10, 12 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(selected_wells, expected_wells)
        print(f"Lower right pattern selected {len(selected_wells)} wells: {sorted(selected_wells)}")
    
    def test_upper_left_pattern_384_well(self):
        """Test upper left pattern selection for 384-well plate."""
        plate_canvas = PlateCanvas(self.root, "384-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_upper_left()
        
        # Get selected wells
        selected_wells = plate_canvas.get_selected_wells()
        
        # Verify pattern: odd rows (A,C,E,G,I,K,M,O) and odd columns (1,3,5,...,23)
        expected_wells = set()
        for row_idx in [0, 2, 4, 6, 8, 10, 12, 14]:  # A, C, E, G, I, K, M, O (0-based)
            for col_idx in range(0, 24, 2):  # 1, 3, 5, ..., 23 (0-based: 0, 2, 4, ..., 22)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(selected_wells, expected_wells)
        print(f"384-well upper left pattern selected {len(selected_wells)} wells")
    
    def test_pattern_selection_callback(self):
        """Test that pattern selection triggers the selection callback."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Set up callback mock
        callback_mock = Mock()
        plate_canvas.set_selection_callback(callback_mock)
        
        # Execute pattern selection
        plate_canvas.select_pattern_upper_left()
        
        # Verify callback was called
        callback_mock.assert_called_once()
        
        # Verify callback was called with the correct selection
        called_wells = callback_mock.call_args[0][0]
        self.assertIsInstance(called_wells, set)
        self.assertGreater(len(called_wells), 0)
    
    def test_additive_pattern_selection(self):
        """Test additive pattern selection functionality."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # First select some wells manually
        manual_wells = {"A1", "B2", "C3"}
        plate_canvas.set_selected_wells(manual_wells)
        
        # Add upper left pattern to selection
        plate_canvas.add_pattern_to_selection('upper_left')
        
        # Get final selection
        final_selection = plate_canvas.get_selected_wells()
        
        # Verify that manual wells are still selected
        for well in manual_wells:
            if well not in final_selection:
                # Check if this well would be selected by upper left pattern
                row_idx = ord(well[0]) - ord('A')
                col_idx = int(well[1:]) - 1
                row_1based = row_idx + 1
                col_1based = col_idx + 1
                is_upper_left = (row_1based % 2 == 1 and col_1based % 2 == 1)
                if not is_upper_left:
                    self.assertIn(well, final_selection, f"Manual well {well} should still be selected")
        
        # Verify that upper left pattern wells are selected
        expected_pattern_wells = set()
        for row_idx in [0, 2, 4, 6]:  # A, C, E, G (0-based)
            for col_idx in [0, 2, 4, 6, 8, 10]:  # 1, 3, 5, 7, 9, 11 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_pattern_wells.add(f"{row_letter}{col_number}")
        
        for well in expected_pattern_wells:
            self.assertIn(well, final_selection, f"Pattern well {well} should be selected")
    
    def test_pattern_selection_integration_with_existing_selection(self):
        """Test that pattern selection works with existing selection methods."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # First select a well manually
        plate_canvas.select_well("A1")
        initial_selection = plate_canvas.get_selected_wells()
        self.assertEqual(initial_selection, {"A1"})
        
        # Now select upper left pattern (which includes A1)
        plate_canvas.select_pattern_upper_left()
        pattern_selection = plate_canvas.get_selected_wells()
        
        # A1 should still be selected as part of the pattern
        self.assertIn("A1", pattern_selection)
        
        # Verify the pattern is correct
        expected_wells = set()
        for row_idx in [0, 2, 4, 6]:  # A, C, E, G (0-based)
            for col_idx in [0, 2, 4, 6, 8, 10]:  # 1, 3, 5, 7, 9, 11 (0-based)
                row_letter = chr(ord('A') + row_idx)
                col_number = col_idx + 1
                expected_wells.add(f"{row_letter}{col_number}")
        
        self.assertEqual(pattern_selection, expected_wells)
    
    def test_main_window_pattern_buttons_exist(self):
        """Test that pattern selection buttons exist in MainWindow."""
        # Mock the startup dialog to avoid interactive prompts
        with patch.object(MainWindow, 'show_startup_dialog', return_value=True):
            main_window = MainWindow(self.root, ":memory:")
            main_window.plate_type = "96"
            main_window.sample_mode = "single"
            main_window.single_sample_config = {"sample": "test", "plate_name": "test_plate"}
            main_window._initialize_plate_interface()
            
            # Check that pattern selection methods exist
            self.assertTrue(hasattr(main_window, '_on_pattern_upper_left'))
            self.assertTrue(hasattr(main_window, '_on_pattern_lower_left'))
            self.assertTrue(hasattr(main_window, '_on_pattern_upper_right'))
            self.assertTrue(hasattr(main_window, '_on_pattern_lower_right'))
            
            # Check that pattern selection buttons exist
            self.assertTrue(hasattr(main_window, 'upper_left_button'))
            self.assertTrue(hasattr(main_window, 'lower_left_button'))
            self.assertTrue(hasattr(main_window, 'upper_right_button'))
            self.assertTrue(hasattr(main_window, 'lower_right_button'))
    
    def test_pattern_selection_visual_feedback(self):
        """Test that pattern selection provides proper visual feedback."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Execute pattern selection
        plate_canvas.select_pattern_upper_left()
        
        # Check that selected wells have the correct visual state
        selected_wells = plate_canvas.get_selected_wells()
        
        for well_name in selected_wells:
            well_info = plate_canvas.wells[well_name]
            self.assertTrue(well_info['selected'], f"Well {well_name} should be marked as selected")
            
            # Check visual appearance (canvas item should have selection color)
            canvas_id = well_info['canvas_id']
            fill_color = plate_canvas.canvas.itemcget(canvas_id, 'fill')
            # Should be selection color (lightblue) or maintain metadata color with selection outline
            self.assertIsNotNone(fill_color)
    
    def test_all_patterns_cover_all_wells(self):
        """Test that all four patterns together cover all wells exactly once."""
        plate_canvas = PlateCanvas(self.root, "96-well")
        
        # Collect wells from each pattern
        all_pattern_wells = set()
        
        # Upper left pattern
        plate_canvas.select_pattern_upper_left()
        upper_left_wells = plate_canvas.get_selected_wells().copy()
        all_pattern_wells.update(upper_left_wells)
        
        # Lower left pattern
        plate_canvas.select_pattern_lower_left()
        lower_left_wells = plate_canvas.get_selected_wells().copy()
        all_pattern_wells.update(lower_left_wells)
        
        # Upper right pattern
        plate_canvas.select_pattern_upper_right()
        upper_right_wells = plate_canvas.get_selected_wells().copy()
        all_pattern_wells.update(upper_right_wells)
        
        # Lower right pattern
        plate_canvas.select_pattern_lower_right()
        lower_right_wells = plate_canvas.get_selected_wells().copy()
        all_pattern_wells.update(lower_right_wells)
        
        # Verify no overlap between patterns
        patterns = [upper_left_wells, lower_left_wells, upper_right_wells, lower_right_wells]
        for i, pattern1 in enumerate(patterns):
            for j, pattern2 in enumerate(patterns):
                if i != j:
                    overlap = pattern1.intersection(pattern2)
                    self.assertEqual(len(overlap), 0, f"Patterns {i} and {j} should not overlap, but found: {overlap}")
        
        # Verify all wells are covered
        all_wells = set(plate_canvas.wells.keys())
        self.assertEqual(all_pattern_wells, all_wells, "All four patterns should cover all wells exactly once")
        
        # Verify each pattern has the expected number of wells for 96-well plate
        # 96-well plate: 8 rows × 12 columns = 96 wells
        # Each pattern should have 4 rows × 6 columns = 24 wells
        expected_wells_per_pattern = 24
        self.assertEqual(len(upper_left_wells), expected_wells_per_pattern)
        self.assertEqual(len(lower_left_wells), expected_wells_per_pattern)
        self.assertEqual(len(upper_right_wells), expected_wells_per_pattern)
        self.assertEqual(len(lower_right_wells), expected_wells_per_pattern)


if __name__ == '__main__':
    unittest.main()