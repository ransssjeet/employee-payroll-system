
from abc import ABC, abstractmethod
from decimal import Decimal


class Employee(ABC):
    """Abstract base class for employee types."""

    def __init__(
        self,
        employee_id,
        name,
        department,
        basic_salary,
        allowances,
        deductions,
    ):
        employee_id = employee_id.strip()
        name = name.strip()
        department = department.strip()

        if not employee_id:
            raise ValueError("Employee ID cannot be blank.")

        if not name:
            raise ValueError("Employee name cannot be blank.")

        if not department:
            raise ValueError("Department cannot be blank.")

        if basic_salary <= 0:
            raise ValueError("Basic salary must be greater than zero.")

        if allowances < 0 or deductions < 0:
            raise ValueError("Allowances and deductions cannot be negative.")

        self.__employee_id = employee_id
        self.__name = name
        self.__department = department
        self.__basic_salary = basic_salary.quantize(Decimal("0.01"))
        self.__allowances = allowances.quantize(Decimal("0.01"))
        self.__deductions = deductions.quantize(Decimal("0.01"))

    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def name(self):
        return self.__name

    @property
    def department(self):
        return self.__department

    @property
    def basic_salary(self):
        return self.__basic_salary

    @property
    def allowances(self):
        return self.__allowances

    @property
    def deductions(self):
        return self.__deductions

    @property
    def gross_salary(self):
        return self.__basic_salary + self.__allowances

    @property
    def net_salary(self):
        return self.gross_salary - self.__deductions

    @property
    @abstractmethod
    def employee_type(self):
        """Each concrete employee class must provide its type."""

    def get_details(self):
        return (
            f"{self.employee_type} | {self.employee_id} | "
            f"{self.name} | {self.department} | "
            f"Net salary: Rs. {self.net_salary:.2f}"
        )


class PermanentEmployee(Employee):
    @property
    def employee_type(self):
        return "Permanent"


class ContractEmployee(Employee):
    @property
    def employee_type(self):
        return "Contract"
