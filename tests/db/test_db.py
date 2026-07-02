import pytest
import logging
from utils.db_helper import DBHelper

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def db():
    """
    Setup a temporary database for testing and tear it down afterward.
    """
    database = DBHelper("test_users.db")
    
    # SETUP: Create a fresh table before tests
    database.execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    yield database  # Hand the DB over to the tests
    
    # TEARDOWN: Drop the table and close connection after tests finish
    database.execute_query("DROP TABLE users")
    database.close()


@pytest.mark.db
class TestDatabaseOperations:
    
    def test_insert_and_verify_user(self, db):
        """Test inserting a user into the DB and reading it back"""
        
        # 1. Insert Data
        logger.info("Inserting user into DB...")
        db.execute_query(
            "INSERT INTO users (name, role) VALUES (?, ?)", 
            ("Chandra Shekar", "Senior SDET")
        )
        
        # 2. Read Data
        logger.info("Fetching users from DB...")
        results = db.fetch_all("SELECT * FROM users WHERE name = ?", ("Chandra Shekar",))
        
        # 3. Assert
        # Results look like this: [(1, 'Chandra Shekar', 'Senior SDET')]
        assert len(results) == 1, "Expected exactly 1 user to be returned"
        assert results[0][1] == "Chandra Shekar"
        assert results[0][2] == "Senior SDET"
        logger.info("✅ Database insertion and verification successful!")
