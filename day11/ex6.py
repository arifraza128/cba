class Vehicle:

    def __init__(self, vid, name, vtype, price):
        self.vid = vid
        self.name = name
        self.vtype = vtype
        self.price = price

    def bill(self, days):

        total = self.price * days

        discount = 0

        if days > 10:
            discount = total * 0.20

        elif days > 5:
            discount = total * 0.10

        final = total - discount

        return total, discount, final


vehicles = []

n = int(input("Enter Number of Vehicles: "))

overall = 0

for i in range(n):

    print("\nVehicle", i + 1)

    vid = input("Vehicle ID: ")
    name = input("Vehicle Name: ")
    vtype = input("Vehicle Type: ")
    price = float(input("Rental Price Per Day: "))
    days = int(input("Rental Days: "))

    vehicle = Vehicle(vid, name, vtype, price)

    total, discount, final = vehicle.bill(days)

    overall += final

    print("\nVehicle Bill")
    print("Vehicle :", name)
    print("Total   :", total)
    print("Discount:", discount)
    print("Payable :", final)

print("\nOverall Amount to Pay:", overall)
