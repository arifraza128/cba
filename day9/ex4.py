from abc import ABC, abstractmethod
import itertools

class Employee(ABC):
    _id_counter = itertools.count(1)

    def __init__(self, name):
        self.emp_id = next(Employee._id_counter)
        self.name = name

    @abstractmethod
    def calculate_salary(self):
        raise NotImplementedError

    @abstractmethod
    def calculate_tax(self, gross_salary):
        raise NotImplementedError

    def generate_salary_slip(self):
        gross = self.calculate_salary()
        tax = self.calculate_tax(gross)
        net = gross - tax
        print(f"\n===== SALARY SLIP: {self.name} (ID:{self.emp_id}) [{self.__class__.__name__}] =====")
        print(f"  Gross Salary : Rs.{gross:,.2f}")
        print(f"  Tax Deducted : Rs.{tax:,.2f}")
        print(f"  NET PAY      : Rs.{net:,.2f}")
        print("=" * 60)
        return net

class FullTimeEmployee(Employee):
    def __init__(self, name, monthly_basic, bonus=0.0, overtime_hours=0, overtime_rate=300):
        super().__init__(name)
        self.monthly_basic = monthly_basic
        self.bonus = bonus
        self.overtime_hours = overtime_hours
        self.overtime_rate = overtime_rate

    def calculate_salary(self):
        overtime_pay = self.overtime_hours * self.overtime_rate
        return self.monthly_basic + self.bonus + overtime_pay

    def calculate_tax(self, gross_salary):
        if gross_salary <= 25000:
            return 0.0
        elif gross_salary <= 50000:
            return (gross_salary - 25000) * 0.05
        elif gross_salary <= 100000:
            return 25000 * 0.05 + (gross_salary - 50000) * 0.10
        else:
            return 25000 * 0.05 + 50000 * 0.10 + (gross_salary - 100000) * 0.20

class PartTimeEmployee(Employee):
    def __init__(self, name, hourly_rate, hours_worked):
        super().__init__(name)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked

    def calculate_tax(self, gross_salary):
        if gross_salary <= 15000:
            return 0.0
        return (gross_salary - 15000) * 0.03

class Intern(Employee):
    def __init__(self, name, monthly_stipend):
        super().__init__(name)
        self.monthly_stipend = monthly_stipend

    def calculate_salary(self):
        return self.monthly_stipend

    def calculate_tax(self, gross_salary):
        return 0.0

class Payroll:
    def __init__(self, company_name):
        self.company_name = company_name
        self.employees = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)
        print(f"[PAYROLL] Added {employee.__class__.__name__}: {employee.name}")

    def run_payroll(self):
        print(f"\n########## PAYROLL RUN: {self.company_name} ##########")
        total_payout = 0.0
        for emp in self.employees:
            total_payout += emp.generate_salary_slip()
        print(f"\nTOTAL NET PAYOUT THIS CYCLE: Rs.{total_payout:,.2f}")
        return total_payout

if __name__ == "__main__":
    payroll = Payroll("TechNova Pvt Ltd")

    ft = FullTimeEmployee("Suresh", monthly_basic=60000, bonus=5000, overtime_hours=10, overtime_rate=350)
    pt = PartTimeEmployee("Meena", hourly_rate=400, hours_worked=80)
    intern = Intern("Kabir", monthly_stipend=15000)

    payroll.add_employee(ft)
    payroll.add_employee(pt)
    payroll.add_employee(intern)

    payroll.run_payroll()
