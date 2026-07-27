seats = [0] * 20

print("Available Seats:", seats.count(0))

seat = 5

if seats[seat - 1] == 0:
    seats[seat - 1] = 1
    print("Seat Booked")

seat = 5

if seats[seat - 1] == 1:
    seats[seat - 1] = 0
    print("Booking Cancelled")

print("Seat Status:", seats)