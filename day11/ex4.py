class BankAccount:

    def __init__(self, acc_no, name, balance):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance
        self.transactions = 0

    def deposit(self, amount):
        self.balance += amount
        self.transactions += 1
        print("Amount Deposited Successfully")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions += 1
            print("Withdrawal Successful")
        else:
            print("Insufficient Balance")

    def check_balance(self):
        print("Current Balance:", self.balance)

    def summary(self):
        print("\n------ Account Summary ------")
        print("Account No :", self.acc_no)
        print("Customer   :", self.name)
        print("Balance    :", self.balance)
        print("Transactions:", self.transactions)


acc = BankAccount(
    input("Account Number: "),
    input("Customer Name: "),
    float(input("Opening Balance: "))
)

while True:

    print("\n1.Deposit")
    print("2.Withdraw")
    print("3.Check Balance")
    print("4.Exit")

    ch = int(input("Enter Choice: "))

    if ch == 1:
        amt = float(input("Enter Amount: "))
        acc.deposit(amt)

    elif ch == 2:
        amt = float(input("Enter Amount: "))
        acc.withdraw(amt)

    elif ch == 3:
        acc.check_balance()

    elif ch == 4:
        break

acc.summary()
