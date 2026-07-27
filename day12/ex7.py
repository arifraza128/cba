students = {}

while True:

    print("\n1.Add")
    print("2.Search")
    print("3.Update")
    print("4.Delete")
    print("5.Display")
    print("6.Exit")

    choice = int(input())

    if choice == 1:
        sid = input("Student ID: ")
        name = input("Student Name: ")
        students[sid] = name

    elif choice == 2:
        sid = input("Student ID: ")

        if sid in students:
            print(students[sid])
        else:
            print("Not Found")

    elif choice == 3:
        sid = input("Student ID: ")

        if sid in students:
            students[sid] = input("New Name: ")

    elif choice == 4:
        sid = input("Student ID: ")

        if sid in students:
            del students[sid]

    elif choice == 5:
        for k, v in students.items():
            print(k, v)

    else:
        break