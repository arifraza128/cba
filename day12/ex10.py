product_ids = [101, 102, 103, 104]

product_names = [
    "Keyboard",
    "Mouse",
    "Monitor",
    "Laptop"
]

prices = {
    101: 700,
    102: 500,
    103: 12000,
    104: 55000
}

pid = int(input("Enter Product ID to Search: "))

if pid in prices:
    index = product_ids.index(pid)

    print("Product:", product_names[index])
    print("Price:", prices[pid])

else:
    print("Product Not Found")

pid = int(input("\nEnter Product ID to Update Price: "))

if pid in prices:
    prices[pid] = float(input("New Price: "))

print("\nProducts Costing More Than Rs1000")

for pid in product_ids:
    if prices[pid] > 1000:
        index = product_ids.index(pid)
        print(product_names[index], "-", prices[pid])

average = sum(prices.values()) / len(prices)

print("\nAverage Product Price:", average)