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

    def execute_query(self, query, params=()):
        """Execute a query that doesn't return data (INSERT, UPDATE, DELETE)"""
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        logger.info(f"Executed Query: {query}")

    def fetch_all(self, query, params=()):
        """Execute a query and return all results (SELECT)"""
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
