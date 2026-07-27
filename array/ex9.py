expenses = [800, 1200, 650, 900, 1500, 1100, 700]

print("Total Expense:", sum(expenses))

maximum = max(expenses)
day = expenses.index(maximum) + 1

print("Maximum Expense:", maximum)
print("Day:", day)

average = sum(expenses) / len(expenses)

count = 0
for e in expenses:
    if e > 1000:
        count += 1

print("Average:", average)
print("Days Above 1000:", count)