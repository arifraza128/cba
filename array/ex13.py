sales1 = [100, 120, 140, 130, 150, 170]
sales2 = [90, 130, 135, 145, 140, 180]

for i in range(len(sales1)):
    if sales1[i] > sales2[i]:
        print("Month", i + 1, ": Salesperson 1")
    elif sales2[i] > sales1[i]:
        print("Month", i + 1, ": Salesperson 2")
    else:
        print("Month", i + 1, ": Equal")

print("Annual Sales 1:", sum(sales1))
print("Annual Sales 2:", sum(sales2))