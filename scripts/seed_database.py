"""
Unified Database Seed Script
============================
This script creates a single realistic SQL database (automation_test.db) 
for all our testing needs (both basic CRUD and advanced SQL).

Tables created:
1. users (for basic CRUD tests in test_db.py)
2. departments (for advanced SQL joins)
3. employees (for advanced SQL queries)
"""
import os
import logging
import sys

# Add project root to path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_helper import DBHelper

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def seed_database():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "automation_test.db")
    db = DBHelper(db_name=db_path)
    
    logger.info("Dropping old tables if they exist...")
    db.execute_query("DROP TABLE IF EXISTS users")
    db.execute_query("DROP TABLE IF EXISTS employees")
    db.execute_query("DROP TABLE IF EXISTS departments")

    # ── Table 1: USERS (For test_db.py) ──
    db.execute_query('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    logger.info("Created 'users' table (empty by default for CRUD tests).")

    # ── Table 2: DEPARTMENTS (For test_sql_queries.py) ──
    db.execute_query('''
        CREATE TABLE departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL
        )
    ''')
    
    # ── Table 3: EMPLOYEES (For test_sql_queries.py) ──
    db.execute_query('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary INTEGER NOT NULL,
            manager_id INTEGER
        )
    ''')

    # Seed data for advanced queries
    departments_data = [
        (10, "Engineering"),
        (20, "HR"),
        (30, "Marketing"),
        (40, "Sales")  
    ]
    db.execute_query("INSERT INTO departments VALUES (?, ?)", departments_data, is_many=True)
    
    employees_data = [
        ("Ravi", 10, 90000, None),   
        ("Priya", 10, 75000, 1),     
        ("Amit", 20, 60000, 1),      
        ("Neha", 10, 85000, 1),      
        ("Suresh", 20, 55000, 3),    
        ("Kavita", 30, 70000, 1),    
        ("Deepak", 30, 65000, 6),    
        ("Priya", 20, 58000, 3)      
    ]
    db.execute_query(
        "INSERT INTO employees (name, department_id, salary, manager_id) VALUES (?, ?, ?, ?)", 
        employees_data,
        is_many=True
    )
    
    db.close()
    logger.info(f"Unified Database seeding complete at {db_path}!")

if __name__ == "__main__":
    seed_database()
