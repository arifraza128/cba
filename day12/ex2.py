months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

sales = []

for month in months:
    amount = int(input(f"Enter sales for {month}: "))
    sales.append(amount)

print("\nTotal Annual Sales:", sum(sales))

max_sale = max(sales)
min_sale = min(sales)

print("Highest Sales:", months[sales.index(max_sale)], "-", max_sale)
print("Lowest Sales:", months[sales.index(min_sale)], "-", min_sale)

print("\nMonths with Sales above Rs50000")

for i in range(len(sales)):
    if sales[i] > 50000:
        print(months[i], sales[i])