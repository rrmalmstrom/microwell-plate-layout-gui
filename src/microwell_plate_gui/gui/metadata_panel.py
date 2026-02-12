"""
Metadata Panel Component for Microwell Plate GUI

This module provides the MetadataPanel class for creating metadata entry forms
with dropdowns, validation, and database integration.

Context7 Reference: ttk.Combobox, ttk.Entry, ttk.Label form widgets and grid layout
"""

import tkinter as tk
from tkinter import ttk
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
        
        # Callbacks for communicating with plate canvas
        self.apply_metadata_callback = None
        self.clear_all_metadata_callback = None
        
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
        
        # Configure grid weights for responsive layout
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)  # For "Other" fields
        
        # Create form title
        title_label = ttk.Label(
            self.main_frame,
            text="Metadata Entry",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
        
        # Sample selection (no project dropdown per requirements)
        self.sample_label = ttk.Label(self.main_frame, text="Sample:")
        self.sample_label.grid(row=1, column=0, sticky="w", pady=2)
        
        # Context7 Reference: ttk.Combobox with "other" option
        self.sample_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.sample_var,
            state="readonly",
            width=30
        )
        self.sample_combo.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Sample "Other" text entry (initially hidden)
        self.sample_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.sample_other_var,
            width=30
        )
        # Will be shown/hidden dynamically
        
        # Plate name selection (populated based on sample selection)
        self.plate_name_label = ttk.Label(self.main_frame, text="Plate Name:")
        self.plate_name_label.grid(row=2, column=0, sticky="w", pady=2)
        
        self.plate_name_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.plate_name_var,
            state="readonly",
            width=30
        )
        self.plate_name_combo.grid(row=2, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Plate name "Other" text entry (initially hidden)
        self.plate_name_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.plate_name_other_var,
            width=30
        )
        # Will be shown/hidden dynamically
        
        # Sample type selection with "other" option
        self.sample_type_label = ttk.Label(self.main_frame, text="Sample Type:")
        self.sample_type_label.grid(row=3, column=0, sticky="w", pady=2)
        
        self.sample_type_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.sample_type_var,
            values=["sample", "neg_cntrl", "pos_cntrl", "unused", "other"],
            state="readonly",
            width=30
        )
        self.sample_type_combo.grid(row=3, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Sample type "Other" text entry (initially hidden)
        self.sample_type_other_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.sample_type_other_var,
            width=30
        )
        # Will be shown/hidden dynamically
        
        # Cell count entry
        self.cell_count_label = ttk.Label(self.main_frame, text="Cell Count:")
        self.cell_count_label.grid(row=4, column=0, sticky="w", pady=2)
        
        # Context7 Reference: ttk.Entry with validation
        self.cell_count_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.cell_count_var,
            width=30,
            validate="key",
            validatecommand=(self.main_frame.register(self._validate_cell_count), "%P")
        )
        self.cell_count_entry.grid(row=4, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Group level 1
        self.group1_label = ttk.Label(self.main_frame, text="Group Level 1:")
        self.group1_label.grid(row=5, column=0, sticky="w", pady=2)
        
        self.group1_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group1_var,
            width=30
        )
        self.group1_entry.grid(row=5, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Group level 2
        self.group2_label = ttk.Label(self.main_frame, text="Group Level 2:")
        self.group2_label.grid(row=6, column=0, sticky="w", pady=2)
        
        self.group2_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group2_var,
            width=30
        )
        self.group2_entry.grid(row=6, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Group level 3
        self.group3_label = ttk.Label(self.main_frame, text="Group Level 3:")
        self.group3_label.grid(row=7, column=0, sticky="w", pady=2)
        
        self.group3_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.group3_var,
            width=30
        )
        self.group3_entry.grid(row=7, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Action buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        
        # Apply metadata button
        self.apply_button = ttk.Button(
            button_frame,
            text="Apply to Selected Wells",
            command=self._apply_metadata
        )
        self.apply_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear form button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear all metadata button
        self.clear_all_button = ttk.Button(
            button_frame,
            text="Clear All Metadata",
            command=self._clear_all_metadata
        )
        self.clear_all_button.pack(side=tk.LEFT)
    
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
        if self.sample_var.get() == "other":
            self.sample_other_entry.grid(row=1, column=2, sticky="ew", pady=2, padx=(5, 0))
        else:
            self.sample_other_entry.grid_remove()
            self.sample_other_var.set("")
    
    def _toggle_plate_name_other_field(self, *args) -> None:
        """Show/hide plate name 'Other' text field based on selection."""
        if self.plate_name_var.get() == "other":
            self.plate_name_other_entry.grid(row=2, column=2, sticky="ew", pady=2, padx=(5, 0))
        else:
            self.plate_name_other_entry.grid_remove()
            self.plate_name_other_var.set("")
    
    def _toggle_sample_type_other_field(self, *args) -> None:
        """Show/hide sample type 'Other' text field based on selection."""
        if self.sample_type_var.get() == "other":
            self.sample_type_other_entry.grid(row=3, column=2, sticky="ew", pady=2, padx=(5, 0))
        else:
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
    
    def _clear_all_metadata(self) -> None:
        """Clear all metadata from all wells."""
        if self.clear_all_metadata_callback:
            self.clear_all_metadata_callback()
            logger.info("Cleared all metadata from plate")
        else:
            logger.warning("No clear_all_metadata_callback set")
    
    def validate_form(self) -> Tuple[bool, List[str]]:
        """
        Validate all form fields.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields (no project field per requirements)
        sample_value = self.sample_var.get().strip()
        if not sample_value:
            errors.append("Sample is required")
        elif sample_value == "other" and not self.sample_other_var.get().strip():
            errors.append("Please specify the sample name when 'other' is selected")
        
        plate_name_value = self.plate_name_var.get().strip()
        if not plate_name_value:
            errors.append("Plate name is required")
        elif plate_name_value == "other" and not self.plate_name_other_var.get().strip():
            errors.append("Please specify the plate name when 'other' is selected")
        
        sample_type_value = self.sample_type_var.get().strip()
        if not sample_type_value:
            errors.append("Sample type is required")
        elif sample_type_value == "other" and not self.sample_type_other_var.get().strip():
            errors.append("Please specify the sample type when 'other' is selected")
        
        if not self.group1_var.get().strip():
            errors.append("Group Level 1 is required")
        
        # Validate cell count if provided
        cell_count = self.cell_count_var.get().strip()
        if cell_count and not self._validate_cell_count(cell_count):
            errors.append("Cell count must be a non-negative integer")
        
        return len(errors) == 0, errors
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get all metadata values as dictionary.
        
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
        
        return {
            'sample': sample_value,
            'plate_name': plate_name_value,
            'sample_type': sample_type_value,
            'cell_count': self.cell_count_var.get().strip(),
            'group1': self.group1_var.get().strip(),
            'group2': self.group2_var.get().strip(),
            'group3': self.group3_var.get().strip()
        }
    
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