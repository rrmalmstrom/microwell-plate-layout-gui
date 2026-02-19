#!/usr/bin/env python3
"""
Automated Environment Test Suite for Microwell Plate GUI
Tests the conda environment without requiring manual GUI interaction

Usage:
    python test_environment.py

This script validates that all required dependencies are available and
the application can start successfully without any manual testing.
"""

import sys
import os
import subprocess
import tempfile
import sqlite3
from pathlib import Path


def print_header(title):
    """Print a formatted test section header"""
    print(f"\n{'='*50}")
    print(f"🧬 {title}")
    print(f"{'='*50}")


def print_test(test_name, status, details=""):
    """Print test result with consistent formatting"""
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {test_name}")
    if details:
        print(f"   {details}")


def test_python_environment():
    """Test Python version and basic environment"""
    print_header("Python Environment Test")
    
    # Test Python version
    python_version = sys.version_info
    version_ok = python_version >= (3, 8)
    print_test("Python Version", version_ok, 
               f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Test current working directory
    cwd = Path.cwd()
    has_src = (cwd / "src" / "microwell_plate_gui").exists()
    print_test("Source Code Present", has_src, f"Working directory: {cwd}")
    
    return version_ok and has_src


def test_standard_library_imports():
    """Test all Python standard library modules used by the app"""
    print_header("Standard Library Import Test")
    
    standard_modules = [
        'tkinter',      # GUI framework
        'sqlite3',      # Database
        'os',           # Operating system interface
        'sys',          # System-specific parameters
        'csv',          # CSV file handling
        'logging',      # Logging facility
        'subprocess',   # Subprocess management
        'tempfile',     # Temporary file creation
        'math',         # Mathematical functions
        'datetime',     # Date and time handling
        're',           # Regular expressions
        'typing',       # Type hints
        'argparse',     # Command-line argument parsing
    ]
    
    all_passed = True
    for module in standard_modules:
        try:
            __import__(module)
            print_test(f"Import {module}", True)
        except ImportError as e:
            print_test(f"Import {module}", False, f"Error: {e}")
            all_passed = False
    
    return all_passed


def test_application_imports():
    """Test that all application modules can be imported"""
    print_header("Application Import Test")
    
    # Add src to path if needed
    src_path = Path.cwd() / "src"
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    app_modules = [
        'microwell_plate_gui',
        'microwell_plate_gui.main',
        'microwell_plate_gui.data.database',
        'microwell_plate_gui.gui.main_window',
        'microwell_plate_gui.gui.plate_canvas',
        'microwell_plate_gui.gui.legend_panel',
        'microwell_plate_gui.gui.metadata_panel',
        'microwell_plate_gui.utils.csv_export',
        'microwell_plate_gui.utils.image_export',
    ]
    
    all_passed = True
    for module in app_modules:
        try:
            __import__(module)
            print_test(f"Import {module}", True)
        except ImportError as e:
            print_test(f"Import {module}", False, f"Error: {e}")
            all_passed = False
    
    return all_passed


def test_ghostscript():
    """Test that ghostscript (ps2pdf) is available for PDF export"""
    print_header("Ghostscript Test")
    
    # Test ps2pdf command
    try:
        result = subprocess.run(['ps2pdf', '--version'], 
                              capture_output=True, text=True, timeout=10)
        ps2pdf_ok = result.returncode == 0
        version_info = result.stdout.strip() if ps2pdf_ok else result.stderr.strip()
        print_test("ps2pdf command", ps2pdf_ok, version_info)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print_test("ps2pdf command", False, f"Error: {e}")
        ps2pdf_ok = False
    
    # Test gs command
    try:
        result = subprocess.run(['gs', '--version'], 
                              capture_output=True, text=True, timeout=10)
        gs_ok = result.returncode == 0
        version_info = result.stdout.strip() if gs_ok else result.stderr.strip()
        print_test("gs command", gs_ok, version_info)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print_test("gs command", False, f"Error: {e}")
        gs_ok = False
    
    return ps2pdf_ok or gs_ok  # Either command working is sufficient


def test_database_functionality():
    """Test database operations without GUI"""
    print_header("Database Functionality Test")
    
    try:
        # Import database manager
        from microwell_plate_gui.data.database import DatabaseManager
        
        # Test in-memory database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        try:
            db = DatabaseManager(db_path)
            print_test("Database creation", True, f"Created test database: {db_path}")
            
            # Clean up
            os.unlink(db_path)
            print_test("Database cleanup", True)
            
            return True
            
        except Exception as e:
            print_test("Database operations", False, f"Error: {e}")
            # Clean up on error
            if os.path.exists(db_path):
                os.unlink(db_path)
            return False
            
    except ImportError as e:
        print_test("Database import", False, f"Error: {e}")
        return False


def test_gui_creation():
    """Test GUI creation without displaying windows"""
    print_header("GUI Creation Test")
    
    try:
        import tkinter as tk
        from microwell_plate_gui.gui.main_window import MainWindow
        
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        try:
            # Test main window creation
            app = MainWindow(root)
            print_test("Main window creation", True)
            
            # Test window destruction
            root.destroy()
            print_test("Window cleanup", True)
            
            return True
            
        except Exception as e:
            print_test("GUI creation", False, f"Error: {e}")
            try:
                root.destroy()
            except:
                pass
            return False
            
    except ImportError as e:
        print_test("GUI import", False, f"Error: {e}")
        return False


def test_csv_export():
    """Test CSV export functionality"""
    print_header("CSV Export Test")
    
    try:
        from microwell_plate_gui.utils.csv_export import export_plate_layout
        print_test("CSV export import", True)
        
        # Test basic CSV operations
        import csv
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            csv_path = tmp_file.name
            writer = csv.writer(tmp_file)
            writer.writerow(['test', 'data'])
        
        # Verify file was created
        if os.path.exists(csv_path):
            print_test("CSV file creation", True, f"Created: {csv_path}")
            os.unlink(csv_path)
            print_test("CSV cleanup", True)
            return True
        else:
            print_test("CSV file creation", False)
            return False
            
    except ImportError as e:
        print_test("CSV export import", False, f"Error: {e}")
        return False
    except Exception as e:
        print_test("CSV operations", False, f"Error: {e}")
        return False


def run_all_tests():
    """Run the complete test suite"""
    print_header("Microwell Plate GUI Environment Test Suite")
    print("Testing conda environment without manual GUI interaction...")
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Standard Library", test_standard_library_imports),
        ("Application Modules", test_application_imports),
        ("Ghostscript (PDF Export)", test_ghostscript),
        ("Database Functionality", test_database_functionality),
        ("GUI Creation", test_gui_creation),
        ("CSV Export", test_csv_export),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_test(f"{test_name} (Exception)", False, f"Unexpected error: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Results Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        print_test(test_name, result)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Environment is ready for distribution")
        print("\nTo run the application:")
        print("   python run_app.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("❌ Environment needs additional packages")
        print("\nTroubleshooting:")
        print("1. Check that you're in the correct conda environment")
        print("2. Verify all packages installed: conda list")
        print("3. Try installing missing packages manually")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)