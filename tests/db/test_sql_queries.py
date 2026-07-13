"""
Advanced SQL Interview Queries Test
===================================
This file demonstrates how to answer the most common SQL interview questions
using pytest to verify our answers are correct.
"""

import pytest
import logging

logger = logging.getLogger(__name__)




@pytest.mark.db
class TestAdvancedSQL:

    def test_second_highest_salary(self, db):
        """
        INTERVIEW QUESTION: "Find the second highest salary of an employee"
        
        Logic: 
        1. Find the MAX salary (which is 90000).
        2. Find the MAX salary of everyone earning LESS than 90000.
        """
        query = """
            SELECT MAX(salary) 
            FROM employees 
            WHERE salary < (SELECT MAX(salary) FROM employees)
        """
        
        logger.info("Executing: Second Highest Salary Query")
        results = db.fetch_all(query)
        
        second_highest = results[0][0]
        logger.info(f"The second highest salary is: {second_highest}")
        
        # We know from our seed data that Neha earns 85000, which is the 2nd highest.
        assert second_highest == 85000


    def test_find_duplicate_names(self, db):
        """
        INTERVIEW QUESTION: "Find duplicate employee names"
        
        Logic: 
        1. GROUP BY name (put everyone with the same name in a pile).
        2. COUNT the size of each pile.
        3. HAVING filters out piles that only have 1 person.
        """
        query = """
            SELECT name, COUNT(*) 
            FROM employees 
            GROUP BY name 
            HAVING COUNT(*) > 1
        """
        
        logger.info("Executing: Find Duplicate Names Query")
        results = db.fetch_all(query)
        
        logger.info(f"Duplicates found: {results}")
        
        # We know from our seed data that "Priya" is in there twice.
        assert len(results) == 1
        assert results[0][0] == "Priya"
        assert results[0][1] == 2


    def test_employees_earning_more_than_manager(self, db):
        """
        INTERVIEW QUESTION: "Find employees earning more than their manager"
        
        Logic: 
        This requires a SELF JOIN. We join the employees table to itself!
        'e' is the employee alias.
        'm' is the manager alias.
        """
        query = """
            SELECT e.name, e.salary, m.name, m.salary
            FROM employees e
            JOIN employees m ON e.manager_id = m.id
            WHERE e.salary > m.salary
        """
        
        logger.info("Executing: Employees > Manager Salary Query")
        results = db.fetch_all(query)
        
        logger.info(f"Employees earning more than manager: {results}")
        
        # In our data: Amit (Manager) earns 60000. Deepak (Manager Kavita) earns 65000 (Kavita 70000). 
        assert len(results) == 0


    def test_average_salary_per_department(self, db):
        """
        INTERVIEW QUESTION: "Find the average salary for each department name"
        
        Logic: 
        1. JOIN employees and departments so we have the department name.
        2. GROUP BY department name.
        3. AVG() calculates the average per group.
        """
        query = """
            SELECT d.dept_name, AVG(e.salary)
            FROM employees e
            JOIN departments d ON e.department_id = d.dept_id
            GROUP BY d.dept_name
        """
        
        logger.info("Executing: Average Salary per Department Query")
        results = db.fetch_all(query)
        
        for dept in results:
            logger.info(f"Department: {dept[0]}, Avg Salary: {dept[1]}")
            
        assert len(results) == 3 # Eng, HR, Marketing (Sales has 0 employees)
