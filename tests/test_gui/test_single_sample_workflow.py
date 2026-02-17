"""
Tests for Single Sample Workflow Integration

This module tests the integration between metadata panel and plate canvas
for the single sample workflow in the microwell plate GUI.

Context7 Reference: Event handling and data binding patterns
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.gui.plate_canvas import PlateCanvas
from microwell_plate_gui.data.database import DatabaseManager


class TestSingleSampleWorkflow:
    """Test suite for single sample workflow integration."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Mock database manager
        self.mock_db = Mock(spec=DatabaseManager)
        self.mock_db.get_existing_samples.return_value = ["Sample1", "Sample2"]
        self.mock_db.generate_plate_names.return_value = ["Project1.Sample1.1", "Project1.Sample1.2"]
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_sample_selection_updates_plate_names(self):
        """Test that selecting project and sample updates plate name dropdown."""
        # Create metadata panel
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set project and sample
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        
        # Trigger the update (this happens automatically via trace_add)
        panel._update_plate_names()
        
        # Verify generate_plate_names was called with correct parameters
        self.mock_db.generate_plate_names.assert_called_with("Project1", "Sample1")
        
        # Verify plate name dropdown was updated
        plate_name_values = panel.plate_name_combo['values']
        assert "Project1.Sample1.1" in plate_name_values
        assert "Project1.Sample1.2" in plate_name_values
        
        # Verify first plate name was auto-selected
        assert panel.plate_name_var.get() == "Project1.Sample1.1"
    
    def test_metadata_application_to_wells(self):
        """Test applying metadata to selected wells."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up complete metadata
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.cell_count_var.set("1000")
        panel.group1_var.set("Group1")
        panel.group2_var.set("Group2")
        panel.group3_var.set("Group3")
        
        # Mock well selection callback
        well_metadata_applied = []
        
        def mock_apply_callback(metadata):
            well_metadata_applied.append(metadata)
        
        # Connect callback (this would normally be done by MainWindow)
        panel._apply_metadata = mock_apply_callback
        
        # Apply metadata
        panel._apply_metadata(panel.get_metadata())
        
        # Verify metadata was applied
        assert len(well_metadata_applied) == 1
        applied_metadata = well_metadata_applied[0]
        assert applied_metadata['project'] == "Project1"
        assert applied_metadata['sample'] == "Sample1"
        assert applied_metadata['plate_name'] == "Project1.Sample1.1"
        assert applied_metadata['sample_type'] == "sample"
        assert applied_metadata['cell_count'] == "1000"
        assert applied_metadata['group1'] == "Group1"
        assert applied_metadata['group2'] == "Group2"
        assert applied_metadata['group3'] == "Group3"
    
    def test_workflow_state_management(self):
        """Test workflow state management and validation."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test initial state - form should be enabled
        assert str(panel.project_combo['state']) == 'readonly'
        assert str(panel.sample_combo['state']) == 'readonly'
        assert str(panel.apply_button['state']) == 'normal'
        
        # Test validation with incomplete form
        is_valid, errors = panel.validate_form()
        assert not is_valid
        assert len(errors) > 0
        
        # Test validation with complete form
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.group1_var.set("Group1")
        
        is_valid, errors = panel.validate_form()
        assert is_valid
        assert len(errors) == 0
        
        # Test form clearing
        panel.clear_form()
        assert panel.project_var.get() == ""
        assert panel.sample_var.get() == ""
        assert panel.plate_name_var.get() == ""
    
    def test_dynamic_plate_name_generation(self):
        """Test dynamic plate name generation based on project/sample selection."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test with no selection
        panel._update_plate_names()
        assert panel.plate_name_combo['values'] == () or panel.plate_name_combo['values'] == ""
        assert panel.plate_name_var.get() == ""
        
        # Test with project only
        panel.project_var.set("Project1")
        panel._update_plate_names()
        assert panel.plate_name_combo['values'] == () or panel.plate_name_combo['values'] == ""
        
        # Test with both project and sample
        panel.sample_var.set("Sample1")
        panel._update_plate_names()
        
        self.mock_db.generate_plate_names.assert_called_with("Project1", "Sample1")
        plate_names = panel.plate_name_combo['values']
        assert len(plate_names) > 0
        assert panel.plate_name_var.get() == plate_names[0]  # Auto-select first
    
    def test_form_enable_disable(self):
        """Test enabling and disabling form widgets."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test disabling form
        panel.enable_form(False)
        assert str(panel.project_combo['state']) == 'disabled'
        assert str(panel.sample_combo['state']) == 'disabled'
        assert str(panel.plate_name_combo['state']) == 'disabled'
        assert str(panel.sample_type_combo['state']) == 'disabled'
        assert str(panel.cell_count_entry['state']) == 'disabled'
        assert str(panel.apply_button['state']) == 'disabled'
        
        # Test enabling form
        panel.enable_form(True)
        assert str(panel.project_combo['state']) == 'readonly'
        assert str(panel.sample_combo['state']) == 'readonly'
        assert str(panel.plate_name_combo['state']) == 'readonly'
        assert str(panel.sample_type_combo['state']) == 'readonly'
        assert str(panel.cell_count_entry['state']) == 'normal'
        assert str(panel.apply_button['state']) == 'normal'


class TestMainWindowIntegration:
    """Test suite for MainWindow integration with components."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_main_window_component_integration(self):
        """Test that MainWindow properly integrates all components."""
        # Create main window with existing database
        main_window = MainWindow(self.root, "example_database.db")
        
        # Verify components are created
        assert hasattr(main_window, 'metadata_panel')
        assert isinstance(main_window.metadata_panel, MetadataPanel)
        assert main_window.metadata_panel.db_manager == main_window.db_manager
        
        # Verify database manager is created
        assert hasattr(main_window, 'db_manager')
        assert main_window.db_path == "example_database.db"
        
        # Test plate type selection creates plate canvas
        main_window.on_plate_type_selected("96", "single")
        assert main_window.plate_type == "96"
        assert main_window.sample_mode == "single"
        assert hasattr(main_window, 'plate_canvas')
        assert isinstance(main_window.plate_canvas, PlateCanvas)
    
    def test_well_selection_integration_setup(self):
        """Test that well selection integration is properly set up."""
        # Create main window and select plate type
        main_window = MainWindow(self.root, "example_database.db")
        main_window.on_plate_type_selected("96", "single")
        
        # Verify integration setup method exists
        assert hasattr(main_window, '_setup_well_selection_integration')
        
        # Verify plate canvas is created
        assert main_window.plate_canvas is not None
        assert main_window.plate_canvas.plate_type == "96-well"


class TestWorkflowValidation:
    """Test suite for workflow validation and error handling."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Mock database manager
        self.mock_db = Mock(spec=DatabaseManager)
        self.mock_db.get_existing_projects.return_value = ["Project1"]
        self.mock_db.get_existing_samples.return_value = ["Sample1"]
        self.mock_db.generate_plate_names.return_value = ["Project1.Sample1.1"]
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_required_field_validation(self):
        """Test validation of required fields."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test with all fields empty
        is_valid, errors = panel.validate_form()
        assert not is_valid
        assert "Project is required" in errors
        assert "Sample is required" in errors
        assert "Plate name is required" in errors
        assert "Sample type is required" in errors
        assert "Group Level 1 is required" in errors
        
        # Test with some fields filled
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        # Note: plate name gets auto-populated when project and sample are set
        panel._update_plate_names()  # This should populate plate name
        
        is_valid, errors = panel.validate_form()
        assert not is_valid
        assert "Project is required" not in errors
        assert "Sample is required" not in errors
        # Plate name should be auto-populated, so check for other required fields
        assert "Sample type is required" in errors
        assert "Group Level 1 is required" in errors
    
    def test_cell_count_validation_edge_cases(self):
        """Test cell count validation with edge cases."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test valid cases
        assert panel._validate_cell_count("") == True  # Empty allowed
        assert panel._validate_cell_count("0") == True  # Zero allowed
        assert panel._validate_cell_count("1000") == True  # Positive integer
        assert panel._validate_cell_count("999999") == True  # Large number
        
        # Test invalid cases
        assert panel._validate_cell_count("-1") == False  # Negative
        assert panel._validate_cell_count("abc") == False  # Non-numeric
        assert panel._validate_cell_count("12.5") == False  # Decimal
        assert panel._validate_cell_count("1e3") == False  # Scientific notation
    
    def test_metadata_consistency_validation(self):
        """Test metadata consistency validation."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up valid metadata
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.group1_var.set("Group1")
        
        # Test valid metadata
        is_valid, errors = panel.validate_form()
        assert is_valid
        assert len(errors) == 0
        
        # Test with invalid cell count
        panel.cell_count_var.set("invalid")
        is_valid, errors = panel.validate_form()
        assert not is_valid
        assert "Cell count must be a non-negative integer" in errors