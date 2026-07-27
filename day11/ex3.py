class Book:

    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def issue_book(self):
        if self.copies > 0:
            self.copies -= 1
            print("Book Issued Successfully")
        else:
            print("Book Not Available")

    def return_book(self):
        self.copies += 1
        print("Book Returned Successfully")

    def display(self):
        print("\nBook ID :", self.book_id)
        print("Title   :", self.title)
        print("Author  :", self.author)
        print("Copies  :", self.copies)


book = Book(
    input("Book ID: "),
    input("Title: "),
    input("Author: "),
    int(input("Available Copies: "))
)

book.display()

choice = int(input("\n1.Issue Book\n2.Return Book\nEnter Choice: "))

if choice == 1:
    book.issue_book()
elif choice == 2:
    book.return_book()

book.display()
