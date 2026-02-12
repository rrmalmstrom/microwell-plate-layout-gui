"""
Legend Panel Component for Microwell Plate GUI

This module provides the LegendPanel class for displaying dynamic legends
that show the mapping between metadata values and visual representations.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional


class LegendPanel:
    """
    Dynamic legend panel that shows color and pattern mappings.
    
    Displays:
    - Group 1 values mapped to colors
    - Group 2 values mapped to patterns
    - Sample type outline colors
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the LegendPanel.
        
        Args:
            parent: Parent tkinter widget
        """
        self.parent = parent
        
        # Create main frame
        self.main_frame = ttk.Frame(parent, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Legend",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        # Scrollable frame for legend content - increased height for better visibility
        self.canvas = tk.Canvas(self.main_frame, height=300)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Legend sections
        self.group1_frame = None
        self.group2_frame = None
        self.sample_type_frame = None
        
        # Initialize with sample type legend (always visible)
        self._create_sample_type_legend()
    
    def _create_sample_type_legend(self):
        """Create the sample type legend section."""
        if self.sample_type_frame:
            self.sample_type_frame.destroy()
        
        self.sample_type_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Sample Types (Outline Colors)",
            padding="5"
        )
        self.sample_type_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Sample type colors (from PlateCanvas)
        sample_types = {
            "sample": "#228B22",      # Forest green
            "neg_cntrl": "#DC143C",   # Crimson
            "pos_cntrl": "#4169E1",   # Royal blue
            "unused": "#696969"       # Dim gray
        }
        
        for i, (sample_type, color) in enumerate(sample_types.items()):
            row_frame = ttk.Frame(self.sample_type_frame)
            row_frame.pack(fill=tk.X, pady=1)
            
            # Color indicator (small circle)
            color_canvas = tk.Canvas(row_frame, width=20, height=20, highlightthickness=0)
            color_canvas.pack(side=tk.LEFT, padx=(0, 5))
            color_canvas.create_oval(2, 2, 18, 18, fill="lightgray", outline=color, width=3)
            
            # Label
            label = ttk.Label(row_frame, text=sample_type.replace("_", " ").title())
            label.pack(side=tk.LEFT)
    
    def update_group1_legend(self, group1_colors: Dict[str, str]):
        """
        Update the Group 1 (colors) legend section.
        
        Args:
            group1_colors: Dictionary mapping Group 1 values to colors
        """
        if self.group1_frame:
            self.group1_frame.destroy()
        
        if not group1_colors:
            return
        
        self.group1_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Group 1 Values (Fill Colors)",
            padding="5"
        )
        self.group1_frame.pack(fill=tk.X, pady=(0, 5))
        
        for value, color in group1_colors.items():
            row_frame = ttk.Frame(self.group1_frame)
            row_frame.pack(fill=tk.X, pady=1)
            
            # Color indicator (filled rectangle)
            color_canvas = tk.Canvas(row_frame, width=20, height=20, highlightthickness=0)
            color_canvas.pack(side=tk.LEFT, padx=(0, 5))
            color_canvas.create_rectangle(2, 2, 18, 18, fill=color, outline="black")
            
            # Label
            label = ttk.Label(row_frame, text=value)
            label.pack(side=tk.LEFT)
    
    def update_group2_legend(self, group2_patterns: Dict[str, str]):
        """
        Update the Group 2 (patterns) legend section.
        
        Args:
            group2_patterns: Dictionary mapping Group 2 values to visual patterns
        """
        if self.group2_frame:
            self.group2_frame.destroy()
        
        if not group2_patterns:
            return
        
        self.group2_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Group 2 Values (Visual Patterns)",
            padding="5"
        )
        self.group2_frame.pack(fill=tk.X, pady=(0, 5))
        
        for value, pattern in group2_patterns.items():
            row_frame = ttk.Frame(self.group2_frame)
            row_frame.pack(fill=tk.X, pady=1)
            
            # Pattern indicator (rectangle with visual pattern overlay)
            pattern_canvas = tk.Canvas(row_frame, width=20, height=20, highlightthickness=0)
            pattern_canvas.pack(side=tk.LEFT, padx=(0, 5))
            
            # Create base rectangle
            pattern_canvas.create_rectangle(2, 2, 18, 18, fill="lightblue", outline="black")
            
            # Add visual pattern overlay
            if pattern:
                self._add_legend_pattern_overlay(pattern_canvas, pattern)
            
            # Label
            label = ttk.Label(row_frame, text=f"{value} ({pattern if pattern else 'solid'})")
            label.pack(side=tk.LEFT)
    
    def _add_legend_pattern_overlay(self, canvas: tk.Canvas, pattern_type: str):
        """
        Add visual pattern overlay to legend canvas that matches the plate canvas patterns exactly.
        
        Args:
            canvas: Canvas widget to add pattern to
            pattern_type: Type of pattern ("dots", "lines", "cross", "grid")
        """
        if pattern_type == "dots":
            # Match plate canvas: 8 dots in 3x3 grid (skipping center) - creates square pattern
            dot_size = 1.5
            center_x, center_y = 10, 10
            for dx in [-4, 0, 4]:
                for dy in [-4, 0, 4]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center like plate canvas
                    canvas.create_oval(
                        center_x + dx - dot_size, center_y + dy - dot_size,
                        center_x + dx + dot_size, center_y + dy + dot_size,
                        fill="black", outline="black"
                    )
        
        elif pattern_type == "lines":
            # Match plate canvas: Two diagonal lines creating X pattern
            canvas.create_line(4, 4, 16, 16, fill="black", width=2)  # Top-left to bottom-right
            canvas.create_line(4, 16, 16, 4, fill="black", width=2)  # Bottom-left to top-right
        
        elif pattern_type == "cross":
            # Match plate canvas: Vertical and horizontal lines creating + pattern
            canvas.create_line(10, 3, 10, 17, fill="black", width=3)  # Vertical line
            canvas.create_line(3, 10, 17, 10, fill="black", width=3)  # Horizontal line
        
        elif pattern_type == "grid":
            # Match plate canvas: Grid pattern with offset lines
            # Vertical lines at offsets
            canvas.create_line(6, 3, 6, 17, fill="black", width=2)
            canvas.create_line(14, 3, 14, 17, fill="black", width=2)
            # Horizontal lines at offsets
            canvas.create_line(3, 6, 17, 6, fill="black", width=2)
            canvas.create_line(3, 14, 17, 14, fill="black", width=2)
            
        elif pattern_type == "circles":
            # Match plate canvas: Small circles in grid (skipping center)
            circle_size = 1.5
            center_x, center_y = 10, 10
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center
                    canvas.create_oval(
                        center_x + dx - circle_size, center_y + dy - circle_size,
                        center_x + dx + circle_size, center_y + dy + circle_size,
                        fill="", outline="black", width=2
                    )
                    
        elif pattern_type == "squares":
            # Match plate canvas: Small squares in grid (skipping center)
            square_size = 1.5
            center_x, center_y = 10, 10
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    if dx == 0 and dy == 0:
                        continue  # Skip center
                    canvas.create_rectangle(
                        center_x + dx - square_size, center_y + dy - square_size,
                        center_x + dx + square_size, center_y + dy + square_size,
                        fill="", outline="black", width=2
                    )
                    
        elif pattern_type == "triangles":
            # Match plate canvas: Small triangles in corners
            center_x, center_y = 10, 10
            for dx in [-4, 4]:
                for dy in [-4, 4]:
                    canvas.create_polygon(
                        center_x + dx, center_y + dy - 1.5,  # Top point
                        center_x + dx - 1.5, center_y + dy + 1.5,  # Bottom left
                        center_x + dx + 1.5, center_y + dy + 1.5,  # Bottom right
                        fill="", outline="black", width=2
                    )
                    
        elif pattern_type == "stars":
            # Match plate canvas: 4-point star
            center_x, center_y = 10, 10
            canvas.create_polygon(
                center_x, center_y - 5,      # Top
                center_x - 1.5, center_y - 1.5,  # Top-left inner
                center_x - 5, center_y,      # Left
                center_x - 1.5, center_y + 1.5,  # Bottom-left inner
                center_x, center_y + 5,      # Bottom
                center_x + 1.5, center_y + 1.5,  # Bottom-right inner
                center_x + 5, center_y,      # Right
                center_x + 1.5, center_y - 1.5,  # Top-right inner
                fill="", outline="black", width=2
            )
            
        elif pattern_type == "diamond":
            # Match plate canvas: Diamond shape
            center_x, center_y = 10, 10
            canvas.create_polygon(
                center_x, center_y - 5,      # Top
                center_x - 3, center_y,      # Left
                center_x, center_y + 5,      # Bottom
                center_x + 3, center_y,      # Right
                fill="", outline="black", width=2
            )
            
        elif pattern_type == "zigzag":
            # Match plate canvas: Zigzag lines
            center_y = 10
            canvas.create_line(
                3, center_y - 2,
                5, center_y + 2,
                7, center_y - 2,
                9, center_y + 2,
                11, center_y - 2,
                13, center_y + 2,
                15, center_y - 2,
                17, center_y + 2,
                fill="black", width=2
            )
            canvas.create_line(
                3, center_y + 2,
                5, center_y - 2,
                7, center_y + 2,
                9, center_y - 2,
                11, center_y + 2,
                13, center_y - 2,
                15, center_y + 2,
                17, center_y - 2,
                fill="black", width=2
            )
    
    def update_legend(self, group1_colors: Dict[str, str], group2_patterns: Dict[str, str]):
        """
        Update both Group 1 and Group 2 legends.
        
        Args:
            group1_colors: Dictionary mapping Group 1 values to colors
            group2_patterns: Dictionary mapping Group 2 values to patterns
        """
        self.update_group1_legend(group1_colors)
        self.update_group2_legend(group2_patterns)
        
        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def clear_legend(self):
        """Clear all dynamic legend sections (keep sample types)."""
        if self.group1_frame:
            self.group1_frame.destroy()
            self.group1_frame = None
        
        if self.group2_frame:
            self.group2_frame.destroy()
            self.group2_frame = None
        
        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))