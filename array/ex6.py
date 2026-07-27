stock = [25, 5, 18, 8, 50, 12, 4]

print("Products Below 10:")

for qty in stock:
    if qty < 10:
        print(qty)

print("Total Inventory:", sum(stock))
print("Maximum Stock:", max(stock))