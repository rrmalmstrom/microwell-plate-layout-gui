"""
Test cases for workflow dialogs in the microwell plate GUI application.

Tests the new single-sample and multi-sample workflow dialogs.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.main_window import SingleSampleDialog, MultiSampleDialog
from microwell_plate_gui.data.database import DatabaseManager


class TestSingleSampleDialog(unittest.TestCase):
    """Test cases for SingleSampleDialog."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        
        # Mock database manager
        self.mock_db_manager = Mock(spec=DatabaseManager)
        self.mock_db_manager.get_existing_samples.return_value = ["Sample1", "Sample2", "Sample3"]
        self.mock_db_manager.generate_plate_names.return_value = ["Project.Sample1.1", "Project.Sample1.2"]
    
    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()
    
    def test_dialog_initialization(self):
        """Test that dialog initializes correctly."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Check that dialog window is created
        self.assertIsNotNone(dialog.dialog)
        self.assertEqual(dialog.dialog.title(), "Single Sample Configuration")
        
        # Check that variables are initialized
        self.assertIsInstance(dialog.sample_var, tk.StringVar)
        self.assertIsInstance(dialog.plate_name_var, tk.StringVar)
        
        dialog.dialog.destroy()
    
    def test_dropdown_population(self):
        """Test that dropdowns are populated from database."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Check that database manager was called
        self.mock_db_manager.get_existing_samples.assert_called_once()
        
        # Check that sample dropdown has values including "other"
        sample_values = dialog.sample_combo['values']
        self.assertIn("Sample1", sample_values)
        self.assertIn("Sample2", sample_values)
        self.assertIn("Sample3", sample_values)
        self.assertIn("other", sample_values)
        
        dialog.dialog.destroy()
    
    def test_sample_selection_updates_plate_names(self):
        """Test that selecting a sample updates plate name dropdown."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Select a sample
        dialog.sample_var.set("Sample1")
        
        # Check that generate_plate_names was called
        self.mock_db_manager.generate_plate_names.assert_called_with("", "Sample1")
        
        # Check that plate name dropdown was updated
        plate_values = dialog.plate_name_combo['values']
        self.assertIn("Project.Sample1.1", plate_values)
        self.assertIn("Project.Sample1.2", plate_values)
        self.assertIn("other", plate_values)
        
        dialog.dialog.destroy()
    
    def test_other_field_visibility(self):
        """Test that 'other' fields show/hide correctly."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Initially, other fields should not be gridded (hidden)
        # Check if they have grid info (if not gridded, grid_info returns empty dict)
        sample_grid_info = dialog.sample_other_entry.grid_info()
        plate_grid_info = dialog.plate_name_other_entry.grid_info()
        self.assertEqual(len(sample_grid_info), 0)  # Not gridded
        self.assertEqual(len(plate_grid_info), 0)   # Not gridded
        
        # Select "other" for sample
        dialog.sample_var.set("other")
        self.root.update()  # Process events
        
        # Sample other field should now be gridded (visible)
        sample_grid_info = dialog.sample_other_entry.grid_info()
        self.assertGreater(len(sample_grid_info), 0)  # Now gridded
        
        # Select "other" for plate name
        dialog.plate_name_var.set("other")
        self.root.update()  # Process events
        
        # Plate name other field should now be gridded (visible)
        plate_grid_info = dialog.plate_name_other_entry.grid_info()
        self.assertGreater(len(plate_grid_info), 0)  # Now gridded
        
        dialog.dialog.destroy()
    
    def test_validation_success(self):
        """Test successful form validation."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Set valid values
        dialog.sample_var.set("Sample1")
        dialog.plate_name_var.set("Project.Sample1.1")
        
        is_valid, errors = dialog._validate_form()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        dialog.dialog.destroy()
    
    def test_validation_failure_empty_sample(self):
        """Test validation failure with empty sample."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Leave sample empty
        dialog.plate_name_var.set("Project.Sample1.1")
        
        is_valid, errors = dialog._validate_form()
        self.assertFalse(is_valid)
        self.assertIn("Sample is required", errors)
        
        dialog.dialog.destroy()
    
    def test_validation_failure_other_without_text(self):
        """Test validation failure when 'other' is selected but no text provided."""
        dialog = SingleSampleDialog(self.root, self.mock_db_manager)
        
        # Select "other" but don't provide text
        dialog.sample_var.set("other")
        dialog.plate_name_var.set("Project.Sample1.1")
        
        is_valid, errors = dialog._validate_form()
        self.assertFalse(is_valid)
        self.assertIn("Please specify the sample name when 'other' is selected", errors)
        
        dialog.dialog.destroy()


class TestMultiSampleDialog(unittest.TestCase):
    """Test cases for MultiSampleDialog."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
    
    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()
    
    def test_dialog_initialization(self):
        """Test that dialog initializes correctly."""
        dialog = MultiSampleDialog(self.root)
        
        # Check that dialog window is created
        self.assertIsNotNone(dialog.dialog)
        self.assertEqual(dialog.dialog.title(), "Multi-Sample Configuration")
        
        # Check that variable is initialized
        self.assertIsInstance(dialog.plate_name_var, tk.StringVar)
        
        dialog.dialog.destroy()
    
    def test_validation_success(self):
        """Test successful validation with plate name."""
        dialog = MultiSampleDialog(self.root)
        
        # Set valid plate name
        dialog.plate_name_var.set("TestPlate123")
        
        # Simulate continue button click
        dialog.result = None
        dialog._on_continue()
        
        # Check that result was set
        self.assertIsNotNone(dialog.result)
        self.assertEqual(dialog.result['sample_plate_name'], "TestPlate123")
        
        dialog.dialog.destroy()
    
    @patch('tkinter.messagebox.showerror')
    def test_validation_failure_empty_plate_name(self, mock_showerror):
        """Test validation failure with empty plate name."""
        dialog = MultiSampleDialog(self.root)
        
        # Leave plate name empty
        dialog.plate_name_var.set("")
        
        # Simulate continue button click
        dialog.result = None
        dialog._on_continue()
        
        # Check that error was shown and result is None
        mock_showerror.assert_called_once_with("Validation Error", "Sample plate name is required")
        self.assertIsNone(dialog.result)
        
        dialog.dialog.destroy()


class TestWorkflowIntegration(unittest.TestCase):
    """Test cases for workflow integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
    
    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()
    
    def test_single_sample_workflow_result_format(self):
        """Test that single sample dialog returns correct result format."""
        mock_db_manager = Mock(spec=DatabaseManager)
        mock_db_manager.get_existing_samples.return_value = ["Sample1"]
        mock_db_manager.generate_plate_names.return_value = ["Project.Sample1.1"]
        
        dialog = SingleSampleDialog(self.root, mock_db_manager)
        
        # Set values and simulate continue
        dialog.sample_var.set("Sample1")
        dialog.plate_name_var.set("Project.Sample1.1")
        dialog._on_continue()
        
        # Check result format
        expected_result = {
            'sample': 'Sample1',
            'plate_name': 'Project.Sample1.1'
        }
        self.assertEqual(dialog.result, expected_result)
        
        dialog.dialog.destroy()
    
    def test_multi_sample_workflow_result_format(self):
        """Test that multi sample dialog returns correct result format."""
        dialog = MultiSampleDialog(self.root)
        
        # Set value and simulate continue
        dialog.plate_name_var.set("MultiSamplePlate")
        dialog._on_continue()
        
        # Check result format
        expected_result = {
            'sample_plate_name': 'MultiSamplePlate'
        }
        self.assertEqual(dialog.result, expected_result)
        
        dialog.dialog.destroy()


if __name__ == '__main__':
    unittest.main()