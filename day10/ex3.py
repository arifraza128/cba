class Student:
    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks

    def calculate_total(self):
        return sum(self.marks)

    def calculate_average(self):
        return self.calculate_total() / len(self.marks)

    def calculate_grade(self):
        avg = self.calculate_average()

        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "F"

    def display_report(self):
        print("\n------ Report Card ------")
        print("Roll Number:", self.roll_no)
        print("Student Name:", self.name)

        for i in range(5):
            print(f"Subject {i+1}: {self.marks[i]}")

        print("Total Marks:", self.calculate_total())
        print("Average:", self.calculate_average())
        print("Grade:", self.calculate_grade())


roll = input("Enter Roll Number: ")
name = input("Enter Student Name: ")

marks = []
for i in range(5):
    mark = float(input(f"Enter Marks of Subject {i+1}: "))
    marks.append(mark)

student = Student(roll, name, marks)
student.display_report()