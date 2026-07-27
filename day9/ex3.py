from abc import ABC, abstractmethod
from datetime import datetime
import itertools

class InsufficientFundsError(Exception):
    pass

class Transaction:
    _id_counter = itertools.count(9001)

    def __init__(self, txn_type, amount, balance_after):
        self.txn_id = next(Transaction._id_counter)
        self.txn_type = txn_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()

    def __str__(self):
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] "
            f"{self.txn_type:<13} Rs.{self.amount:>10.2f}  Bal: Rs.{self.balance_after:.2f}"
        )

class Account(ABC):
    _id_counter = itertools.count(100001)

    def __init__(self, holder_name, opening_balance=0.0):
        self.account_number = next(Account._id_counter)
        self.holder_name = holder_name
        self.__balance = opening_balance
        self.history = []
        if opening_balance:
            self.history.append(Transaction("DEPOSIT", opening_balance, self.__balance))

    def get_balance(self):
        return self.__balance

    def _set_balance(self, value):
        self.__balance = value

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self._set_balance(self.get_balance() + amount)
        self.history.append(Transaction("DEPOSIT", amount, self.get_balance()))
        print(
            f"[DEPOSIT] Rs.{amount:.2f} deposited to A/C {self.account_number}. "
            f"New balance: Rs.{self.get_balance():.2f}"
        )

    @abstractmethod
    def withdraw(self, amount):
        raise NotImplementedError

    @abstractmethod
    def apply_interest(self):
        raise NotImplementedError

    def mini_statement(self, last_n=5):
        print(f"\n--- Mini Statement: A/C {self.account_number} ({self.holder_name}) ---")
        for txn in self.history[-last_n:]:
            print(" ", txn)
        print(f"Current Balance: Rs.{self.get_balance():.2f}")

    def __str__(self):
        return f"A/C {self.account_number} ({self.__class__.__name__}) - {self.holder_name}: Rs.{self.get_balance():.2f}"

class SavingsAccount(Account):
    INTEREST_RATE = 0.04
    MIN_BALANCE = 500

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if self.get_balance() - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                f"Withdrawal denied: Savings account must maintain min balance of Rs.{self.MIN_BALANCE}."
            )
        self._set_balance(self.get_balance() - amount)
        self.history.append(Transaction("WITHDRAW", amount, self.get_balance()))
        print(f"[WITHDRAW] Rs.{amount:.2f} withdrawn from A/C {self.account_number}.")

    def apply_interest(self):
        interest = self.get_balance() * self.INTEREST_RATE
        self._set_balance(self.get_balance() + interest)
        self.history.append(Transaction("INTEREST", interest, self.get_balance()))
        print(f"[INTEREST] Rs.{interest:.2f} credited to A/C {self.account_number}.")
        return interest

class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 10000

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if self.get_balance() - amount < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(
                f"Withdrawal denied: exceeds overdraft limit of Rs.{self.OVERDRAFT_LIMIT}."
            )
        self._set_balance(self.get_balance() - amount)
        self.history.append(Transaction("WITHDRAW", amount, self.get_balance()))
        print(
            f"[WITHDRAW] Rs.{amount:.2f} withdrawn from A/C {self.account_number} "
            f"(Balance may be negative due to overdraft)."
        )

    def apply_interest(self):
        print(f"[INTEREST] A/C {self.account_number} is a Current Account - no interest applicable.")
        return 0.0

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, acc_type, holder_name, opening_balance=0.0):
        if acc_type.lower() == "savings":
            acc = SavingsAccount(holder_name, opening_balance)
        elif acc_type.lower() == "current":
            acc = CurrentAccount(holder_name, opening_balance)
        else:
            raise ValueError("Unknown account type. Use 'savings' or 'current'.")
        self.accounts[acc.account_number] = acc
        print(f"[BANK] {acc_type.title()} account created: {acc}")
        return acc

    def transfer(self, from_acc_no, to_acc_no, amount):
        src = self.accounts.get(from_acc_no)
        dst = self.accounts.get(to_acc_no)
        if not src or not dst:
            print("Invalid account number(s).")
            return
        try:
            src.withdraw(amount)
            src.history[-1].txn_type = "TRANSFER_OUT"
            dst.deposit(amount)
            dst.history[-1].txn_type = "TRANSFER_IN"
            print(f"[TRANSFER] Rs.{amount:.2f} transferred from A/C {from_acc_no} to A/C {to_acc_no}.")
        except InsufficientFundsError as e:
            print(f"[ERROR] Transfer failed: {e}")

    def apply_interest_all(self):
        for acc in self.accounts.values():
            acc.apply_interest()

if __name__ == "__main__":
    bank = Bank("National Trust Bank")

    savings = bank.create_account("savings", "Anita", 5000)
    current = bank.create_account("current", "Rohit", 2000)

    savings.deposit(1500)
    savings.withdraw(1000)

    current.withdraw(8000)
    bank.transfer(savings.account_number, current.account_number, 500)

    print("\n--- Applying interest across all accounts (polymorphism) ---")
    bank.apply_interest_all()

    savings.mini_statement()
    current.mini_statement()

    print("\n--- Trying to breach savings minimum balance ---")
    try:
        savings.withdraw(100000)
    except InsufficientFundsError as e:
        print(f"[ERROR] {e}")
