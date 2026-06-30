class Employer():
    __next_id = 1000

    def __init__(self):
        self.id = Employer.__next_id
        Employer.__next_id += 1

    @classmethod
    def get_next_id(cls):
        return cls.__next_id
    
    @classmethod
    def create_employee(cls, name, role):
        
        if role.lower() == "manager":
            return Manager(name)
        elif role.lower() == "intern":
            return Intern(name)
        elif role.lower() == "qa engineer":
            return QAEngineer(name)
        else:
            return Employee(name)

class Employee(Employer):
    def __init__(self, name, role="Employee"):
        super().__init__()
        self.name = name
        self.role = role

    def employee_details(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Role": self.role
        }

    def work(self):
        return f"{self.name} is working..."

class Manager(Employee):
    def __init__(self, name):
        super().__init__(name, "Manager")
        self.team = []

    def add_member(self):
        self.team.append(Employee.name)

    def work(self):
        return f"{self.name} is managing team"

    def employee_details(self):
        details = super().employee_details()
        details["Team"] = self.team
        return details

class QAEngineer(Employee):
    def __init__(self, name):
        super().__init__(name, "QA Engineer")
        self.tools = ["Python", "Pytest"]

    def work(self):
        return f"{self.name} is testing..."

    def employee_details(self):
        details = super().employee_details()
        details["Tools"] = self.tools
        return details

class Intern(Employee):
    def __init__(self, name):
        super().__init__(name, "Intern")
        self.duration = "6 months"

    def work(self):
        return f"{self.name} is learning..."

    def employee_details(self):
        details = super().employee_details()
        details["Duration"] = self.duration
        return details

emp1 = Employer.create_employee("John", "Developer")
emp2 = Employer.create_employee("Jane", "QA Engineer")
emp3 = Employer.create_employee("Bob", "Manager")
emp4 = Employer.create_employee("Alice", "Intern")

print(emp1.employee_details())
print("-" * 30)
print(emp2.employee_details())
print("-" * 30)
print(emp3.employee_details())
print("-" * 30)
print(emp4.employee_details())

all_employees = [emp1, emp2, emp3, emp4]
for emp in all_employees:
    print(emp.work())



