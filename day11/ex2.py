class Product:

    def __init__(self, pid, name, price, qty):
        self.pid = pid
        self.name = name
        self.price = price
        self.qty = qty

    def total(self):
        return self.price * self.qty


cart = []

n = int(input("Enter number of products: "))

for i in range(n):
    print("\nProduct", i + 1)

    pid = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    qty = int(input("Quantity: "))

    cart.append(Product(pid, name, price, qty))

grand_total = 0

print("\n----------- Invoice -----------")

for item in cart:
    item_total = item.total()
    grand_total += item_total

    print(item.pid, item.name, item.price, item.qty, item_total)

discount = 0

if grand_total > 5000:
    discount = grand_total * 0.15
elif grand_total > 3000:
    discount = grand_total * 0.10

final_amount = grand_total - discount

print("\nGrand Total :", grand_total)
print("Discount    :", discount)
print("Final Amount:", final_amount)
