class ElectricityBill:
    def __init__(self, consumer_no, customer_name, units):
        self.consumer_no = consumer_no
        self.customer_name = customer_name
        self.units = units

    def calculate_bill(self):
        if self.units <= 100:
            amount = self.units * 5

        elif self.units <= 200:
            amount = (100 * 5) + ((self.units - 100) * 7)

        else:
            amount = (100 * 5) + (100 * 7) + ((self.units - 200) * 10)

        surcharge = 0

        if amount > 5000:
            surcharge = amount * 0.05

        final_bill = amount + surcharge

        print("\n------ Electricity Bill ------")
        print("Consumer Number :", self.consumer_no)
        print("Customer Name   :", self.customer_name)
        print("Units Consumed  :", self.units)
        print("Bill Amount     : ₹", amount)
        print("Surcharge       : ₹", surcharge)
        print("Final Bill      : ₹", final_bill)


consumer = input("Enter Consumer Number: ")
name = input("Enter Customer Name: ")
units = int(input("Enter Units Consumed: "))

bill = ElectricityBill(consumer, name, units)
bill.calculate_bill()