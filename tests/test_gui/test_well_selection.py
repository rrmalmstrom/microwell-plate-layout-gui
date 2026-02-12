"""
Tests for Well Selection Component

This module tests the well selection functionality including rectangular drag selection,
selection state management, and visual feedback for the microwell plate GUI.

Context7 Reference: Canvas mouse event handling and selection patterns
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.plate_canvas import PlateCanvas
from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.data.database import DatabaseManager


class TestWellSelection:
    """Test suite for well selection functionality."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Create a test frame for the canvas
        self.test_frame = ttk.Frame(self.root)
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_rectangular_drag_selection(self):
        """Test rectangular drag selection functionality."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Test initial state - no wells selected
        assert len(canvas.selected_wells) == 0
        
        # Simulate rectangular selection
        # Start drag at well A1 (top-left)
        start_x, start_y = canvas._get_well_center(0, 0)
        # End drag at well C3 (should select A1:C3 rectangle)
        end_x, end_y = canvas._get_well_center(2, 2)
        
        # Simulate drag selection
        canvas._start_drag_selection(start_x, start_y)
        canvas._update_drag_selection(end_x, end_y)
        canvas._end_drag_selection(end_x, end_y)
        
        # Verify wells in rectangle are selected
        expected_wells = {"A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"}
        assert canvas.selected_wells == expected_wells
        
        # Verify visual feedback is applied
        for well_name in expected_wells:
            well_id = canvas.well_items[well_name]
            fill_color = canvas.canvas.itemcget(well_id, 'fill')
            assert fill_color == canvas.selection_color
    
    def test_selection_state_management(self):
        """Test selection state management and clearing."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Select some wells
        wells_to_select = {"A1", "B2", "C3"}
        canvas.select_wells(wells_to_select)
        
        # Verify selection state
        assert canvas.selected_wells == wells_to_select
        assert canvas.has_selection()
        
        # Test getting selected well count
        assert canvas.get_selected_count() == 3
        
        # Test clearing selection
        canvas.clear_selection()
        assert len(canvas.selected_wells) == 0
        assert not canvas.has_selection()
        assert canvas.get_selected_count() == 0
        
        # Verify visual state is cleared
        for well_name in wells_to_select:
            well_id = canvas.well_items[well_name]
            fill_color = canvas.canvas.itemcget(well_id, 'fill')
            assert fill_color == canvas.default_well_color
    
    def test_selection_modification(self):
        """Test modifying existing selection (add/remove wells)."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Initial selection
        initial_wells = {"A1", "A2", "B1", "B2"}
        canvas.select_wells(initial_wells)
        assert canvas.selected_wells == initial_wells
        
        # Add wells to selection
        additional_wells = {"C1", "C2"}
        canvas.add_to_selection(additional_wells)
        expected_total = initial_wells | additional_wells
        assert canvas.selected_wells == expected_total
        
        # Remove wells from selection
        wells_to_remove = {"A2", "B2"}
        canvas.remove_from_selection(wells_to_remove)
        expected_remaining = expected_total - wells_to_remove
        assert canvas.selected_wells == expected_remaining
        
        # Test toggle selection
        canvas.toggle_well_selection("A1")  # Should remove A1
        assert "A1" not in canvas.selected_wells
        
        canvas.toggle_well_selection("D1")  # Should add D1
        assert "D1" in canvas.selected_wells
    
    def test_individual_well_clicking(self):
        """Test individual well selection by clicking."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Simulate clicking on well A1
        well_a1_id = canvas.well_items["A1"]
        
        # Create mock event for well click
        mock_event = Mock()
        mock_event.widget = canvas.canvas
        mock_event.item = well_a1_id
        
        # Simulate click
        canvas._on_well_click(mock_event)
        
        # Verify A1 is selected
        assert "A1" in canvas.selected_wells
        assert canvas.get_selected_count() == 1
        
        # Click again to deselect
        canvas._on_well_click(mock_event)
        assert "A1" not in canvas.selected_wells
        assert canvas.get_selected_count() == 0
    
    def test_selection_visual_feedback(self):
        """Test visual feedback for selected wells."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Test default visual state
        well_id = canvas.well_items["A1"]
        default_color = canvas.canvas.itemcget(well_id, 'fill')
        assert default_color == canvas.default_well_color
        
        # Select well and test visual change
        canvas.select_wells({"A1"})
        selected_color = canvas.canvas.itemcget(well_id, 'fill')
        assert selected_color == canvas.selection_color
        assert selected_color != default_color
        
        # Clear selection and test visual reset
        canvas.clear_selection()
        reset_color = canvas.canvas.itemcget(well_id, 'fill')
        assert reset_color == canvas.default_well_color
    
    def test_selection_bounds_validation(self):
        """Test selection bounds validation for different plate types."""
        # Test 96-well plate bounds
        canvas_96 = PlateCanvas(self.test_frame, "96-well")
        
        # Valid wells for 96-well plate
        valid_wells = {"A1", "H12"}  # Corner wells
        canvas_96.select_wells(valid_wells)
        assert canvas_96.selected_wells == valid_wells
        
        # Test 384-well plate bounds
        canvas_384 = PlateCanvas(self.test_frame, "384-well")
        
        # Valid wells for 384-well plate
        valid_wells_384 = {"A1", "P24"}  # Corner wells
        canvas_384.select_wells(valid_wells_384)
        assert canvas_384.selected_wells == valid_wells_384
        
        # Test invalid well names (should be ignored)
        invalid_wells = {"Z99", "AA1"}
        canvas_96.select_wells(invalid_wells)
        assert len(canvas_96.selected_wells) == 0  # Invalid wells ignored
    
    def test_drag_selection_visual_preview(self):
        """Test visual preview during drag selection."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Start drag selection
        start_x, start_y = canvas._get_well_center(0, 0)
        canvas._start_drag_selection(start_x, start_y)
        
        # Verify drag rectangle is created
        assert hasattr(canvas, 'drag_rectangle')
        assert canvas.drag_rectangle is not None
        
        # Update drag selection
        end_x, end_y = canvas._get_well_center(2, 2)
        canvas._update_drag_selection(end_x, end_y)
        
        # Verify drag rectangle is updated
        coords = canvas.canvas.coords(canvas.drag_rectangle)
        assert len(coords) == 4  # Rectangle coordinates
        
        # End drag selection
        canvas._end_drag_selection(end_x, end_y)
        
        # Verify drag rectangle is removed
        assert canvas.drag_rectangle is None
    
    def test_selection_callbacks(self):
        """Test selection change callbacks."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Set up callback
        callback_calls = []
        def selection_callback(selected_wells):
            callback_calls.append(selected_wells.copy())
        
        canvas.set_selection_callback(selection_callback)
        
        # Test selection triggers callback
        wells = {"A1", "B2"}
        canvas.select_wells(wells)
        
        assert len(callback_calls) == 1
        assert callback_calls[0] == wells
        
        # Test clearing selection triggers callback
        canvas.clear_selection()
        
        assert len(callback_calls) == 2
        assert callback_calls[1] == set()


class TestWellSelectionIntegration:
    """Test suite for well selection integration with main application."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_selection_integration_with_metadata_panel(self):
        """Test integration between well selection and metadata panel."""
        # Create main window with components
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Verify components are connected
        assert main_window.plate_canvas is not None
        assert main_window.metadata_panel is not None
        
        # Test well selection
        wells_to_select = {"A1", "A2", "B1", "B2"}
        main_window.plate_canvas.select_wells(wells_to_select)
        
        # Verify selection state
        assert main_window.plate_canvas.selected_wells == wells_to_select
        assert main_window.plate_canvas.has_selection()
    
    def test_metadata_application_to_selected_wells(self):
        """Test applying metadata to selected wells."""
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Select wells
        wells_to_select = {"A1", "A2", "B1", "B2"}
        main_window.plate_canvas.select_wells(wells_to_select)
        
        # Set up metadata
        metadata = {
            'project': 'TestProject',
            'sample': 'TestSample',
            'plate_name': 'TestProject.TestSample.1',
            'sample_type': 'sample',
            'cell_count': '1000',
            'group1': 'Group1',
            'group2': 'Group2',
            'group3': 'Group3'
        }
        
        # Apply metadata to selected wells
        main_window.plate_canvas.apply_metadata_to_selection(metadata)
        
        # Verify metadata is stored for selected wells
        for well_name in wells_to_select:
            well_metadata = main_window.plate_canvas.get_well_metadata(well_name)
            assert well_metadata == metadata
    
    def test_selection_persistence_across_operations(self):
        """Test that selection persists across various operations."""
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Select wells
        wells_to_select = {"A1", "A2", "B1", "B2"}
        main_window.plate_canvas.select_wells(wells_to_select)
        
        # Verify selection persists after metadata operations
        initial_selection = main_window.plate_canvas.selected_wells.copy()
        
        # Simulate metadata form operations (no project_var anymore)
        main_window.metadata_panel.sample_var.set("TestSample")
        
        # Selection should still be intact
        assert main_window.plate_canvas.selected_wells == initial_selection
        
        # Clear selection explicitly
        main_window.plate_canvas.clear_selection()
        assert len(main_window.plate_canvas.selected_wells) == 0


class TestWellSelectionEdgeCases:
    """Test suite for well selection edge cases and error handling."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        self.test_frame = ttk.Frame(self.root)
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_empty_selection_operations(self):
        """Test operations on empty selection."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Test operations on empty selection
        assert canvas.get_selected_count() == 0
        assert not canvas.has_selection()
        
        # Clear empty selection (should not error)
        canvas.clear_selection()
        assert canvas.get_selected_count() == 0
        
        # Remove from empty selection (should not error)
        canvas.remove_from_selection({"A1", "B2"})
        assert canvas.get_selected_count() == 0
    
    def test_duplicate_selection_operations(self):
        """Test selecting already selected wells."""
        canvas = PlateCanvas(self.test_frame, "96-well")
        
        # Select wells
        wells = {"A1", "B2"}
        canvas.select_wells(wells)
        assert canvas.selected_wells == wells
        
        # Select same wells again (should not duplicate)
        canvas.select_wells(wells)
        assert canvas.selected_wells == wells
        assert canvas.get_selected_count() == 2
        
        # Add already selected wells (should not duplicate)
        canvas.add_to_selection({"A1"})
        assert canvas.selected_wells == wells
        assert canvas.get_selected_count() == 2
    
    def test_large_selection_performance(self):
        """Test performance with large selections."""
        canvas = PlateCanvas(self.test_frame, "384-well")
        
        # Select all wells (384 wells)
        all_wells = set()
        for row in range(16):  # A-P
            for col in range(24):  # 1-24
                row_letter = chr(ord('A') + row)
                well_name = f"{row_letter}{col + 1}"
                all_wells.add(well_name)
        
        # This should complete without performance issues
        canvas.select_wells(all_wells)
        assert canvas.get_selected_count() == 384
        assert canvas.selected_wells == all_wells
        
        # Clear large selection
        canvas.clear_selection()
        assert canvas.get_selected_count() == 0