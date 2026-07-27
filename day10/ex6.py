class Book:
    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def borrow_book(self):
        if self.copies > 0:
            self.copies -= 1
            print("Book Borrowed Successfully.")
        else:
            print("Book Currently Unavailable")

    def return_book(self):
        self.copies += 1
        print("Book Returned Successfully.")

    def display(self):
        print("\n----- Book Details -----")
        print("Book ID:", self.book_id)
        print("Title:", self.title)
        print("Author:", self.author)
        print("Available Copies:", self.copies)


book_id = input("Enter Book ID: ")
title = input("Enter Book Title: ")
author = input("Enter Author Name: ")
copies = int(input("Enter Available Copies: "))

book = Book(book_id, title, author, copies)

while True:
    print("\n===== Library Menu =====")
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. Display Availability")
    print("4. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        book.borrow_book()

    elif choice == 2:
        book.return_book()

    elif choice == 3:
        book.display()

    elif choice == 4:
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")