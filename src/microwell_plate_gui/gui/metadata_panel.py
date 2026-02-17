"""
Metadata Panel Component for Microwell Plate GUI

This module provides the MetadataPanel class for creating metadata entry forms
with dropdowns, validation, and database integration.

Context7 Reference: ttk.Combobox, ttk.Entry, ttk.Label form widgets and grid layout
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, List, Tuple, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetadataPanel:
    """
    Metadata entry panel with form widgets and database integration.
    
    Context7 Reference: 
    - ttk.Combobox for dropdown selections
    - ttk.Entry for text input with validation
    - ttk.Label for form labels
    - Grid layout management for organized form structure
    """
    
    def __init__(self, parent: tk.Widget, db_manager):
        """
        Initialize the MetadataPanel.
        
        Args:
            parent: Parent tkinter widget
            db_manager: DatabaseManager instance for dropdown population
        """
        self.parent = parent
        self.db_manager = db_manager
        
        # Callbacks for communicating with plate canvas and main window
        self.apply_metadata_callback = None
        self.clear_all_metadata_callback = None
        self.export_csv_callback = None
        self.exit_callback = None
        self.export_image_callback = None
        
        # Initialize StringVar variables for all form fields
        self.sample_var = tk.StringVar()
        self.sample_other_var = tk.StringVar()
        self.plate_name_var = tk.StringVar()
        self.plate_name_other_var = tk.StringVar()
        self.sample_type_var = tk.StringVar()
        self.sample_type_other_var = tk.StringVar()
        self.cell_count_var = tk.StringVar()
        self.group1_var = tk.StringVar()
        self.group2_var = tk.StringVar()
        self.group3_var = tk.StringVar()
        
        # Create the form
        self._create_form()
        self._populate_dropdowns()
        self._setup_callbacks()
    
    def _create_form(self) -> None:
        """Create the metadata form with Context7 grid layout."""
        # Context7 Reference: ttk.Frame as container for form widgets
        self.main_frame = ttk.Frame(self.parent, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure parent grid weights for responsive layout
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Configure grid weights for responsive layout
        self.main_frame.columnconfigure(1, weight=2)  # Main fields get more space
        self.main_frame.columnconfigure(2, weight=1)  # "Other" fields get less space but still responsive
        
        # Initialize row tracking for dynamic layout
        self.current_row = 0
        
        # Create form title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Metadata Entry",
            font=("Arial", 14, "bold")
        )
        self.title_label.grid(row=self.current_row, column=0, columnspan=3, pady=(0, 15), sticky="w")
        self.current_row += 1
        
        # Sample selection (no project dropdown per requirements)
        self.sample_label = ttk.Label(self.main_frame, text="Sample:")
        self.sample_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        # Context7 Reference: ttk.Combobox with "other" option
        self.sample_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.sample_var,
            state="readonly",
            width=30
        )
        self.sample_combo.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Sample "Other" text entry (initially hidden)
        # Context7 Reference: Entry widget with proper state management
        self.sample_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.sample_other_var,
            state='normal'  # Ensure it's editable from creation
        )
        # Store row for dynamic positioning
        self.sample_row = self.current_row
        self.current_row += 1
        
        # Plate name selection (populated based on sample selection)
        self.plate_name_label = ttk.Label(self.main_frame, text="Plate Name:")
        self.plate_name_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        self.plate_name_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.plate_name_var,
            state="readonly",
            width=30
        )
        self.plate_name_combo.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Plate name "Other" text entry (initially hidden)
        self.plate_name_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.plate_name_other_var,
            state='normal'
        )
        self.plate_name_row = self.current_row
        self.current_row += 1
        
        # Sample type selection with "other" option
        self.sample_type_label = ttk.Label(self.main_frame, text="Sample Type:")
        self.sample_type_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        self.sample_type_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.sample_type_var,
            values=["sample", "neg_cntrl", "pos_cntrl", "unused", "other"],
            state="readonly",
            width=30
        )
        self.sample_type_combo.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Sample type "Other" text entry (initially hidden)
        self.sample_type_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.sample_type_other_var,
            state='normal'
        )
        # Create "Specify:" label for sample type other field
        self.sample_type_other_label = ttk.Label(self.main_frame, text="Specify:")
        
        self.sample_type_row = self.current_row
        self.current_row += 1
        
        # Cell count entry
        self.cell_count_label = ttk.Label(self.main_frame, text="Cell Count:")
        self.cell_count_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        # Context7 Reference: ttk.Entry with validation
        self.cell_count_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.cell_count_var,
            width=30,
            validate="key",
            validatecommand=(self.main_frame.register(self._validate_cell_count), "%P")
        )
        self.cell_count_entry.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.cell_count_row = self.current_row
        self.current_row += 1
        
        # Group level 1
        self.group1_label = ttk.Label(self.main_frame, text="Group Level 1:")
        self.group1_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        self.group1_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group1_var,
            width=30
        )
        self.group1_entry.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group1_row = self.current_row
        self.current_row += 1
        
        # Group level 2
        self.group2_label = ttk.Label(self.main_frame, text="Group Level 2:")
        self.group2_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        self.group2_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group2_var,
            width=30
        )
        self.group2_entry.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group2_row = self.current_row
        self.current_row += 1
        
        # Group level 3
        self.group3_label = ttk.Label(self.main_frame, text="Group Level 3:")
        self.group3_label.grid(row=self.current_row, column=0, sticky="w", pady=2)
        
        self.group3_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group3_var,
            width=30
        )
        self.group3_entry.grid(row=self.current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group3_row = self.current_row
        self.current_row += 1
        
        # Action buttons frame - Phase 4.2 improved layout
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=self.current_row, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Configure button frame for two-row layout
        self.button_frame.columnconfigure(0, weight=1)
        
        # Primary action buttons frame (top row)
        self.primary_buttons_frame = ttk.Frame(self.button_frame)
        self.primary_buttons_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Apply metadata button
        self.apply_button = ttk.Button(
            self.primary_buttons_frame,
            text="Apply to Selected Wells",
            command=self._apply_metadata
        )
        self.apply_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear form button
        self.clear_button = ttk.Button(
            self.primary_buttons_frame,
            text="Clear Form",
            command=self.clear_form
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Reset all metadata button - using visual cues that work on macOS
        self.clear_all_button = ttk.Button(
            self.primary_buttons_frame,
            text="🔄 Reset All Metadata",
            command=self._clear_all_metadata,
            width=18
        )
        self.clear_all_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Export button frame (bottom row) - full width
        self.export_frame = ttk.Frame(self.button_frame)
        self.export_frame.grid(row=1, column=0, sticky="ew")
        
        # Export CSV button - prominent placement on separate row
        # Now also exports image automatically
        self.export_csv_button = ttk.Button(
            self.export_frame,
            text="📊 Export CSV & Image",
            command=self._export_csv,
            width=20
        )
        self.export_csv_button.pack(pady=(5, 0))
        
        # Exit button - at the bottom
        self.exit_button = ttk.Button(
            self.export_frame,
            text="🚪 Exit Application",
            command=self._exit_application,
            width=20
        )
        self.exit_button.pack(pady=(5, 0))
    
    def _populate_dropdowns(self) -> None:
        """Populate dropdown widgets with data from database."""
        try:
            # Populate sample dropdown with "other" option
            samples = self.db_manager.get_existing_samples()
            samples_with_other = samples + ["other"]
            self.sample_combo['values'] = samples_with_other
            logger.info(f"Populated sample dropdown with {len(samples)} samples")
            
            # Plate name dropdown will be populated based on sample selection
            # Sample type dropdown already has static values including "other"
            
        except Exception as e:
            logger.error(f"Error populating dropdowns: {e}")
            # Set empty values if database error
            self.sample_combo['values'] = ["other"]
    
    def _setup_callbacks(self) -> None:
        """Setup callbacks for dynamic dropdown updates and 'Other' field management."""
        # Context7 Reference: StringVar trace for dynamic updates
        self.sample_var.trace_add("write", self._on_sample_change)
        self.sample_var.trace_add("write", self._toggle_sample_other_field)
        self.plate_name_var.trace_add("write", self._toggle_plate_name_other_field)
        self.sample_type_var.trace_add("write", self._toggle_sample_type_other_field)
    
    def _on_sample_change(self, *args) -> None:
        """Callback when sample selection changes."""
        self._update_plate_names()
    
    def _update_plate_names(self) -> None:
        """Update plate name dropdown based on sample selection."""
        sample = self.sample_var.get()
        
        if sample and sample != "other":
            try:
                # Generate plate names based on sample (without project)
                plate_names = self.db_manager.generate_plate_names("", sample)
                plate_names_with_other = plate_names + ["other"]
                self.plate_name_combo['values'] = plate_names_with_other
                logger.info(f"Updated plate names for {sample}: {len(plate_names)} plates")
                
                # Auto-select first plate name if available
                if plate_names:
                    self.plate_name_var.set(plate_names[0])
                    
            except Exception as e:
                logger.error(f"Error updating plate names: {e}")
                self.plate_name_combo['values'] = ["other"]
        else:
            self.plate_name_combo['values'] = ["other"]
            self.plate_name_var.set("")
    
    def _toggle_sample_other_field(self, *args) -> None:
        """Show/hide sample 'Other' text field based on selection."""
        # Context7 Reference: Proper grid layout management for dynamic widgets
        if self.sample_var.get() == "other":
            # Position in column 2 (next to dropdown)
            self.sample_other_entry.grid(
                row=self.sample_row,
                column=2,
                sticky="ew",
                pady=2,
                padx=(5, 0)
            )
            # Ensure proper state and focus
            self.sample_other_entry.configure(state='normal')
            self.sample_other_entry.focus_set()
        else:
            self.sample_other_entry.grid_remove()
            self.sample_other_var.set("")
    
    def _toggle_plate_name_other_field(self, *args) -> None:
        """Show/hide plate name 'Other' text field based on selection."""
        if self.plate_name_var.get() == "other":
            # Position in column 2 (next to dropdown)
            self.plate_name_other_entry.grid(
                row=self.plate_name_row,
                column=2,
                sticky="ew",
                pady=2,
                padx=(5, 0)
            )
            # Ensure proper state and focus
            self.plate_name_other_entry.configure(state='normal')
            self.plate_name_other_entry.focus_set()
        else:
            self.plate_name_other_entry.grid_remove()
            self.plate_name_other_var.set("")
    
    def _toggle_sample_type_other_field(self, *args) -> None:
        """Show/hide sample type 'Other' text field based on selection."""
        # Context7 Reference: Dynamic widget positioning with proper grid management
        if self.sample_type_var.get() == "other":
            # Place the "Other" field in column 2 (next to the dropdown) to avoid row conflicts
            self.sample_type_other_entry.grid(
                row=self.sample_type_row,
                column=2,
                sticky="ew",
                pady=2,
                padx=(5, 0)
            )
            
            # Ensure the entry is properly configured and focusable
            self.sample_type_other_entry.configure(state='normal')
            self.sample_type_other_entry.focus_set()
            
        else:
            # Hide the other field
            self.sample_type_other_entry.grid_remove()
            self.sample_type_other_var.set("")
    
    
    def _validate_cell_count(self, value: str) -> bool:
        """
        Validate cell count input - must be non-negative integer.
        
        Context7 Reference: Entry widget validation with validatecommand
        
        Args:
            value: Input value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if value == "":
            return True  # Allow empty for clearing
        
        try:
            count = int(value)
            return count >= 0  # Allow zero and positive integers
        except ValueError:
            return False
    
    def _apply_metadata(self) -> None:
        """Apply current metadata to selected wells and clear form."""
        # Validate form first
        is_valid, errors = self.validate_form()
        
        if not is_valid:
            # Show validation errors (placeholder for now)
            logger.warning(f"Form validation failed: {errors}")
            return
        
        # Get metadata and trigger callback
        metadata = self.get_metadata()
        logger.info(f"Applying metadata: {metadata}")
        
        # Call the plate canvas to apply metadata to selected wells
        if self.apply_metadata_callback:
            self.apply_metadata_callback(metadata)
            
            # Clear the form after successful application
            self.clear_form()
            logger.info("Form cleared after metadata application")
        else:
            logger.warning("No apply_metadata_callback set")
    
    def set_apply_metadata_callback(self, callback):
        """Set the callback function for applying metadata to wells."""
        self.apply_metadata_callback = callback
    
    def set_clear_all_metadata_callback(self, callback):
        """Set the callback function for clearing all metadata from wells."""
        self.clear_all_metadata_callback = callback
    
    def set_export_csv_callback(self, callback):
        """Set the callback function for exporting CSV."""
        self.export_csv_callback = callback
    
    def set_exit_callback(self, callback):
        """Set the callback function for exiting the application."""
        self.exit_callback = callback
    
    def set_export_image_callback(self, callback):
        """Set the callback function for exporting images."""
        self.export_image_callback = callback
    
    def _clear_all_metadata(self) -> None:
        """Clear all metadata from all wells."""
        if self.clear_all_metadata_callback:
            self.clear_all_metadata_callback()
            logger.info("Cleared all metadata from plate")
        else:
            logger.warning("No clear_all_metadata_callback set")
    
    def _export_csv(self) -> None:
        """Export plate layout to CSV file."""
        csv_filename = None
        try:
            if self.export_csv_callback:
                # The CSV export callback should return the filename
                csv_filename = self.export_csv_callback()
                logger.info(f"CSV export completed: {csv_filename}")
            else:
                logger.warning("No export_csv_callback set")
                messagebox.showerror("Export Error", "CSV export functionality not available")
                return
        except Exception as e:
            logger.error(f"Error during CSV export: {e}")
            messagebox.showerror("Export Error", f"Failed to export CSV: {str(e)}")
            return
        
        # After successful CSV export, also export image automatically
        try:
            if self.export_image_callback and csv_filename:
                # Generate image filename based on CSV filename
                image_filename = csv_filename.replace('.csv', '_layout.pdf')
                
                logger.info(f"Attempting automatic image export to: {image_filename}")
                success = self.export_image_callback(image_filename)
                if success:
                    logger.info(f"Image export completed successfully: {image_filename}")
                    # Show success message for image export too
                    messagebox.showinfo(
                        "Export Complete",
                        f"Both CSV and image exported successfully!\n\nCSV: {csv_filename}\nImage: {image_filename}"
                    )
                else:
                    logger.warning(f"Image export failed: {image_filename}")
                    messagebox.showwarning(
                        "Partial Export",
                        f"CSV exported successfully, but image export failed.\n\nCSV: {csv_filename}\nImage export failed: {image_filename}"
                    )
            else:
                if not self.export_image_callback:
                    logger.warning("No export_image_callback set for automatic image export")
                    messagebox.showwarning(
                        "Image Export Unavailable",
                        f"CSV exported successfully, but image export is not configured.\n\nCSV: {csv_filename or 'Unknown'}"
                    )
                elif not csv_filename:
                    logger.warning("No CSV filename available for image export")
                    messagebox.showwarning(
                        "Image Export Unavailable",
                        "CSV exported successfully, but filename not available for image export."
                    )
                
        except Exception as e:
            logger.error(f"Error during automatic image export: {e}")
            messagebox.showwarning(
                "Image Export Error",
                f"CSV exported successfully, but image export encountered an error.\n\nCSV: {csv_filename or 'Unknown'}\nError: {str(e)}"
            )
    
    def _exit_application(self) -> None:
        """Exit the application with confirmation dialog."""
        try:
            # Show confirmation dialog
            result = messagebox.askyesno(
                "Exit Application",
                "Are you sure you want to exit the application?\n\nAny unsaved changes will be lost."
            )
            
            if result:  # User confirmed exit
                logger.info("Application exit confirmed by user")
                if self.exit_callback:
                    self.exit_callback()
                else:
                    # Fallback: terminate the application completely
                    import sys
                    import os
                    self.parent.quit()
                    self.parent.destroy()
                    os._exit(0)  # Force exit the Python process
            else:
                logger.info("Application exit cancelled by user")
                
        except Exception as e:
            logger.error(f"Error during application exit: {e}")
            messagebox.showerror("Exit Error", f"An error occurred while exiting: {str(e)}")
            # Force exit even if there's an error
            import sys
            import os
            os._exit(1)
    
    
    def clear_form(self) -> None:
        """Clear all form fields."""
        self.sample_var.set("")
        self.sample_other_var.set("")
        self.plate_name_var.set("")
        self.plate_name_other_var.set("")
        self.sample_type_var.set("")
        self.sample_type_other_var.set("")
        self.cell_count_var.set("")
        self.group1_var.set("")
        self.group2_var.set("")
        self.group3_var.set("")
        
        # Hide all "other" fields
        self.sample_other_entry.grid_remove()
        self.plate_name_other_entry.grid_remove()
        self.sample_type_other_entry.grid_remove()
        
        logger.info("Form cleared")
    
    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Set form values from metadata dictionary.
        
        Args:
            metadata: Dictionary containing form values
        """
        self.sample_var.set(metadata.get('sample', ''))
        self.plate_name_var.set(metadata.get('plate_name', ''))
        self.sample_type_var.set(metadata.get('sample_type', ''))
        self.cell_count_var.set(metadata.get('cell_count', ''))
        self.group1_var.set(metadata.get('group1', ''))
        self.group2_var.set(metadata.get('group2', ''))
        self.group3_var.set(metadata.get('group3', ''))
        
        logger.info("Form populated with metadata")
    
    def enable_form(self, enabled: bool = True) -> None:
        """
        Enable or disable all form widgets.
        
        Args:
            enabled: True to enable, False to disable
        """
        state = "readonly" if enabled else "disabled"
        entry_state = "normal" if enabled else "disabled"
        
        self.sample_combo.configure(state=state)
        self.plate_name_combo.configure(state=state)
        self.sample_type_combo.configure(state=state)
        self.cell_count_entry.configure(state=entry_state)
        self.group1_entry.configure(state=entry_state)
        self.group2_entry.configure(state=entry_state)
        self.group3_entry.configure(state=entry_state)
        self.apply_button.configure(state=entry_state)
        self.clear_button.configure(state=entry_state)
        
        # Also enable/disable "Other" entry fields
        self.sample_other_entry.configure(state=entry_state)
        self.plate_name_other_entry.configure(state=entry_state)
        self.sample_type_other_entry.configure(state=entry_state)
    
    def hide_sample_and_plate_fields(self):
        """
        Hide sample and plate name fields for single-sample mode.
        These are already configured in the intermediate dialog.
        """
        # Hide sample widgets
        self.sample_label.grid_remove()
        self.sample_combo.grid_remove()
        self.sample_other_entry.grid_remove()
        
        # Hide plate name widgets
        self.plate_name_label.grid_remove()
        self.plate_name_combo.grid_remove()
        self.plate_name_other_entry.grid_remove()
        
        # Adjust grid layout for remaining widgets
        self._adjust_grid_layout_after_hiding_fields()
    
    def hide_plate_name_field(self):
        """
        Hide plate name field for multi-sample mode.
        Plate name is already configured in the intermediate dialog.
        """
        # Hide plate name widgets
        self.plate_name_label.grid_remove()
        self.plate_name_combo.grid_remove()
        self.plate_name_other_entry.grid_remove()
        
        # Adjust grid layout for multi-sample mode (keep sample dropdown visible)
        self._adjust_grid_layout_for_multi_sample_mode()
    
    def _adjust_grid_layout_after_hiding_fields(self):
        """Adjust grid layout after hiding some fields."""
        # Context7 Reference: Proper grid layout management after dynamic changes
        current_row = 1  # Start after title
        
        # Sample type (always visible) - update its stored row position
        self.sample_type_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.sample_type_combo.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.sample_type_row = current_row
        current_row += 1
        
        # Cell count (always visible) - update its stored row position
        self.cell_count_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.cell_count_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.cell_count_row = current_row
        current_row += 1
        
        # Group levels (always visible) - update their stored row positions
        self.group1_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group1_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group1_row = current_row
        current_row += 1
        
        self.group2_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group2_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group2_row = current_row
        current_row += 1
        
        self.group3_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group3_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group3_row = current_row
        current_row += 1
        
        # Move button frame to the new position
        self.button_frame.grid(row=current_row, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Note: Do NOT call _toggle_sample_type_other_field() here to avoid recursion
        # The "Other" field visibility will be handled by the existing trace callbacks
    
    def _adjust_grid_layout_for_multi_sample_mode(self):
        """Adjust grid layout for multi-sample mode (keep sample dropdown, hide plate name)."""
        # Context7 Reference: Proper grid layout management for multi-sample mode
        current_row = 1  # Start after title
        
        # Sample dropdown (visible in multi-sample mode) - update its stored row position
        self.sample_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.sample_combo.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.sample_row = current_row
        current_row += 1
        
        # Sample type (always visible) - update its stored row position
        self.sample_type_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.sample_type_combo.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.sample_type_row = current_row
        current_row += 1
        
        # Cell count (always visible) - update its stored row position
        self.cell_count_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.cell_count_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.cell_count_row = current_row
        current_row += 1
        
        # Group levels (always visible) - update their stored row positions
        self.group1_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group1_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group1_row = current_row
        current_row += 1
        
        self.group2_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group2_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group2_row = current_row
        current_row += 1
        
        self.group3_label.grid(row=current_row, column=0, sticky="w", pady=2)
        self.group3_entry.grid(row=current_row, column=1, sticky="ew", pady=2, padx=(5, 0))
        self.group3_row = current_row
        current_row += 1
        
        # Move button frame to the new position
        self.button_frame.grid(row=current_row, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Note: The "Other" field visibility will be handled by the existing trace callbacks
    
    def set_single_sample_defaults(self, config: dict):
        """
        Set default values for single-sample mode.
        
        Args:
            config: Dictionary with 'sample' and 'plate_name' keys
        """
        # Store the single-sample configuration for use in metadata generation
        self._single_sample_config = config
        
        # Update form title to indicate single-sample mode
        if hasattr(self, 'title_label'):
            self.title_label.configure(text="Metadata Entry (Single Sample Mode)")
    
    def set_multi_sample_defaults(self, config: dict):
        """
        Set default values for multi-sample mode.
        
        Args:
            config: Dictionary with 'sample_plate_name' key
        """
        # Store the multi-sample configuration for use in metadata generation
        self._multi_sample_config = config
        
        # Update form title to indicate multi-sample mode
        if hasattr(self, 'title_label'):
            self.title_label.configure(text="Metadata Entry (Multi-Sample Mode)")
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get all metadata values as dictionary.
        Now handles both single-sample and multi-sample modes.
        
        Returns:
            Dictionary containing all form values
        """
        # Get actual values, using "other" text fields when "other" is selected
        sample_value = self.sample_var.get().strip()
        if sample_value == "other":
            sample_value = self.sample_other_var.get().strip()
        
        plate_name_value = self.plate_name_var.get().strip()
        if plate_name_value == "other":
            plate_name_value = self.plate_name_other_var.get().strip()
        
        sample_type_value = self.sample_type_var.get().strip()
        if sample_type_value == "other":
            sample_type_value = self.sample_type_other_var.get().strip()
        
        # Handle single-sample mode: use pre-configured values
        if hasattr(self, '_single_sample_config') and self._single_sample_config:
            sample_value = self._single_sample_config['sample']
            plate_name_value = self._single_sample_config['plate_name']
        
        # Handle multi-sample mode: use pre-configured plate name
        if hasattr(self, '_multi_sample_config') and self._multi_sample_config:
            plate_name_value = self._multi_sample_config['sample_plate_name']
        
        return {
            'sample': sample_value,
            'plate_name': plate_name_value,
            'sample_type': sample_type_value,
            'cell_count': self.cell_count_var.get().strip(),
            'group1': self.group1_var.get().strip(),
            'group2': self.group2_var.get().strip(),
            'group3': self.group3_var.get().strip()
        }
    
    def validate_form(self) -> Tuple[bool, List[str]]:
        """
        Validate all form fields.
        Updated to handle single-sample and multi-sample modes.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # In single-sample mode, sample and plate are pre-configured
        if not (hasattr(self, '_single_sample_config') and self._single_sample_config):
            # Check sample field (only if not in single-sample mode)
            sample_value = self.sample_var.get().strip()
            if not sample_value:
                errors.append("Sample is required")
            elif sample_value == "other" and not self.sample_other_var.get().strip():
                errors.append("Please specify the sample name when 'other' is selected")
        
        # In both single and multi-sample modes, plate name is pre-configured
        if not (hasattr(self, '_single_sample_config') and self._single_sample_config) and \
           not (hasattr(self, '_multi_sample_config') and self._multi_sample_config):
            # Check plate name field (only if not in single or multi-sample mode)
            plate_name_value = self.plate_name_var.get().strip()
            if not plate_name_value:
                errors.append("Plate name is required")
            elif plate_name_value == "other" and not self.plate_name_other_var.get().strip():
                errors.append("Please specify the plate name when 'other' is selected")
        
        # Sample type is always required
        sample_type_value = self.sample_type_var.get().strip()
        if not sample_type_value:
            errors.append("Sample type is required")
        elif sample_type_value == "other" and not self.sample_type_other_var.get().strip():
            errors.append("Please specify the sample type when 'other' is selected")
        
        # Group Level 1 is required except for "unused" wells
        if sample_type_value != "unused" and not self.group1_var.get().strip():
            errors.append("Group Level 1 is required")
        
        # Validate cell count if provided
        cell_count = self.cell_count_var.get().strip()
        if cell_count and not self._validate_cell_count(cell_count):
            errors.append("Cell count must be a non-negative integer")
        
        return len(errors) == 0, errors