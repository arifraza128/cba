class Product:
    def __init__(self, product_id, product_name, quantity, minimum_stock):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.minimum_stock = minimum_stock

    def sell_product(self, qty):
        if qty <= self.quantity:
            self.quantity -= qty
            print("Product Sold Successfully.")
        else:
            print("Cannot Sell! Insufficient Stock.")

    def restock_product(self, qty):
        self.quantity += qty
        print("Stock Updated Successfully.")

    def check_stock(self):
        print("\n------ Product Details ------")
        print("Product ID :", self.product_id)
        print("Product Name :", self.product_name)
        print("Available Quantity :", self.quantity)

        if self.quantity == 0:
            print("Status : Out of Stock")
        elif self.quantity <= self.minimum_stock:
            print("Status : Low Stock")
        else:
            print("Status : Stock Available")


product_id = input("Enter Product ID: ")
product_name = input("Enter Product Name: ")
quantity = int(input("Enter Available Quantity: "))
minimum_stock = int(input("Enter Minimum Stock Level: "))

product = Product(product_id, product_name, quantity, minimum_stock)

while True:
    print("\n===== Inventory Menu =====")
    print("1. Sell Product")
    print("2. Restock Product")
    print("3. Check Stock")
    print("4. Exit")

    choice = int(input("Enter Your Choice: "))

    if choice == 1:
        qty = int(input("Enter Quantity to Sell: "))
        product.sell_product(qty)

    elif choice == 2:
        qty = int(input("Enter Quantity to Restock: "))
        product.restock_product(qty)

    elif choice == 3:
        product.check_stock()

    elif choice == 4:
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")