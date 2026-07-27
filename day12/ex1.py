marks = []

n = int(input("Enter number of students: "))

for i in range(n):
    mark = int(input(f"Enter mark {i+1}: "))
    marks.append(mark)

print("\nAll Marks:")
for mark in marks:
    print(mark)

print("Highest Mark:", max(marks))
print("Lowest Mark:", min(marks))
print("Average Marks:", sum(marks) / len(marks))