"""
Test suite for database reader functionality.

Context7 Reference: SQLite read-only operations for dropdown population
- Database connection and table detection
- Sample and project data retrieval
- Plate name generation logic
- Error handling for missing databases
"""

import unittest
import tempfile
import os
from pathlib import Path
import sqlite3

# Import the modules we'll be testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from microwell_plate_gui.data.database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test database reader functionality."""
    
    def setUp(self):
        """Set up test database for each test."""
        # Create temporary database file with test data
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Create test database with sample data
        self._create_test_database()
        
        # Initialize database manager
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        # Close database connection
        if hasattr(self.db_manager, 'close'):
            self.db_manager.close()
        
        # Remove temporary database file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def _create_test_database(self):
        """Create test database with sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create example_database table
        cursor.execute("""
            CREATE TABLE example_database (
                Proposal INTEGER,
                Project TEXT,
                Sample TEXT,
                Number_of_sorted_plates INTEGER
            )
        """)
        
        # Insert test data
        test_data = [
            (599999, 'BP9735', 'SitukAM', 3),
            (599999, 'BP9735', 'SitukaPM', 3),
            (599999, 'BP9735', 'WCBP1AM', 4),
            (599999, 'BP9735', 'WCBP1PR', 5),
            (600000, 'BP9736', 'TestSample1', 2),
            (600000, 'BP9736', 'TestSample2', 1),
        ]
        
        cursor.executemany("""
            INSERT INTO example_database (Proposal, Project, Sample, Number_of_sorted_plates)
            VALUES (?, ?, ?, ?)
        """, test_data)
        
        conn.commit()
        conn.close()
    
    def test_database_connection(self):
        """Test database connection functionality."""
        # Should be able to get a connection
        conn = self.db_manager.get_connection()
        self.assertIsNotNone(conn)
        
        # Should be able to execute basic queries
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        self.assertIsNotNone(version)
    
    def test_missing_database_handling(self):
        """Test graceful handling of missing database files."""
        # Test with non-existent database
        missing_db_manager = DatabaseManager('/nonexistent/path/database.db')
        
        # Should handle missing database gracefully
        self.assertIsNone(missing_db_manager.get_connection())
        self.assertEqual(missing_db_manager.get_existing_projects(), [])
        self.assertEqual(missing_db_manager.get_existing_samples(), [])
    
    def test_table_detection(self):
        """Test table existence detection."""
        # Should detect existing table
        self.assertTrue(self.db_manager.table_exists('example_database'))
        
        # Should return False for non-existent table
        self.assertFalse(self.db_manager.table_exists('nonexistent_table'))
    
    def test_project_retrieval(self):
        """Test retrieving unique projects."""
        projects = self.db_manager.get_existing_projects()
        
        # Should return expected projects
        expected_projects = ['BP9735', 'BP9736']
        self.assertEqual(sorted(projects), sorted(expected_projects))
    
    def test_sample_retrieval(self):
        """Test retrieving unique samples."""
        samples = self.db_manager.get_existing_samples()
        
        # Should return expected samples
        expected_samples = ['SitukAM', 'SitukaPM', 'WCBP1AM', 'WCBP1PR', 'TestSample1', 'TestSample2']
        self.assertEqual(sorted(samples), sorted(expected_samples))
    
    def test_proposal_retrieval(self):
        """Test retrieving unique proposals."""
        proposals = self.db_manager.get_existing_proposals()
        
        # Should return expected proposals
        expected_proposals = [599999, 600000]
        self.assertEqual(sorted(proposals), sorted(expected_proposals))
    
    def test_data_by_project(self):
        """Test retrieving data filtered by project."""
        # Test BP9735 project
        bp9735_data = self.db_manager.get_existing_data_by_project('BP9735')
        self.assertEqual(len(bp9735_data), 4)
        
        # Verify all records are for BP9735
        for record in bp9735_data:
            self.assertEqual(record['Project'], 'BP9735')
        
        # Test BP9736 project
        bp9736_data = self.db_manager.get_existing_data_by_project('BP9736')
        self.assertEqual(len(bp9736_data), 2)
        
        # Test non-existent project
        empty_data = self.db_manager.get_existing_data_by_project('NonExistent')
        self.assertEqual(len(empty_data), 0)
    
    def test_data_by_sample(self):
        """Test retrieving data filtered by sample."""
        # Test specific sample
        situk_data = self.db_manager.get_existing_data_by_sample('SitukAM')
        self.assertEqual(len(situk_data), 1)
        self.assertEqual(situk_data[0]['Sample'], 'SitukAM')
        self.assertEqual(situk_data[0]['Number_of_sorted_plates'], 3)
        
        # Test non-existent sample
        empty_data = self.db_manager.get_existing_data_by_sample('NonExistent')
        self.assertEqual(len(empty_data), 0)
    
    def test_plate_name_generation(self):
        """Test plate name generation logic."""
        # Test SitukAM with 3 plates
        plate_names = self.db_manager.generate_plate_names('BP9735', 'SitukAM')
        expected_names = ['BP9735.SitukAM.1', 'BP9735.SitukAM.2', 'BP9735.SitukAM.3']
        self.assertEqual(plate_names, expected_names)
        
        # Test WCBP1PR with 5 plates
        plate_names = self.db_manager.generate_plate_names('BP9735', 'WCBP1PR')
        expected_names = ['BP9735.WCBP1PR.1', 'BP9735.WCBP1PR.2', 'BP9735.WCBP1PR.3', 
                         'BP9735.WCBP1PR.4', 'BP9735.WCBP1PR.5']
        self.assertEqual(plate_names, expected_names)
        
        # Test non-existent combination
        empty_names = self.db_manager.generate_plate_names('NonExistent', 'Sample')
        self.assertEqual(empty_names, [])
    
    def test_database_statistics(self):
        """Test database statistics generation."""
        stats = self.db_manager.get_existing_data_statistics()
        
        # Verify expected statistics
        self.assertEqual(stats['total_records'], 6)
        self.assertEqual(stats['unique_proposals'], 2)
        self.assertEqual(stats['unique_projects'], 2)
        self.assertEqual(stats['unique_samples'], 6)
        self.assertEqual(stats['min_plates'], 1)
        self.assertEqual(stats['max_plates'], 5)
        self.assertEqual(stats['total_plates'], 18)  # 3+3+4+5+2+1
        
        # Average should be 3.0
        self.assertEqual(stats['avg_plates'], 3.0)
    
    def test_context_manager(self):
        """Test context manager functionality."""
        db_path = self.db_path
        
        # Test context manager
        with DatabaseManager(db_path) as db:
            projects = db.get_existing_projects()
            self.assertGreater(len(projects), 0)
        
        # Connection should be closed after context manager
        # Note: We can't easily test this without accessing private attributes


class TestDatabaseIntegration(unittest.TestCase):
    """Test database integration scenarios."""
    
    def test_empty_database(self):
        """Test behavior with empty database."""
        # Create empty database
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            conn = sqlite3.connect(temp_db.name)
            conn.close()
            
            # Initialize with empty database
            db_manager = DatabaseManager(temp_db.name)
            
            # Should handle empty database gracefully
            self.assertEqual(db_manager.get_existing_projects(), [])
            self.assertEqual(db_manager.get_existing_samples(), [])
            self.assertEqual(db_manager.get_existing_proposals(), [])
            
            db_manager.close()
            
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)
    
    def test_database_with_different_schema(self):
        """Test behavior with database that has different schema."""
        # Create database with different table
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            
            # Create different table
            cursor.execute("""
                CREATE TABLE different_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
            """)
            conn.commit()
            conn.close()
            
            # Initialize with different schema
            db_manager = DatabaseManager(temp_db.name)
            
            # Should handle missing expected table gracefully
            self.assertEqual(db_manager.get_existing_projects(), [])
            self.assertEqual(db_manager.get_existing_samples(), [])
            
            db_manager.close()
            
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)


if __name__ == '__main__':
    unittest.main()