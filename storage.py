
import csv
from pathlib import Path


class CSVStorage:
    EMPLOYEE_FIELDS = (
        "employee_id",
        "name",
        "department",
        "employee_type",
        "basic_salary",
        "allowances",
        "deductions",
    )

    PAYSLIP_FIELDS = (
        "generated_at",
        "employee_id",
        "name",
        "department",
        "employee_type",
        "basic_salary",
        "allowances",
        "gross_salary",
        "deductions",
        "net_salary",
    )


    def __init__(self, employees_file, payslips_file):
        self.__employees_path = Path(employees_file)
        self.__payslips_path = Path(payslips_file)

    def _read(self, path, fields):
        if not path.exists():
            return []
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                return []
            missing = set(fields) - set(reader.fieldnames)
            if missing:
                raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")
            return [{key: (row.get(key) or "").strip() for key in fields} for row in reader]

    def load_all(self):
        return (self._read(self.__employees_path, self.EMPLOYEE_FIELDS),
                self._read(self.__payslips_path, self.PAYSLIP_FIELDS))

    def save_employees(self, employees):
        self.__employees_path.parent.mkdir(parents=True, exist_ok=True)
        with self.__employees_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.EMPLOYEE_FIELDS)
            writer.writeheader()
            for employee in employees:
                writer.writerow({
                    "employee_id": employee.employee_id,
                    "name": employee.name,
                    "department": employee.department,
                    "employee_type": employee.employee_type.lower(),
                    "basic_salary": f"{employee.basic_salary:.2f}",
                    "allowances": f"{employee.allowances:.2f}",
                    "deductions": f"{employee.deductions:.2f}",
                })

    def save_payslips(self, payslips):
        self.__payslips_path.parent.mkdir(parents=True, exist_ok=True)
        with self.__payslips_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.PAYSLIP_FIELDS)
            writer.writeheader()
            writer.writerows(payslips)
