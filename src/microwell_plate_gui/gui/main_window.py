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
        
        # Center dialog on parent
        self.dialog.transient(parent)
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
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Continue",
            command=self._on_continue
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
    
    def __init__(self, root: tk.Tk):
        """
        Initialize main window.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.plate_type = None
        self.sample_mode = None
        
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
        self.metadata_frame = ttk.Frame(self.paned_window)
        
        # Add frames to paned window with equal weight
        self.paned_window.add(self.plate_frame, weight=1)
        self.paned_window.add(self.metadata_frame, weight=1)
        
        # Add placeholder labels for now
        ttk.Label(
            self.plate_frame,
            text="Plate Visualization Panel\n(Canvas will be implemented in Phase 1.3)",
            font=("Arial", 12),
            anchor=tk.CENTER
        ).pack(expand=True)
        
        ttk.Label(
            self.metadata_frame,
            text="Metadata Entry Panel\n(Forms will be implemented in Phase 2)",
            font=("Arial", 12),
            anchor=tk.CENTER
        ).pack(expand=True)
        
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