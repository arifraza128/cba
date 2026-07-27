marks = [65, 80, 92, 74, 88, 56, 79, 95, 68, 83]

print("Marks:", marks)

topper = max(marks)
average = sum(marks) / len(marks)

count = 0
for mark in marks:
    if mark > 75:
        count += 1

print("Topper:", topper)
print("Average:", average)
print("Students Above 75:", count)