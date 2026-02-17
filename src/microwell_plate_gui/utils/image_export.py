"""
Simple image export utilities for microwell plate GUI.

This module provides the simplest possible approach to export canvas content as PDF files.
Uses tkinter's built-in postscript() method and converts to PDF using system tools.
"""

import logging
import os
import subprocess
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


class ImageExporter:
    """Simple image exporter that uses tkinter's postscript method and converts to PDF."""

    def capture_plate_and_legend(self, plate_canvas, legend_panel, filename: str) -> bool:
        """
        Export both plate canvas and legend panel to a combined PDF file.
        
        Args:
            plate_canvas: The PlateCanvas instance
            legend_panel: The LegendPanel instance
            filename (str): Output filename (will be saved as PDF)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not filename:
                logger.error("No filename provided")
                return False
            
            # Get the actual canvas widgets
            plate_widget = plate_canvas.canvas if hasattr(plate_canvas, 'canvas') else plate_canvas
            legend_widget = legend_panel.canvas if hasattr(legend_panel, 'canvas') else legend_panel
            
            # Ensure filename ends with .pdf
            if not filename.lower().endswith('.pdf'):
                filename = os.path.splitext(filename)[0] + '.pdf'
            
            logger.info(f"Exporting plate and legend to PDF: {filename}")
            
            # Method 1: Export both widgets to PostScript and combine
            try:
                # Create temporary PostScript files
                with tempfile.NamedTemporaryFile(suffix='_plate.ps', delete=False) as temp_plate_ps:
                    plate_ps_file = temp_plate_ps.name
                
                with tempfile.NamedTemporaryFile(suffix='_legend.ps', delete=False) as temp_legend_ps:
                    legend_ps_file = temp_legend_ps.name
                
                # Export plate canvas to PostScript
                plate_widget.postscript(file=plate_ps_file, colormode='color')
                logger.info(f"Plate canvas exported to PostScript: {plate_ps_file}")
                
                # Export legend panel to PostScript
                legend_widget.postscript(file=legend_ps_file, colormode='color')
                logger.info(f"Legend panel exported to PostScript: {legend_ps_file}")
                
                # Create combined PostScript file
                with tempfile.NamedTemporaryFile(suffix='_combined.ps', delete=False) as temp_combined_ps:
                    combined_ps_file = temp_combined_ps.name
                
                # Combine PostScript files side by side
                self._combine_postscript_files(plate_ps_file, legend_ps_file, combined_ps_file)
                
                # Convert combined PostScript to PDF using system tools
                conversion_success = False
                
                # Try ps2pdf (part of Ghostscript)
                try:
                    result = subprocess.run([
                        'ps2pdf', combined_ps_file, filename
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and os.path.exists(filename):
                        conversion_success = True
                        logger.info("Converted combined PostScript to PDF using ps2pdf")
                    else:
                        logger.warning(f"ps2pdf failed: {result.stderr}")
                except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
                    logger.warning(f"ps2pdf not available: {e}")
                
                # Try ghostscript directly
                if not conversion_success:
                    try:
                        result = subprocess.run([
                            'gs', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite',
                            f'-sOutputFile={filename}', combined_ps_file
                        ], capture_output=True, text=True, timeout=30)
                        
                        if result.returncode == 0 and os.path.exists(filename):
                            conversion_success = True
                            logger.info("Converted combined PostScript to PDF using Ghostscript")
                        else:
                            logger.warning(f"Ghostscript failed: {result.stderr}")
                    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
                        logger.warning(f"Ghostscript not available: {e}")
                
                # Clean up temporary PostScript files
                for temp_file in [plate_ps_file, legend_ps_file, combined_ps_file]:
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                
                if conversion_success:
                    logger.info(f"Successfully exported combined PDF: {filename}")
                    return True
                else:
                    logger.error("All PostScript to PDF conversion methods failed")
                    # Fallback: Just export plate canvas
                    return self._export_plate_only(plate_widget, filename)
                    
            except Exception as e:
                logger.error(f"Combined PostScript export failed: {e}")
                # Fallback: Just export plate canvas
                return self._export_plate_only(plate_widget, filename)
            
        except Exception as e:
            logger.error(f"Image export completely failed: {e}")
            return False

    def _combine_postscript_files(self, plate_ps_file: str, legend_ps_file: str, output_ps_file: str):
        """
        Combine two PostScript files side by side into a single PostScript file.
        
        Args:
            plate_ps_file: Path to plate PostScript file
            legend_ps_file: Path to legend PostScript file
            output_ps_file: Path to output combined PostScript file
        """
        try:
            with open(output_ps_file, 'w') as output_file:
                # Write PostScript header
                output_file.write("%!PS-Adobe-3.0\n")
                output_file.write("%%BoundingBox: 0 0 800 600\n")
                output_file.write("%%Pages: 1\n")
                output_file.write("%%Page: 1 1\n")
                
                # Save graphics state
                output_file.write("gsave\n")
                
                # Include plate canvas on the left side
                output_file.write("% Plate Canvas\n")
                output_file.write("0 0 translate\n")
                output_file.write("0.8 0.8 scale\n")  # Scale down slightly
                
                # Read and include plate PostScript content (skip header)
                with open(plate_ps_file, 'r') as plate_file:
                    plate_content = plate_file.read()
                    # Skip PostScript header lines
                    lines = plate_content.split('\n')
                    content_start = 0
                    for i, line in enumerate(lines):
                        if line.startswith('%%EndComments') or line.startswith('%%BeginProlog') or 'translate' in line:
                            content_start = i + 1
                            break
                    
                    # Write the actual drawing commands
                    for line in lines[content_start:]:
                        if not line.startswith('showpage'):  # Don't show page yet
                            output_file.write(line + '\n')
                
                # Restore graphics state and move to right side for legend
                output_file.write("grestore\n")
                output_file.write("gsave\n")
                output_file.write("% Legend Panel\n")
                output_file.write("400 0 translate\n")  # Move to right side
                output_file.write("0.6 0.6 scale\n")  # Scale down legend
                
                # Read and include legend PostScript content (skip header)
                with open(legend_ps_file, 'r') as legend_file:
                    legend_content = legend_file.read()
                    # Skip PostScript header lines
                    lines = legend_content.split('\n')
                    content_start = 0
                    for i, line in enumerate(lines):
                        if line.startswith('%%EndComments') or line.startswith('%%BeginProlog') or 'translate' in line:
                            content_start = i + 1
                            break
                    
                    # Write the actual drawing commands
                    for line in lines[content_start:]:
                        if not line.startswith('showpage'):  # Don't show page yet
                            output_file.write(line + '\n')
                
                # Restore graphics state and show page
                output_file.write("grestore\n")
                output_file.write("showpage\n")
                
            logger.info(f"Successfully combined PostScript files: {output_ps_file}")
            
        except Exception as e:
            logger.error(f"Failed to combine PostScript files: {e}")
            raise

    def _export_plate_only(self, plate_widget, filename: str) -> bool:
        """
        Fallback method to export just the plate canvas.
        
        Args:
            plate_widget: The plate canvas widget
            filename: Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Falling back to plate-only export")
            
            # Create temporary PostScript file
            with tempfile.NamedTemporaryFile(suffix='.ps', delete=False) as temp_ps:
                ps_file = temp_ps.name
            
            # Export canvas to PostScript
            plate_widget.postscript(file=ps_file, colormode='color')
            logger.info(f"Plate canvas exported to PostScript: {ps_file}")
            
            # Convert PostScript to PDF
            try:
                result = subprocess.run([
                    'ps2pdf', ps_file, filename
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and os.path.exists(filename):
                    logger.info("Converted plate-only PostScript to PDF using ps2pdf")
                    return True
                else:
                    logger.warning(f"ps2pdf failed: {result.stderr}")
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
                logger.warning(f"ps2pdf not available: {e}")
            
            # Clean up
            try:
                os.remove(ps_file)
            except:
                pass
                
            return False
            
        except Exception as e:
            logger.error(f"Plate-only export failed: {e}")
            return False

    def generate_default_filename(self, plate_name: str) -> str:
        """Generate a default filename for PDF export."""
        safe_name = "".join(c for c in plate_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        if not safe_name:
            safe_name = "plate_layout"
        
        return f"{safe_name}_layout.pdf"