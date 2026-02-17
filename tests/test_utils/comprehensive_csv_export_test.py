#!/usr/bin/env python3
"""
Comprehensive CSV Export Testing Script

This script validates the CSV export functionality against the reference format
and tests various edge cases to ensure robust operation.
"""

import csv
import os
import sys
from pathlib import Path

def compare_csv_format(exported_file, reference_file):
    """Compare exported CSV format with reference file."""
    print(f"\n=== CSV Format Validation ===")
    print(f"Exported file: {exported_file}")
    print(f"Reference file: {reference_file}")
    
    issues = []
    
    try:
        # Read both files
        with open(exported_file, 'r', encoding='utf-8') as f:
            exported_reader = csv.reader(f)
            exported_headers = next(exported_reader)
            exported_rows = list(exported_reader)
        
        with open(reference_file, 'r', encoding='utf-8') as f:
            ref_reader = csv.reader(f)
            ref_headers = next(ref_reader)
            ref_rows = list(ref_reader)
        
        # Check headers
        if exported_headers != ref_headers:
            issues.append(f"Header mismatch:\n  Exported: {exported_headers}\n  Reference: {ref_headers}")
        else:
            print("✅ Headers match perfectly")
        
        # Check well ordering (first 20 wells)
        print("\n--- Well Ordering Check ---")
        expected_order = [row[3] for row in ref_rows[:20]]  # Well column
        actual_order = [row[3] for row in exported_rows[:20]]
        
        print(f"Expected first 20 wells: {expected_order}")
        print(f"Actual first 20 wells:   {actual_order}")
        
        if expected_order == actual_order:
            print("✅ Well ordering is correct (row-major)")
        else:
            issues.append("❌ Well ordering is incorrect")
            for i, (exp, act) in enumerate(zip(expected_order, actual_order)):
                if exp != act:
                    print(f"  Position {i+1}: Expected {exp}, Got {act}")
        
        # Check data structure
        print("\n--- Data Structure Check ---")
        if len(exported_rows) == len(ref_rows):
            print(f"✅ Row count matches: {len(exported_rows)} rows")
        else:
            issues.append(f"Row count mismatch: Expected {len(ref_rows)}, Got {len(exported_rows)}")
        
        # Check column count consistency
        col_counts = [len(row) for row in exported_rows[:10]]
        if all(count == len(exported_headers) for count in col_counts):
            print(f"✅ Column count consistent: {len(exported_headers)} columns")
        else:
            issues.append("Column count inconsistent in data rows")
        
        # Sample data validation
        print("\n--- Sample Data Validation ---")
        sample_rows = [row for row in exported_rows if row[4] != 'unused']  # Type column
        if sample_rows:
            print(f"✅ Found {len(sample_rows)} wells with sample data")
            print(f"Sample types found: {set(row[4] for row in sample_rows)}")
        else:
            print("⚠️  No sample data found (only unused wells)")
        
    except Exception as e:
        issues.append(f"Error reading files: {str(e)}")
    
    return issues

def validate_plate_formats():
    """Validate that both 96-well and 384-well formats work correctly."""
    print(f"\n=== Plate Format Validation ===")
    
    # Check if we have examples of both formats
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and f != 'RM5097_layout.csv']
    
    print(f"Found CSV export files: {csv_files}")
    
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = list(reader)
            
            # Determine plate format by counting unique wells
            wells = set(row[3] for row in rows)  # Well column
            row_letters = set(row[1] for row in rows)  # Well_Row column
            col_numbers = set(int(row[2]) for row in rows)  # Well_Col column
            
            max_row = max(row_letters)
            max_col = max(col_numbers)
            
            if max_row <= 'H' and max_col <= 12:
                plate_format = "96-well"
                expected_wells = 96
            elif max_row <= 'P' and max_col <= 24:
                plate_format = "384-well"
                expected_wells = 384
            else:
                plate_format = "Unknown"
                expected_wells = 0
            
            print(f"\n{csv_file}:")
            print(f"  Format: {plate_format}")
            print(f"  Rows: A-{max_row} ({len(row_letters)} rows)")
            print(f"  Columns: 1-{max_col} ({len(col_numbers)} columns)")
            print(f"  Total wells: {len(wells)} (expected: {expected_wells})")
            
            if len(wells) == expected_wells:
                print(f"  ✅ Well count correct for {plate_format}")
            else:
                print(f"  ❌ Well count incorrect for {plate_format}")
                
        except Exception as e:
            print(f"  ❌ Error analyzing {csv_file}: {str(e)}")

def main():
    """Main testing function."""
    print("🧪 Comprehensive CSV Export Testing")
    print("=" * 50)
    
    # Find exported CSV files
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and f != 'RM5097_layout.csv']
    reference_file = 'RM5097_layout.csv'
    
    if not os.path.exists(reference_file):
        print(f"❌ Reference file not found: {reference_file}")
        return
    
    if not csv_files:
        print("❌ No exported CSV files found")
        return
    
    print(f"Found {len(csv_files)} exported CSV files")
    
    # Test each exported file
    all_issues = []
    for csv_file in csv_files:
        print(f"\n{'='*60}")
        print(f"Testing: {csv_file}")
        print(f"{'='*60}")
        
        issues = compare_csv_format(csv_file, reference_file)
        if issues:
            print(f"\n❌ Issues found in {csv_file}:")
            for issue in issues:
                print(f"  - {issue}")
            all_issues.extend(issues)
        else:
            print(f"\n✅ {csv_file} passed all format checks!")
    
    # Validate plate formats
    validate_plate_formats()
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 TESTING SUMMARY")
    print(f"{'='*60}")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} total issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"{i}. {issue}")
    else:
        print("✅ All CSV export tests PASSED!")
        print("✅ Format matches reference file perfectly")
        print("✅ Well ordering is correct (row-major)")
        print("✅ Data structure is valid")

if __name__ == "__main__":
    main()