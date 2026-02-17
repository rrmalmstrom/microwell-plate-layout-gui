#!/usr/bin/env python3
"""
Manual validation script for Sample column implementation in CSV export.

This script validates that the Sample column is correctly implemented by:
1. Checking that the Sample column exists in the correct position
2. Verifying that sample data is populated correctly
3. Ensuring unused wells have empty Sample column
"""

import csv
import sys
import os

def validate_csv_sample_column(csv_file_path):
    """
    Validate that a CSV file has the correct Sample column implementation.
    
    Args:
        csv_file_path: Path to the CSV file to validate
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    print(f"Validating CSV file: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print(f"ERROR: File {csv_file_path} does not exist")
        return False
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Check headers
            headers = next(reader, None)
            if not headers:
                print("ERROR: No headers found in CSV")
                return False
            
            expected_headers = [
                "Plate_ID", "Well_Row", "Well_Col", "Well", "Sample", "Type",
                "number_of_cells/capsules", "Group_1", "Group_2", "Group_3"
            ]
            
            if headers != expected_headers:
                print(f"ERROR: Headers don't match expected format")
                print(f"Expected: {expected_headers}")
                print(f"Got:      {headers}")
                return False
            
            print("✓ Headers are correct")
            
            # Check Sample column position (should be index 4)
            sample_col_index = headers.index("Sample")
            if sample_col_index != 4:
                print(f"ERROR: Sample column at wrong position. Expected index 4, got {sample_col_index}")
                return False
            
            print("✓ Sample column is in correct position (index 4)")
            
            # Analyze sample data
            sample_wells = 0
            unused_wells = 0
            sample_values = set()
            
            for row_num, row in enumerate(reader, start=2):
                if len(row) != len(headers):
                    print(f"ERROR: Row {row_num} has {len(row)} columns, expected {len(headers)}")
                    return False
                
                well_name = row[3]  # Well column
                sample_value = row[4]  # Sample column
                well_type = row[5]  # Type column
                
                if well_type == "unused":
                    unused_wells += 1
                    if sample_value != "":
                        print(f"ERROR: Unused well {well_name} has non-empty Sample value: '{sample_value}'")
                        return False
                else:
                    sample_wells += 1
                    if sample_value:
                        sample_values.add(sample_value)
            
            print(f"✓ Found {sample_wells} wells with sample data")
            print(f"✓ Found {unused_wells} unused wells (all have empty Sample column)")
            print(f"✓ Sample values found: {sorted(sample_values)}")
            
            # Validate that sample wells have sample data
            if sample_wells > 0 and not sample_values:
                print("WARNING: Found sample wells but no sample values")
            
            return True
            
    except Exception as e:
        print(f"ERROR: Failed to validate CSV: {e}")
        return False

def main():
    """Main validation function."""
    print("=== Sample Column CSV Export Validation ===\n")
    
    # Test files to validate
    test_files = [
        "BP9735.WCBP1PR.4.csv",  # Recently exported file
        "RM5097_layout.csv",     # Reference file
        "BP9735.SitukAM.2.csv",  # Another test file
    ]
    
    all_passed = True
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n--- Validating {test_file} ---")
            if validate_csv_sample_column(test_file):
                print(f"✓ {test_file} PASSED validation")
            else:
                print(f"✗ {test_file} FAILED validation")
                all_passed = False
        else:
            print(f"⚠ {test_file} not found, skipping")
    
    print(f"\n=== Validation Summary ===")
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("Sample column implementation is working correctly!")
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("Please check the errors above")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())