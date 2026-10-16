from datetime import datetime
from decimal import Decimal
from employee import PermanentEmployee, ContractEmployee

class PayrollSystem:
    """Stores employees and prepares payroll summaries and payslips."""
    def __init__(self, storage):
        self.__employees = {}
        self.__payslips = []
        self.__storage = storage

    def add_employee(self, employee_id, name, department, basic, allowances, deductions, employee_type="permanent"):
        employee_id = employee_id.strip()
        if employee_id in self.__employees:
            raise ValueError("That employee ID already exists.")
        kind = employee_type.strip().lower()
        if kind == "permanent":
            employee = PermanentEmployee(employee_id, name, department, basic, allowances, deductions)
        elif kind == "contract":
            employee = ContractEmployee(employee_id, name, department, basic, allowances, deductions)
        else:
            raise ValueError("Employee type must be permanent or contract.")
        self.__employees[employee.employee_id] = employee
        self.save_data()
        return employee

    def get_employee(self, employee_id):
        employee_id = employee_id.strip()
        if employee_id not in self.__employees:
            raise KeyError("Employee not found. Check the ID.")
        return self.__employees[employee_id]

    def display_employees(self):
        if not self.__employees:
            print("No employees found.")
            return
        print("\n--- Employee List ---")
        for employee in self.__employees.values():
            print(employee.get_details())

    def search_employee(self, query):
        query = query.strip().lower()
        matches = [employee for employee in self.__employees.values()
                   if query == employee.employee_id.lower()
                   or query in employee.name.lower()]
        if not matches:
            print("No matching employee found.")
            return
        for employee in matches:
            print(employee.get_details())

    def generate_payslip(self, employee_id):
        employee = self.get_employee(employee_id)
        payslip = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "employee_type": employee.employee_type,
            "basic_salary": f"{employee.basic_salary:.2f}",
            "allowances": f"{employee.allowances:.2f}",
            "gross_salary": f"{employee.gross_salary:.2f}",
            "deductions": f"{employee.deductions:.2f}",
            "net_salary": f"{employee.net_salary:.2f}",
        }
        self.__payslips.append(payslip)
        self.save_data()
        return (
            "========== PAYSLIP ==========\n"
            f"Generated: {payslip['generated_at']}\n"
            f"Employee ID: {payslip['employee_id']}\n"
            f"Name: {payslip['name']}\n"
            f"Department: {payslip['department']}\n"
            f"Employee type: {payslip['employee_type']}\n"
            f"Basic salary: Rs. {payslip['basic_salary']}\n"
            f"Allowances: Rs. {payslip['allowances']}\n"
            f"Gross salary: Rs. {payslip['gross_salary']}\n"
            f"Deductions: Rs. {payslip['deductions']}\n"
            f"NET SALARY: Rs. {payslip['net_salary']}\n"
            "============================="
        )

    def display_payslips(self):
        if not self.__payslips:
            print("No payslips saved.")
            return
        for slip in self.__payslips:
            print(f"{slip['generated_at']} | {slip['employee_id']} | "
                  f"{slip['name']} | Net: Rs. {slip['net_salary']}")

    def save_data(self):
        self.__storage.save_employees(list(self.__employees.values()))
        self.__storage.save_payslips(self.__payslips)

    def load_data(self):
        employees, payslips = self.__storage.load_all()
        for row in employees:
            cls = PermanentEmployee if row["employee_type"].lower() == "permanent" else ContractEmployee
            employee = cls(
                row["employee_id"], row["name"], row["department"],
                Decimal(row["basic_salary"]), Decimal(row["allowances"]),
                Decimal(row["deductions"]),
            )
            self.__employees[employee.employee_id] = employee
        self.__payslips = payslips
