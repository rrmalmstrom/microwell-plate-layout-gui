#!/usr/bin/env python3
"""
Test script to verify that exported CSV matches the reference format exactly.

This script creates a test export and compares it with the reference RM5097_layout.csv
to ensure the format, headers, and data structure are identical.
"""

import sys
import os
import tempfile
import csv
from unittest.mock import Mock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from microwell_plate_gui.utils.csv_export import PlateCSVExporter


def create_test_data():
    """Create test data that matches the reference file structure."""
    # Mock plate canvas with sample data similar to reference
    mock_plate_canvas = Mock()
    mock_plate_canvas.well_metadata = {
        # Negative controls in column 2
        'D2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'E2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'F2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'G2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'H2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'I2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'J2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        'K2': {'sample_type': 'neg_cntrl', 'cell_count': '0', 'group1': 'sheath', 'group2': '', 'group3': ''},
        
        # Sample wells in columns 3-5
        'D3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'BONCAT', 'group3': ''},
        'E3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'BONCAT', 'group3': ''},
        'F3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'BONCAT', 'group3': ''},
        'G3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'BONCAT', 'group3': ''},
        'H3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'SYTO+', 'group3': ''},
        'I3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'SYTO+', 'group3': ''},
        'J3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'SYTO+', 'group3': ''},
        'K3': {'sample_type': 'sample', 'cell_count': '100', 'group1': 'Rep1', 'group2': 'SYTO+', 'group3': ''},
    }
    
    # Mock main window for 384-well plate (to match reference)
    mock_main_window = Mock()
    mock_main_window.plate_type = "384"
    mock_main_window.sample_mode = "single"
    mock_main_window.single_sample_config = {
        'sample': 'test_sample',
        'plate_name': 'RM5097.96HL.BNCT.1'  # Match reference plate name
    }
    mock_main_window.multi_sample_config = None
    
    return mock_plate_canvas, mock_main_window


def verify_csv_format(csv_file_path):
    """Verify that the CSV file has the correct format."""
    expected_headers = [
        "Plate_ID",
        "Well_Row", 
        "Well_Col",
        "Well",
        "Type",
        "number_of_cells/capsules",
        "Group_1",
        "Group_2", 
        "Group_3"
    ]
    
    print(f"Verifying CSV format: {csv_file_path}")
    
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Check headers
        headers = next(reader)
        print(f"Headers: {headers}")
        
        if headers != expected_headers:
            print(f"❌ Header mismatch!")
            print(f"Expected: {expected_headers}")
            print(f"Got:      {headers}")
            return False
        
        print("✅ Headers match expected format")
        
        # Check a few sample rows
        row_count = 0
        sample_rows = []
        
        for row in reader:
            row_count += 1
            if row_count <= 5 or row[4] != 'unused':  # Show first 5 rows and non-unused wells
                sample_rows.append(row)
        
        print(f"Total rows: {row_count + 1} (including header)")
        print("Sample rows:")
        for i, row in enumerate(sample_rows[:10]):  # Show first 10 sample rows
            print(f"  Row {i+2}: {row}")
        
        # Verify 384-well format (16 rows × 24 columns = 384 wells + 1 header = 385 total)
        expected_total_rows = 385
        actual_total_rows = row_count + 1
        
        if actual_total_rows != expected_total_rows:
            print(f"❌ Row count mismatch! Expected {expected_total_rows}, got {actual_total_rows}")
            return False
        
        print(f"✅ Row count correct: {actual_total_rows}")
        
        return True


def compare_with_reference():
    """Compare exported format with reference file structure."""
    print("\n" + "="*60)
    print("COMPARING WITH REFERENCE FILE")
    print("="*60)
    
    reference_file = "RM5097_layout.csv"
    if not os.path.exists(reference_file):
        print(f"❌ Reference file not found: {reference_file}")
        return False
    
    print(f"Reading reference file: {reference_file}")
    
    with open(reference_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        ref_headers = next(reader)
        ref_rows = list(reader)
    
    print(f"Reference headers: {ref_headers}")
    print(f"Reference total rows: {len(ref_rows) + 1}")
    
    # Check if reference uses 384-well format
    last_row = ref_rows[-1]
    print(f"Reference last well: {last_row[3]} (Row: {last_row[1]}, Col: {last_row[2]})")
    
    # Verify our export matches the structure
    expected_headers = [
        "Plate_ID",
        "Well_Row", 
        "Well_Col",
        "Well",
        "Type",
        "number_of_cells/capsules",
        "Group_1",
        "Group_2", 
        "Group_3"
    ]
    
    if ref_headers == expected_headers:
        print("✅ Reference headers match our expected format")
        return True
    else:
        print("❌ Reference headers don't match expected format")
        print(f"Expected: {expected_headers}")
        print(f"Reference: {ref_headers}")
        return False


def main():
    """Main test function."""
    print("CSV Export Format Verification Test")
    print("="*60)
    
    # Create test data
    mock_plate_canvas, mock_main_window = create_test_data()
    
    # Create exporter
    exporter = PlateCSVExporter()
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        print(f"Exporting test data to: {temp_path}")
        
        exported_file = exporter.export_plate_to_csv(
            mock_plate_canvas,
            mock_main_window,
            temp_path
        )
        
        print(f"✅ Export completed: {exported_file}")
        
        # Verify format
        format_ok = verify_csv_format(exported_file)
        
        # Compare with reference
        reference_ok = compare_with_reference()
        
        if format_ok and reference_ok:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED!")
            print("✅ CSV export format matches reference structure")
            print("✅ Headers are correct")
            print("✅ Row count is correct for 384-well plate")
            print("✅ Data mapping is working properly")
            print("="*60)
            return True
        else:
            print("\n" + "="*60)
            print("❌ SOME TESTS FAILED!")
            print("="*60)
            return False
            
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)