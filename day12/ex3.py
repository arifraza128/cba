employees = []

while True:
    print("\n1.Add")
    print("2.Remove")
    print("3.Search")
    print("4.Display")
    print("5.Count")
    print("6.Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        name = input("Employee Name: ")
        employees.append(name)

    elif choice == 2:
        name = input("Employee to Remove: ")
        if name in employees:
            employees.remove(name)
            print("Removed")
        else:
            print("Not Found")

    elif choice == 3:
        name = input("Employee to Search: ")
        if name in employees:
            print("Employee Found")
        else:
            print("Not Found")

    elif choice == 4:
        print(employees)

    elif choice == 5:
        print("Total Employees:", len(employees))

    else:
        break