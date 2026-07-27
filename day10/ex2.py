class ShoppingCart:
    def __init__(self, customer_name, product_name, quantity, price):
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def calculate_bill(self):
        total = self.quantity * self.price

        if total > 10000:
            discount = total * 0.20
        elif total > 5000:
            discount = total * 0.10
        else:
            discount = 0

        final_bill = total - discount

        print("\n------ Shopping Bill ------")
        print("Customer:", self.customer_name)
        print("Product:", self.product_name)
        print("Quantity:", self.quantity)
        print("Price per Item:", self.price)
        print("Total Amount:", total)
        print("Discount:", discount)
        print("Final Bill:", final_bill)


customer = input("Enter Customer Name: ")
product = input("Enter Product Name: ")
quantity = int(input("Enter Quantity: "))
price = float(input("Enter Price per Item: "))

cart = ShoppingCart(customer, product, quantity, price)
cart.calculate_bill()