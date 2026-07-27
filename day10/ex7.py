class Order:
    def __init__(self, customer_name, food_item, quantity, price):
        self.customer_name = customer_name
        self.food_item = food_item
        self.quantity = quantity
        self.price = price

    def calculate_bill(self):
        total = self.quantity * self.price

        if total >= 800:
            delivery_charge = 0
            message = "Eligible for Free Delivery"
        else:
            delivery_charge = 60
            message = "Delivery Charge Applied"

        final_bill = total + delivery_charge

        print("\n------ Food Order Bill ------")
        print("Customer Name :", self.customer_name)
        print("Food Item     :", self.food_item)
        print("Quantity      :", self.quantity)
        print("Price         : ₹", self.price)
        print("Total         : ₹", total)
        print("Delivery      : ₹", delivery_charge)
        print("Final Bill    : ₹", final_bill)
        print(message)


customer = input("Enter Customer Name: ")
food = input("Enter Food Item: ")
quantity = int(input("Enter Quantity: "))
price = float(input("Enter Price per Item: "))

order = Order(customer, food, quantity, price)
order.calculate_bill()