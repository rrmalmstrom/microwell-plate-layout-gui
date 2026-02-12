"""
Tests for Metadata Panel Component

This module tests the metadata entry form with dropdowns, validation,
and database integration for the microwell plate GUI.

Context7 Reference: ttk.Combobox, ttk.Entry, ttk.Label form widgets
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.data.database import DatabaseManager


class TestMetadataPanel:
    """Test suite for MetadataPanel component."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Mock database manager
        self.mock_db = Mock(spec=DatabaseManager)
        self.mock_db.get_existing_projects.return_value = ["Project1", "Project2", "Project3"]
        self.mock_db.get_existing_samples.return_value = ["Sample1", "Sample2", "Sample3"]
        self.mock_db.generate_plate_names.return_value = ["Project1.Sample1.1", "Project1.Sample1.2"]
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_metadata_form_creation(self):
        """Test that metadata form is created with all required fields."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Verify panel is created
        assert panel.parent == self.root
        assert panel.db_manager == self.mock_db
        
        # Verify main frame exists
        assert hasattr(panel, 'main_frame')
        assert isinstance(panel.main_frame, ttk.Frame)
        
        # Verify all required form fields exist
        assert hasattr(panel, 'project_var')
        assert hasattr(panel, 'sample_var')
        assert hasattr(panel, 'plate_name_var')
        assert hasattr(panel, 'sample_type_var')
        assert hasattr(panel, 'cell_count_var')
        assert hasattr(panel, 'group1_var')
        assert hasattr(panel, 'group2_var')
        assert hasattr(panel, 'group3_var')
        
        # Verify StringVar types
        assert isinstance(panel.project_var, tk.StringVar)
        assert isinstance(panel.sample_var, tk.StringVar)
        assert isinstance(panel.plate_name_var, tk.StringVar)
        assert isinstance(panel.sample_type_var, tk.StringVar)
        assert isinstance(panel.cell_count_var, tk.StringVar)
        assert isinstance(panel.group1_var, tk.StringVar)
        assert isinstance(panel.group2_var, tk.StringVar)
        assert isinstance(panel.group3_var, tk.StringVar)
    
    def test_dropdown_population(self):
        """Test that dropdowns are populated from database."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Verify database methods were called
        self.mock_db.get_existing_projects.assert_called_once()
        self.mock_db.get_existing_samples.assert_called_once()
        
        # Verify project dropdown has correct values
        assert hasattr(panel, 'project_combo')
        assert isinstance(panel.project_combo, ttk.Combobox)
        project_values = panel.project_combo['values']
        assert "Project1" in project_values
        assert "Project2" in project_values
        assert "Project3" in project_values
        
        # Verify sample dropdown has correct values
        assert hasattr(panel, 'sample_combo')
        assert isinstance(panel.sample_combo, ttk.Combobox)
        sample_values = panel.sample_combo['values']
        assert "Sample1" in sample_values
        assert "Sample2" in sample_values
        assert "Sample3" in sample_values
        
        # Verify sample type dropdown has predefined values
        assert hasattr(panel, 'sample_type_combo')
        assert isinstance(panel.sample_type_combo, ttk.Combobox)
        sample_type_values = panel.sample_type_combo['values']
        assert "sample" in sample_type_values
        assert "neg_cntrl" in sample_type_values
        assert "pos_cntrl" in sample_type_values
        assert "unused" in sample_type_values
        assert "other" in sample_type_values
    
    def test_dynamic_plate_name_dropdown(self):
        """Test that plate name dropdown updates when project/sample changes."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set project and sample
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        
        # Trigger the update callback
        panel._update_plate_names()
        
        # Verify generate_plate_names was called with correct parameters
        self.mock_db.generate_plate_names.assert_called_with("Project1", "Sample1")
        
        # Verify plate name dropdown was updated
        assert hasattr(panel, 'plate_name_combo')
        plate_name_values = panel.plate_name_combo['values']
        assert "Project1.Sample1.1" in plate_name_values
        assert "Project1.Sample1.2" in plate_name_values
    
    def test_form_validation(self):
        """Test basic form validation functionality."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test empty form validation
        is_valid, errors = panel.validate_form()
        assert not is_valid
        assert len(errors) > 0
        
        # Test with required fields filled
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.cell_count_var.set("1000")
        panel.group1_var.set("Group1")
        
        is_valid, errors = panel.validate_form()
        assert is_valid
        assert len(errors) == 0
    
    def test_cell_count_validation(self):
        """Test that cell count field only accepts integers."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test valid integer
        panel.cell_count_var.set("1000")
        is_valid = panel._validate_cell_count("1000")
        assert is_valid
        
        # Test invalid non-integer
        is_valid = panel._validate_cell_count("abc")
        assert not is_valid
        
        # Test negative number
        is_valid = panel._validate_cell_count("-100")
        assert not is_valid
        
        # Test zero
        is_valid = panel._validate_cell_count("0")
        assert is_valid
    
    def test_form_layout_grid(self):
        """Test that form uses grid layout properly."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Verify main frame is gridded
        grid_info = panel.main_frame.grid_info()
        assert grid_info  # Should have grid information
        
        # Verify labels and widgets are properly arranged
        # This tests the Context7 grid layout implementation
        assert hasattr(panel, 'project_label')
        assert hasattr(panel, 'sample_label')
        assert hasattr(panel, 'plate_name_label')
        assert hasattr(panel, 'sample_type_label')
        assert hasattr(panel, 'cell_count_label')
        assert hasattr(panel, 'group1_label')
        assert hasattr(panel, 'group2_label')
        assert hasattr(panel, 'group3_label')
        
        # Verify all labels are ttk.Label instances
        assert isinstance(panel.project_label, ttk.Label)
        assert isinstance(panel.sample_label, ttk.Label)
        assert isinstance(panel.plate_name_label, ttk.Label)
        assert isinstance(panel.sample_type_label, ttk.Label)
        assert isinstance(panel.cell_count_label, ttk.Label)
        assert isinstance(panel.group1_label, ttk.Label)
        assert isinstance(panel.group2_label, ttk.Label)
        assert isinstance(panel.group3_label, ttk.Label)
    
    def test_get_metadata_values(self):
        """Test retrieving all metadata values as dictionary."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set all values
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.cell_count_var.set("1000")
        panel.group1_var.set("Group1")
        panel.group2_var.set("Group2")
        panel.group3_var.set("Group3")
        
        metadata = panel.get_metadata()
        
        assert metadata['project'] == "Project1"
        assert metadata['sample'] == "Sample1"
        assert metadata['plate_name'] == "Project1.Sample1.1"
        assert metadata['sample_type'] == "sample"
        assert metadata['cell_count'] == "1000"
        assert metadata['group1'] == "Group1"
        assert metadata['group2'] == "Group2"
        assert metadata['group3'] == "Group3"
    
    def test_clear_form(self):
        """Test clearing all form fields."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set all values
        panel.project_var.set("Project1")
        panel.sample_var.set("Sample1")
        panel.plate_name_var.set("Project1.Sample1.1")
        panel.sample_type_var.set("sample")
        panel.cell_count_var.set("1000")
        panel.group1_var.set("Group1")
        panel.group2_var.set("Group2")
        panel.group3_var.set("Group3")
        
        # Clear form
        panel.clear_form()
        
        # Verify all fields are empty
        assert panel.project_var.get() == ""
        assert panel.sample_var.get() == ""
        assert panel.plate_name_var.get() == ""
        assert panel.sample_type_var.get() == ""
        assert panel.cell_count_var.get() == ""
        assert panel.group1_var.get() == ""
        assert panel.group2_var.get() == ""
        assert panel.group3_var.get() == ""


class TestMetadataPanelIntegration:
    """Integration tests for MetadataPanel with real database."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Use real database manager with test database
        self.db_path = "example_database.db"
        if os.path.exists(self.db_path):
            self.db_manager = DatabaseManager(self.db_path)
        else:
            # Skip integration tests if database doesn't exist
            pytest.skip("Test database not available")
    
    def teardown_method(self):
        """Cleanup after each test."""
        if hasattr(self, 'db_manager'):
            self.db_manager.close()
        if self.root:
            self.root.destroy()
    
    def test_real_database_integration(self):
        """Test metadata panel with real database."""
        if not hasattr(self, 'db_manager'):
            pytest.skip("Database not available")
            
        panel = MetadataPanel(self.root, self.db_manager)
        
        # Verify dropdowns are populated with real data
        project_values = panel.project_combo['values']
        sample_values = panel.sample_combo['values']
        
        # Should have some values from real database
        assert len(project_values) > 0
        assert len(sample_values) > 0
        
        # Test dynamic plate name generation with real data
        if len(project_values) > 0 and len(sample_values) > 0:
            panel.project_var.set(project_values[0])
            panel.sample_var.set(sample_values[0])
            panel._update_plate_names()
            
            plate_name_values = panel.plate_name_combo['values']
            assert len(plate_name_values) > 0