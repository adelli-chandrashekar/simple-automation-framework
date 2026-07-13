import pytest
import logging

logger = logging.getLogger(__name__)

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
        logger.info("Database insertion and verification successful!")

    def test_insert_multiple_users(self, db):
        """Insert multiple users and verify all were stored"""

        # 1. Define 3 users
        users = [
            ("Priya Sharma", "SDET"),
            ("Rahul Verma", "Developer"),
            ("Anita Desai", "QA Lead"),
        ]

        # We can now use our optimized execute_query method with the is_many flag!
        db.execute_query(
            "INSERT INTO users (name, role) VALUES (?, ?)", users, is_many=True
        )

        # 2. Fetch all users from the table
        results = db.fetch_all("SELECT * FROM users")

        # 3. Assert — 1 from previous test + 3 new = 4 total
        assert len(results) >= 3, "Expected at least 3 users in the table"
        logger.info(f"Total users in DB: {len(results)}")

        # 4. Verify specific user exists using list comprehension
        names = [row[1] for row in results]
        assert "Priya Sharma" in names, "Priya Sharma should be in the DB"

    def test_update_user_role(self, db):
        """Update a user's role and verify the change"""

        # UPDATE query
        db.execute_query(
            "UPDATE users SET role = ? WHERE name = ?",
            ("Lead SDET", "Chandra Shekar")
        )

        # Verify the update
        results = db.fetch_all(
            "SELECT role FROM users WHERE name = ?", ("Chandra Shekar",)
        )
        assert results[0][0] == "Lead SDET"
        logger.info("User role updated successfully!")

    def test_delete_user(self, db):
        """Delete a user and verify they are gone"""

        # DELETE query
        db.execute_query("DELETE FROM users WHERE name = ?", ("Rahul Verma",))

        # Verify deletion
        results = db.fetch_all(
            "SELECT * FROM users WHERE name = ?", ("Rahul Verma",)
        )
        assert len(results) == 0, "Rahul Verma should be deleted"
        logger.info("User deleted successfully!")

    def test_count_users_by_role(self, db):
        """SQL aggregation: COUNT users grouped by role"""

        results = db.fetch_all(
            "SELECT role, COUNT(*) FROM users GROUP BY role"
        )
        logger.info(f"Users by role: {results}")
        assert len(results) > 0, "Should have at least one role group"
