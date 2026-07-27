from abc import ABC, abstractmethod
from datetime import datetime
import itertools

class SeatAlreadyBookedError(Exception):
    pass

class User:
    _id_counter = itertools.count(1)

    def __init__(self, name, email):
        self.user_id = next(User._id_counter)
        self.name = name
        self.email = email

class Customer(User):
    def __init__(self, name, email, age=25, is_student=False):
        super().__init__(name, email)
        self.age = age
        self.is_student = is_student
        self.bookings = []

class Seat:
    def __init__(self, seat_no, seat_type="Normal"):
        self.seat_no = seat_no
        self.seat_type = seat_type
        self.__is_booked = False

    def is_available(self):
        return not self.__is_booked

    def book(self):
        if self.__is_booked:
            raise SeatAlreadyBookedError(f"Seat {self.seat_no} is already booked!")
        self.__is_booked = True

    def release(self):
        self.__is_booked = False

    def __str__(self):
        status = "BOOKED" if self.__is_booked else "OPEN"
        return f"{self.seat_no}({self.seat_type})[{status}]"

class Screen:
    def __init__(self, screen_no, rows=5, cols=6):
        self.screen_no = screen_no
        self.seats = {}
        for r in range(rows):
            row_letter = chr(65 + r)
            seat_type = "Premium" if r < 2 else "Normal"
            for c in range(1, cols + 1):
                seat_no = f"{row_letter}{c}"
                self.seats[seat_no] = Seat(seat_no, seat_type)
        self.showtimes = {}

    def schedule_show(self, showtime, movie):
        self.showtimes[showtime] = movie

    def available_seats(self):
        return [s for s in self.seats.values() if s.is_available()]

    def display_seats(self):
        print(f"\nScreen {self.screen_no} seat map:")
        rows = {}
        for seat in self.seats.values():
            rows.setdefault(seat.seat_no[0], []).append(seat)
        for row_letter in sorted(rows):
            print("  " + "  ".join(str(s) for s in rows[row_letter]))

class Theater:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.screens = []

    def add_screen(self, screen: Screen):
        self.screens.append(screen)

class Movie:
    def __init__(self, title, duration_min, genre, base_price=200):
        self.title = title
        self.duration_min = duration_min
        self.genre = genre
        self.base_price = base_price

    def __str__(self):
        return f"{self.title} ({self.genre}, {self.duration_min} min)"

class PricingEngine:
    SEAT_TYPE_MULTIPLIER = {"Normal": 1.0, "Premium": 1.5, "Recliner": 2.0}

    @staticmethod
    def calculate_price(movie: Movie, seat: Seat, showtime: str, customer: Customer):
        price = movie.base_price * PricingEngine.SEAT_TYPE_MULTIPLIER.get(seat.seat_type, 1.0)
        hour = int(showtime.split(":")[0])
        if 18 <= hour <= 22:
            price *= 1.2
        if customer.is_student:
            price *= 0.85
        elif customer.age >= 60:
            price *= 0.80
        return round(price, 2)

class Booking:
    _id_counter = itertools.count(7001)

    def __init__(self, customer, movie, screen, showtime, seats):
        self.booking_id = next(Booking._id_counter)
        self.customer = customer
        self.movie = movie
        self.screen = screen
        self.showtime = showtime
        self.seats = seats
        self.total_amount = 0.0
        self.status = "PENDING_PAYMENT"
        self.timestamp = datetime.now()

    def confirm(self, payment: "Payment"):
        self.total_amount = sum(
            PricingEngine.calculate_price(self.movie, s, self.showtime, self.customer)
            for s in self.seats
        )
        payment.pay(self.total_amount)
        self.status = "CONFIRMED"
        self.generate_ticket()

    def cancel(self):
        for seat in self.seats:
            seat.release()
        self.status = "CANCELLED"
        print(f"[CANCEL] Booking #{self.booking_id} cancelled, seats released.")

    def generate_ticket(self):
        print("\n========== E-TICKET ==========")
        print(f" Booking ID : {self.booking_id}")
        print(f" Movie      : {self.movie}")
        print(f" Screen     : {self.screen.screen_no}")
        print(f" Showtime   : {self.showtime}")
        print(f" Customer   : {self.customer.name}")
        print(f" Seats      : {', '.join(s.seat_no for s in self.seats)}")
        print(f" Amount Paid: Rs.{self.total_amount:.2f}")
        print("===============================")

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CardPayment(Payment):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        print(f"[PAYMENT] Rs.{amount:.2f} charged to card ending {self.card_number[-4:] }.")

class WalletPayment(Payment):
    def __init__(self, wallet_name):
        self.wallet_name = wallet_name

    def pay(self, amount):
        print(f"[PAYMENT] Rs.{amount:.2f} paid via {self.wallet_name} wallet.")

class BookingService:
    @staticmethod
    def book_tickets(customer, screen, showtime, seat_numbers):
        movie = screen.showtimes.get(showtime)
        if not movie:
            print("No movie scheduled at that showtime.")
            return None

        selected_seats = []
        try:
            for seat_no in seat_numbers:
                seat = screen.seats.get(seat_no)
                if not seat:
                    raise ValueError(f"Seat {seat_no} does not exist.")
                if not seat.is_available():
                    raise SeatAlreadyBookedError(f"Seat {seat_no} is already booked!")
                selected_seats.append(seat)

            for seat in selected_seats:
                seat.book()

            booking = Booking(customer, movie, screen, showtime, selected_seats)
            customer.bookings.append(booking)
            print(f"[BOOKING] Seats {seat_numbers} locked for {customer.name}.")
            return booking
        except (SeatAlreadyBookedError, ValueError) as e:
            print(f"[ERROR] Booking failed: {e}")
            return None

if __name__ == "__main__":
    theater = Theater("PVR Cinemas", "Bengaluru")
    screen1 = Screen(screen_no=1, rows=4, cols=6)

    movie = Movie("Interstellar Odyssey", 150, "Sci-Fi", base_price=250)
    screen1.schedule_show("19:00", movie)
    theater.add_screen(screen1)

    screen1.display_seats()

    alice = Customer("Alice", "alice@mail.com", age=22, is_student=True)
    bob = Customer("Bob", "bob@mail.com", age=65)

    print("\n--- Alice books seats A1, A2 ---")
    booking1 = BookingService.book_tickets(alice, screen1, "19:00", ["A1", "A2"])
    if booking1:
        booking1.confirm(CardPayment("4111111111111234"))

    print("\n--- Bob tries to book A1 (already booked) -> prevented ---")
    booking2 = BookingService.book_tickets(bob, screen1, "19:00", ["A1", "B1"])

    print("\n--- Bob books B1, B2 instead (senior discount applies) ---")
    booking3 = BookingService.book_tickets(bob, screen1, "19:00", ["B1", "B2"])
    if booking3:
        booking3.confirm(WalletPayment("Paytm"))

    print("\n--- Real-time seat availability ---")
    screen1.display_seats()
    print(f"Seats still available: {len(screen1.available_seats())}")

    print("\n--- Cancel Alice's booking (releases seats) ---")
    booking1.cancel()
    screen1.display_seats()
