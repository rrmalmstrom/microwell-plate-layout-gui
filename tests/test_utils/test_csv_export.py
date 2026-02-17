"""
Comprehensive tests for CSV export functionality.

Tests cover:
- 96-well and 384-well plate formats
- Data mapping and field validation
- File I/O operations
- Error handling scenarios
- Integration with existing data structures
- Clear functionality integration
"""

import unittest
import tempfile
import os
import csv
from unittest.mock import Mock, patch, MagicMock
import sys
import tkinter as tk

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.utils.csv_export import (
    PlateCSVExporter, 
    CSVExportError, 
    export_plate_layout
)


class TestPlateCSVExporter(unittest.TestCase):
    """Test cases for PlateCSVExporter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.exporter = PlateCSVExporter()
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock plate canvas
        self.mock_plate_canvas = Mock()
        self.mock_plate_canvas.well_metadata = {}
        
        # Mock main window
        self.mock_main_window = Mock()
        self.mock_main_window.plate_type = "96"
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'test_sample',
            'plate_name': 'test_plate'
        }
        self.mock_main_window.multi_sample_config = None
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_plate_format_configurations(self):
        """Test that plate format configurations are correct."""
        # Test 96-well format
        format_96 = self.exporter.PLATE_FORMATS["96"]
        self.assertEqual(format_96["rows"], 8)
        self.assertEqual(format_96["cols"], 12)
        self.assertEqual(format_96["row_labels"], "ABCDEFGH")
        self.assertEqual(format_96["max_col"], 12)
        
        # Test 384-well format
        format_384 = self.exporter.PLATE_FORMATS["384"]
        self.assertEqual(format_384["rows"], 16)
        self.assertEqual(format_384["cols"], 24)
        self.assertEqual(format_384["row_labels"], "ABCDEFGHIJKLMNOP")
        self.assertEqual(format_384["max_col"], 24)
    
    def test_csv_headers(self):
        """Test that CSV headers match reference format."""
        expected_headers = [
            "Plate_ID",
            "Well_Row",
            "Well_Col",
            "Well",
            "Sample",
            "Type",
            "number_of_cells/capsules",
            "Group_1",
            "Group_2",
            "Group_3"
        ]
        self.assertEqual(self.exporter.CSV_HEADERS, expected_headers)
    
    def test_validate_export_inputs_success(self):
        """Test successful input validation."""
        # Add some metadata to pass validation
        self.mock_plate_canvas.well_metadata = {'A1': {'sample_type': 'sample'}}
        # Should not raise exception
        self.exporter._validate_export_inputs(self.mock_plate_canvas, self.mock_main_window)
    
    def test_validate_export_inputs_missing_well_metadata(self):
        """Test validation failure for missing well_metadata."""
        mock_canvas = Mock()
        del mock_canvas.well_metadata  # Remove attribute
        
        with self.assertRaises(CSVExportError) as context:
            self.exporter._validate_export_inputs(mock_canvas, self.mock_main_window)
        
        self.assertIn("well_metadata", str(context.exception))
    
    def test_validate_export_inputs_missing_plate_type(self):
        """Test validation failure for missing plate_type."""
        mock_window = Mock()
        del mock_window.plate_type  # Remove attribute
        
        with self.assertRaises(CSVExportError) as context:
            self.exporter._validate_export_inputs(self.mock_plate_canvas, mock_window)
        
        self.assertIn("plate_type", str(context.exception))
    
    def test_validate_export_inputs_unsupported_plate_type(self):
        """Test validation failure for unsupported plate type."""
        self.mock_main_window.plate_type = "invalid"
        
        with self.assertRaises(CSVExportError) as context:
            self.exporter._validate_export_inputs(self.mock_plate_canvas, self.mock_main_window)
        
        self.assertIn("Unsupported plate type", str(context.exception))
    
    def test_validate_export_inputs_empty_plate(self):
        """Test validation failure for empty plate."""
        self.mock_plate_canvas.well_metadata = {}
        
        with self.assertRaises(CSVExportError) as context:
            self.exporter._validate_export_inputs(self.mock_plate_canvas, self.mock_main_window)
        
        self.assertIn("No metadata found", str(context.exception))
    
    def test_get_plate_name_single_sample_mode(self):
        """Test plate name extraction for single sample mode."""
        plate_name = self.exporter._get_plate_name(self.mock_main_window)
        self.assertEqual(plate_name, "test_plate")
    
    def test_get_plate_name_multi_sample_mode(self):
        """Test plate name extraction for multi-sample mode."""
        self.mock_main_window.sample_mode = "multi"
        self.mock_main_window.single_sample_config = None
        self.mock_main_window.multi_sample_config = {
            'sample_plate_name': 'multi_test_plate'
        }
        
        plate_name = self.exporter._get_plate_name(self.mock_main_window)
        self.assertEqual(plate_name, "multi_test_plate")
    
    def test_get_plate_name_fallback(self):
        """Test plate name fallback when no configuration available."""
        self.mock_main_window.single_sample_config = None
        self.mock_main_window.multi_sample_config = None
        
        with patch('microwell_plate_gui.utils.csv_export.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "20240101_120000"
            plate_name = self.exporter._get_plate_name(self.mock_main_window)
            self.assertEqual(plate_name, "plate_96well_20240101_120000")
    
    def test_generate_filename(self):
        """Test filename generation."""
        # Test normal plate name
        filename = self.exporter._generate_filename("test_plate")
        self.assertEqual(filename, "test_plate.csv")
        
        # Test plate name with special characters
        filename = self.exporter._generate_filename("test/plate:name")
        self.assertEqual(filename, "test_plate_name.csv")
        
        # Test plate name already with .csv extension
        filename = self.exporter._generate_filename("test_plate.csv")
        self.assertEqual(filename, "test_plate.csv")
    
    def test_generate_well_csv_row_unused_well(self):
        """Test CSV row generation for unused well."""
        row = self.exporter._generate_well_csv_row(
            "A1", "A", 1, {}, "test_plate", self.mock_main_window
        )
        
        expected = [
            "test_plate",  # Plate_ID
            "A",           # Well_Row
            "1",           # Well_Col
            "A1",          # Well
            "",            # Sample
            "unused",      # Type
            "",            # number_of_cells/capsules
            "",            # Group_1
            "",            # Group_2
            ""             # Group_3
        ]
        self.assertEqual(row, expected)
    
    def test_generate_well_csv_row_with_metadata(self):
        """Test CSV row generation for well with metadata."""
        metadata = {
            'sample_type': 'sample',
            'cell_count': '100',
            'group1': 'Rep1',
            'group2': 'BONCAT',
            'group3': 'treatment'
        }
        
        row = self.exporter._generate_well_csv_row(
            "A1", "A", 1, metadata, "test_plate", self.mock_main_window
        )
        
        expected = [
            "test_plate",  # Plate_ID
            "A",           # Well_Row
            "1",           # Well_Col
            "A1",          # Well
            "test_sample", # Sample (from single_sample_config)
            "sample",      # Type
            "100",         # number_of_cells/capsules
            "Rep1",        # Group_1
            "BONCAT",      # Group_2
            "treatment"    # Group_3
        ]
        self.assertEqual(row, expected)
    
    def test_generate_well_csv_row_unused_type_clears_fields(self):
        """Test that unused type clears group and cell count fields."""
        metadata = {
            'sample_type': 'unused',
            'cell_count': '100',  # Should be cleared
            'group1': 'Rep1',     # Should be cleared
            'group2': 'BONCAT',   # Should be cleared
            'group3': 'treatment' # Should be cleared
        }
        
        row = self.exporter._generate_well_csv_row(
            "A1", "A", 1, metadata, "test_plate", self.mock_main_window
        )
        
        expected = [
            "test_plate",  # Plate_ID
            "A",           # Well_Row
            "1",           # Well_Col
            "A1",          # Well
            "",            # Sample (cleared for unused)
            "unused",      # Type
            "",            # number_of_cells/capsules (cleared)
            "",            # Group_1 (cleared)
            "",            # Group_2 (cleared)
            ""             # Group_3 (cleared)
        ]
        self.assertEqual(row, expected)
    
    def test_generate_csv_data_96_well(self):
        """Test CSV data generation for 96-well plate."""
        # Add some test metadata
        self.mock_plate_canvas.well_metadata = {
            'A1': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1'},
            'B2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'control'}
        }
        
        plate_config = self.exporter.PLATE_FORMATS["96"]
        csv_data = self.exporter._generate_csv_data(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            plate_config, 
            "test_plate"
        )
        
        # Check headers
        self.assertEqual(csv_data[0], self.exporter.CSV_HEADERS)
        
        # Check total rows (header + 96 wells)
        self.assertEqual(len(csv_data), 97)
        
        # Check first data row (A1)
        a1_row = csv_data[1]
        self.assertEqual(a1_row[0], "test_plate")  # Plate_ID
        self.assertEqual(a1_row[1], "A")           # Well_Row
        self.assertEqual(a1_row[2], "1")           # Well_Col
        self.assertEqual(a1_row[3], "A1")          # Well
        self.assertEqual(a1_row[4], "test_sample") # Sample
        self.assertEqual(a1_row[5], "sample")      # Type
        
        # Check that wells are in correct order (A1, A2, ..., A12, B1, B2, ...)
        self.assertEqual(csv_data[1][3], "A1")   # First well
        self.assertEqual(csv_data[2][3], "A2")   # Second well
        self.assertEqual(csv_data[12][3], "A12") # Last well of first row
        self.assertEqual(csv_data[13][3], "B1")  # First well of second row
    
    def test_generate_csv_data_384_well(self):
        """Test CSV data generation for 384-well plate."""
        self.mock_main_window.plate_type = "384"
        
        # Add some test metadata
        self.mock_plate_canvas.well_metadata = {
            'A1': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1'},
            'P24': {'sample_type': 'sample', 'cell_count': '50', 'group1': 'Rep2'}
        }
        
        plate_config = self.exporter.PLATE_FORMATS["384"]
        csv_data = self.exporter._generate_csv_data(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            plate_config, 
            "test_plate"
        )
        
        # Check headers
        self.assertEqual(csv_data[0], self.exporter.CSV_HEADERS)
        
        # Check total rows (header + 384 wells)
        self.assertEqual(len(csv_data), 385)
        
        # Check first and last wells
        self.assertEqual(csv_data[1][3], "A1")    # First well
        self.assertEqual(csv_data[-1][3], "P24")  # Last well
    
    def test_write_csv_file_success(self):
        """Test successful CSV file writing."""
        test_file = os.path.join(self.temp_dir, "test_export.csv")
        csv_data = [
            self.exporter.CSV_HEADERS,
            ["test_plate", "A", "1", "A1", "sample", "100", "Rep1", "BONCAT", ""]
        ]
        
        # Should not raise exception
        self.exporter._write_csv_file(test_file, csv_data)
        
        # Verify file was created and has correct content
        self.assertTrue(os.path.exists(test_file))
        
        # Read with standard UTF-8 encoding
        with open(test_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(rows, csv_data)
    
    def test_write_csv_file_permission_error(self):
        """Test CSV file writing with permission error."""
        # Try to write to a directory that doesn't exist and can't be created
        invalid_path = "/invalid/path/test.csv"
        csv_data = [self.exporter.CSV_HEADERS]
        
        with self.assertRaises(CSVExportError) as context:
            self.exporter._write_csv_file(invalid_path, csv_data)
        
        self.assertIn("error writing", str(context.exception).lower())
    
    def test_validate_csv_format_success(self):
        """Test successful CSV format validation."""
        test_file = os.path.join(self.temp_dir, "test_validate.csv")
        
        # Create valid CSV file
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.exporter.CSV_HEADERS)
            writer.writerow(["test_plate", "A", "1", "A1", "test_sample", "sample", "100", "Rep1", "BONCAT", ""])
        
        is_valid, errors = self.exporter.validate_csv_format(test_file)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_csv_format_invalid_headers(self):
        """Test CSV format validation with invalid headers."""
        test_file = os.path.join(self.temp_dir, "test_invalid_headers.csv")
        
        # Create CSV with invalid headers
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Invalid", "Headers"])
            writer.writerow(["test_plate", "A", "1", "A1", "sample", "100", "Rep1", "BONCAT", ""])
        
        is_valid, errors = self.exporter.validate_csv_format(test_file)
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid headers" in error for error in errors))
    
    def test_validate_csv_format_invalid_well_name(self):
        """Test CSV format validation with invalid well name."""
        test_file = os.path.join(self.temp_dir, "test_invalid_well.csv")
        
        # Create CSV with invalid well name
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.exporter.CSV_HEADERS)
            writer.writerow(["test_plate", "A", "1", "INVALID", "test_sample", "sample", "100", "Rep1", "BONCAT", ""])
        
        is_valid, errors = self.exporter.validate_csv_format(test_file)
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid well name" in error for error in errors))
    
    def test_export_plate_to_csv_full_integration(self):
        """Test full CSV export integration."""
        # Set up test data
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample_type': 'sample',
                'cell_count': '100',
                'group1': 'Rep1',
                'group2': 'BONCAT',
                'group3': ''
            },
            'A2': {
                'sample_type': 'neg_cntrl',
                'cell_count': '0',
                'group1': 'control',
                'group2': '',
                'group3': ''
            }
        }
        
        test_file = os.path.join(self.temp_dir, "integration_test.csv")
        
        # Perform export
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Verify export
        self.assertEqual(exported_file, test_file)
        self.assertTrue(os.path.exists(test_file))
        
        # Validate CSV format
        is_valid, errors = self.exporter.validate_csv_format(test_file)
        self.assertTrue(is_valid, f"CSV validation failed: {errors}")
        
        # Check specific content
        with open(test_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Check headers
            self.assertEqual(rows[0], self.exporter.CSV_HEADERS)
            
            # Check A1 row
            a1_row = rows[1]
            self.assertEqual(a1_row[3], "A1")
            self.assertEqual(a1_row[4], "test_sample")  # Sample
            self.assertEqual(a1_row[5], "sample")       # Type
            self.assertEqual(a1_row[6], "100")          # number_of_cells/capsules
            self.assertEqual(a1_row[7], "Rep1")         # Group_1
            self.assertEqual(a1_row[8], "BONCAT")       # Group_2
            
            # Check A2 row
            a2_row = rows[2]
            self.assertEqual(a2_row[3], "A2")
            self.assertEqual(a2_row[4], "test_sample")  # Sample
            self.assertEqual(a2_row[5], "neg_cntrl")    # Type
            self.assertEqual(a2_row[6], "0")            # number_of_cells/capsules
            self.assertEqual(a2_row[7], "control")      # Group_1


class TestConvenienceFunction(unittest.TestCase):
    """Test cases for the convenience export function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock components
        self.mock_plate_canvas = Mock()
        self.mock_plate_canvas.well_metadata = {
            'A1': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1'}
        }
        
        self.mock_main_window = Mock()
        self.mock_main_window.plate_type = "96"
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'test_sample',
            'plate_name': 'test_plate'
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_export_plate_layout_convenience_function(self):
        """Test the convenience export function."""
        test_file = os.path.join(self.temp_dir, "convenience_test.csv")
        
        exported_file = export_plate_layout(
            self.mock_plate_canvas,
            self.mock_main_window,
            test_file
        )
        
        self.assertEqual(exported_file, test_file)
        self.assertTrue(os.path.exists(test_file))


class TestClearFunctionalityIntegration(unittest.TestCase):
    """Test integration with existing clear functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.exporter = PlateCSVExporter()
        
        # Mock plate canvas with metadata
        self.mock_plate_canvas = Mock()
        self.mock_plate_canvas.well_metadata = {
            'A1': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1'},
            'A2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'control'}
        }
        
        self.mock_main_window = Mock()
        self.mock_main_window.plate_type = "96"
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'test_sample',
            'plate_name': 'test_plate'
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_export_after_clear_fails_validation(self):
        """Test that export fails validation after clear operation."""
        # First, verify export works with data
        test_file = os.path.join(self.temp_dir, "before_clear.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas,
            self.mock_main_window,
            test_file
        )
        self.assertTrue(os.path.exists(exported_file))
        
        # Simulate clear operation
        self.mock_plate_canvas.well_metadata.clear()
        
        # Now export should fail validation
        test_file_after = os.path.join(self.temp_dir, "after_clear.csv")
        with self.assertRaises(CSVExportError) as context:
            self.exporter.export_plate_to_csv(
                self.mock_plate_canvas,
                self.mock_main_window,
                test_file_after
            )
        
        self.assertIn("No metadata found", str(context.exception))
    
    def test_export_state_reset_after_clear(self):
        """Test that export state is properly reset after clear."""
        # Verify we have metadata initially
        self.assertTrue(bool(self.mock_plate_canvas.well_metadata))
        
        # Simulate clear operation
        self.mock_plate_canvas.well_metadata.clear()
        
        # Verify metadata is cleared
        self.assertFalse(bool(self.mock_plate_canvas.well_metadata))
        
        # Verify validation catches empty state
        with self.assertRaises(CSVExportError):
            self.exporter._validate_export_inputs(
                self.mock_plate_canvas,
                self.mock_main_window
            )


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)