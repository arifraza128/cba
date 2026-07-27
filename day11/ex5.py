class Student:

    def __init__(self, roll, name, marks):
        self.roll = roll
        self.name = name
        self.marks = marks

    def total(self):
        return sum(self.marks)

    def percentage(self):
        return self.total() / 5

    def grade(self):
        per = self.percentage()

        if per >= 90:
            return "A"
        elif per >= 80:
            return "B"
        elif per >= 70:
            return "C"
        elif per >= 60:
            return "D"
        else:
            return "F"

    def report(self):
        print("\n------ Report Card ------")
        print("Roll No    :", self.roll)
        print("Name       :", self.name)
        print("Marks      :", self.marks)
        print("Total      :", self.total())
        print("Percentage :", self.percentage())
        print("Grade      :", self.grade())


roll = input("Roll Number: ")
name = input("Student Name: ")

marks = []

for i in range(5):
    marks.append(float(input(f"Subject {i+1} Marks: ")))

student = Student(roll, name, marks)

student.report()
