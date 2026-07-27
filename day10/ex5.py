class Account:
    def __init__(self, account_number, holder_name, balance):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print("₹", amount, "deposited successfully.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print("₹", amount, "withdrawn successfully.")
        else:
            print("Insufficient Balance!")

    def display_balance(self):
        print("Current Balance: ₹", self.balance)


acc_no = input("Enter Account Number: ")
holder = input("Enter Account Holder Name: ")
balance = float(input("Enter Initial Balance: "))

account = Account(acc_no, holder, balance)

while True:
    print("\n===== ATM MENU =====")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Display Balance")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        amount = float(input("Enter Deposit Amount: "))
        account.deposit(amount)

    elif choice == 2:
        amount = float(input("Enter Withdraw Amount: "))
        account.withdraw(amount)

    elif choice == 3:
        account.display_balance()

    elif choice == 4:
        print("Thank You for Using ATM!")
        break

    else:
        print("Invalid Choice!")