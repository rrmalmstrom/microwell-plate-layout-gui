"""
Plate Canvas Component for Microwell Plate GUI

This module provides the PlateCanvas class for rendering interactive microwell plates
with support for 96-well and 384-well formats, well selection, and visual feedback.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Tuple, Optional, Set, Callable
import math


class PlateCanvas:
    """
    Interactive canvas widget for displaying and selecting wells in microwell plates.
    
    Supports both 96-well (8x12) and 384-well (16x24) plate formats with:
    - Visual well grid rendering
    - Mouse-based well selection
    - Coordinate-based well naming (A1, B2, etc.)
    - Selection state management
    - Customizable well colors and sizes
    """
    
    def __init__(self, parent: tk.Widget, plate_type: str = "96-well", 
                 well_size: int = 20, well_spacing: int = 5):
        """
        Initialize the PlateCanvas.
        
        Args:
            parent: Parent tkinter widget
            plate_type: Either "96-well" or "384-well"
            well_size: Diameter of each well in pixels
            well_spacing: Spacing between wells in pixels
        """
        self.parent = parent
        self.plate_type = plate_type
        self.well_size = well_size
        self.well_spacing = well_spacing
        
        # Plate dimensions
        if plate_type in ["96-well", "96"]:
            self.rows = 8
            self.cols = 12
        elif plate_type in ["384-well", "384"]:
            self.rows = 16
            self.cols = 24
        else:
            raise ValueError(f"Unsupported plate type: {plate_type}")
        
        # Calculate canvas dimensions
        self.canvas_width = (self.cols * (well_size + well_spacing)) + well_spacing + 60  # Extra for labels
        self.canvas_height = (self.rows * (well_size + well_spacing)) + well_spacing + 60  # Extra for labels
        
        # Create canvas
        self.canvas = tk.Canvas(
            parent,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='white',
            relief='sunken',
            borderwidth=2
        )
        
        # Well management
        self.wells: Dict[str, Dict] = {}  # well_name -> {canvas_id, x, y, selected, ...}
        self.well_items: Dict[str, int] = {}  # well_name -> canvas_id (for test compatibility)
        self.selected_wells: Set[str] = set()
        self.well_metadata: Dict[str, Dict] = {}  # well_name -> metadata
        
        # Visual settings
        self.default_well_color = 'lightgray'
        self.selection_color = 'lightblue'
        
        # Sample type outline colors (ring around wells)
        self.sample_type_outline_colors = {
            "sample": "#228B22",      # Forest green outline for sample wells
            "neg_cntrl": "#DC143C",   # Crimson outline for negative controls
            "pos_cntrl": "#4169E1",   # Royal blue outline for positive controls
            "unused": "#696969"       # Dim gray outline for unused wells
        }
        
        # Dynamic color and pattern mappings
        self.group1_colors = {}       # Maps Group 1 values to colors
        self.group2_patterns = {}     # Maps Group 2 values to stipple patterns
        
        # Available colors for Group 1 values (distinct, colorblind-friendly)
        self.available_colors = [
            "#FF6B6B",  # Red
            "#4ECDC4",  # Teal
            "#45B7D1",  # Blue
            "#96CEB4",  # Green
            "#FFEAA7",  # Yellow
            "#DDA0DD",  # Plum
            "#98D8C8",  # Mint
            "#F7DC6F",  # Light Yellow
            "#BB8FCE",  # Light Purple
            "#85C1E9",  # Light Blue
            "#F8C471",  # Orange
            "#82E0AA"   # Light Green
        ]
        
        # Available visual patterns for Group 2 values (using overlay shapes)
        self.available_patterns = [
            "dots",       # Small dots overlay
            "lines",      # Diagonal lines overlay
            "cross",      # Cross pattern overlay
            "grid",       # Grid pattern overlay
            "circles",    # Small circles overlay
            "squares",    # Small squares overlay
            "triangles",  # Small triangles overlay
            "stars",      # Star pattern overlay
            "diamond",    # Diamond pattern overlay
            "zigzag",     # Zigzag lines overlay
        ]
        
        self.color_index = 0
        self.pattern_index = 0
        
        # Mouse event tracking
        self.drag_start: Optional[Tuple[int, int]] = None
        self.is_dragging = False
        self.drag_rectangle: Optional[int] = None
        
        # Callbacks
        self.selection_callback: Optional[Callable[[Set[str]], None]] = None
        
        # Initialize the plate
        self._create_wells()
        self._bind_events()
    
    def _create_wells(self) -> None:
        """Create all wells on the canvas with proper positioning and labels."""
        # Clear existing wells
        self.canvas.delete("all")
        self.wells.clear()
        
        # Starting positions (offset for labels)
        start_x = 40
        start_y = 40
        
        # Create column labels (1, 2, 3, ...)
        for col in range(self.cols):
            x = start_x + (col * (self.well_size + self.well_spacing)) + (self.well_size // 2)
            y = 20
            self.canvas.create_text(x, y, text=str(col + 1), font=("Arial", 8))
        
        # Create row labels (A, B, C, ...)
        for row in range(self.rows):
            x = 20
            y = start_y + (row * (self.well_size + self.well_spacing)) + (self.well_size // 2)
            row_letter = chr(ord('A') + row)
            self.canvas.create_text(x, y, text=row_letter, font=("Arial", 8))
        
        # Create wells
        for row in range(self.rows):
            row_letter = chr(ord('A') + row)
            for col in range(self.cols):
                col_number = col + 1
                well_name = f"{row_letter}{col_number}"
                
                # Calculate well position
                x = start_x + (col * (self.well_size + self.well_spacing))
                y = start_y + (row * (self.well_size + self.well_spacing))
                
                # Create well circle
                canvas_id = self.canvas.create_oval(
                    x, y,
                    x + self.well_size, y + self.well_size,
                    fill=self.default_well_color,
                    outline='black',
                    width=1,
                    tags=("well", well_name)
                )
                
                # Store well information
                self.wells[well_name] = {
                    'name': well_name,
                    'canvas_id': canvas_id,
                    'x': x,
                    'y': y,
                    'center_x': x + (self.well_size // 2),
                    'center_y': y + (self.well_size // 2),
                    'selected': False,
                    'row': row,
                    'col': col
                }
                
                # Store for test compatibility
                self.well_items[well_name] = canvas_id
    
    def _bind_events(self) -> None:
        """Bind mouse events for well selection using Context7 Canvas documentation."""
        # Context7 Reference: Canvas widget event binding
        # Bind events to the canvas widget itself for general mouse interaction
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Motion>", self._on_hover)
        
        # Context7 Reference: tag_bind for item-specific events
        # Bind events to well items using tags for more precise interaction
        self.canvas.tag_bind("well", "<Button-1>", self._on_well_click)
        self.canvas.tag_bind("well", "<Enter>", self._on_well_enter)
        self.canvas.tag_bind("well", "<Leave>", self._on_well_leave)
    
    def _on_click(self, event: tk.Event) -> None:
        """Handle mouse click events."""
        self.drag_start = (event.x, event.y)
        self.is_dragging = False
        
        # Find clicked well
        well_name = self._get_well_at_position(event.x, event.y)
        if well_name:
            self._toggle_well_selection(well_name)
    
    def _on_drag(self, event: tk.Event) -> None:
        """Handle mouse drag events for multi-well selection."""
        if self.drag_start is None:
            return
        
        # Check if we've moved enough to start dragging
        dx = abs(event.x - self.drag_start[0])
        dy = abs(event.y - self.drag_start[1])
        
        if not self.is_dragging and (dx > 5 or dy > 5):
            self.is_dragging = True
        
        if self.is_dragging:
            # Select all wells in drag rectangle
            self._select_wells_in_rectangle(
                self.drag_start[0], self.drag_start[1],
                event.x, event.y
            )
    
    def _on_release(self, event: tk.Event) -> None:
        """Handle mouse release events."""
        self.drag_start = None
        self.is_dragging = False
        
        # Notify callback of selection change
        if self.selection_callback:
            self.selection_callback(self.selected_wells.copy())
    
    def _on_hover(self, event: tk.Event) -> None:
        """Handle mouse hover events for visual feedback."""
        well_name = self._get_well_at_position(event.x, event.y)
        
        # Update cursor
        if well_name:
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="")
    
    def _on_well_click(self, event: tk.Event) -> None:
        """Handle clicks specifically on well items using Context7 tag_bind."""
        # Context7 Reference: event.widget.gettags(event.item) for item identification
        if hasattr(event, 'item') and event.item:
            tags = self.canvas.gettags(event.item)
            # Find well name from tags
            well_name = None
            for tag in tags:
                if tag != "well" and tag in self.wells:
                    well_name = tag
                    break
            
            if well_name:
                self._toggle_well_selection(well_name)
    
    def _on_well_enter(self, event: tk.Event) -> None:
        """Handle mouse entering a well item."""
        self.canvas.config(cursor="hand2")
    
    def _on_well_leave(self, event: tk.Event) -> None:
        """Handle mouse leaving a well item."""
        self.canvas.config(cursor="")
    
    def _get_well_at_position(self, x: int, y: int) -> Optional[str]:
        """
        Get the well name at the given canvas coordinates.
        
        Args:
            x: X coordinate on canvas
            y: Y coordinate on canvas
            
        Returns:
            Well name (e.g., "A1") or None if no well at position
        """
        for well_name, well_info in self.wells.items():
            well_x = well_info['x']
            well_y = well_info['y']
            
            # Check if point is within well circle
            if (well_x <= x <= well_x + self.well_size and
                well_y <= y <= well_y + self.well_size):
                
                # More precise circle check
                center_x = well_info['center_x']
                center_y = well_info['center_y']
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if distance <= self.well_size // 2:
                    return well_name
        
        return None
    
    def _select_wells_in_rectangle(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Select all wells within the given rectangle using Context7 find_overlapping.
        
        Args:
            x1, y1: Top-left corner of rectangle
            x2, y2: Bottom-right corner of rectangle
        """
        # Context7 Reference: canvas.find_overlapping for finding items in region
        # Normalize rectangle coordinates
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        # Clear current selection
        self._clear_selection()
        
        # Use Context7's find_overlapping to get items in the rectangle
        overlapping_items = self.canvas.find_overlapping(min_x, min_y, max_x, max_y)
        
        # Filter for well items and select them
        for item_id in overlapping_items:
            tags = self.canvas.gettags(item_id)
            if "well" in tags:
                # Find the well name from tags
                for tag in tags:
                    if tag != "well" and tag in self.wells:
                        self._select_well(tag)
                        break
    
    def _toggle_well_selection(self, well_name: str) -> None:
        """Toggle the selection state of a well."""
        if well_name in self.selected_wells:
            self._deselect_well(well_name)
        else:
            self._select_well(well_name)
    
    def _select_well(self, well_name: str) -> None:
        """Select a specific well."""
        if well_name not in self.wells:
            return
        
        self.selected_wells.add(well_name)
        self.wells[well_name]['selected'] = True
        
        # Update visual appearance - preserve metadata colors if they exist
        canvas_id = self.wells[well_name]['canvas_id']
        if well_name in self.well_metadata:
            # Well has metadata - keep its colors but add selection indication
            well_info = self.wells[well_name]
            fill_color = well_info.get('fill_color', self.default_well_color)
            outline_color = well_info.get('outline_color', 'black')
            # Remove pattern overlay during selection and add selection indication
            self._remove_pattern_overlay(well_name)
            self.canvas.itemconfig(canvas_id, fill=fill_color, outline='#0000FF', width=4)
        else:
            # Well has no metadata - use selection color
            self.canvas.itemconfig(canvas_id, fill=self.selection_color, outline='#0000FF', width=3)
    
    def _deselect_well(self, well_name: str) -> None:
        """Deselect a specific well."""
        if well_name not in self.wells:
            return
        
        self.selected_wells.discard(well_name)
        self.wells[well_name]['selected'] = False
        
        # Update visual appearance - restore metadata colors if they exist
        canvas_id = self.wells[well_name]['canvas_id']
        if well_name in self.well_metadata:
            # Well has metadata - restore its metadata colors and patterns
            well_info = self.wells[well_name]
            fill_color = well_info.get('fill_color', self.default_well_color)
            outline_color = well_info.get('outline_color', 'black')
            visual_pattern = well_info.get('visual_pattern', '')
            sample_type = well_info.get('sample_type', 'unused')
            outline_width = 3 if sample_type != 'unused' else 2
            self.canvas.itemconfig(canvas_id, fill=fill_color, outline=outline_color, width=outline_width)
            
            # Restore pattern overlay if it exists
            if visual_pattern:
                self._add_pattern_overlay(well_name, visual_pattern)
        else:
            # Well has no metadata - use default color
            self.canvas.itemconfig(canvas_id, fill=self.default_well_color, outline='black', width=1)
    
    def _clear_selection(self) -> None:
        """Clear all well selections."""
        for well_name in list(self.selected_wells):
            self._deselect_well(well_name)
    
    def get_selected_wells(self) -> Set[str]:
        """
        Get the set of currently selected wells.
        
        Returns:
            Set of well names (e.g., {"A1", "B2", "C3"})
        """
        return self.selected_wells.copy()
    
    def set_selected_wells(self, well_names: Set[str]) -> None:
        """
        Set the selection to the specified wells.
        
        Args:
            well_names: Set of well names to select
        """
        self._clear_selection()
        for well_name in well_names:
            if well_name in self.wells:
                self._select_well(well_name)
    
    def clear_selection(self) -> None:
        """Clear all well selections."""
        self._clear_selection()
        
        # Notify callback
        if self.selection_callback:
            self.selection_callback(set())
    
    def set_selection_callback(self, callback: Callable[[Set[str]], None]) -> None:
        """
        Set a callback function to be called when well selection changes.
        
        Args:
            callback: Function that takes a set of selected well names
        """
        self.selection_callback = callback
    
    def get_well_coordinates(self, well_name: str) -> Optional[Tuple[int, int]]:
        """
        Get the row and column coordinates for a well.
        
        Args:
            well_name: Well name (e.g., "A1")
            
        Returns:
            Tuple of (row, col) or None if well doesn't exist
        """
        if well_name not in self.wells:
            return None
        
        well_info = self.wells[well_name]
        return (well_info['row'], well_info['col'])
    
    def get_well_name(self, row: int, col: int) -> Optional[str]:
        """
        Get the well name for given row and column coordinates.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            Well name (e.g., "A1") or None if coordinates are invalid
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return None
        
        row_letter = chr(ord('A') + row)
        col_number = col + 1
        return f"{row_letter}{col_number}"
    
    def pack(self, **kwargs) -> None:
        """Pack the canvas widget."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs) -> None:
        """Grid the canvas widget."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs) -> None:
        """Place the canvas widget."""
        self.canvas.place(**kwargs)
    
    # Additional methods expected by tests
    def get_well_by_name(self, well_name: str) -> Optional[Dict]:
        """
        Get well information by well name.
        
        Args:
            well_name: Well name (e.g., "A1")
            
        Returns:
            Well information dictionary or None if not found
        """
        return self.wells.get(well_name)
    
    def select_well(self, well_name: str) -> None:
        """
        Select a specific well (public interface).
        
        Args:
            well_name: Well name to select
        """
        self._select_well(well_name)
    
    def deselect_well(self, well_name: str) -> None:
        """
        Deselect a specific well (public interface).
        
        Args:
            well_name: Well name to deselect
        """
        self._deselect_well(well_name)
    
    def select_rectangle(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Select wells within a rectangular area (public interface).
        
        Args:
            x1, y1: Top-left corner coordinates
            x2, y2: Bottom-right corner coordinates
        """
        self._select_wells_in_rectangle(x1, y1, x2, y2)
    
    def on_well_click(self, event: tk.Event) -> None:
        """
        Handle well click events (public interface).
        
        Args:
            event: Tkinter event object
        """
        self._on_click(event)
    
    def on_mouse_drag(self, event: tk.Event) -> None:
        """
        Handle mouse drag events (public interface).
        
        Args:
            event: Tkinter event object
        """
        self._on_drag(event)
    
    def row_letter_to_index(self, row_letter: str) -> int:
        """
        Convert row letter to zero-based index.
        
        Args:
            row_letter: Row letter (A, B, C, etc.)
            
        Returns:
            Zero-based row index
        """
        return ord(row_letter.upper()) - ord('A')
    
    def index_to_row_letter(self, row_index: int) -> str:
        """
        Convert zero-based row index to row letter.
        
        Args:
            row_index: Zero-based row index
            
        Returns:
            Row letter (A, B, C, etc.)
        """
        return chr(ord('A') + row_index)
    
    def parse_well_name(self, well_name: str) -> Tuple[int, int]:
        """
        Parse well name into row and column indices.
        
        Args:
            well_name: Well name (e.g., "A1", "H12")
            
        Returns:
            Tuple of (row_index, col_index) both zero-based
        """
        if not well_name or len(well_name) < 2:
            raise ValueError(f"Invalid well name: {well_name}")
        
        row_letter = well_name[0].upper()
        col_str = well_name[1:]
        
        try:
            row_index = self.row_letter_to_index(row_letter)
            col_index = int(col_str) - 1  # Convert to zero-based
            return (row_index, col_index)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid well name: {well_name}") from e
    
    def pixel_to_well(self, x: int, y: int) -> Optional[str]:
        """
        Convert pixel coordinates to well name (public interface).
        
        Args:
            x: X coordinate on canvas
            y: Y coordinate on canvas
            
        Returns:
            Well name or None if no well at position
        """
        return self._get_well_at_position(x, y)
    
    # Well Selection Methods (Required by tests)
    
    def _get_well_center(self, row: int, col: int) -> Tuple[int, int]:
        """
        Get the center coordinates of a well by row/col indices.
        
        Args:
            row: Zero-based row index
            col: Zero-based column index
            
        Returns:
            Tuple of (center_x, center_y) coordinates
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError(f"Invalid well position: row={row}, col={col}")
        
        well_name = f"{chr(ord('A') + row)}{col + 1}"
        if well_name in self.wells:
            well_info = self.wells[well_name]
            return (well_info['center_x'], well_info['center_y'])
        else:
            # Calculate if well info not available
            start_x = 40
            start_y = 40
            x = start_x + (col * (self.well_size + self.well_spacing)) + (self.well_size // 2)
            y = start_y + (row * (self.well_size + self.well_spacing)) + (self.well_size // 2)
            return (x, y)
    
    def select_wells(self, well_names: Set[str]) -> None:
        """
        Select a set of wells and update visual feedback.
        
        Args:
            well_names: Set of well names to select
        """
        # Clear current selection without triggering callback
        for well_name in list(self.selected_wells):
            if well_name in self.wells:
                self.wells[well_name]['selected'] = False
                canvas_id = self.wells[well_name]['canvas_id']
                self.canvas.itemconfig(canvas_id, fill=self.default_well_color)
        self.selected_wells.clear()
        
        # Select new wells
        for well_name in well_names:
            if well_name in self.wells:
                self.wells[well_name]['selected'] = True
                self.selected_wells.add(well_name)
                # Update visual feedback
                canvas_id = self.wells[well_name]['canvas_id']
                self.canvas.itemconfig(canvas_id, fill=self.selection_color)
        
        # Trigger callback once for the final state
        if self.selection_callback:
            self.selection_callback(self.selected_wells.copy())
    
    def has_selection(self) -> bool:
        """
        Check if any wells are currently selected.
        
        Returns:
            True if wells are selected, False otherwise
        """
        return len(self.selected_wells) > 0
    
    def get_selected_count(self) -> int:
        """
        Get the number of currently selected wells.
        
        Returns:
            Number of selected wells
        """
        return len(self.selected_wells)
    
    def add_to_selection(self, well_names: Set[str]) -> None:
        """
        Add wells to the current selection.
        
        Args:
            well_names: Set of well names to add to selection
        """
        for well_name in well_names:
            if well_name in self.wells and well_name not in self.selected_wells:
                self.wells[well_name]['selected'] = True
                self.selected_wells.add(well_name)
                # Update visual feedback
                canvas_id = self.wells[well_name]['canvas_id']
                self.canvas.itemconfig(canvas_id, fill=self.selection_color)
        
        # Trigger callback
        if self.selection_callback:
            self.selection_callback(self.selected_wells.copy())
    
    def remove_from_selection(self, well_names: Set[str]) -> None:
        """
        Remove wells from the current selection.
        
        Args:
            well_names: Set of well names to remove from selection
        """
        for well_name in well_names:
            if well_name in self.selected_wells:
                self.wells[well_name]['selected'] = False
                self.selected_wells.remove(well_name)
                # Update visual feedback
                canvas_id = self.wells[well_name]['canvas_id']
                self.canvas.itemconfig(canvas_id, fill=self.default_well_color)
        
        # Trigger callback
        if self.selection_callback:
            self.selection_callback(self.selected_wells.copy())
    
    def toggle_well_selection(self, well_name: str) -> None:
        """
        Toggle the selection state of a single well.
        
        Args:
            well_name: Name of well to toggle
        """
        if well_name in self.selected_wells:
            self.remove_from_selection({well_name})
        else:
            self.add_to_selection({well_name})
    
    def _start_drag_selection(self, x: int, y: int) -> None:
        """
        Start a rectangular drag selection.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        self.drag_start = (x, y)
        self.is_dragging = True
        
        # Create visual drag rectangle
        self.drag_rectangle = self.canvas.create_rectangle(
            x, y, x, y,
            outline='blue',
            width=2,
            fill='lightblue',
            stipple='gray25'
        )
    
    def _update_drag_selection(self, x: int, y: int) -> None:
        """
        Update the drag selection rectangle.
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
        """
        if self.is_dragging and self.drag_start and self.drag_rectangle:
            start_x, start_y = self.drag_start
            # Update rectangle coordinates
            self.canvas.coords(self.drag_rectangle, start_x, start_y, x, y)
    
    def _end_drag_selection(self, x: int, y: int) -> None:
        """
        End the drag selection and select wells in the rectangle.
        
        Args:
            x: Ending x coordinate
            y: Ending y coordinate
        """
        if self.is_dragging and self.drag_start:
            start_x, start_y = self.drag_start
            
            # Select wells in rectangle
            self._select_wells_in_rectangle(start_x, start_y, x, y)
            
            # Clean up drag state
            if self.drag_rectangle:
                self.canvas.delete(self.drag_rectangle)
                self.drag_rectangle = None
            
            self.drag_start = None
            self.is_dragging = False
    
    def apply_metadata_to_selection(self, metadata: Dict) -> None:
        """
        Apply metadata to all currently selected wells and update their colors.
        
        Args:
            metadata: Dictionary of metadata to apply
        """
        selected_wells_copy = self.selected_wells.copy()
        
        for well_name in selected_wells_copy:
            # Store metadata
            self.well_metadata[well_name] = metadata.copy()
            
            # Update well color based on sample type
            sample_type = metadata.get('sample_type', 'sample')
            self._update_well_color(well_name, sample_type)
        
        # Clear selection to show the color change immediately
        self.clear_selection()
        
        # Log the metadata application
        print(f"Applied metadata to {len(selected_wells_copy)} wells: {metadata}")
    
    def _update_well_color(self, well_name: str, sample_type: str) -> None:
        """
        Update well visualization using value-based color and texture system:
        - Outline color = Sample type
        - Fill color = Group 1 value (each unique value gets different color)
        - Fill pattern = Group 2 value (each unique value gets different stipple)
        - Group 3 = Stored but not displayed
        
        Args:
            well_name: Name of the well (e.g., 'A1')
            sample_type: Type of sample ('sample', 'neg_cntrl', 'pos_cntrl', 'unused')
        """
        if well_name not in self.wells:
            return
            
        well_info = self.wells[well_name]
        canvas_id = well_info['canvas_id']
        metadata = self.well_metadata.get(well_name, {})
        
        # Get outline color for sample type
        outline_color = self.sample_type_outline_colors.get(sample_type, self.sample_type_outline_colors["unused"])
        outline_width = 3 if sample_type != 'unused' else 2
        
        # Get Group 1 and Group 2 values
        group1_value = metadata.get('group1', '').strip()
        group2_value = metadata.get('group2', '').strip()
        group3_value = metadata.get('group3', '').strip()  # Store but don't display
        
        # Determine fill color based on Group 1 value
        if group1_value:
            if group1_value not in self.group1_colors:
                # Assign new color to this Group 1 value
                color_idx = self.color_index % len(self.available_colors)
                self.group1_colors[group1_value] = self.available_colors[color_idx]
                self.color_index += 1
            fill_color = self.group1_colors[group1_value]
        else:
            fill_color = self.default_well_color
        
        # Determine visual pattern based on Group 2 value
        if group2_value:
            if group2_value not in self.group2_patterns:
                # Assign new pattern to this Group 2 value
                pattern_idx = self.pattern_index % len(self.available_patterns)
                self.group2_patterns[group2_value] = self.available_patterns[pattern_idx]
                self.pattern_index += 1
            visual_pattern = self.group2_patterns[group2_value]
        else:
            visual_pattern = ""  # No pattern (solid fill)
        
        # Apply colors to the well (remove old pattern overlays first)
        self._remove_pattern_overlay(well_name)
        
        if well_name in self.selected_wells:
            # For selected wells, use selection color but keep the outline
            self.canvas.itemconfig(canvas_id,
                                 fill=self.selection_color,
                                 outline=outline_color,
                                 width=outline_width)
        else:
            # For unselected wells, use the value-based colors
            self.canvas.itemconfig(canvas_id,
                                 fill=fill_color,
                                 outline=outline_color,
                                 width=outline_width)
        
        # Add visual pattern overlay if Group 2 value exists
        if visual_pattern and well_name not in self.selected_wells:
            self._add_pattern_overlay(well_name, visual_pattern)
            
        # Update the well's stored info
        self.wells[well_name]['outline_color'] = outline_color
        self.wells[well_name]['sample_type'] = sample_type
        self.wells[well_name]['group1_value'] = group1_value
        self.wells[well_name]['group2_value'] = group2_value
        self.wells[well_name]['group3_value'] = group3_value
        self.wells[well_name]['fill_color'] = fill_color
        self.wells[well_name]['visual_pattern'] = visual_pattern
    
    def _determine_group_level(self, metadata: Dict) -> str:
        """
        Determine the primary group level from metadata.
        Priority: Group 1 > Group 2 > Group 3 > none
        
        Args:
            metadata: Well metadata dictionary
            
        Returns:
            Group level string ('group1', 'group2', 'group3', or 'none')
        """
        if metadata.get('group1', '').strip():
            return 'group1'
        elif metadata.get('group2', '').strip():
            return 'group2'
        elif metadata.get('group3', '').strip():
            return 'group3'
        else:
            return 'none'
    
    def get_well_metadata(self, well_name: str) -> Optional[Dict]:
        """
        Get metadata for a specific well.
        
        Args:
            well_name: Name of the well
            
        Returns:
            Metadata dictionary or None if no metadata
        """
        return self.well_metadata.get(well_name)
    
    def clear_all_metadata(self) -> None:
        """
        Clear all metadata from all wells and reset their colors to default.
        """
        # Clear metadata storage
        self.well_metadata.clear()
        
        # Clear dynamic color and pattern mappings
        self.group1_colors.clear()
        self.group2_patterns.clear()
        self.color_index = 0
        self.pattern_index = 0
        
        # Reset all well colors to default and remove pattern overlays
        for well_name, well_info in self.wells.items():
            canvas_id = well_info['canvas_id']
            
            # Remove any pattern overlays
            self._remove_pattern_overlay(well_name)
            
            # Reset to default well appearance
            if well_name in self.selected_wells:
                # If well is selected, use selection color
                self.canvas.itemconfig(canvas_id,
                                     fill=self.selection_color,
                                     outline=self.selection_color,
                                     width=2)
            else:
                # Use default colors (unused sample type, no groups)
                self.canvas.itemconfig(canvas_id,
                                     fill=self.default_well_color,  # Default fill
                                     outline=self.sample_type_outline_colors["unused"],  # Default outline
                                     width=1)
            
            # Clear stored metadata attributes
            attributes_to_clear = ['fill_color', 'outline_color', 'sample_type', 'group_level',
                                 'group1_value', 'group2_value', 'group3_value', 'metadata_color',
                                 'visual_pattern', 'pattern_overlays']
            for attr in attributes_to_clear:
                if attr in well_info:
                    del well_info[attr]
        
        print("Cleared all metadata from plate")
    
    def _add_pattern_overlay(self, well_name: str, pattern_type: str) -> None:
        """
        Add a visual pattern overlay to a well to represent Group 2 values.
        
        Args:
            well_name: Name of the well (e.g., 'A1')
            pattern_type: Type of pattern ('dots', 'lines', 'cross', 'grid')
        """
        if well_name not in self.wells:
            return
            
        well_info = self.wells[well_name]
        x = well_info['x']
        y = well_info['y']
        size = self.well_size
        center_x = well_info['center_x']
        center_y = well_info['center_y']
        
        # Store pattern overlay items for later removal
        if 'pattern_overlays' not in well_info:
            well_info['pattern_overlays'] = []
        
        if pattern_type == "dots":
            # Add small dots
            dot_size = 2
            for dx in [-4, 0, 4]:
                for dy in [-4, 0, 4]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center
                    dot_id = self.canvas.create_oval(
                        center_x + dx - dot_size, center_y + dy - dot_size,
                        center_x + dx + dot_size, center_y + dy + dot_size,
                        fill="black", outline="black"
                    )
                    well_info['pattern_overlays'].append(dot_id)
                    
        elif pattern_type == "lines":
            # Add diagonal lines
            line_id1 = self.canvas.create_line(
                x + 3, y + 3, x + size - 3, y + size - 3,
                fill="black", width=1
            )
            line_id2 = self.canvas.create_line(
                x + 3, y + size - 3, x + size - 3, y + 3,
                fill="black", width=1
            )
            well_info['pattern_overlays'].extend([line_id1, line_id2])
            
        elif pattern_type == "cross":
            # Add cross pattern
            line_id1 = self.canvas.create_line(
                center_x, y + 3, center_x, y + size - 3,
                fill="black", width=2
            )
            line_id2 = self.canvas.create_line(
                x + 3, center_y, x + size - 3, center_y,
                fill="black", width=2
            )
            well_info['pattern_overlays'].extend([line_id1, line_id2])
            
        elif pattern_type == "grid":
            # Add grid pattern
            # Vertical lines
            for offset in [-4, 4]:
                line_id = self.canvas.create_line(
                    center_x + offset, y + 3, center_x + offset, y + size - 3,
                    fill="black", width=1
                )
                well_info['pattern_overlays'].append(line_id)
            # Horizontal lines
            for offset in [-4, 4]:
                line_id = self.canvas.create_line(
                    x + 3, center_y + offset, x + size - 3, center_y + offset,
                    fill="black", width=1
                )
                well_info['pattern_overlays'].append(line_id)
                
        elif pattern_type == "circles":
            # Add small circles
            circle_size = 2
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center
                    circle_id = self.canvas.create_oval(
                        center_x + dx - circle_size, center_y + dy - circle_size,
                        center_x + dx + circle_size, center_y + dy + circle_size,
                        fill="", outline="black", width=2
                    )
                    well_info['pattern_overlays'].append(circle_id)
                    
        elif pattern_type == "squares":
            # Add small squares
            square_size = 2
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center
                    square_id = self.canvas.create_rectangle(
                        center_x + dx - square_size, center_y + dy - square_size,
                        center_x + dx + square_size, center_y + dy + square_size,
                        fill="", outline="black", width=2
                    )
                    well_info['pattern_overlays'].append(square_id)
                    
        elif pattern_type == "triangles":
            # Add small triangles
            for dx in [-5, 5]:
                for dy in [-5, 5]:
                    triangle_id = self.canvas.create_polygon(
                        center_x + dx, center_y + dy - 2,  # Top point
                        center_x + dx - 2, center_y + dy + 2,  # Bottom left
                        center_x + dx + 2, center_y + dy + 2,  # Bottom right
                        fill="", outline="black", width=2
                    )
                    well_info['pattern_overlays'].append(triangle_id)
                    
        elif pattern_type == "stars":
            # Add star pattern (simplified 4-point star)
            star_id = self.canvas.create_polygon(
                center_x, center_y - 6,      # Top
                center_x - 2, center_y - 2,  # Top-left inner
                center_x - 6, center_y,      # Left
                center_x - 2, center_y + 2,  # Bottom-left inner
                center_x, center_y + 6,      # Bottom
                center_x + 2, center_y + 2,  # Bottom-right inner
                center_x + 6, center_y,      # Right
                center_x + 2, center_y - 2,  # Top-right inner
                fill="", outline="black", width=2
            )
            well_info['pattern_overlays'].append(star_id)
            
        elif pattern_type == "diamond":
            # Add diamond pattern
            diamond_id = self.canvas.create_polygon(
                center_x, center_y - 6,      # Top
                center_x - 4, center_y,      # Left
                center_x, center_y + 6,      # Bottom
                center_x + 4, center_y,      # Right
                fill="", outline="black", width=2
            )
            well_info['pattern_overlays'].append(diamond_id)
            
        elif pattern_type == "zigzag":
            # Add zigzag lines
            zigzag_id1 = self.canvas.create_line(
                x + 3, center_y - 3,
                x + 6, center_y + 3,
                x + 9, center_y - 3,
                x + 12, center_y + 3,
                x + 15, center_y - 3,
                x + size - 3, center_y + 3,
                fill="black", width=2
            )
            zigzag_id2 = self.canvas.create_line(
                x + 3, center_y + 3,
                x + 6, center_y - 3,
                x + 9, center_y + 3,
                x + 12, center_y - 3,
                x + 15, center_y + 3,
                x + size - 3, center_y - 3,
                fill="black", width=2
            )
            well_info['pattern_overlays'].extend([zigzag_id1, zigzag_id2])
    
    def _remove_pattern_overlay(self, well_name: str) -> None:
        """
        Remove any existing pattern overlay from a well.
        
        Args:
            well_name: Name of the well (e.g., 'A1')
        """
        if well_name not in self.wells:
            return
            
        well_info = self.wells[well_name]
        if 'pattern_overlays' in well_info:
            for overlay_id in well_info['pattern_overlays']:
                try:
                    self.canvas.delete(overlay_id)
                except tk.TclError:
                    pass  # Item already deleted
            well_info['pattern_overlays'] = []