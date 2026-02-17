"""
CSV Export Utility for Microwell Plate GUI

This module provides functionality to export plate layout data to CSV format
matching the exact structure of reference layout files. Supports both 96-well
and 384-well plate formats with dynamic well ordering and proper field mapping.

Key Features:
- Dynamic plate format support (96-well: A-H, 1-12; 384-well: A-P, 1-24)
- Proper well ordering (row-major: A1, A2, ..., A12, B1, B2, ...)
- Field mapping from metadata to CSV columns
- Plate name-based filename generation
- Data validation and error handling
- Integration with existing PlateCanvas data structures
"""

import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class CSVExportError(Exception):
    """Custom exception for CSV export operations."""
    pass


class PlateCSVExporter:
    """
    Handles CSV export for microwell plate layouts.
    
    Supports both 96-well and 384-well formats with proper field mapping
    and well ordering to match reference CSV structure.
    """
    
    # CSV column headers matching reference format
    CSV_HEADERS = [
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
    
    # Plate format configurations
    PLATE_FORMATS = {
        "96": {
            "rows": 8,
            "cols": 12,
            "row_labels": "ABCDEFGH",
            "max_col": 12
        },
        "384": {
            "rows": 16,
            "cols": 24,
            "row_labels": "ABCDEFGHIJKLMNOP",
            "max_col": 24
        }
    }
    
    def __init__(self):
        """Initialize the CSV exporter."""
        pass
    
    def export_plate_to_csv(self, plate_canvas, main_window, filename: Optional[str] = None) -> str:
        """
        Export plate data to CSV format matching reference layout structure.
        
        Args:
            plate_canvas: PlateCanvas instance with well_metadata
            main_window: MainWindow instance with plate configuration
            filename: Optional target CSV file path. If None, auto-generated from plate name
            
        Returns:
            str: Path to the exported CSV file
            
        Raises:
            CSVExportError: If export fails due to validation or I/O errors
        """
        try:
            # Validate inputs
            self._validate_export_inputs(plate_canvas, main_window)
            
            # Get plate configuration
            plate_type = main_window.plate_type
            plate_config = self.PLATE_FORMATS[plate_type]
            
            # Get plate name for CSV data and filename
            plate_name = self._get_plate_name(main_window)
            
            # Generate filename if not provided
            if filename is None:
                filename = self._generate_filename(plate_name)
            
            # Generate CSV data
            csv_data = self._generate_csv_data(
                plate_canvas, 
                main_window, 
                plate_config, 
                plate_name
            )
            
            # Write CSV file
            self._write_csv_file(filename, csv_data)
            
            logger.info(f"Successfully exported plate layout to: {filename}")
            return filename
            
        except Exception as e:
            error_msg = f"Failed to export CSV: {str(e)}"
            logger.error(error_msg)
            raise CSVExportError(error_msg) from e
    
    def _validate_export_inputs(self, plate_canvas, main_window) -> None:
        """
        Validate inputs for CSV export.
        
        Args:
            plate_canvas: PlateCanvas instance
            main_window: MainWindow instance
            
        Raises:
            CSVExportError: If validation fails
        """
        if not hasattr(plate_canvas, 'well_metadata'):
            raise CSVExportError("PlateCanvas missing well_metadata attribute")
        
        if not hasattr(main_window, 'plate_type'):
            raise CSVExportError("MainWindow missing plate_type attribute")
        
        if main_window.plate_type not in self.PLATE_FORMATS:
            raise CSVExportError(f"Unsupported plate type: {main_window.plate_type}")
        
        # Check if plate has any metadata (prevent export of empty plates)
        if not plate_canvas.well_metadata:
            raise CSVExportError("No metadata found on plate. Cannot export empty plate.")
        
        logger.info(f"Validation passed: {len(plate_canvas.well_metadata)} wells with metadata")
    
    def _get_plate_name(self, main_window) -> str:
        """
        Extract plate name from main window configuration.
        
        Args:
            main_window: MainWindow instance
            
        Returns:
            str: Plate name for CSV data and filename
        """
        # Single sample mode: use configured plate name
        if (main_window.sample_mode == "single" and 
            main_window.single_sample_config and 
            'plate_name' in main_window.single_sample_config):
            return main_window.single_sample_config['plate_name']
        
        # Multi-sample mode: use sample plate name
        if (main_window.sample_mode == "multi" and 
            main_window.multi_sample_config and 
            'sample_plate_name' in main_window.multi_sample_config):
            return main_window.multi_sample_config['sample_plate_name']
        
        # Fallback: generate default name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"plate_{main_window.plate_type}well_{timestamp}"
    
    def _generate_filename(self, plate_name: str) -> str:
        """
        Generate CSV filename based on plate name.
        
        Args:
            plate_name: Name of the plate
            
        Returns:
            str: Generated filename with .csv extension
        """
        # Sanitize plate name for filename
        safe_name = re.sub(r'[^\w\-_.]', '_', plate_name)
        
        # Ensure .csv extension
        if not safe_name.lower().endswith('.csv'):
            safe_name += '.csv'
        
        return safe_name
    
    def _generate_csv_data(self, plate_canvas, main_window, plate_config: Dict, plate_name: str) -> List[List[str]]:
        """
        Generate CSV data rows for the plate layout.
        
        Args:
            plate_canvas: PlateCanvas instance with well_metadata
            main_window: MainWindow instance
            plate_config: Plate format configuration
            plate_name: Name of the plate for Plate_ID column
            
        Returns:
            List[List[str]]: CSV data rows including headers
        """
        csv_rows = [self.CSV_HEADERS]  # Start with headers
        
        # Generate wells in proper order (row-major: A1, A2, A3, ..., A12, B1, B2, ...)
        for row_idx in range(plate_config["rows"]):
            for col_num in range(1, plate_config["cols"] + 1):
                row_letter = plate_config["row_labels"][row_idx]
                well_name = f"{row_letter}{col_num}"
                
                # Get metadata for this well
                metadata = plate_canvas.well_metadata.get(well_name, {})
                
                # Generate CSV row for this well
                csv_row = self._generate_well_csv_row(
                    well_name,
                    row_letter,
                    col_num,
                    metadata,
                    plate_name,
                    main_window
                )
                csv_rows.append(csv_row)
        
        logger.info(f"Generated {len(csv_rows)-1} data rows for {plate_config['rows']}x{plate_config['cols']} plate")
        return csv_rows
    
    def _generate_well_csv_row(self, well_name: str, row_letter: str, col_num: int,
                              metadata: Dict[str, Any], plate_name: str, main_window) -> List[str]:
        """
        Generate a single CSV row for a well.
        
        Args:
            well_name: Well identifier (e.g., 'A1')
            row_letter: Row letter (e.g., 'A')
            col_num: Column number (e.g., 1)
            metadata: Well metadata dictionary
            plate_name: Plate name for Plate_ID column
            main_window: MainWindow instance for sample configuration
            
        Returns:
            List[str]: CSV row data
        """
        # Determine sample name based on mode and configuration
        sample_name = self._get_sample_name_for_well(metadata, main_window)
        
        # Map metadata fields to CSV columns with defaults for unused wells
        if not metadata:
            # Empty well - mark as unused
            return [
                plate_name,           # Plate_ID
                row_letter,           # Well_Row
                str(col_num),         # Well_Col
                well_name,            # Well
                "",                   # Sample (empty for unused wells)
                "unused",             # Type
                "",                   # number_of_cells/capsules
                "",                   # Group_1
                "",                   # Group_2
                ""                    # Group_3
            ]
        
        # Well with metadata
        sample_type = metadata.get('sample_type', 'unused')
        cell_count = metadata.get('cell_count', '')
        group1 = metadata.get('group1', '')
        group2 = metadata.get('group2', '')
        group3 = metadata.get('group3', '')
        
        # Handle unused wells - clear group fields if type is unused
        if sample_type == 'unused':
            group1 = group2 = group3 = ''
            cell_count = ''
            sample_name = ""  # No sample name for unused wells
        
        return [
            plate_name,           # Plate_ID
            row_letter,           # Well_Row
            str(col_num),         # Well_Col
            well_name,            # Well
            sample_name,          # Sample
            sample_type,          # Type
            cell_count,           # number_of_cells/capsules
            group1,               # Group_1
            group2,               # Group_2
            group3                # Group_3
        ]
    
    def _get_sample_name_for_well(self, metadata: Dict[str, Any], main_window) -> str:
        """
        Get the sample name for a well based on the sample mode and configuration.
        
        Args:
            metadata: Well metadata dictionary
            main_window: MainWindow instance with sample configuration
            
        Returns:
            str: Sample name for the well
        """
        # If well is unused, return empty string
        if not metadata or metadata.get('sample_type') == 'unused':
            return ""
        
        # Single sample mode: use pre-configured sample name
        if (main_window.sample_mode == "single" and
            main_window.single_sample_config and
            'sample' in main_window.single_sample_config):
            return main_window.single_sample_config['sample']
        
        # Multi-sample mode: use sample from well metadata
        if main_window.sample_mode == "multi":
            # In multi-sample mode, the sample name should be stored in the metadata
            # This comes from the user's selection during the metadata entry process
            return metadata.get('sample', '')
        
        # Fallback: return empty string
        return ""
    
    def _write_csv_file(self, filename: str, csv_data: List[List[str]]) -> None:
        """
        Write CSV data to file.
        
        Args:
            filename: Target file path
            csv_data: CSV data rows including headers
            
        Raises:
            CSVExportError: If file writing fails
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
            
            # Write CSV file with proper encoding and formatting
            # Use standard UTF-8 without BOM for better compatibility with data processing tools
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csv_data)
            
            logger.info(f"CSV file written successfully: {filename}")
            
        except PermissionError as e:
            raise CSVExportError(f"Permission denied writing to {filename}: {str(e)}")
        except OSError as e:
            raise CSVExportError(f"File system error writing to {filename}: {str(e)}")
        except Exception as e:
            raise CSVExportError(f"Unexpected error writing CSV file: {str(e)}")
    
    def validate_csv_format(self, filename: str) -> Tuple[bool, List[str]]:
        """
        Validate that exported CSV matches expected format.
        
        Args:
            filename: Path to CSV file to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        errors = []
        
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                # Check headers
                headers = next(reader, None)
                if headers != self.CSV_HEADERS:
                    errors.append(f"Invalid headers. Expected: {self.CSV_HEADERS}, Got: {headers}")
                
                # Check data rows
                row_count = 0
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    row_count += 1
                    
                    # Check column count
                    if len(row) != len(self.CSV_HEADERS):
                        errors.append(f"Row {row_num}: Expected {len(self.CSV_HEADERS)} columns, got {len(row)}")
                    
                    # Basic data validation
                    if len(row) >= 4:
                        well_name = row[3]
                        if not re.match(r'^[A-P]\d{1,2}$', well_name):
                            errors.append(f"Row {row_num}: Invalid well name format: {well_name}")
                
                logger.info(f"Validated CSV: {row_count} data rows")
                
        except FileNotFoundError:
            errors.append(f"CSV file not found: {filename}")
        except Exception as e:
            errors.append(f"Error validating CSV: {str(e)}")
        
        return len(errors) == 0, errors


# Convenience function for direct export
def export_plate_layout(plate_canvas, main_window, filename: Optional[str] = None) -> str:
    """
    Convenience function to export plate layout to CSV.
    
    Args:
        plate_canvas: PlateCanvas instance with well_metadata
        main_window: MainWindow instance with plate configuration
        filename: Optional target CSV file path
        
    Returns:
        str: Path to exported CSV file
        
    Raises:
        CSVExportError: If export fails
    """
    exporter = PlateCSVExporter()
    return exporter.export_plate_to_csv(plate_canvas, main_window, filename)