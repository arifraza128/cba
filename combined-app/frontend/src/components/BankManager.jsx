import { useEffect, useState } from "react";

function BankManager({ onUpdate, showToast }) {
  const [account, setAccount] = useState(null);
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchAccount = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/account");
      const data = await response.json();
      setAccount(data);
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error("Error fetching account:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccount();
  }, []);

  const handleTransaction = async (type) => {
    if (!amount || Number(amount) <= 0) {
      if (showToast) showToast("Please enter a valid amount!", "error");
      return;
    }

    const endpoint = type === "deposit" ? "/api/deposit" : "/api/withdraw";

    try {
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: Number(amount) }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (showToast) showToast(data.message || "Transaction failed", "error");
        return;
      }

      setAmount("");
      if (showToast) showToast(data.message || "Transaction successful!", "success");
      fetchAccount();
    } catch (error) {
      console.error(error);
      if (showToast) showToast("Connection failed.", "error");
    }
  };

  if (loading) {
    return (
      <div className="module-container loading-container">
        <h3>Loading Bank Transactions...</h3>
      </div>
    );
  }

  if (!account) {
    return (
      <div className="module-container loading-container">
        <h3 className="text-danger">Failed to connect to Bank Server.</h3>
      </div>
    );
  }

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>🏦 Bank Transaction Manager</h2>
        <p>Deposit, withdraw, and check your current financial statements</p>
      </div>

      <div className="bank-metrics-row">
        <div className="card balance-card opening-balance">
          <span className="bal-label">Opening Balance</span>
          <h3 className="bal-value">₹{account.openingBalance.toLocaleString()}</h3>
        </div>
        <div className="card balance-card current-balance glowing-border">
          <span className="bal-label text-indigo">Current Account Balance</span>
          <h1 className="bal-value text-emerald">₹{account.currentBalance.toLocaleString()}</h1>
        </div>
      </div>

      <div className="module-grid">
        {/* Transaction Action Form */}
        <div className="card form-card">
          <h3>Make Transaction</h3>
          <div className="modern-form mt-4">
            <div className="input-group">
              <label>Amount (₹)</label>
              <input
                type="number"
                placeholder="e.g. 5000"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </div>

            <div className="bank-actions-row">
              <button
                className="btn btn-emerald"
                onClick={() => handleTransaction("deposit")}
              >
                📥 Deposit Money
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleTransaction("withdraw")}
              >
                📤 Withdraw Money
              </button>
            </div>
          </div>
        </div>

        {/* History of Transactions */}
        <div className="card list-card">
          <h3>Transaction Statements ({account.transactions.length})</h3>
          <div className="items-list scrollable history-list">
            {account.transactions.length === 0 ? (
              <div className="empty-state">
                <span>🏦</span>
                <p>No transaction history recorded yet.</p>
              </div>
            ) : (
              account.transactions
                .slice()
                .reverse()
                .map((tx) => (
                  <div className="tx-row" key={tx.id}>
                    <div className="tx-meta">
                      <span className={`tx-type-pill ${tx.type === "credit" ? "credit-pill" : "debit-pill"}`}>
                        {tx.type === "credit" ? "🟢 Deposit" : "🔴 Withdrawal"}
                      </span>
                      <span className="tx-time">{tx.date}</span>
                    </div>
                    <strong className={`tx-amount ${tx.type === "credit" ? "text-emerald" : "text-rose"}`}>
                      {tx.type === "credit" ? "+" : "-"} ₹{tx.amount.toLocaleString()}
                    </strong>
                  </div>
                ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default BankManager;
