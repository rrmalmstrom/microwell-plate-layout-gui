"""
Tests for the plate canvas GUI component.

Context7 Reference: Tkinter Canvas widget for interactive grid layouts
- Using canvas.create_oval for well visualization
- Using canvas.tag_bind for mouse event handling
- Using canvas.find_withtag for item management
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.plate_canvas import PlateCanvas


class TestPlateCanvas:
    """Test suite for PlateCanvas class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        self.parent_frame = tk.Frame(self.root)
    
    def teardown_method(self):
        """Cleanup after each test method."""
        if self.root:
            self.root.destroy()
    
    def test_plate_canvas_creation(self):
        """Test that PlateCanvas can be created successfully."""
        # Context7 Reference: Canvas widget creation
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        assert canvas is not None
        assert canvas.plate_type == "96"
    
    def test_96_well_grid_layout(self):
        """Test that 96-well plate grid is created correctly."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # 96-well plate should have 8 rows (A-H) and 12 columns (1-12)
        assert canvas.rows == 8
        assert canvas.cols == 12
        assert len(canvas.wells) == 96
    
    def test_384_well_grid_layout(self):
        """Test that 384-well plate grid is created correctly."""
        canvas = PlateCanvas(self.parent_frame, plate_type="384")
        
        # 384-well plate should have 16 rows (A-P) and 24 columns (1-24)
        assert canvas.rows == 16
        assert canvas.cols == 24
        assert len(canvas.wells) == 384
    
    def test_well_coordinate_calculation(self):
        """Test that well coordinates are calculated correctly."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Test specific well coordinates
        well_a1 = canvas.get_well_by_name("A1")
        assert well_a1 is not None
        assert well_a1['row'] == 0
        assert well_a1['col'] == 0
        
        well_h12 = canvas.get_well_by_name("H12")
        assert well_h12 is not None
        assert well_h12['row'] == 7
        assert well_h12['col'] == 11
    
    def test_well_visual_creation(self):
        """Test that well visuals are created on canvas."""
        # Context7 Reference: canvas.create_oval for circular wells
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Should have canvas items for each well
        canvas_items = canvas.canvas.find_all()
        assert len(canvas_items) >= 96  # At least one item per well
    
    def test_well_naming_convention(self):
        """Test that wells follow proper naming convention."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Test row letters A-H for 96-well
        expected_wells = ["A1", "A12", "H1", "H12"]
        for well_name in expected_wells:
            well = canvas.get_well_by_name(well_name)
            assert well is not None
            assert well['name'] == well_name
    
    def test_384_well_naming_convention(self):
        """Test that 384-well plate uses A-P rows."""
        canvas = PlateCanvas(self.parent_frame, plate_type="384")
        
        # Test row letters A-P for 384-well
        expected_wells = ["A1", "A24", "P1", "P24"]
        for well_name in expected_wells:
            well = canvas.get_well_by_name(well_name)
            assert well is not None
            assert well['name'] == well_name
    
    def test_well_selection_state(self):
        """Test that wells can be selected and deselected."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Initially no wells should be selected
        assert len(canvas.selected_wells) == 0
        
        # Select a well
        canvas.select_well("A1")
        assert "A1" in canvas.selected_wells
        
        # Deselect a well
        canvas.deselect_well("A1")
        assert "A1" not in canvas.selected_wells
    
    def test_rectangular_selection_method(self):
        """Test that rectangular selection method exists."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Should have method for rectangular selection
        assert hasattr(canvas, 'select_rectangle')
        assert callable(canvas.select_rectangle)
    
    def test_mouse_event_binding(self):
        """Test that mouse events are bound to wells."""
        # Context7 Reference: canvas.tag_bind for mouse events
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Should have mouse event handlers
        assert hasattr(canvas, 'on_well_click')
        assert callable(canvas.on_well_click)
        
        assert hasattr(canvas, 'on_mouse_drag')
        assert callable(canvas.on_mouse_drag)


class TestWellCoordinateCalculation:
    """Test suite for well coordinate calculations."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.parent_frame = tk.Frame(self.root)
    
    def teardown_method(self):
        """Cleanup after each test method."""
        if self.root:
            self.root.destroy()
    
    def test_row_letter_to_index(self):
        """Test conversion from row letter to index."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        assert canvas.row_letter_to_index('A') == 0
        assert canvas.row_letter_to_index('H') == 7
    
    def test_384_well_row_letters(self):
        """Test that 384-well plate supports A-P rows."""
        canvas = PlateCanvas(self.parent_frame, plate_type="384")
        
        assert canvas.row_letter_to_index('A') == 0
        assert canvas.row_letter_to_index('P') == 15
    
    def test_well_name_parsing(self):
        """Test parsing of well names like 'A1', 'H12'."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        row, col = canvas.parse_well_name("A1")
        assert row == 0 and col == 0
        
        row, col = canvas.parse_well_name("H12")
        assert row == 7 and col == 11
    
    def test_pixel_to_well_conversion(self):
        """Test conversion from pixel coordinates to well coordinates."""
        canvas = PlateCanvas(self.parent_frame, plate_type="96")
        
        # Should have method to convert pixel coordinates to well
        assert hasattr(canvas, 'pixel_to_well')
        assert callable(canvas.pixel_to_well)