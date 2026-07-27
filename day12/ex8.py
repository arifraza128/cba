accounts = {}

while True:

    print("\n1.Add Account")
    print("2.Search")
    print("3.Deposit")
    print("4.Withdraw")
    print("5.Display")
    print("6.Exit")

    choice = int(input())

    if choice == 1:
        acc = input("Account Number: ")
        balance = float(input("Balance: "))
        accounts[acc] = balance

    elif choice == 2:
        acc = input("Account Number: ")

        if acc in accounts:
            print("Balance:", accounts[acc])

    elif choice == 3:
        acc = input("Account Number: ")
        amount = float(input("Deposit Amount: "))
        accounts[acc] += amount

    elif choice == 4:
        acc = input("Account Number: ")
        amount = float(input("Withdraw Amount: "))

        if accounts[acc] >= amount:
            accounts[acc] -= amount
        else:
            print("Insufficient Balance")

    elif choice == 5:
        for k, v in accounts.items():
            print(k, ":", v)

    else:
        break