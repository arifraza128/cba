temps = [30, 32, 29, 35, 31, 33, 28]

highest = max(temps)
lowest = min(temps)
average = sum(temps) / len(temps)

count = 0
for t in temps:
    if t > average:
        count += 1

print("Temperatures:", temps)
print("Highest:", highest)
print("Lowest:", lowest)
print("Average:", average)
print("Days Above Average:", count)