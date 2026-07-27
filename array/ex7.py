attendance = ['P', 'A', 'P', 'P', 'A', 'P', 'P', 'A', 'P', 'P']

present = attendance.count('P')
absent = attendance.count('A')

percentage = (present / len(attendance)) * 100

print("Present:", present)
print("Absent:", absent)
print("Attendance %:", percentage)