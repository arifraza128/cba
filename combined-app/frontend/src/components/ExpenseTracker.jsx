import { useEffect, useState } from "react";

function ExpenseTracker({ onUpdate, showToast }) {
  const [expenses, setExpenses] = useState([]);
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");

  const fetchExpenses = () => {
    fetch("http://localhost:5000/expenses")
      .then((res) => res.json())
      .then((data) => {
        setExpenses(data);
        if (onUpdate) onUpdate();
      })
      .catch((err) => console.error("Error fetching expenses:", err));
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const addExpense = (e) => {
    e.preventDefault();

    if (!amount || !category) {
      if (showToast) showToast("Please fill in Amount and Category!", "error");
      return;
    }

    const expense = { amount, category, description };

    fetch("http://localhost:5000/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(expense),
    })
      .then((res) => res.json())
      .then((data) => {
        setExpenses([...expenses, data]);
        setAmount("");
        setCategory("");
        setDescription("");
        if (showToast) showToast("Expense added successfully!", "success");
        if (onUpdate) onUpdate();
      })
      .catch((err) => {
        console.error(err);
        if (showToast) showToast("Failed to add expense.", "error");
      });
  };

  const deleteExpense = (id) => {
    fetch(`http://localhost:5000/expenses/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setExpenses(expenses.filter((exp) => exp.id !== id));
        if (showToast) showToast("Expense deleted successfully!", "info");
        if (onUpdate) onUpdate();
      })
      .catch((err) => {
        console.error(err);
        if (showToast) showToast("Failed to delete expense.", "error");
      });
  };

  const total = expenses.reduce((sum, exp) => sum + Number(exp.amount), 0);

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>📊 Expense Tracker</h2>
        <p>Monitor your outgoing costs and manage categories</p>
      </div>

      <div className="module-grid">
        {/* Input Form */}
        <div className="card form-card">
          <h3>Record New Expense</h3>
          <form onSubmit={addExpense} className="modern-form">
            <div className="input-group">
              <label>Amount (₹)</label>
              <input
                type="number"
                placeholder="e.g. 500"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Category</label>
              <input
                type="text"
                placeholder="e.g. Food, Transport, Rent"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Description</label>
              <input
                type="text"
                placeholder="e.g. Dinner with family"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary">
              ➕ Add Expense
            </button>
          </form>
        </div>

        {/* Expenses List */}
        <div className="card list-card">
          <div className="list-summary-header">
            <h3>Expense Summary</h3>
            <div className="metric-badge">
              Total Spent: <strong>₹{total.toLocaleString()}</strong>
            </div>
          </div>

          <div className="items-list scrollable">
            {expenses.length === 0 ? (
              <div className="empty-state">
                <span>💸</span>
                <p>No expenses logged yet. Add one to get started!</p>
              </div>
            ) : (
              expenses
                .slice()
                .reverse()
                .map((exp) => (
                  <div className="item-row" key={exp.id}>
                    <div className="item-main">
                      <div className="item-title-row">
                        <span className="item-badge">{exp.category}</span>
                        <span className="item-price">₹{Number(exp.amount).toLocaleString()}</span>
                      </div>
                      {exp.description && <p className="item-desc">{exp.description}</p>}
                    </div>
                    <button
                      className="btn-icon-delete"
                      onClick={() => deleteExpense(exp.id)}
                      title="Delete Expense"
                    >
                      🗑️
                    </button>
                  </div>
                ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExpenseTracker;
