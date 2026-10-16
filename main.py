from decimal import Decimal, InvalidOperation
from payroll import PayrollSystem
from storage import CSVStorage

def read_money(prompt):
    while True:
        try:
            amount = Decimal(input(prompt).strip())
            if not amount.is_finite() or amount < 0:
                print("Enter a valid amount (zero or greater).")
            elif amount != amount.quantize(Decimal("0.01")):
                print("Use no more than two decimal places.")
            else:
                return amount
        except InvalidOperation:
            print("Invalid amount. Example: 25000 or 25000.50")

def main():
    storage = CSVStorage("data/employees.csv", "data/payslips.csv")
    payroll = PayrollSystem(storage)
    payroll.load_data()

    while True:
        print("\n========== EMPLOYEE PAYROLL SYSTEM ==========")
        print("1. Add employee")
        print("2. Display all employees")
        print("3. Search employee")
        print("4. Calculate salary")
        print("5. Generate payslip")
        print("6. View saved payslips")
        print("7. Save data")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                employee_id = input("Employee ID: ").strip()
                name = input("Employee name: ").strip()
                department = input("Department: ").strip()
                basic = read_money("Basic salary: Rs. ")
                allowance = read_money("Allowances: Rs. ")
                deduction = read_money("Deductions: Rs. ")
                payroll.add_employee(employee_id, name, department, basic, allowance, deduction)
                print("Employee added successfully.")
            elif choice == "2":
                payroll.display_employees()
            elif choice == "3":
                query = input("Enter employee ID or name: ").strip()
                payroll.search_employee(query)
            elif choice == "4":
                employee_id = input("Employee ID: ").strip()
                employee = payroll.get_employee(employee_id)
                print(f"Employee: {employee.name}")
                print(f"Gross salary: Rs. {employee.gross_salary:.2f}")
                print(f"Total deductions: Rs. {employee.deductions:.2f}")
                print(f"Net salary: Rs. {employee.net_salary:.2f}")
            elif choice == "5":
                employee_id = input("Employee ID: ").strip()
                payslip = payroll.generate_payslip(employee_id)
                print("\n" + payslip)
            elif choice == "6":
                payroll.display_payslips()
            elif choice == "7":
                payroll.save_data()
                print("Data saved.")
            elif choice == "0":
                payroll.save_data()
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a listed option.")
        except (ValueError, KeyError, OSError) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
