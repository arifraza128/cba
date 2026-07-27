class Employee:
    def __init__(self, emp_id, name, days_present):
        self.emp_id = emp_id
        self.name = name
        self.days_present = days_present

    def attendance_percentage(self):
        return (self.days_present / 5) * 100

    def display(self):
        print("\n----- Employee Details -----")
        print("Employee ID:", self.emp_id)
        print("Employee Name:", self.name)
        print("Days Present:", self.days_present)

        percentage = self.attendance_percentage()
        print("Attendance Percentage:", percentage, "%")

        if percentage >= 90:
            print("Excellent Attendance")
        elif percentage >= 75:
            print("Good Attendance")
        else:
            print("Needs Improvement")


emp_id = input("Enter Employee ID: ")
name = input("Enter Employee Name: ")
days = int(input("Enter Days Present (0-5): "))

emp = Employee(emp_id, name, days)
emp.display()