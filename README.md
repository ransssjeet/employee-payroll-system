# Bleep Project 04 — Employee Payroll System

A beginner-friendly Python console project using OOP to manage employee records and prepare salary summaries/payslips.

## Features
- Add employees
- Calculate gross and net salary
- Generate payslips
- Search employees by ID or name
- Display employee list and saved payslips
- Save and reload data using CSV files
- Validate values and handle common errors

## Salary formula
- Gross salary = Basic salary + Allowances
- Net salary = Gross salary - Deductions

This is a simple educational formula; it does not calculate statutory taxes or benefits.

## OOP concepts
- Classes and objects: `Employee`, `PermanentEmployee`, `ContractEmployee`, `PayrollSystem`, `CSVStorage`
- Encapsulation: private employee attributes
- Inheritance: permanent and contract employee classes inherit from `Employee`
- Abstraction: `Employee` uses `ABC` and `@abstractmethod`
- Polymorphism: employee types provide their own `employee_type`
- File handling: CSV reads/writes
- Exception handling: validation errors are caught in the menu

## Run
Requires Python 3.10 or newer and no third-party packages.

```bash
python main.py
```

Employee and payslip data are stored under `data/`. This is an educational example, not production payroll software.
