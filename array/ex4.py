salaries = [45000, 52000, 60000, 39000, 70000]

updated = []

for salary in salaries:
    updated.append(salary * 1.10)

print("Updated Salaries:", updated)

print("Above 50000:")
for salary in updated:
    if salary > 50000:
        print(salary)