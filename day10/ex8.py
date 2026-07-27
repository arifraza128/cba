class MovieTicket:
    def __init__(self, customer_name, movie_name, tickets, ticket_price):
        self.customer_name = customer_name
        self.movie_name = movie_name
        self.tickets = tickets
        self.ticket_price = ticket_price

    def booking_summary(self):
        total = self.tickets * self.ticket_price

        if self.tickets >= 5:
            discount = total * 0.15
        elif self.tickets >= 3:
            discount = total * 0.10
        else:
            discount = 0

        final_bill = total - discount

        print("\n------ Booking Summary ------")
        print("Customer Name :", self.customer_name)
        print("Movie Name    :", self.movie_name)
        print("Tickets       :", self.tickets)
        print("Ticket Price  : ₹", self.ticket_price)
        print("Total Bill    : ₹", total)
        print("Discount      : ₹", discount)
        print("Final Bill    : ₹", final_bill)


customer = input("Enter Customer Name: ")
movie = input("Enter Movie Name: ")
tickets = int(input("Enter Number of Tickets: "))
price = float(input("Enter Ticket Price: "))

ticket = MovieTicket(customer, movie, tickets, price)
ticket.booking_summary()