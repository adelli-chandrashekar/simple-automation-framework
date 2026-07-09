"""
Seed Script — Populate the Database with Sample Data
=====================================================
This script creates a fresh SQLite database with realistic test data.
Run it once to have something to view and query against.

Usage:
    python scripts/seed_database.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import DBHelper

def seed():
    db = DBHelper("automation_test.db")
    db.connect()

    # 1. Create the users table
    db.execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')

    # 2. Create the test_results table
    db.execute_query('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT NOT NULL,
            status TEXT NOT NULL,
            duration_seconds REAL,
            executed_by TEXT NOT NULL,
            executed_on TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Insert sample users
    users = [
        ("Chandra Shekar", "chandra@company.com", "Senior SDET", "QA Engineering"),
        ("Priya Sharma", "priya@company.com", "SDET", "QA Engineering"),
        ("Rahul Verma", "rahul@company.com", "Developer", "Backend"),
        ("Anita Desai", "anita@company.com", "QA Lead", "QA Engineering"),
        ("Vikram Singh", "vikram@company.com", "DevOps Engineer", "Infrastructure"),
        ("Meera Patel", "meera@company.com", "SDET", "QA Engineering"),
        ("Arjun Reddy", "arjun@company.com", "Developer", "Frontend"),
        ("Sneha Kulkarni", "sneha@company.com", "Product Manager", "Product"),
    ]

    for name, email, role, dept in users:
        db.execute_query(
            "INSERT INTO users (name, email, role, department) VALUES (?, ?, ?, ?)",
            (name, email, role, dept)
        )

    # 4. Insert sample test results
    test_results = [
        ("test_login_success", "PASSED", 1.23, "Chandra Shekar"),
        ("test_login_failure", "PASSED", 0.89, "Chandra Shekar"),
        ("test_create_single_user", "PASSED", 2.15, "Chandra Shekar"),
        ("test_get_user_by_id", "PASSED", 0.95, "Priya Sharma"),
        ("test_get_nonexistent_user", "FAILED", 1.50, "Priya Sharma"),
        ("test_delete_user", "PASSED", 1.10, "Chandra Shekar"),
        ("test_put_update_user_full", "PASSED", 1.80, "Meera Patel"),
        ("test_patch_update_user_partial", "SKIPPED", 0.00, "Meera Patel"),
        ("test_login_success", "PASSED", 1.05, "Chandra Shekar"),
        ("test_create_multiple_users", "FAILED", 3.20, "Priya Sharma"),
    ]

    for test_name, status, duration, executed_by in test_results:
        db.execute_query(
            "INSERT INTO test_results (test_name, status, duration_seconds, executed_by) VALUES (?, ?, ?, ?)",
            (test_name, status, duration, executed_by)
        )

    # 5. Verify the data
    print("\n[USERS TABLE]")
    print("-" * 70)
    rows = db.fetch_all("SELECT * FROM users")
    for row in rows:
        print(f"  ID: {row[0]} | {row[1]:20s} | {row[2]:25s} | {row[3]:15s} | {row[4]}")

    print(f"\n[TEST RESULTS TABLE]")
    print("-" * 70)
    rows = db.fetch_all("SELECT * FROM test_results")
    for row in rows:
        print(f"  ID: {row[0]} | {row[1]:35s} | {row[2]:8s} | {row[3]:.2f}s | {row[4]:20s} | {row[5]}")

    # 6. Show some SQL queries in action
    print(f"\n[QUERY] Users in QA Engineering department:")
    qa_users = db.fetch_all("SELECT name, role FROM users WHERE department = ?", ("QA Engineering",))
    for u in qa_users:
        print(f"  {u[0]} -- {u[1]}")

    print(f"\n[QUERY] Failed test results:")
    failed = db.fetch_all("SELECT test_name, executed_by FROM test_results WHERE status = ?", ("FAILED",))
    for f in failed:
        print(f"  FAIL: {f[0]} -- run by {f[1]}")

    print(f"\n[QUERY] Average test duration:")
    avg = db.fetch_all("SELECT AVG(duration_seconds) FROM test_results WHERE status = 'PASSED'")
    print(f"  Average duration of passed tests: {avg[0][0]:.2f} seconds")

    db.close()
    print("\nDatabase seeded successfully! File: automation_test.db")


if __name__ == "__main__":
    seed()
