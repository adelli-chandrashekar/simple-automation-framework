import sqlite3
import logging

logger = logging.getLogger(__name__)

class DBHelper:
    """
    A simple helper to connect to a local SQLite database.
    In a real enterprise environment, you would just swap sqlite3 
    with psycopg2 (for Postgres) or pyodbc (for SQL Server).
    """

    def __init__(self, db_name="automation_test.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_name)
        logger.info(f"Connected to Database: {self.db_name}")
        return self.conn

    def _get_cursor(self):
        """Helper to ensure we have a valid connection and return a cursor."""
        if not self.conn:
            self.connect()
        return self.conn.cursor()

    def execute_query(self, query, params=(), is_many=False):
        """Execute a query (INSERT, UPDATE, DELETE). Supports bulk execution if is_many=True."""
        cursor = self._get_cursor()
        
        if is_many:
            cursor.executemany(query, params)
            logger.info(f"Bulk Executed Query: {query} with {len(params)} rows")
        else:
            cursor.execute(query, params)
            logger.info(f"Executed Query: {query}")
            
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """Execute a query and return all results (SELECT)"""
        cursor = self._get_cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
