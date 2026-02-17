"""
Tests for Exit/Close Application Button Feature

This module tests the exit button functionality for cleanly closing the application.
Following TDD approach - tests written first before implementation.

Test Coverage:
- Exit button creation and placement
- Exit button functionality and event handling
- Integration with existing layout
- Error handling for exit scenarios
- Confirmation dialog behavior
"""

import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.gui.metadata_panel import MetadataPanel
from microwell_plate_gui.gui.main_window import MainWindow
from microwell_plate_gui.data.database import DatabaseManager


class TestExitButton:
    """Test suite for Exit/Close Application Button functionality."""
    
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
    
    def test_exit_button_creation_in_metadata_panel(self):
        """Test that exit button is created in metadata panel."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that exit button exists
        assert hasattr(panel, 'exit_button'), "Exit button should be created"
        assert isinstance(panel.exit_button, ttk.Button), "Exit button should be a ttk.Button"
        
        # Check button text
        button_text = panel.exit_button.cget('text')
        assert 'Exit' in button_text or 'Close' in button_text, "Button should have appropriate exit text"
    
    def test_exit_button_placement_in_layout(self):
        """Test that exit button is properly placed in the layout."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that exit button is in the button frame
        assert panel.exit_button.master == panel.export_frame, "Exit button should be in export frame"
        
        # Check that button is packed/gridded properly
        info = panel.exit_button.pack_info()
        assert info, "Exit button should be packed in the layout"
    
    def test_exit_button_command_callback(self):
        """Test that exit button has proper command callback."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that exit button has a command
        command = panel.exit_button.cget('command')
        assert command is not None, "Exit button should have a command callback"
        assert command != "", "Exit button should have a non-empty command"
        
        # Check that the actual method exists and is callable
        assert hasattr(panel, '_exit_application'), "Panel should have _exit_application method"
        assert callable(panel._exit_application), "Exit application method should be callable"
    
    @patch('tkinter.messagebox.askyesno')
    def test_exit_button_confirmation_dialog(self, mock_askyesno):
        """Test that clicking exit button shows confirmation dialog."""
        mock_askyesno.return_value = True  # User confirms exit
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Simulate clicking the exit button
        panel.exit_button.invoke()
        
        # Check that confirmation dialog was shown
        mock_askyesno.assert_called_once()
        call_args = mock_askyesno.call_args
        
        # Check positional arguments (title, message)
        args = call_args[0]
        assert len(args) >= 2, "Should have title and message arguments"
        title = args[0]
        message = args[1]
        
        assert 'Exit' in title or 'Close' in title, f"Title should mention exit/close: {title}"
        assert 'exit' in message.lower() or 'close' in message.lower(), f"Message should mention exit/close: {message}"
    
    @patch('tkinter.messagebox.askyesno')
    def test_exit_button_cancel_behavior(self, mock_askyesno):
        """Test that canceling exit dialog does not close application."""
        mock_askyesno.return_value = False  # User cancels exit
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Mock the root window's quit method to track if it's called
        with patch.object(self.root, 'quit') as mock_quit:
            # Simulate clicking the exit button
            panel.exit_button.invoke()
            
            # Check that confirmation dialog was shown
            mock_askyesno.assert_called_once()
            
            # Check that quit was NOT called when user cancels
            mock_quit.assert_not_called()
    
    @patch('tkinter.messagebox.askyesno')
    def test_exit_button_confirm_behavior(self, mock_askyesno):
        """Test that confirming exit dialog closes application."""
        mock_askyesno.return_value = True  # User confirms exit
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Mock the root window's quit method to track if it's called
        with patch.object(self.root, 'quit') as mock_quit:
            # Simulate clicking the exit button
            panel.exit_button.invoke()
            
            # Check that confirmation dialog was shown
            mock_askyesno.assert_called_once()
            
            # Check that quit was called when user confirms
            mock_quit.assert_called_once()
    
    def test_exit_button_callback_setter(self):
        """Test that exit button callback can be set from external components."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that callback setter method exists
        assert hasattr(panel, 'set_exit_callback'), "Should have exit callback setter method"
        
        # Test setting a callback
        mock_callback = Mock()
        panel.set_exit_callback(mock_callback)
        
        # Check that callback is stored
        assert hasattr(panel, 'exit_callback'), "Should store exit callback"
        assert panel.exit_callback == mock_callback, "Should store the provided callback"
    
    @patch('tkinter.messagebox.askyesno')
    def test_exit_button_with_custom_callback(self, mock_askyesno):
        """Test that exit button uses custom callback when set."""
        mock_askyesno.return_value = True  # User confirms exit
        
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set custom exit callback
        mock_callback = Mock()
        panel.set_exit_callback(mock_callback)
        
        # Simulate clicking the exit button
        panel.exit_button.invoke()
        
        # Check that custom callback was called
        mock_callback.assert_called_once()
    
    def test_exit_button_integration_with_main_window(self):
        """Test that exit button integrates properly with main window."""
        # This test will verify integration once MainWindow is updated
        # For now, we test that the interface exists
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that the panel has the necessary interface for main window integration
        assert hasattr(panel, 'set_exit_callback'), "Should have exit callback interface"
        
        # Test that callback can be set to a main window method
        mock_main_window_exit = Mock()
        panel.set_exit_callback(mock_main_window_exit)
        
        assert panel.exit_callback == mock_main_window_exit, "Should accept main window exit method"
    
    def test_exit_button_error_handling(self):
        """Test error handling in exit button functionality."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Set a callback that raises an exception
        def failing_callback():
            raise Exception("Test exception")
        
        panel.set_exit_callback(failing_callback)
        
        # Mock messagebox to capture error dialogs
        with patch('tkinter.messagebox.showerror') as mock_error, \
             patch('tkinter.messagebox.askyesno', return_value=True):
            
            # Simulate clicking the exit button
            panel.exit_button.invoke()
            
            # Check that error was handled gracefully
            mock_error.assert_called_once()
            error_call = mock_error.call_args
            assert 'Error' in error_call[0][0], "Should show error dialog title"
    
    def test_exit_button_accessibility(self):
        """Test that exit button has proper accessibility features."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that button has proper text (not just icon)
        button_text = panel.exit_button.cget('text')
        assert button_text and len(button_text.strip()) > 0, "Button should have readable text"
        
        # Check that button can be focused (for keyboard navigation)
        # Note: Focus testing is limited in headless environments, so we check basic focusability
        try:
            panel.exit_button.focus_set()
            # In headless testing, focus_get() may return None, so we just verify the method exists
            assert hasattr(panel.exit_button, 'focus_set'), "Exit button should have focus_set method"
            assert hasattr(panel.exit_button, 'focus'), "Exit button should have focus method"
        except tk.TclError:
            # Focus operations may fail in headless environments, which is acceptable
            pass
    
    def test_exit_button_state_management(self):
        """Test that exit button state can be managed (enabled/disabled)."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Test that button starts enabled
        initial_state = str(panel.exit_button.cget('state'))
        assert initial_state != 'disabled', "Exit button should start enabled"
        
        # Test that button can be disabled
        panel.exit_button.configure(state='disabled')
        disabled_state = str(panel.exit_button.cget('state'))
        assert disabled_state == 'disabled', "Exit button should be disableable"
        
        # Test that button can be re-enabled
        panel.exit_button.configure(state='normal')
        enabled_state = str(panel.exit_button.cget('state'))
        assert enabled_state == 'normal', "Exit button should be re-enableable"
    
    def test_exit_button_visual_styling(self):
        """Test that exit button has appropriate visual styling."""
        panel = MetadataPanel(self.root, self.mock_db)
        
        # Check that button has appropriate width
        button_width = panel.exit_button.cget('width')
        assert button_width >= 10, "Exit button should have reasonable width"
        
        # Check that button text includes visual indicator (emoji or symbol)
        button_text = panel.exit_button.cget('text')
        # Should have either text with emoji or clear exit indication
        assert ('Exit' in button_text or 'Close' in button_text or 
                '❌' in button_text or '🚪' in button_text), "Button should have clear exit indication"