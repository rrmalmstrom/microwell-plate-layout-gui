"""
Main window GUI component for the microwell plate application.

Context7 Reference: Tkinter application architecture patterns and main window setup
- Using tkinter.Tk for main application root
- Using ttk.Panedwindow for split layout design  
- Following standard widget configuration patterns
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .metadata_panel import MetadataPanel
from .plate_canvas import PlateCanvas
from .legend_panel import LegendPanel
from ..data.database import DatabaseManager


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
        self.plate_type_var = tk.StringVar(value="96")
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


class MainWindow:
    """
    Main application window with split layout design.
    
    Context7 Reference: 
    - tkinter.Tk application root setup
    - ttk.Panedwindow for split layout
    - Standard widget configuration patterns
    """
    
    def __init__(self, root: tk.Tk, db_path: str = "example_database.db"):
        """
        Initialize main window.
        
        Args:
            root: Tkinter root window
            db_path: Path to SQLite database file
        """
        self.root = root
        self.plate_type = None
        self.sample_mode = None
        self.db_path = db_path
        
        # Initialize database manager
        self.db_manager = DatabaseManager(db_path)
        
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
        # Context7 Reference: ttk.Panedwindow for split layout
        self.paned_window = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create frames for each panel
        self.plate_frame = ttk.Frame(self.paned_window)
        self.right_panel_frame = ttk.Frame(self.paned_window)
        
        # Add frames to paned window - plate gets more space
        self.paned_window.add(self.plate_frame, weight=2)
        self.paned_window.add(self.right_panel_frame, weight=1)
        
        # Create vertical paned window for right panel (metadata + legend)
        self.right_paned_window = ttk.Panedwindow(self.right_panel_frame, orient=tk.VERTICAL)
        self.right_paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for metadata and legend
        self.metadata_frame = ttk.Frame(self.right_paned_window)
        self.legend_frame = ttk.Frame(self.right_paned_window)
        
        # Add frames to right paned window - give legend more space
        self.right_paned_window.add(self.metadata_frame, weight=3)
        self.right_paned_window.add(self.legend_frame, weight=2)
        
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
        Show startup dialog for plate configuration.
        
        Returns:
            True if user selected configuration, False if cancelled
        """
        dialog = StartupDialog(self.root)
        result = dialog.show()
        
        if result:
            self.plate_type = result['plate_type']
            self.sample_mode = result['sample_mode']
            return True
        return False
        
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
        
        # Create plate canvas now that we know the plate type
        self._create_plate_canvas()
    
    def _create_plate_canvas(self):
        """Create the plate canvas with the selected plate type."""
        if self.plate_type:
            # Remove placeholder
            if hasattr(self, 'plate_canvas_placeholder'):
                self.plate_canvas_placeholder.destroy()
            
            # Create plate canvas
            plate_type_str = f"{self.plate_type}-well"
            self.plate_canvas = PlateCanvas(self.plate_frame, plate_type_str)
            
            # Pack the canvas to make it visible
            self.plate_canvas.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Connect plate canvas to metadata panel for well selection
            self._setup_well_selection_integration()
    
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
            
            # Set up well selection callback for logging and UI updates
            def on_well_selection_changed(selected_wells):
                print(f"Wells selected: {selected_wells}")
                # Enable/disable apply button based on selection
                if hasattr(self.metadata_panel, 'apply_button'):
                    if selected_wells:
                        self.metadata_panel.apply_button.configure(state='normal')
                    else:
                        self.metadata_panel.apply_button.configure(state='disabled')
            
            # Connect the callback to the plate canvas
            self.plate_canvas.set_selection_callback(on_well_selection_changed)
    
    def _update_legend(self):
        """Update the legend panel with current color and pattern mappings."""
        if self.legend_panel and self.plate_canvas:
            self.legend_panel.update_legend(
                self.plate_canvas.group1_colors,
                self.plate_canvas.group2_patterns
            )