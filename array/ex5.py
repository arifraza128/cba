runs = [45, 67, 0, 102, 88, 12, 56, 0, 75, 41, 63, 99, 28, 0, 51]

print("Total Runs:", sum(runs))
print("Highest Score:", max(runs))

half = 0
duck = 0

for run in runs:
    if run >= 50:
        half += 1
    if run == 0:
        duck += 1

print("Half Centuries:", half)
print("Ducks:", duck)