"""
ATDD (Acceptance Test Driven Development) tests for CSV export Sample column functionality.

These tests follow ATDD principles by testing user-facing scenarios and acceptance criteria:
- Single-sample mode: Sample column populated with configured sample name
- Multi-sample mode: Sample column populated with well-specific sample data
- Unused wells: Sample column remains empty
- CSV format: Sample column positioned correctly between Well and Type columns

Test scenarios cover both happy path and edge cases to ensure robust functionality.
"""

import unittest
import tempfile
import os
import csv
from unittest.mock import Mock
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.utils.csv_export import (
    PlateCSVExporter, 
    CSVExportError, 
    export_plate_layout
)


class TestSampleColumnATDD(unittest.TestCase):
    """
    ATDD tests for Sample column functionality in CSV export.
    
    These tests verify that the Sample column is correctly populated based on
    the sample mode (single vs multi) and well metadata configuration.
    """
    
    def setUp(self):
        """Set up test fixtures for ATDD scenarios."""
        self.exporter = PlateCSVExporter()
        self.temp_dir = tempfile.mkdtemp()
        
        # Base mock plate canvas
        self.mock_plate_canvas = Mock()
        self.mock_plate_canvas.well_metadata = {}
        
        # Base mock main window
        self.mock_main_window = Mock()
        self.mock_main_window.plate_type = "96"
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_csv_headers_include_sample_column(self):
        """
        ATDD Scenario: CSV headers must include Sample column in correct position
        
        Given: A CSV exporter
        When: I check the CSV headers
        Then: The Sample column should be positioned between Well and Type columns
        """
        expected_headers = [
            "Plate_ID",
            "Well_Row", 
            "Well_Col",
            "Well",
            "Sample",  # Sample column should be here
            "Type",
            "number_of_cells/capsules",
            "Group_1",
            "Group_2", 
            "Group_3"
        ]
        self.assertEqual(self.exporter.CSV_HEADERS, expected_headers)
    
    def test_single_sample_mode_populates_sample_column(self):
        """
        ATDD Scenario: Single-sample mode populates Sample column with configured sample name
        
        Given: A plate in single-sample mode with sample name "TestSample123"
        And: Wells A1 and B2 have sample metadata
        When: I export the plate to CSV
        Then: All non-unused wells should have "TestSample123" in the Sample column
        """
        # Given: Single-sample mode configuration
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'TestSample123',
            'plate_name': 'TestPlate'
        }
        self.mock_main_window.multi_sample_config = None
        
        # And: Wells with sample metadata
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample_type': 'sample',
                'cell_count': '100',
                'group1': 'Rep1',
                'group2': 'BONCAT',
                'group3': ''
            },
            'B2': {
                'sample_type': 'neg_control',
                'cell_count': '0',
                'group1': 'control',
                'group2': '',
                'group3': ''
            }
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "single_sample_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Verify Sample column content
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Check headers
            self.assertEqual(rows[0][4], "Sample")
            
            # Find A1 and B2 rows and verify Sample column
            for row in rows[1:]:  # Skip header
                if row[3] == "A1":  # Well column
                    self.assertEqual(row[4], "TestSample123", "A1 should have configured sample name")
                    self.assertEqual(row[5], "sample", "A1 should have sample type")
                elif row[3] == "B2":  # Well column
                    self.assertEqual(row[4], "TestSample123", "B2 should have configured sample name")
                    self.assertEqual(row[5], "neg_control", "B2 should have neg_control type")
                elif row[5] == "unused":  # Type column for unused wells
                    self.assertEqual(row[4], "", "Unused wells should have empty Sample column")
    
    def test_multi_sample_mode_uses_well_specific_sample_data(self):
        """
        ATDD Scenario: Multi-sample mode uses well-specific sample data
        
        Given: A plate in multi-sample mode
        And: Well A1 has sample "SampleA" and well B2 has sample "SampleB"
        When: I export the plate to CSV
        Then: A1 should have "SampleA" and B2 should have "SampleB" in Sample column
        """
        # Given: Multi-sample mode configuration
        self.mock_main_window.sample_mode = "multi"
        self.mock_main_window.single_sample_config = None
        self.mock_main_window.multi_sample_config = {
            'sample_plate_name': 'MultiSamplePlate'
        }
        
        # And: Wells with different sample data
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample': 'SampleA',  # Well-specific sample
                'sample_type': 'sample',
                'cell_count': '100',
                'group1': 'Rep1'
            },
            'B2': {
                'sample': 'SampleB',  # Different well-specific sample
                'sample_type': 'sample',
                'cell_count': '50',
                'group1': 'Rep2'
            },
            'C3': {
                'sample': 'SampleC',
                'sample_type': 'pos_control',
                'cell_count': '75',
                'group1': 'control'
            }
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "multi_sample_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Verify well-specific Sample column content
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Find specific wells and verify their sample data
            for row in rows[1:]:  # Skip header
                if row[3] == "A1":
                    self.assertEqual(row[4], "SampleA", "A1 should have SampleA")
                elif row[3] == "B2":
                    self.assertEqual(row[4], "SampleB", "B2 should have SampleB")
                elif row[3] == "C3":
                    self.assertEqual(row[4], "SampleC", "C3 should have SampleC")
                elif row[5] == "unused":  # Type column for unused wells
                    self.assertEqual(row[4], "", "Unused wells should have empty Sample column")
    
    def test_unused_wells_have_empty_sample_column(self):
        """
        ATDD Scenario: Unused wells have empty Sample column
        
        Given: A plate with some unused wells
        When: I export the plate to CSV
        Then: Unused wells should have empty Sample column
        """
        # Given: Mixed well configuration
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'TestSample',
            'plate_name': 'TestPlate'
        }
        
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample_type': 'sample',
                'cell_count': '100'
            },
            'B2': {
                'sample_type': 'unused',  # Explicitly unused
                'cell_count': '',
                'group1': '',
                'group2': '',
                'group3': ''
            }
            # C3 has no metadata (implicitly unused)
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "unused_wells_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Verify unused wells have empty Sample column
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            for row in rows[1:]:  # Skip header
                if row[3] == "A1":
                    self.assertEqual(row[4], "TestSample", "A1 should have sample name")
                    self.assertEqual(row[5], "sample", "A1 should be sample type")
                elif row[3] == "B2":
                    self.assertEqual(row[4], "", "B2 (unused) should have empty Sample column")
                    self.assertEqual(row[5], "unused", "B2 should be unused type")
                elif row[3] == "C3":
                    self.assertEqual(row[4], "", "C3 (no metadata) should have empty Sample column")
                    self.assertEqual(row[5], "unused", "C3 should be unused type")
    
    def test_sample_column_position_in_csv_output(self):
        """
        ATDD Scenario: Sample column is in correct position in CSV output
        
        Given: A plate with sample data
        When: I export the plate to CSV
        Then: The Sample column should be the 5th column (index 4) in each row
        """
        # Given: Sample configuration
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'PositionTest',
            'plate_name': 'TestPlate'
        }
        
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample_type': 'sample',
                'cell_count': '100',
                'group1': 'Rep1',
                'group2': 'BONCAT',
                'group3': 'treatment'
            }
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "position_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Verify column positions
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Check header positions
            headers = rows[0]
            self.assertEqual(headers[0], "Plate_ID")
            self.assertEqual(headers[1], "Well_Row")
            self.assertEqual(headers[2], "Well_Col")
            self.assertEqual(headers[3], "Well")
            self.assertEqual(headers[4], "Sample")  # Sample should be 5th column
            self.assertEqual(headers[5], "Type")
            self.assertEqual(headers[6], "number_of_cells/capsules")
            self.assertEqual(headers[7], "Group_1")
            self.assertEqual(headers[8], "Group_2")
            self.assertEqual(headers[9], "Group_3")
            
            # Check A1 data positions
            a1_row = None
            for row in rows[1:]:
                if row[3] == "A1":
                    a1_row = row
                    break
            
            self.assertIsNotNone(a1_row, "A1 row should exist")
            self.assertEqual(a1_row[0], "TestPlate")      # Plate_ID
            self.assertEqual(a1_row[1], "A")              # Well_Row
            self.assertEqual(a1_row[2], "1")              # Well_Col
            self.assertEqual(a1_row[3], "A1")             # Well
            self.assertEqual(a1_row[4], "PositionTest")   # Sample
            self.assertEqual(a1_row[5], "sample")         # Type
            self.assertEqual(a1_row[6], "100")            # number_of_cells/capsules
            self.assertEqual(a1_row[7], "Rep1")           # Group_1
            self.assertEqual(a1_row[8], "BONCAT")         # Group_2
            self.assertEqual(a1_row[9], "treatment")      # Group_3
    
    def test_missing_sample_config_fallback(self):
        """
        ATDD Scenario: Missing sample configuration falls back gracefully
        
        Given: A plate with no sample configuration
        When: I export the plate to CSV
        Then: Sample column should be empty for all wells
        """
        # Given: No sample configuration
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = None
        self.mock_main_window.multi_sample_config = None
        
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                'sample_type': 'sample',
                'cell_count': '100'
            }
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "no_config_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Sample column should be empty
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            for row in rows[1:]:  # Skip header
                if row[3] == "A1":
                    self.assertEqual(row[4], "", "A1 should have empty Sample column when no config")
                    self.assertEqual(row[5], "sample", "A1 should still have correct type")
    
    def test_multi_sample_missing_well_sample_data(self):
        """
        ATDD Scenario: Multi-sample mode with missing well sample data
        
        Given: A plate in multi-sample mode
        And: A well has metadata but no sample field
        When: I export the plate to CSV
        Then: That well should have empty Sample column
        """
        # Given: Multi-sample mode
        self.mock_main_window.sample_mode = "multi"
        self.mock_main_window.single_sample_config = None
        self.mock_main_window.multi_sample_config = {
            'sample_plate_name': 'MultiSamplePlate'
        }
        
        # And: Well with missing sample field
        self.mock_plate_canvas.well_metadata = {
            'A1': {
                # No 'sample' field
                'sample_type': 'sample',
                'cell_count': '100',
                'group1': 'Rep1'
            }
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "missing_sample_data_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Sample column should be empty
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            for row in rows[1:]:  # Skip header
                if row[3] == "A1":
                    self.assertEqual(row[4], "", "A1 should have empty Sample column when sample field missing")
                    self.assertEqual(row[5], "sample", "A1 should still have correct type")
    
    def test_384_well_plate_sample_column(self):
        """
        ATDD Scenario: Sample column works correctly for 384-well plates
        
        Given: A 384-well plate in single-sample mode
        When: I export the plate to CSV
        Then: All wells should have correct Sample column data
        """
        # Given: 384-well plate configuration
        self.mock_main_window.plate_type = "384"
        self.mock_main_window.sample_mode = "single"
        self.mock_main_window.single_sample_config = {
            'sample': 'Sample384',
            'plate_name': 'Plate384'
        }
        
        self.mock_plate_canvas.well_metadata = {
            'A1': {'sample_type': 'sample', 'cell_count': '100'},
            'P24': {'sample_type': 'sample', 'cell_count': '50'}  # Last well
        }
        
        # When: Export to CSV
        test_file = os.path.join(self.temp_dir, "384_well_test.csv")
        exported_file = self.exporter.export_plate_to_csv(
            self.mock_plate_canvas, 
            self.mock_main_window, 
            test_file
        )
        
        # Then: Verify 384-well format and Sample column
        with open(exported_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Should have 385 rows (header + 384 wells)
            self.assertEqual(len(rows), 385, "Should have 384 wells + header")
            
            # Check first and last wells
            for row in rows[1:]:
                if row[3] == "A1":
                    self.assertEqual(row[4], "Sample384", "A1 should have sample name")
                elif row[3] == "P24":
                    self.assertEqual(row[4], "Sample384", "P24 should have sample name")
                elif row[5] == "unused":
                    self.assertEqual(row[4], "", "Unused wells should have empty Sample column")


if __name__ == '__main__':
    # Run ATDD tests with verbose output
    unittest.main(verbosity=2)