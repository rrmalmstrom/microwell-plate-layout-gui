"""
Database reader module for microwell plate GUI application.

Context7 Reference: SQLite database operations for reading existing data
- Read-only database access for dropdown population
- Sample and project data retrieval
- Plate name generation logic
- Error handling for missing databases
"""

import sqlite3
import os
from typing import Dict, List, Optional, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database reader for handling SQLite read operations.
    
    Context7 Reference: SQLite read-only operations
    - Read existing sample/project data for dropdown population
    - Generate plate names based on database content
    - Graceful handling of missing database files
    """
    
    def __init__(self, db_path: str):
        """
        Initialize database reader.
        
        Args:
            db_path: Path to existing SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        
        # Initialize database connection
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize database connection."""
        try:
            if not os.path.exists(self.db_path):
                logger.warning(f"Database file not found: {self.db_path}")
                return
                
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            
            logger.info(f"Database connected: {self.db_path}")
            
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            self.connection = None
    
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """
        Get database connection.
        
        Returns:
            SQLite connection object or None if not available
        """
        return self.connection
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists in database.
        
        Args:
            table_name: Name of table to check
            
        Returns:
            True if table exists, False otherwise
        """
        if not self.connection:
            return False
            
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    
    def get_existing_projects(self) -> List[str]:
        """
        Get unique projects from existing database table.
        
        Returns:
            List of project names from example_database table
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Project FROM example_database ORDER BY Project")
        
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_existing_samples(self) -> List[str]:
        """
        Get unique samples from existing database table.
        
        Returns:
            List of sample names from example_database table
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Sample FROM example_database ORDER BY Sample")
        
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_existing_proposals(self) -> List[int]:
        """
        Get unique proposals from existing database table.
        
        Returns:
            List of proposal numbers from example_database table
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Proposal FROM example_database ORDER BY Proposal")
        
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_existing_data_by_project(self, project: str) -> List[Dict[str, Any]]:
        """
        Get all data for a specific project from existing database.
        
        Args:
            project: Project name to filter by
            
        Returns:
            List of data dictionaries for the project
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM example_database WHERE Project = ? ORDER BY Sample", (project,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_existing_data_by_sample(self, sample: str) -> List[Dict[str, Any]]:
        """
        Get all data for a specific sample from existing database.
        
        Args:
            sample: Sample name to filter by
            
        Returns:
            List of data dictionaries for the sample
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM example_database WHERE Sample = ?", (sample,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def generate_plate_names(self, project: str, sample: str) -> List[str]:
        """
        Generate plate names based on sample (and optionally project).
        
        Format: {Project}.{Sample}.{plate_number}
        Example: BP9735.SitukAM.1, BP9735.SitukAM.2, BP9735.SitukAM.3
        
        Args:
            project: Project name (can be empty string)
            sample: Sample name
            
        Returns:
            List of generated plate names
        """
        if not self.connection or not self.table_exists('example_database'):
            return []
        
        cursor = self.connection.cursor()
        
        # If no project specified, get the first project for this sample
        if not project:
            cursor.execute("""
                SELECT DISTINCT Project, Number_of_sorted_plates
                FROM example_database
                WHERE Sample = ?
                LIMIT 1
            """, (sample,))
            
            row = cursor.fetchone()
            if not row:
                return []
            
            project = row[0]
            num_plates = row[1]
        else:
            # Get number of plates for this project/sample combination
            cursor.execute("""
                SELECT Number_of_sorted_plates
                FROM example_database
                WHERE Project = ? AND Sample = ?
            """, (project, sample))
            
            row = cursor.fetchone()
            if not row:
                return []
            
            num_plates = row[0]
        
        # Generate plate names
        plate_names = []
        for i in range(1, num_plates + 1):
            plate_name = f"{project}.{sample}.{i}"
            plate_names.append(plate_name)
        
        return plate_names
    
    def get_existing_data_statistics(self) -> Dict[str, Any]:
        """
        Get statistics from existing database table.
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.connection or not self.table_exists('example_database'):
            return {}
        
        cursor = self.connection.cursor()
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM example_database")
        total_records = cursor.fetchone()[0]
        
        # Unique counts
        cursor.execute("SELECT COUNT(DISTINCT Proposal) FROM example_database")
        unique_proposals = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT Project) FROM example_database")
        unique_projects = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT Sample) FROM example_database")
        unique_samples = cursor.fetchone()[0]
        
        # Plate statistics
        cursor.execute("""
            SELECT MIN(Number_of_sorted_plates), MAX(Number_of_sorted_plates), 
                   AVG(Number_of_sorted_plates), SUM(Number_of_sorted_plates)
            FROM example_database
        """)
        min_plates, max_plates, avg_plates, total_plates = cursor.fetchone()
        
        return {
            'total_records': total_records,
            'unique_proposals': unique_proposals,
            'unique_projects': unique_projects,
            'unique_samples': unique_samples,
            'min_plates': min_plates,
            'max_plates': max_plates,
            'avg_plates': round(avg_plates, 2) if avg_plates else 0,
            'total_plates': total_plates
        }
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()