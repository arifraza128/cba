from abc import ABC, abstractmethod
from datetime import datetime
import itertools

class User:
    _id_counter = itertools.count(1)

    def __init__(self, name, email, password):
        self.user_id = next(User._id_counter)
        self.name = name
        self.email = email
        self.__password = password
        self.is_logged_in = False

    def login(self, email, password):
        if self.email == email and self.__password == password:
            self.is_logged_in = True
            print(f"[LOGIN] {self.name} logged in successfully.")
            return True
        print("[LOGIN] Invalid credentials.")
        return False

    def logout(self):
        self.is_logged_in = False
        print(f"[LOGOUT] {self.name} logged out.")

    def __str__(self):
        return f"User(#{self.user_id}, {self.name})"

class Customer(User):
    def __init__(self, name, email, password, address):
        super().__init__(name, email, password)
        self.address = address
        self.orders = []

    def place_order(self, restaurant, item_names, coupon_code=None):
        if not self.is_logged_in:
            print("Please login before placing an order.")
            return None

        items = []
        for name in item_names:
            item = restaurant.get_menu_item(name)
            if item and item.is_available:
                items.append(item)
            else:
                print(f"  -> '{name}' not available, skipping.")

        if not items:
            print("No valid items to order.")
            return None

        order = Order(self, restaurant, items)
        if coupon_code:
            order.apply_coupon(coupon_code)
        self.orders.append(order)
        restaurant.receive_order(order)
        print(f"[ORDER] Order #{order.order_id} placed by {self.name}.")
        return order

    def cancel_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                order.cancel()
                return
        print("Order not found.")

    def track_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                print(f"Order #{order_id} status: {order.status}")
                return order.status
        print("Order not found.")

class MenuItem:
    def __init__(self, name, price, category="General"):
        self.name = name
        self.price = price
        self.category = category
        self.is_available = True

    def update_price(self, new_price):
        self.price = new_price

    def __str__(self):
        return f"{self.name} (Rs.{self.price})"

class Restaurant:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.menu = {}
        self.incoming_orders = []

    def add_menu_item(self, item: MenuItem):
        self.menu[item.name] = item
        print(f"[MENU] {self.name} added '{item.name}'.")

    def update_menu_item(self, name, price=None, available=None):
        item = self.menu.get(name)
        if not item:
            print("Item not found.")
            return
        if price is not None:
            item.update_price(price)
        if available is not None:
            item.is_available = available
        print(f"[MENU] Updated '{name}'.")

    def get_menu_item(self, name):
        return self.menu.get(name)

    def receive_order(self, order):
        self.incoming_orders.append(order)

    def update_order_status(self, order_id, status):
        for order in self.incoming_orders:
            if order.order_id == order_id:
                order.update_status(status)
                return
        print("Order not found in restaurant queue.")

class Coupon:
    CODES = {
        "WELCOME50": 0.50,
        "SAVE10": 0.10,
        "FEST20": 0.20,
    }

    @classmethod
    def get_discount(cls, code):
        return cls.CODES.get(code.upper(), 0.0)

class Order:
    _id_counter = itertools.count(1001)
    GST_RATE = 0.05
    DELIVERY_CHARGE = 40
    FREE_DELIVERY_ABOVE = 500
    STATUS_FLOW = ["PLACED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED"]

    def __init__(self, customer: Customer, restaurant: Restaurant, items):
        self.order_id = next(Order._id_counter)
        self.__customer = customer
        self.__restaurant = restaurant
        self.__items = list(items)
        self.__discount_pct = 0.0
        self.status = "PLACED"
        self.timestamp = datetime.now()
        self.payment = None

    def get_items(self):
        return list(self.__items)

    def get_customer(self):
        return self.__customer

    def apply_coupon(self, code):
        pct = Coupon.get_discount(code)
        if pct:
            self.__discount_pct = pct
            print(f"[COUPON] '{code}' applied: {int(pct * 100)}% off.")
        else:
            print(f"[COUPON] '{code}' invalid.")

    def subtotal(self):
        return sum(i.price for i in self.__items)

    def generate_bill(self):
        sub = self.subtotal()
        discount = sub * self.__discount_pct
        after_discount = sub - discount
        gst = after_discount * self.GST_RATE
        delivery = 0 if after_discount >= self.FREE_DELIVERY_ABOVE else self.DELIVERY_CHARGE
        total = after_discount + gst + delivery

        print(f"\n----- BILL: Order #{self.order_id} -----")
        for i in self.__items:
            print(f"  {i.name:<20} Rs.{i.price:.2f}")
        print(f"  Subtotal:            Rs.{sub:.2f}")
        print(f"  Discount:           -Rs.{discount:.2f}")
        print(f"  GST (5%):            Rs.{gst:.2f}")
        print(f"  Delivery charge:     Rs.{delivery:.2f}")
        print(f"  TOTAL:               Rs.{total:.2f}")
        print("-----------------------------------")
        return round(total, 2)

    def update_status(self, status):
        if status in self.STATUS_FLOW:
            self.status = status
            print(f"[STATUS] Order #{self.order_id} -> {status}")

    def cancel(self):
        if self.status == "PLACED":
            self.status = "CANCELLED"
            print(f"[CANCEL] Order #{self.order_id} cancelled successfully.")
        else:
            print(f"[CANCEL] Cannot cancel - order already {self.status}.")

    def pay(self, payment_method: "Payment"):
        amount = self.generate_bill()
        self.payment = payment_method
        payment_method.pay(amount)

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(Payment):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        print(f"[PAYMENT] Rs.{amount:.2f} paid via Credit Card ending {self.card_number[-4:]}.")

class UPIPayment(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        print(f"[PAYMENT] Rs.{amount:.2f} paid via UPI ({self.upi_id}).")

class CashOnDelivery(Payment):
    def pay(self, amount):
        print(f"[PAYMENT] Rs.{amount:.2f} to be collected as Cash on Delivery.")

if __name__ == "__main__":
    restaurant = Restaurant("Spice Villa", "MG Road")
    restaurant.add_menu_item(MenuItem("Paneer Butter Masala", 220))
    restaurant.add_menu_item(MenuItem("Butter Naan", 40))
    restaurant.add_menu_item(MenuItem("Gulab Jamun", 60))
    restaurant.update_menu_item("Butter Naan", price=45)

    alice = Customer("Alice", "alice@mail.com", "pass123", "12 Park Street")
    alice.login("alice@mail.com", "pass123")

    order1 = alice.place_order(
        restaurant, ["Paneer Butter Masala", "Butter Naan"], coupon_code="SAVE10"
    )
    order2 = alice.place_order(restaurant, ["Gulab Jamun"])

    restaurant.update_order_status(order1.order_id, "PREPARING")
    alice.track_order(order1.order_id)

    order1.pay(UPIPayment("alice@upi"))
    order2.pay(CashOnDelivery())

    alice.cancel_order(order2.order_id)
