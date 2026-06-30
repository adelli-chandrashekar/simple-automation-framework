import logging
from library.emp_factory import Employer, Employee, Manager, QAEngineer, Intern

logger = logging.getLogger(__name__)

class TestEmployeeFactory:
    """Test the Factory Method Pattern implementation in Employer"""

    def test_factory_creates_correct_type(self):
        """Verify the factory method returns the correct subclass based on role"""
        logger.info("Starting factory type creation test")
        
        # Create one of each using the factory method
        manager = Employer.create_employee("Bob", "manager")
        qa = Employer.create_employee("Jane", "QA Engineer")
        intern = Employer.create_employee("Alice", "intern")
        dev = Employer.create_employee("John", "developer")

        # Check types
        assert isinstance(manager, Manager)
        logger.info("✅ Successfully created and verified Manager object")
        
        assert isinstance(qa, QAEngineer)
        logger.info("✅ Successfully created and verified QAEngineer object")
        
        assert isinstance(intern, Intern)
        logger.info("✅ Successfully created and verified Intern object")
        
        assert isinstance(dev, Employee)  # Default fallback
        assert type(dev) is Employee
        logger.info("✅ Successfully verified fallback to default Employee object")

    def test_employee_ids_are_unique_and_incrementing(self):
        """Verify that each employee gets a unique ID incremented from 1000"""
        logger.info("Starting unique ID increment test")
        
        emp1 = Employer.create_employee("Emp1", "test")
        logger.info(f"Created first employee with ID: {emp1.id}")
        
        emp2 = Employer.create_employee("Emp2", "test")
        logger.info(f"Created second employee with ID: {emp2.id}")
        
        assert emp1.id < emp2.id
        assert emp2.id == emp1.id + 1
        logger.info("✅ Successfully verified that IDs are unique and incrementing sequentially")

    def test_polymorphism_work_method(self):
        """Verify polymorphism — different subclasses have different work() behavior"""
        logger.info("Starting polymorphism work() method test")
        
        qa = Employer.create_employee("Jane", "qa engineer")
        intern = Employer.create_employee("Alice", "intern")
        manager = Employer.create_employee("Bob", "manager")

        assert qa.work() == "Jane is testing..."
        logger.info(f"✅ QAEngineer work(): '{qa.work()}'")
        
        assert intern.work() == "Alice is learning..."
        logger.info(f"✅ Intern work(): '{intern.work()}'")
        
        assert manager.work() == "Bob is managing team"
        logger.info(f"✅ Manager work(): '{manager.work()}'")

    def test_employee_details_format(self):
        """Verify that subclasses correctly extend the base employee_details()"""
        logger.info("Starting employee details dictionary format test")
        
        qa = Employer.create_employee("Jane", "qa engineer")
        details = qa.employee_details()
        logger.info(f"Generated QAEngineer details dictionary: {details}")
        
        # Check type
        assert isinstance(details, dict)
        
        # Should contain base details
        assert details.get("Name") == "Jane"
        assert details.get("Role") == "QA Engineer"
        logger.info("✅ Verified base Employee details (Name, Role)")
        
        # Should contain subclass specific details
        assert "Tools" in details
        assert "Python" in details["Tools"]
        logger.info("✅ Verified inherited subclass details (Tools list)")
