"""
Main window GUI component for the microwell plate application.

Context7 Reference: Tkinter application architecture patterns and main window setup
- Using tkinter.Tk for main application root
- Using ttk.Panedwindow for split layout design  
- Following standard widget configuration patterns
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
import logging
import os
from .metadata_panel import MetadataPanel
from .plate_canvas import PlateCanvas
from .legend_panel import LegendPanel
from ..data.database import DatabaseManager
from ..utils.csv_export import export_plate_layout, CSVExportError

logger = logging.getLogger(__name__)


class StartupDialog:
    """
    Startup dialog for selecting plate type and sample mode.
    
    Context7 Reference: Standard dialog patterns with tkinter.Toplevel
    """
    
    def __init__(self, parent: tk.Tk):
        """
        Initialize startup dialog.
        
        Args:
            parent: Parent window
        """
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Microwell Plate Setup")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Center dialog on parent - Context7 Reference: wm_transient for modal dialogs
        self.dialog.wm_transient(parent)
        self.dialog.grab_set()
        
        # Variables for user selections
        self.plate_type_var = tk.StringVar(value="384")  # Default to 384-well format
        self.sample_mode_var = tk.StringVar(value="single")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Microwell Plate Layout Designer",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Plate type selection
        plate_frame = ttk.LabelFrame(main_frame, text="Plate Type", padding="10")
        plate_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(
            plate_frame,
            text="96-well plate (A-H, 1-12)",
            variable=self.plate_type_var,
            value="96"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            plate_frame,
            text="384-well plate (A-P, 1-24)",
            variable=self.plate_type_var,
            value="384"
        ).pack(anchor=tk.W)
        
        # Sample mode selection
        sample_frame = ttk.LabelFrame(main_frame, text="Sample Mode", padding="10")
        sample_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Radiobutton(
            sample_frame,
            text="Single sample per plate (typical)",
            variable=self.sample_mode_var,
            value="single"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            sample_frame,
            text="Multiple samples per plate",
            variable=self.sample_mode_var,
            value="multi"
        ).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Use tk.Button instead of ttk.Button for better macOS compatibility
        # Context7 Reference: Basic tk.Button creation with explicit text
        tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Continue",
            command=self._on_continue,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT)
        
    def _on_continue(self):
        """Handle continue button click."""
        self.result = {
            'plate_type': self.plate_type_var.get(),
            'sample_mode': self.sample_mode_var.get()
        }
        self.dialog.destroy()
        
    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()
        
    def show(self) -> Optional[dict]:
        """
        Show dialog and return result.
        
        Returns:
            Dict with plate_type and sample_mode, or None if cancelled
        """
        # Center on parent
        self.dialog.update_idletasks()
        x = (self.parent.winfo_x() + 
             (self.parent.winfo_width() // 2) - 
             (self.dialog.winfo_width() // 2))
        y = (self.parent.winfo_y() + 
             (self.parent.winfo_height() // 2) - 
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
        # Wait for dialog to close
        self.parent.wait_window(self.dialog)
        return self.result


class SingleSampleDialog:
    """
    Dialog for single-sample mode to select sample and plate name.
    
    Context7 Reference: Modal dialog with Toplevel, Combobox widgets, and form validation
    """
    
    def __init__(self, parent: tk.Tk, db_manager):
        """
        Initialize single-sample dialog.
        
        Args:
            parent: Parent window
            db_manager: DatabaseManager instance for dropdown population
        """
        self.parent = parent
        self.db_manager = db_manager
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Single Sample Configuration")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        
        # Center dialog on parent - Context7 Reference: wm_transient for modal dialogs
        self.dialog.wm_transient(parent)
        self.dialog.grab_set()
        
        # Variables for user selections
        self.sample_var = tk.StringVar()
        self.sample_other_var = tk.StringVar()
        self.plate_name_var = tk.StringVar()
        self.plate_name_other_var = tk.StringVar()
        
        self._create_widgets()
        self._populate_dropdowns()
        self._setup_callbacks()
        
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Single Sample Configuration",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Select sample and plate name to apply to all wells:",
            font=("Arial", 10)
        )
        desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Sample selection
        sample_label = ttk.Label(main_frame, text="Sample:")
        sample_label.grid(row=2, column=0, sticky="w", pady=5)
        
        # Context7 Reference: ttk.Combobox with "other" option
        self.sample_combo = ttk.Combobox(
            main_frame,
            textvariable=self.sample_var,
            state="readonly",
            width=25
        )
        self.sample_combo.grid(row=2, column=1, sticky="ew", pady=5, padx=(5, 0))
        
        # Sample "Other" text entry (initially hidden)
        self.sample_other_entry = ttk.Entry(
            main_frame,
            textvariable=self.sample_other_var,
            width=25
        )
        
        # Plate name selection
        plate_label = ttk.Label(main_frame, text="Plate Name:")
        plate_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.plate_name_combo = ttk.Combobox(
            main_frame,
            textvariable=self.plate_name_var,
            state="readonly",
            width=25
        )
        self.plate_name_combo.grid(row=3, column=1, sticky="ew", pady=5, padx=(5, 0))
        
        # Plate name "Other" text entry (initially hidden)
        self.plate_name_other_entry = ttk.Entry(
            main_frame,
            textvariable=self.plate_name_other_var,
            width=25
        )
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Continue",
            command=self._on_continue,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT)
        
    def _populate_dropdowns(self):
        """Populate dropdown widgets with data from database."""
        try:
            # Populate sample dropdown with "other" option
            samples = self.db_manager.get_existing_samples()
            samples_with_other = samples + ["other"]
            self.sample_combo['values'] = samples_with_other
            
        except Exception as e:
            # Set empty values if database error
            self.sample_combo['values'] = ["other"]
    
    def _setup_callbacks(self):
        """Setup callbacks for dynamic dropdown updates and 'Other' field management."""
        # Context7 Reference: StringVar trace for dynamic updates
        self.sample_var.trace_add("write", self._on_sample_change)
        self.sample_var.trace_add("write", self._toggle_sample_other_field)
        self.plate_name_var.trace_add("write", self._toggle_plate_name_other_field)
    
    def _on_sample_change(self, *args):
        """Callback when sample selection changes."""
        self._update_plate_names()
    
    def _update_plate_names(self):
        """Update plate name dropdown based on sample selection."""
        sample = self.sample_var.get()
        
        if sample and sample != "other":
            try:
                # Generate plate names based on sample (without project)
                plate_names = self.db_manager.generate_plate_names("", sample)
                plate_names_with_other = plate_names + ["other"]
                self.plate_name_combo['values'] = plate_names_with_other
                
                # Auto-select first plate name if available
                if plate_names:
                    self.plate_name_var.set(plate_names[0])
                    
            except Exception as e:
                self.plate_name_combo['values'] = ["other"]
        else:
            self.plate_name_combo['values'] = ["other"]
            self.plate_name_var.set("")
    
    def _toggle_sample_other_field(self, *args):
        """Show/hide sample 'Other' text field based on selection."""
        if self.sample_var.get() == "other":
            self.sample_other_entry.grid(row=2, column=2, sticky="ew", pady=5, padx=(5, 0))
        else:
            self.sample_other_entry.grid_remove()
            self.sample_other_var.set("")
    
    def _toggle_plate_name_other_field(self, *args):
        """Show/hide plate name 'Other' text field based on selection."""
        if self.plate_name_var.get() == "other":
            self.plate_name_other_entry.grid(row=3, column=2, sticky="ew", pady=5, padx=(5, 0))
        else:
            self.plate_name_other_entry.grid_remove()
            self.plate_name_other_var.set("")
    
    def _validate_form(self):
        """Validate form inputs."""
        errors = []
        
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
        
        return len(errors) == 0, errors
    
    def _on_continue(self):
        """Handle continue button click."""
        is_valid, errors = self._validate_form()
        
        if not is_valid:
            # Show validation errors (simple message for now)
            error_msg = "\n".join(errors)
            tk.messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get actual values, using "other" text fields when "other" is selected
        sample_value = self.sample_var.get().strip()
        if sample_value == "other":
            sample_value = self.sample_other_var.get().strip()
        
        plate_name_value = self.plate_name_var.get().strip()
        if plate_name_value == "other":
            plate_name_value = self.plate_name_other_var.get().strip()
        
        self.result = {
            'sample': sample_value,
            'plate_name': plate_name_value
        }
        self.dialog.destroy()
        
    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()
        
    def show(self) -> Optional[dict]:
        """
        Show dialog and return result.
        
        Returns:
            Dict with sample and plate_name, or None if cancelled
        """
        # Center on parent
        self.dialog.update_idletasks()
        x = (self.parent.winfo_x() +
             (self.parent.winfo_width() // 2) -
             (self.dialog.winfo_width() // 2))
        y = (self.parent.winfo_y() +
             (self.parent.winfo_height() // 2) -
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
        # Wait for dialog to close
        self.parent.wait_window(self.dialog)
        return self.result


class MultiSampleDialog:
    """
    Dialog for multi-sample mode to enter sample plate name.
    
    Context7 Reference: Simple modal dialog with text entry and validation
    """
    
    def __init__(self, parent: tk.Tk):
        """
        Initialize multi-sample dialog.
        
        Args:
            parent: Parent window
        """
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Multi-Sample Configuration")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # Center dialog on parent - Context7 Reference: wm_transient for modal dialogs
        self.dialog.wm_transient(parent)
        self.dialog.grab_set()
        
        # Variable for user input
        self.plate_name_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Multi-Sample Configuration",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Enter the sample plate name for this multi-sample plate:",
            font=("Arial", 10)
        )
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Plate name entry
        plate_label = ttk.Label(main_frame, text="Sample Plate Name:")
        plate_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.plate_name_entry = ttk.Entry(
            main_frame,
            textvariable=self.plate_name_var,
            width=30
        )
        self.plate_name_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.plate_name_entry.focus()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Continue",
            command=self._on_continue,
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT)
    
    def _on_continue(self):
        """Handle continue button click."""
        plate_name = self.plate_name_var.get().strip()
        
        if not plate_name:
            tk.messagebox.showerror("Validation Error", "Sample plate name is required")
            return
        
        self.result = {
            'sample_plate_name': plate_name
        }
        self.dialog.destroy()
        
    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()
        
    def show(self) -> Optional[dict]:
        """
        Show dialog and return result.
        
        Returns:
            Dict with sample_plate_name, or None if cancelled
        """
        # Center on parent
        self.dialog.update_idletasks()
        x = (self.parent.winfo_x() +
             (self.parent.winfo_width() // 2) -
             (self.dialog.winfo_width() // 2))
        y = (self.parent.winfo_y() +
             (self.parent.winfo_height() // 2) -
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
        # Wait for dialog to close
        self.parent.wait_window(self.dialog)
        return self.result


class MainWindow:
    """
    Main application window with split layout design.
    
    Context7 Reference: 
    - tkinter.Tk application root setup
    - ttk.Panedwindow for split layout
    - Standard widget configuration patterns
    """
    
    def __init__(self, root: tk.Tk, project_directory: str = None):
        """
        Initialize main window.
        
        Args:
            root: Tkinter root window
            project_directory: Path to project directory containing database files
        """
        self.root = root
        self.plate_type = None
        self.sample_mode = None
        
        # Set project directory and construct database path
        if project_directory is None:
            project_directory = os.getcwd()
        
        self.project_directory = project_directory
        self.db_path = os.path.join(project_directory, "example_database.db")
        
        print(f"📁 Project directory: {self.project_directory}")
        print(f"🗄️ Database path: {self.db_path}")
        
        # Initialize database manager
        self.db_manager = DatabaseManager(self.db_path)
        
        # Workflow state for single-sample mode
        self.single_sample_config = None  # Will store sample and plate_name
        self.multi_sample_config = None   # Will store sample_plate_name
        
        # Initialize components
        self.plate_canvas = None
        self.metadata_panel = None
        self.legend_panel = None
        
        self._setup_window()
        self._create_layout()
        
    def _setup_window(self):
        """Setup main window properties."""
        # Context7 Reference: tkinter.Tk configuration
        self.root.title("Microwell Plate Layout Designer")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def _create_layout(self):
        """Create split layout with paned window."""
        # Context7 Reference: ttk.Panedwindow for split layout with proper sizing
        self.paned_window = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create frames for each panel
        self.plate_frame = ttk.Frame(self.paned_window)
        self.right_panel_frame = ttk.Frame(self.paned_window)
        
        # Add frames to paned window with appropriate sizing
        # Context7 Reference: weight parameter controls relative sizing
        # Left panel gets reasonable fixed proportion, right panel gets most expansion
        self.paned_window.add(self.plate_frame, weight=2)  # Fixed reasonable size for plate
        self.paned_window.add(self.right_panel_frame, weight=3)  # More expansion for right panel
        
        # Create vertical paned window for right panel (metadata + legend)
        self.right_paned_window = ttk.Panedwindow(self.right_panel_frame, orient=tk.VERTICAL)
        self.right_paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for metadata and legend
        self.metadata_frame = ttk.Frame(self.right_paned_window)
        self.legend_frame = ttk.Frame(self.right_paned_window)
        
        # Add frames to right paned window with improved proportions for Phase 4.2
        # Context7 Reference: Proper weight distribution for better visibility
        # Reduced metadata weight to give legend more space, preventing scrollbar issues
        self.right_paned_window.add(self.metadata_frame, weight=2)
        self.right_paned_window.add(self.legend_frame, weight=3)
        
        # Create metadata and legend panels
        self.metadata_panel = MetadataPanel(self.metadata_frame, self.db_manager)
        self.legend_panel = LegendPanel(self.legend_frame)
        
        # Placeholder for plate canvas (will be created after startup dialog)
        self.plate_canvas_placeholder = ttk.Label(
            self.plate_frame,
            text="Select plate type from startup dialog to initialize plate canvas",
            font=("Arial", 12),
            anchor=tk.CENTER
        )
        self.plate_canvas_placeholder.pack(expand=True)
        
    def show_startup_dialog(self) -> bool:
        """
        Show startup dialog for plate configuration and handle workflow.
        
        Returns:
            True if user completed configuration, False if cancelled
        """
        # Step 1: Show initial startup dialog
        dialog = StartupDialog(self.root)
        result = dialog.show()
        
        if not result:
            return False
        
        self.plate_type = result['plate_type']
        self.sample_mode = result['sample_mode']
        
        # Step 2: Show mode-specific intermediate dialog
        if self.sample_mode == "single":
            # Single-sample mode: get sample and plate selection
            single_dialog = SingleSampleDialog(self.root, self.db_manager)
            single_result = single_dialog.show()
            
            if not single_result:
                return False
            
            self.single_sample_config = single_result
            
        elif self.sample_mode == "multi":
            # Multi-sample mode: get sample plate name
            multi_dialog = MultiSampleDialog(self.root)
            multi_result = multi_dialog.show()
            
            if not multi_result:
                return False
            
            self.multi_sample_config = multi_result
        
        # Step 3: Initialize the plate canvas and UI
        self._initialize_plate_interface()
        return True
    
    def _initialize_plate_interface(self):
        """Initialize the plate interface after workflow configuration."""
        # Update window title to show configuration
        mode_text = f"{self.sample_mode} sample"
        if self.sample_mode == "single" and self.single_sample_config:
            sample_name = self.single_sample_config['sample']
            mode_text += f" ({sample_name})"
        elif self.sample_mode == "multi" and self.multi_sample_config:
            plate_name = self.multi_sample_config['sample_plate_name']
            mode_text += f" ({plate_name})"
        
        title = f"Microwell Plate Layout Designer - {self.plate_type}-well ({mode_text})"
        self.root.title(title)
        
        # Create plate canvas now that we know the plate type
        self._create_plate_canvas()
        
        # Add configuration display panel
        self._create_configuration_display()
        
        # Configure metadata panel based on mode
        self._configure_metadata_panel_for_mode()
    
    def _configure_metadata_panel_for_mode(self):
        """Configure metadata panel based on selected mode."""
        if self.metadata_panel:
            if self.sample_mode == "single":
                # In single-sample mode, hide sample and plate dropdowns from metadata panel
                # since they were already selected in the intermediate dialog
                self.metadata_panel.hide_sample_and_plate_fields()
                
                # Pre-populate with single-sample configuration
                if self.single_sample_config:
                    self.metadata_panel.set_single_sample_defaults(self.single_sample_config)
                    
            elif self.sample_mode == "multi":
                # In multi-sample mode, show sample dropdown but hide plate name field
                # since plate name was set in intermediate dialog
                self.metadata_panel.hide_plate_name_field()
                
                # Pre-populate with multi-sample configuration
                if self.multi_sample_config:
                    self.metadata_panel.set_multi_sample_defaults(self.multi_sample_config)
        
    def on_plate_type_selected(self, plate_type: str, sample_mode: str):
        """
        Handle plate type selection callback.
        
        Args:
            plate_type: "96" or "384"
            sample_mode: "single" or "multi"
        """
        self.plate_type = plate_type
        self.sample_mode = sample_mode
        
        # Update window title to show configuration
        title = f"Microwell Plate Layout Designer - {plate_type}-well ({sample_mode} sample)"
        self.root.title(title)
        
        # Note: Plate canvas creation is now handled in _initialize_plate_interface()
        # after the workflow dialogs are completed
    
    def _create_plate_canvas(self):
        """Create the plate canvas with the selected plate type."""
        if self.plate_type:
            # Remove placeholder
            if hasattr(self, 'plate_canvas_placeholder'):
                self.plate_canvas_placeholder.destroy()
            
            # Destroy existing plate canvas if it exists to prevent duplicates
            if hasattr(self, 'plate_canvas') and self.plate_canvas:
                self.plate_canvas.canvas.destroy()
                self.plate_canvas = None
            
            # Create plate canvas with responsive sizing
            # Context7 Reference: Responsive canvas sizing based on available space
            plate_type_str = f"{self.plate_type}-well"
            
            # Calculate appropriate well size based on plate type for better visibility
            if self.plate_type == "96":
                well_size = 25  # Larger wells for 96-well plates
                well_spacing = 6
            else:  # 384-well
                well_size = 15  # Smaller wells for 384-well plates to fit
                well_spacing = 4
            
            self.plate_canvas = PlateCanvas(
                self.plate_frame,
                plate_type_str,
                well_size=well_size,
                well_spacing=well_spacing
            )
            
            # Pack the canvas to make it visible with proper padding
            self.plate_canvas.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Connect plate canvas to metadata panel for well selection
            self._setup_well_selection_integration()
    
    def _create_configuration_display(self):
        """Create a prominent display panel showing the current configuration."""
        # Create configuration frame at the top of the plate frame
        # Initialize config_display_frame if it doesn't exist
        if not hasattr(self, 'config_display_frame'):
            self.config_display_frame = None
            
        if self.config_display_frame:
            self.config_display_frame.destroy()
        
        self.config_display_frame = ttk.LabelFrame(
            self.plate_frame,
            text="Current Configuration",
            padding="10"
        )
        self.config_display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Configuration details with larger, more prominent text
        config_text = ""
        if self.sample_mode == "single" and self.single_sample_config:
            sample = self.single_sample_config['sample']
            plate_name = self.single_sample_config['plate_name']
            config_text = f"Mode: Single Sample | Sample: {sample} | Plate: {plate_name}"
        elif self.sample_mode == "multi" and self.multi_sample_config:
            plate_name = self.multi_sample_config['sample_plate_name']
            config_text = f"Mode: Multi-Sample | Sample Plate: {plate_name}"
        
        config_label = ttk.Label(
            self.config_display_frame,
            text=config_text,
            font=("Arial", 14, "bold"),
            foreground="navy"
        )
        config_label.pack(anchor=tk.CENTER, pady=5)
        
        # Add pattern selection panel
        self._create_pattern_selection_panel()
    
    def _create_pattern_selection_panel(self):
        """Create a panel with four pattern selection buttons."""
        # Create pattern selection frame
        if not hasattr(self, 'pattern_selection_frame'):
            self.pattern_selection_frame = None
            
        if self.pattern_selection_frame:
            self.pattern_selection_frame.destroy()
        
        self.pattern_selection_frame = ttk.LabelFrame(
            self.plate_frame,
            text="Pattern Selection",
            padding="10"
        )
        self.pattern_selection_frame.pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # Create a grid layout for the four buttons (2x2)
        button_frame = ttk.Frame(self.pattern_selection_frame)
        button_frame.pack(expand=True)
        
        # Configure grid weights for even distribution
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        
        # Upper Left Button (odd rows, odd columns)
        self.upper_left_button = tk.Button(
            button_frame,
            text="Upper Left\n(Odd Rows, Odd Cols)",
            command=self._on_pattern_upper_left,
            font=("Arial", 10),
            padx=10,
            pady=8,
            bg="#E8F4FD",
            relief="raised",
            borderwidth=2
        )
        self.upper_left_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Upper Right Button (odd rows, even columns)
        self.upper_right_button = tk.Button(
            button_frame,
            text="Upper Right\n(Odd Rows, Even Cols)",
            command=self._on_pattern_upper_right,
            font=("Arial", 10),
            padx=10,
            pady=8,
            bg="#FDF4E8",
            relief="raised",
            borderwidth=2
        )
        self.upper_right_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # Lower Left Button (even rows, odd columns)
        self.lower_left_button = tk.Button(
            button_frame,
            text="Lower Left\n(Even Rows, Odd Cols)",
            command=self._on_pattern_lower_left,
            font=("Arial", 10),
            padx=10,
            pady=8,
            bg="#F4E8FD",
            relief="raised",
            borderwidth=2
        )
        self.lower_left_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Lower Right Button (even rows, even columns)
        self.lower_right_button = tk.Button(
            button_frame,
            text="Lower Right\n(Even Rows, Even Cols)",
            command=self._on_pattern_lower_right,
            font=("Arial", 10),
            padx=10,
            pady=8,
            bg="#E8FDF4",
            relief="raised",
            borderwidth=2
        )
        self.lower_right_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # Add instruction label
        instruction_label = ttk.Label(
            self.pattern_selection_frame,
            text="Click a pattern button to automatically select wells in that pattern",
            font=("Arial", 9),
            foreground="gray"
        )
        instruction_label.pack(pady=(5, 0))
    
    def _on_pattern_upper_left(self):
        """Handle upper left pattern button click."""
        if self.plate_canvas:
            self.plate_canvas.select_pattern_upper_left()
            print("Selected upper left pattern (odd rows, odd columns)")
    
    def _on_pattern_lower_left(self):
        """Handle lower left pattern button click."""
        if self.plate_canvas:
            self.plate_canvas.select_pattern_lower_left()
            print("Selected lower left pattern (even rows, odd columns)")
    
    def _on_pattern_upper_right(self):
        """Handle upper right pattern button click."""
        if self.plate_canvas:
            self.plate_canvas.select_pattern_upper_right()
            print("Selected upper right pattern (odd rows, even columns)")
    
    def _on_pattern_lower_right(self):
        """Handle lower right pattern button click."""
        if self.plate_canvas:
            self.plate_canvas.select_pattern_lower_right()
            print("Selected lower right pattern (even rows, even columns)")
    
    def _setup_well_selection_integration(self):
        """Setup integration between plate canvas, metadata panel, and legend panel."""
        # Connect metadata panel to plate canvas for applying metadata
        if self.plate_canvas and self.metadata_panel:
            # Wrap the apply metadata callback to also update legend
            def apply_metadata_with_legend_update(metadata):
                self.plate_canvas.apply_metadata_to_selection(metadata)
                # Update legend after metadata is applied
                self._update_legend()
            
            self.metadata_panel.set_apply_metadata_callback(apply_metadata_with_legend_update)
            
            # Wrap the clear all metadata callback to also clear legend
            def clear_all_metadata_with_legend_update():
                self.plate_canvas.clear_all_metadata()
                # Clear legend after metadata is cleared
                if self.legend_panel:
                    self.legend_panel.clear_legend()
            
            self.metadata_panel.set_clear_all_metadata_callback(clear_all_metadata_with_legend_update)
            
            # Set up CSV export callback
            self.metadata_panel.set_export_csv_callback(self._export_csv)
            
            # Set up image export callback
            self.metadata_panel.set_export_image_callback(self._export_image)
            
            # Set up exit callback
            self.metadata_panel.set_exit_callback(self._exit_application)
            
            # Set up well selection callback for logging and UI updates
            def on_well_selection_changed(selected_wells):
                print(f"Wells selected: {selected_wells}")
                # Enable/disable apply button based on selection
                if hasattr(self.metadata_panel, 'apply_button'):
                    if selected_wells:
                        self.metadata_panel.apply_button.configure(state='normal')
                    else:
                        self.metadata_panel.apply_button.configure(state='disabled')
                
                # Enable/disable export button based on whether plate has metadata
                if hasattr(self.metadata_panel, 'export_csv_button'):
                    has_metadata = bool(self.plate_canvas.well_metadata)
                    if has_metadata:
                        self.metadata_panel.export_csv_button.configure(state='normal')
                    else:
                        self.metadata_panel.export_csv_button.configure(state='disabled')
            
            # Connect the callback to the plate canvas
            self.plate_canvas.set_selection_callback(on_well_selection_changed)
            
            # Initial state for export button
            if hasattr(self.metadata_panel, 'export_csv_button'):
                has_metadata = bool(self.plate_canvas.well_metadata)
                if has_metadata:
                    self.metadata_panel.export_csv_button.configure(state='normal')
                else:
                    self.metadata_panel.export_csv_button.configure(state='disabled')
    
    def _update_legend(self):
        """Update the legend panel with current color and pattern mappings."""
        if self.legend_panel and self.plate_canvas:
            self.legend_panel.update_legend(
                self.plate_canvas.group1_colors,
                self.plate_canvas.group2_patterns
            )
    
    def _export_csv(self):
        """Export plate layout to CSV file with file dialog."""
        try:
            # Validate that we have data to export
            if not self.plate_canvas or not self.plate_canvas.well_metadata:
                messagebox.showwarning(
                    "Export Warning",
                    "No metadata found on plate. Please add metadata to wells before exporting."
                )
                return None
            
            # Get default filename based on plate name
            default_filename = self._get_default_export_filename()
            
            # Show file save dialog
            filename = filedialog.asksaveasfilename(
                title="Export Plate Layout",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_filename,
                initialdir=self.project_directory
            )
            
            if not filename:  # User cancelled
                return None
            
            # Perform the export
            exported_file = export_plate_layout(self.plate_canvas, self, filename)
            
            # Show success message
            messagebox.showinfo(
                "Export Successful",
                f"Plate layout exported successfully to:\n{exported_file}"
            )
            
            logger.info(f"CSV export completed: {exported_file}")
            return exported_file  # Return the filename for image export
            
        except CSVExportError as e:
            logger.error(f"CSV export error: {e}")
            messagebox.showerror("Export Error", str(e))
            return None
        except Exception as e:
            logger.error(f"Unexpected export error: {e}")
            messagebox.showerror("Export Error", f"An unexpected error occurred: {str(e)}")
            return None
    
    def _get_default_export_filename(self) -> str:
        """
        Generate default filename for CSV export based on plate configuration.
        
        Returns:
            str: Default filename for CSV export
        """
        # Get plate name from configuration
        if self.sample_mode == "single" and self.single_sample_config:
            plate_name = self.single_sample_config.get('plate_name', 'plate')
        elif self.sample_mode == "multi" and self.multi_sample_config:
            plate_name = self.multi_sample_config.get('sample_plate_name', 'plate')
        else:
            plate_name = f"plate_{self.plate_type}well"
        
        # Sanitize filename
        import re
        safe_name = re.sub(r'[^\w\-_.]', '_', plate_name)
        
        # Ensure .csv extension
        if not safe_name.lower().endswith('.csv'):
            safe_name += '.csv'
        
        return safe_name
    
    def _export_image(self, filename: str) -> bool:
        """
        Export plate layout and legend as image file.
        
        Args:
            filename: Target file path for the exported image
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            from ..utils.image_export import ImageExporter
            
            # Validate that we have components to export
            if not self.plate_canvas or not self.legend_panel:
                logger.error("Missing plate canvas or legend panel for image export")
                return False
            
            # Create image exporter and perform export
            # Pass the actual canvas widget, not the PlateCanvas wrapper
            exporter = ImageExporter()
            success = exporter.capture_plate_and_legend(
                self.plate_canvas.canvas,  # Use the actual tkinter Canvas widget
                self.legend_panel,
                filename
            )
            
            if success:
                logger.info(f"Image export completed successfully: {filename}")
            else:
                logger.error(f"Image export failed: {filename}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error during image export: {e}")
            return False
    
    def _exit_application(self) -> None:
        """
        Exit the application cleanly.
        
        Performs any necessary cleanup before closing the application.
        """
        try:
            logger.info("Exiting application...")
            
            # Perform any cleanup here if needed
            # For example: save settings, close database connections, etc.
            
            # Close the main window and terminate the Python process
            self.quit()
            self.destroy()
            import os
            os._exit(0)  # Force exit the Python process
            
        except Exception as e:
            logger.error(f"Error during application exit: {e}")
            # Force quit even if there's an error
            import os
            os._exit(1)