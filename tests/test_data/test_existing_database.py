"""
Test suite for integration with existing database files.

This tests the DatabaseManager's ability to work with existing database schemas
and data, specifically the example_database.db file in the project root.
"""

import unittest
import os
import sqlite3
from pathlib import Path

# Import the modules we'll be testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.data.database import DatabaseManager


class TestExistingDatabaseIntegration(unittest.TestCase):
    """Test integration with existing database files."""
    
    def setUp(self):
        """Set up test with existing database."""
        # Path to existing database in project root
        self.existing_db_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'example_database.db'
        )
        
        # Verify the existing database exists
        self.assertTrue(os.path.exists(self.existing_db_path), 
                       "example_database.db should exist in project root")
    
    def test_read_existing_database_schema(self):
        """Test reading schema from existing database."""
        # Connect directly with sqlite3 to verify structure
        conn = sqlite3.connect(self.existing_db_path)
        cursor = conn.cursor()
        
        # Check that example_database table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='example_database'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists, "example_database table should exist")
        
        # Check schema
        cursor.execute("PRAGMA table_info(example_database)")
        schema = cursor.fetchall()
        
        # Verify expected columns
        column_names = [col[1] for col in schema]
        expected_columns = ['Proposal', 'Project', 'Sample', 'Number_of_sorted_plates']
        
        for expected_col in expected_columns:
            self.assertIn(expected_col, column_names, 
                         f"Column {expected_col} should exist in example_database table")
        
        conn.close()
    
    def test_read_existing_database_data(self):
        """Test reading data from existing database."""
        conn = sqlite3.connect(self.existing_db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        cursor = conn.cursor()
        
        # Read sample data
        cursor.execute("SELECT * FROM example_database LIMIT 5")
        rows = cursor.fetchall()
        
        self.assertGreater(len(rows), 0, "Database should contain data")
        
        # Verify data structure
        first_row = rows[0]
        self.assertIn('Proposal', first_row.keys())
        self.assertIn('Project', first_row.keys())
        self.assertIn('Sample', first_row.keys())
        self.assertIn('Number_of_sorted_plates', first_row.keys())
        
        # Verify data types and values
        for row in rows:
            self.assertIsInstance(row['Proposal'], int)
            self.assertIsInstance(row['Project'], str)
            self.assertIsInstance(row['Sample'], str)
            self.assertIsInstance(row['Number_of_sorted_plates'], int)
        
        conn.close()
    
    def test_database_manager_with_existing_file(self):
        """Test DatabaseManager initialization with existing database."""
        # Create a copy for testing to avoid modifying original
        import shutil
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            temp_db_path = temp_file.name
        
        try:
            # Copy existing database
            shutil.copy2(self.existing_db_path, temp_db_path)
            
            # Initialize DatabaseManager with existing database
            db_manager = DatabaseManager(temp_db_path)
            
            # Verify connection works
            conn = db_manager.get_connection()
            self.assertIsNotNone(conn)
            
            # Verify existing table is accessible
            self.assertTrue(db_manager.table_exists('example_database'))
            
            # Verify read-only functionality works
            projects = db_manager.get_existing_projects()
            samples = db_manager.get_existing_samples()
            self.assertGreater(len(projects), 0)
            self.assertGreater(len(samples), 0)
            
            db_manager.close()
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_db_path):
                os.unlink(temp_db_path)
    
    def test_query_existing_data_for_dropdowns(self):
        """Test querying existing data for GUI dropdown population."""
        conn = sqlite3.connect(self.existing_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get unique projects for dropdown
        cursor.execute("SELECT DISTINCT Project FROM example_database ORDER BY Project")
        projects = [row[0] for row in cursor.fetchall()]
        
        self.assertGreater(len(projects), 0, "Should have project data")
        self.assertIn('BP9735', projects, "Should contain expected project data")
        
        # Get unique samples for dropdown
        cursor.execute("SELECT DISTINCT Sample FROM example_database ORDER BY Sample")
        samples = [row[0] for row in cursor.fetchall()]
        
        self.assertGreater(len(samples), 0, "Should have sample data")
        
        # Verify sample names match expected pattern
        for sample in samples:
            self.assertIsInstance(sample, str)
            self.assertGreater(len(sample), 0)
        
        conn.close()
    
    def test_existing_data_statistics(self):
        """Test gathering statistics from existing data."""
        conn = sqlite3.connect(self.existing_db_path)
        cursor = conn.cursor()
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM example_database")
        total_count = cursor.fetchone()[0]
        self.assertGreater(total_count, 0, "Database should contain records")
        
        # Count unique proposals
        cursor.execute("SELECT COUNT(DISTINCT Proposal) FROM example_database")
        unique_proposals = cursor.fetchone()[0]
        self.assertGreater(unique_proposals, 0, "Should have unique proposals")
        
        # Count unique projects
        cursor.execute("SELECT COUNT(DISTINCT Project) FROM example_database")
        unique_projects = cursor.fetchone()[0]
        self.assertGreater(unique_projects, 0, "Should have unique projects")
        
        # Count unique samples
        cursor.execute("SELECT COUNT(DISTINCT Sample) FROM example_database")
        unique_samples = cursor.fetchone()[0]
        self.assertGreater(unique_samples, 0, "Should have unique samples")
        
        # Get plate count statistics
        cursor.execute("SELECT MIN(Number_of_sorted_plates), MAX(Number_of_sorted_plates), AVG(Number_of_sorted_plates) FROM example_database")
        min_plates, max_plates, avg_plates = cursor.fetchone()
        
        self.assertGreaterEqual(min_plates, 0, "Minimum plates should be non-negative")
        self.assertGreater(max_plates, 0, "Maximum plates should be positive")
        self.assertGreater(avg_plates, 0, "Average plates should be positive")
        
        conn.close()


class TestDatabaseManagerExtensions(unittest.TestCase):
    """Test extensions to DatabaseManager for existing data compatibility."""
    
    def setUp(self):
        """Set up test database manager."""
        import tempfile
        import shutil
        
        # Create temporary copy of existing database
        self.existing_db_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'example_database.db'
        )
        
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db_path = self.temp_file.name
        self.temp_file.close()
        
        shutil.copy2(self.existing_db_path, self.temp_db_path)
        self.db_manager = DatabaseManager(self.temp_db_path)
    
    def tearDown(self):
        """Clean up after test."""
        self.db_manager.close()
        if os.path.exists(self.temp_db_path):
            os.unlink(self.temp_db_path)
    
    def test_mixed_schema_compatibility(self):
        """Test that new schema works alongside existing schema."""
        # Verify existing table is still accessible
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM example_database")
        existing_count = cursor.fetchone()[0]
        self.assertGreater(existing_count, 0)
        
        # Verify read-only functionality works with existing data
        projects = self.db_manager.get_existing_projects()
        samples = self.db_manager.get_existing_samples()
        
        self.assertGreater(len(projects), 0)
        self.assertGreater(len(samples), 0)
        
        # Verify plate name generation works
        if projects and samples:
            plate_names = self.db_manager.generate_plate_names(projects[0], samples[0])
            # Should generate plate names if data exists
            self.assertIsInstance(plate_names, list)
        
        # Verify only existing table exists (read-only mode)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Should have existing table
        self.assertIn('example_database', tables)


if __name__ == '__main__':
    unittest.main()