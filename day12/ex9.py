book_ids = [101, 102, 103]

book_titles = [
    "Python",
    "Java",
    "C++"
]

copies = {
    101: 5,
    102: 3,
    103: 8
}

search = int(input("Enter Book ID: "))

if search in copies:

    index = book_ids.index(search)

    print("Book ID:", search)
    print("Title:", book_titles[index])
    print("Available Copies:", copies[search])

else:
    print("Book Not Found")

print("\nAll Books")

for i in range(len(book_ids)):
    print(book_ids[i], book_titles[i], copies[book_ids[i]])