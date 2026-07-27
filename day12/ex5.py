movies = []

while True:

    print("\n1.Add Movie")
    print("2.Remove Movie")
    print("3.Search Movie")
    print("4.Sort Movies")
    print("5.Display")
    print("6.Exit")

    choice = int(input())

    if choice == 1:
        movies.append(input("Movie Name: "))

    elif choice == 2:
        movie = input("Movie to Remove: ")

        if movie in movies:
            movies.remove(movie)

    elif choice == 3:
        movie = input("Search Movie: ")

        if movie in movies:
            print("Movie Found")
        else:
            print("Movie Not Found")

    elif choice == 4:
        movies.sort()
        print("Movies Sorted")

    elif choice == 5:
        print(movies)

    else:
        break