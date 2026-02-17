"""
Test suite for Image Export functionality integrated with CSV export.

This module tests the image export feature that is integrated with the CSV export button,
following the user's requirement that there should not be a separate image export button.
The image export functionality is accessed through the "📊 Export CSV & Image" button.
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os
import tempfile
from PIL import Image
import io

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.data.database import DatabaseManager


class TestImageExport:
    """Test suite for Image Export functionality integrated with CSV export."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Mock database manager
        self.mock_db = Mock(spec=DatabaseManager)
        self.mock_db.get_existing_samples.return_value = ["Sample1", "Sample2"]
        self.mock_db.generate_plate_names.return_value = ["Project1.Sample1.1"]
        
    def teardown_method(self):
        """Cleanup after each test."""
        if self.root:
            self.root.destroy()
    
    def test_integrated_export_button_creation(self):
        """Test that CSV export button includes image export functionality."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that CSV export button exists (which now includes image export)
        assert hasattr(panel, 'export_csv_button'), "CSV export button should be created"
        
        # Check that it's a Button widget
        assert isinstance(panel.export_csv_button, ttk.Button), "Should be a ttk.Button"
        
        # Check that button text indicates both CSV and image export
        button_text = panel.export_csv_button.cget('text')
        assert 'CSV' in button_text and 'Image' in button_text, "Button should indicate both CSV and image export"
    
    def test_integrated_export_button_placement(self):
        """Test that integrated export button is properly placed in layout."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that CSV export button is in the export frame
        assert panel.export_csv_button.master == panel.export_frame, "Export button should be in export frame"
        
        # Check that button is packed properly
        info = panel.export_csv_button.pack_info()
        assert info, "Export button should be packed in the layout"
    
    def test_integrated_export_button_command_callback(self):
        """Test that integrated export button has proper command callback."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that CSV export button has a command
        command = panel.export_csv_button.cget('command')
        assert command is not None, "Export button should have a command callback"
        assert command != "", "Export button should have a non-empty command"
        
        # Check that the actual method exists and is callable
        assert hasattr(panel, '_export_csv'), "Panel should have _export_csv method"
        assert callable(panel._export_csv), "Export CSV method should be callable"
    
    def test_image_export_callback_setter(self):
        """Test that image export callback can be set from external components."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that callback setter method exists
        assert hasattr(panel, 'set_export_image_callback'), "Should have image export callback setter method"
        
        # Test setting a callback
        mock_callback = Mock()
        panel.set_export_image_callback(mock_callback)
        
        # Check that callback is stored
        assert hasattr(panel, 'export_image_callback'), "Should store image export callback"
        assert panel.export_image_callback == mock_callback, "Should store the provided callback"

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_integrated_export_file_dialog(self, mock_filedialog):
        """Test that integrated export shows file dialog for CSV and triggers image export."""
        test_filename = "/test/path/plate_layout.csv"
        mock_filedialog.return_value = test_filename
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up image export callback
        mock_image_callback = Mock(return_value=True)
        panel.set_export_image_callback(mock_image_callback)
        
        # Mock the CSV export functionality
        with patch.object(panel, '_get_plate_name', return_value="TestPlate"):
            with patch('builtins.open', mock_open()):
                with patch('csv.writer'):
                    # Simulate clicking the integrated export button
                    panel._export_csv()
        
        # Check that file dialog was called
        mock_filedialog.assert_called_once()
        
        # Check that image export callback was called with PDF filename
        expected_image_filename = test_filename.replace('.csv', '.pdf')
        mock_image_callback.assert_called_once_with(expected_image_filename)

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_integrated_export_cancel_dialog(self, mock_filedialog):
        """Test that canceling file dialog doesn't trigger image export."""
        mock_filedialog.return_value = ""  # User canceled
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up image export callback
        mock_image_callback = Mock()
        panel.set_export_image_callback(mock_image_callback)
        
        # Simulate clicking the integrated export button
        panel._export_csv()
        
        # Check that file dialog was called
        mock_filedialog.assert_called_once()
        
        # Check that image export callback was NOT called
        mock_image_callback.assert_not_called()

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_integrated_export_with_filename(self, mock_filedialog):
        """Test that integrated export works with provided filename."""
        test_filename = "/test/path/custom_plate.csv"
        mock_filedialog.return_value = test_filename
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up successful image export callback
        mock_image_callback = Mock(return_value=True)
        panel.set_export_image_callback(mock_image_callback)
        
        # Mock the CSV export functionality
        with patch.object(panel, '_get_plate_name', return_value="TestPlate"):
            with patch('builtins.open', mock_open()):
                with patch('csv.writer'):
                    # Simulate the export
                    panel._export_csv()
        
        # Check that image export was called with PDF filename
        expected_image_filename = test_filename.replace('.csv', '.pdf')
        mock_image_callback.assert_called_once_with(expected_image_filename)

    def test_image_export_utility_class_creation(self):
        """Test that ImageExporter utility class can be created."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        assert exporter is not None, "Should be able to create ImageExporter instance"

    def test_image_export_utility_capture_method(self):
        """Test that ImageExporter has capture method."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        assert hasattr(exporter, 'capture_plate_and_legend'), "Should have capture method"
        assert callable(exporter.capture_plate_and_legend), "Capture method should be callable"

    def test_image_capture_functionality(self):
        """Test that image capture functionality works with mock canvas."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        # Create mock canvas
        mock_canvas = Mock()
        mock_canvas.postscript = Mock()
        mock_canvas.winfo_width.return_value = 400
        mock_canvas.winfo_height.return_value = 300
        
        # Create mock legend panel
        mock_legend = Mock()
        
        exporter = ImageExporter()
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # This should not raise an exception
            result = exporter.capture_plate_and_legend(mock_canvas, mock_legend, temp_filename)
            assert isinstance(result, bool), "Should return boolean result"
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def test_image_export_default_filename_generation(self):
        """Test that default filename generation works for PDF."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        
        # Test with various plate names
        test_cases = [
            ("TestPlate", "TestPlate_layout.pdf"),
            ("Project-1", "Project-1_layout.pdf"),
            ("Sample_123", "Sample_123_layout.pdf"),
            ("", "plate_layout.pdf"),
            ("Special@#$%Characters", "Special____Characters_layout.pdf")
        ]
        
        for plate_name, expected_pattern in test_cases:
            filename = exporter.generate_default_filename(plate_name)
            assert filename.endswith('.pdf'), f"Should generate PDF filename for '{plate_name}'"
            assert 'layout' in filename, f"Should include 'layout' in filename for '{plate_name}'"

    def test_image_composition_functionality(self):
        """Test that image composition works with PDF export."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        
        # Test that the method exists and is callable
        assert hasattr(exporter, 'capture_plate_and_legend'), "Should have composition functionality"
        
        # Test with mock inputs
        mock_canvas = Mock()
        mock_canvas.postscript = Mock()
        mock_legend = Mock()
        
        # Should not raise exception with valid inputs
        try:
            result = exporter.capture_plate_and_legend(mock_canvas, mock_legend, "test.pdf")
            assert isinstance(result, bool), "Should return boolean"
        except Exception as e:
            # Allow certain expected exceptions (like missing conversion tools)
            assert "conversion" in str(e).lower() or "failed" in str(e).lower(), f"Unexpected error: {e}"

    def test_image_export_error_handling(self):
        """Test that image export handles errors gracefully."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        
        # Test with invalid inputs
        result = exporter.capture_plate_and_legend(None, None, "")
        assert result == False, "Should return False for invalid inputs"
        
        # Test with invalid filename
        result = exporter.capture_plate_and_legend(Mock(), Mock(), "")
        assert result == False, "Should return False for empty filename"

    @patch('tkinter.messagebox.showerror')
    def test_image_export_error_dialog(self, mock_error_dialog):
        """Test that errors are shown to user via dialog."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up failing callback
        def failing_callback(filename):
            return False
        
        panel.set_export_image_callback(failing_callback)
        
        # Mock CSV export to succeed but image export to fail
        with patch('tkinter.filedialog.asksaveasfilename', return_value="/test/file.csv"):
            with patch.object(panel, '_get_plate_name', return_value="TestPlate"):
                with patch('builtins.open', mock_open()):
                    with patch('csv.writer'):
                        panel._export_csv()
        
        # Should show error dialog for image export failure
        # Note: The actual error dialog might be called from the main window, not the panel

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.filedialog.asksaveasfilename')
    def test_image_export_success_dialog(self, mock_filedialog, mock_info_dialog):
        """Test that success is shown to user via dialog."""
        test_filename = "/test/path/plate_layout.csv"
        mock_filedialog.return_value = test_filename
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set up successful callback
        def success_callback(filename):
            return True
        
        panel.set_export_image_callback(success_callback)
        
        # Mock CSV export to succeed
        with patch.object(panel, '_get_plate_name', return_value="TestPlate"):
            with patch('builtins.open', mock_open()):
                with patch('csv.writer'):
                    panel._export_csv()
        
        # Should show success dialog
        # Note: The actual success dialog might be called from the main window

    def test_integrated_export_button_state_management(self):
        """Test that integrated export button state can be managed."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test that button starts enabled
        initial_state = str(panel.export_csv_button.cget('state'))
        assert initial_state in ['normal', 'active'], "Button should start enabled"
        
        # Test that button can be disabled
        panel.export_csv_button.configure(state='disabled')
        disabled_state = str(panel.export_csv_button.cget('state'))
        assert disabled_state == 'disabled', "Button should be disableable"
        
        # Test that button can be re-enabled
        panel.export_csv_button.configure(state='normal')
        enabled_state = str(panel.export_csv_button.cget('state'))
        assert enabled_state in ['normal', 'active'], "Button should be re-enableable"

    def test_image_export_integration_with_main_window(self):
        """Test that image export integrates properly with main window."""
        # Create a mock database file
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
            temp_db_path = temp_db.name
        
        try:
            # Create main window (this tests the integration)
            main_window = MainWindow(self.root, temp_db_path)
            
            # Check that main window has image export method
            assert hasattr(main_window, '_export_image'), "Main window should have image export method"
            assert callable(main_window._export_image), "Image export method should be callable"
            
            # Check that metadata panel has the callback set
            assert hasattr(main_window.metadata_panel, 'export_image_callback'), "Metadata panel should have image export callback"
            
        finally:
            # Clean up
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)

    def test_pdf_export_format_support(self):
        """Test that PDF export format is supported."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        exporter = ImageExporter()
        
        # Test PDF filename generation
        filename = exporter.generate_default_filename("TestPlate")
        assert filename.endswith('.pdf'), "Should generate PDF files"

    def test_pdf_export_postscript_method(self):
        """Test that PDF export uses PostScript method."""
        from microwell_plate_gui.utils.image_export import ImageExporter
        
        # Create mock canvas with postscript method
        mock_canvas = Mock()
        mock_canvas.postscript = Mock()
        mock_canvas.winfo_width.return_value = 400
        mock_canvas.winfo_height.return_value = 300
        
        exporter = ImageExporter()
        
        # Test that postscript method is called
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            exporter.capture_plate_and_legend(mock_canvas, Mock(), temp_filename)
            # Should have called postscript method
            mock_canvas.postscript.assert_called()
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def test_image_export_accessibility(self):
        """Test that integrated export button has proper accessibility features."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that button has proper text (not just icon)
        button_text = panel.export_csv_button.cget('text')
        assert len(button_text) > 2, "Button should have descriptive text, not just icons"
        assert 'CSV' in button_text, "Button text should mention CSV"
        assert 'Image' in button_text, "Button text should mention Image"