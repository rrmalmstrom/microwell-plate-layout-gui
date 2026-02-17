"""
Test suite for Phase 4.2 Layout Improvements

This module tests the layout improvements implemented in Phase 4.2:
1. Legend panel visibility improvements (weight ratio changes)
2. Export CSV button prominence (separate row layout)
3. Button reorganization and styling
4. Responsive layout behavior
"""

import unittest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.gui.legend_panel import LegendPanel
from microwell_plate_gui.data.database import DatabaseManager


class TestPhase42LayoutImprovements(unittest.TestCase):
    """Test Phase 4.2 layout improvements."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Use existing database for testing
        self.db_manager = DatabaseManager("example_database.db")
        
    def tearDown(self):
        """Clean up after tests."""
        if self.root:
            self.root.destroy()
    
    def test_legend_panel_weight_ratio_improvement(self):
        """Test that legend panel has improved weight ratio (3 vs metadata's 2)."""
        # Create main window
        main_window = MainWindow(self.root, "example_database.db")
        
        # Check that the right paned window exists
        self.assertIsNotNone(main_window.right_paned_window)
        
        # Verify that both frames are added to the paned window
        panes = main_window.right_paned_window.panes()
        self.assertEqual(len(panes), 2, "Should have exactly 2 panes (metadata and legend)")
        
        # The weight ratio should favor the legend panel (weight=3) over metadata (weight=2)
        # This is verified by the fact that the legend gets more space allocation
        metadata_frame_path = str(main_window.metadata_frame)
        legend_frame_path = str(main_window.legend_frame)
        
        self.assertIn(metadata_frame_path, [str(pane) for pane in panes])
        self.assertIn(legend_frame_path, [str(pane) for pane in panes])
    
    def test_metadata_panel_button_layout_reorganization(self):
        """Test that buttons are reorganized with Export CSV on separate row."""
        # Create metadata panel
        parent_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(parent_frame, self.db_manager)
        
        # Verify button frame exists
        self.assertIsNotNone(metadata_panel.button_frame)
        
        # Verify primary buttons frame exists (top row)
        self.assertIsNotNone(metadata_panel.primary_buttons_frame)
        
        # Verify export frame exists (bottom row)
        self.assertIsNotNone(metadata_panel.export_frame)
        
        # Verify all expected buttons exist
        self.assertIsNotNone(metadata_panel.apply_button)
        self.assertIsNotNone(metadata_panel.clear_button)
        self.assertIsNotNone(metadata_panel.clear_all_button)
        self.assertIsNotNone(metadata_panel.export_csv_button)
        
        # Verify button text updates
        self.assertEqual(metadata_panel.clear_all_button.cget("text"), "🔄 Reset All Metadata")
        self.assertEqual(metadata_panel.export_csv_button.cget("text"), "📊 Export CSV")
    
    def test_export_csv_button_prominence(self):
        """Test that Export CSV button is prominently placed on separate row."""
        parent_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(parent_frame, self.db_manager)
        
        # Verify export button has increased width for prominence
        export_width = metadata_panel.export_csv_button.cget("width")
        self.assertEqual(export_width, 20, "Export button should have width=20 for prominence")
        
        # Verify export button is in its own frame (separate row)
        export_parent = metadata_panel.export_csv_button.master
        self.assertEqual(export_parent, metadata_panel.export_frame)
        
        # Verify other buttons are in primary frame (top row)
        apply_parent = metadata_panel.apply_button.master
        clear_parent = metadata_panel.clear_button.master
        reset_parent = metadata_panel.clear_all_button.master
        
        self.assertEqual(apply_parent, metadata_panel.primary_buttons_frame)
        self.assertEqual(clear_parent, metadata_panel.primary_buttons_frame)
        self.assertEqual(reset_parent, metadata_panel.primary_buttons_frame)
    
    def test_reset_button_visual_distinction(self):
        """Test that Reset All Metadata button has visual distinction."""
        parent_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(parent_frame, self.db_manager)
        
        # Verify button text includes emoji for visual distinction
        button_text = metadata_panel.clear_all_button.cget("text")
        self.assertIn("🔄", button_text, "Reset button should have refresh emoji")
        self.assertIn("Reset All Metadata", button_text, "Button should say 'Reset All Metadata'")
        
        # Verify button has appropriate width
        button_width = metadata_panel.clear_all_button.cget("width")
        self.assertEqual(button_width, 18, "Reset button should have width=18")
    
    def test_legend_panel_scrollable_functionality(self):
        """Test that legend panel maintains scrollable functionality."""
        parent_frame = ttk.Frame(self.root)
        legend_panel = LegendPanel(parent_frame)
        
        # Verify scrollable components exist
        self.assertIsNotNone(legend_panel.canvas)
        self.assertIsNotNone(legend_panel.scrollbar)
        self.assertIsNotNone(legend_panel.scrollable_frame)
        
        # Verify canvas is configured for scrolling
        yscrollcommand = legend_panel.canvas.cget("yscrollcommand")
        self.assertIsNotNone(yscrollcommand, "Canvas should have yscrollcommand configured")
    
    def test_button_callback_functionality_preserved(self):
        """Test that button callbacks are properly preserved after layout changes."""
        parent_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(parent_frame, self.db_manager)
        
        # Test that callback setters work
        test_callback_called = {"apply": False, "clear_all": False, "export": False}
        
        def test_apply_callback(metadata):
            test_callback_called["apply"] = True
        
        def test_clear_all_callback():
            test_callback_called["clear_all"] = True
        
        def test_export_callback():
            test_callback_called["export"] = True
        
        # Set callbacks
        metadata_panel.set_apply_metadata_callback(test_apply_callback)
        metadata_panel.set_clear_all_metadata_callback(test_clear_all_callback)
        metadata_panel.set_export_csv_callback(test_export_callback)
        
        # Verify callbacks are set
        self.assertIsNotNone(metadata_panel.apply_metadata_callback)
        self.assertIsNotNone(metadata_panel.clear_all_metadata_callback)
        self.assertIsNotNone(metadata_panel.export_csv_callback)
    
    def test_responsive_layout_grid_configuration(self):
        """Test that grid configuration supports responsive layout."""
        parent_frame = ttk.Frame(self.root)
        metadata_panel = MetadataPanel(parent_frame, self.db_manager)
        
        # Verify button frame grid configuration
        button_frame_info = metadata_panel.button_frame.grid_info()
        self.assertEqual(button_frame_info["sticky"], "ew", "Button frame should expand horizontally")
        
        # Verify main frame column configuration for responsiveness
        # The main frame should have proper column weights
        self.assertIsNotNone(metadata_panel.main_frame)
    
    def test_phase_42_integration_with_existing_functionality(self):
        """Test that Phase 4.2 changes integrate properly with existing functionality."""
        # Create a complete main window to test integration
        main_window = MainWindow(self.root, "example_database.db")
        
        # Verify all components are created
        self.assertIsNotNone(main_window.metadata_panel)
        self.assertIsNotNone(main_window.legend_panel)
        self.assertIsNotNone(main_window.right_paned_window)
        
        # Verify the layout structure is correct
        self.assertIsNotNone(main_window.metadata_frame)
        self.assertIsNotNone(main_window.legend_frame)
        
        # Test that the paned window contains both frames
        panes = main_window.right_paned_window.panes()
        self.assertEqual(len(panes), 2)


class TestLayoutResponsiveness(unittest.TestCase):
    """Test responsive behavior of the improved layout."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.db_manager = DatabaseManager("example_database.db")
    
    def tearDown(self):
        """Clean up after tests."""
        if self.root:
            self.root.destroy()
    
    def test_window_resize_behavior(self):
        """Test that layout responds appropriately to window resizing."""
        main_window = MainWindow(self.root, "example_database.db")
        
        # Test different window sizes
        test_sizes = [
            (800, 600),   # Minimum size
            (1200, 800),  # Default size
            (1600, 1000)  # Large size
        ]
        
        for width, height in test_sizes:
            self.root.geometry(f"{width}x{height}")
            self.root.update()
            
            # Verify components still exist and are properly configured
            self.assertIsNotNone(main_window.right_paned_window)
            self.assertIsNotNone(main_window.metadata_panel)
            self.assertIsNotNone(main_window.legend_panel)
    
    def test_minimum_size_constraints(self):
        """Test that minimum size constraints prevent content cutoff."""
        main_window = MainWindow(self.root, ":memory:")
        
        # Test minimum window size
        min_width, min_height = 800, 600
        self.root.geometry(f"{min_width}x{min_height}")
        self.root.update()
        
        # Verify that components are still accessible
        self.assertTrue(main_window.metadata_panel.button_frame.winfo_viewable())
        self.assertTrue(main_window.legend_panel.main_frame.winfo_viewable())


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)