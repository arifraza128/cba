class Employee:
    def __init__(self, emp_id, name, department, working_days, present_days):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.working_days = working_days
        self.present_days = present_days

    def attendance_percentage(self):
        return (self.present_days / self.working_days) * 100

    def attendance_status(self):
        percentage = self.attendance_percentage()

        if percentage >= 90:
            return "Excellent"
        elif percentage >= 75:
            return "Good"
        else:
            return "Needs Improvement"

    def display(self):
        print("\n------ Employee Report ------")
        print("Employee ID :", self.emp_id)
        print("Name        :", self.name)
        print("Department  :", self.department)
        print("Working Days:", self.working_days)
        print("Present Days:", self.present_days)
        print("Attendance  : {:.2f}%".format(self.attendance_percentage()))
        print("Status      :", self.attendance_status())


emp = Employee(
    input("Employee ID: "),
    input("Name: "),
    input("Department: "),
    int(input("Working Days: ")),
    int(input("Present Days: "))
)

emp.display()
