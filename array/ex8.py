ids = [101, 102, 103, 101, 104, 105, 102, 106]

duplicates = []

for i in ids:
    if ids.count(i) > 1 and i not in duplicates:
        duplicates.append(i)

print("Duplicate IDs:", duplicates)

unique = list(set(ids))

print("Unique IDs:", unique)