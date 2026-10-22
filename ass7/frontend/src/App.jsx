import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [account, setAccount] = useState(null);
  const [amount, setAmount] = useState("");

  // Get account data
  const fetchAccount = async () => {
    const response = await fetch(
      "http://localhost:5000/api/account"
    );

    const data = await response.json();

    setAccount(data);
  };

  useEffect(() => {
    fetchAccount();
  }, []);

  // Deposit
  const depositMoney = async () => {
    if (!amount) {
      alert("Enter amount");
      return;
    }

    const response = await fetch(
      "http://localhost:5000/api/deposit",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: Number(amount),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.message);
      return;
    }

    setAmount("");
    fetchAccount();
  };

  // Withdraw
  const withdrawMoney = async () => {
    if (!amount) {
      alert("Enter amount");
      return;
    }

    const response = await fetch(
      "http://localhost:5000/api/withdraw",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: Number(amount),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.message);
      return;
    }

    setAmount("");
    fetchAccount();
  };

  if (!account) {
    return <h2>Loading...</h2>;
  }

  return (
    <div className="container">
      <h1>🏦 Bank Transaction Manager</h1>

      {/* Balance */}
      <div className="balance-card">
        <p>Opening Balance</p>

        <h2>
          ₹{account.openingBalance.toLocaleString()}
        </h2>

        <p>Current Balance</p>

        <h1>
          ₹{account.currentBalance.toLocaleString()}
        </h1>
      </div>

      {/* Transaction Form */}
      <div className="transaction-box">
        <h2>Make Transaction</h2>

        <input
          type="number"
          placeholder="Enter amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <div className="buttons">
          <button onClick={depositMoney}>
            Deposit
          </button>

          <button onClick={withdrawMoney}>
            Withdraw
          </button>
        </div>
      </div>

      {/* Transaction History */}
      <div className="history">
        <h2>Transaction History</h2>

        {account.transactions.length === 0 ? (
          <p>No transactions yet.</p>
        ) : (
          account.transactions
            .slice()
            .reverse()
            .map((transaction) => (
              <div
                className="transaction"
                key={transaction.id}
              >
                <div>
                  <h3>
                    {transaction.type === "credit"
                      ? "🟢 Credit"
                      : "🔴 Debit"}
                  </h3>

                  <p>{transaction.date}</p>
                </div>

                <strong
                  className={
                    transaction.type === "credit"
                      ? "credit"
                      : "debit"
                  }
                >
                  {transaction.type === "credit"
                    ? "+"
                    : "-"}
                  ₹{transaction.amount.toLocaleString()}
                </strong>
              </div>
            ))
        )}
      </div>
    </div>
  );
}

export default App;
