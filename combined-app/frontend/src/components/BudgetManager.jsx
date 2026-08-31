import { useState, useEffect } from "react";

function BudgetManager({ onUpdate, showToast }) {
  const [income, setIncome] = useState(() => {
    return localStorage.getItem("budget_income") || "";
  });

  const [budgets, setBudgets] = useState(() => {
    const saved = localStorage.getItem("budget_data");
    return saved
      ? JSON.parse(saved)
      : [
          { category: "Food", budget: 10000, spent: 0 },
          { category: "Travel", budget: 5000, spent: 0 },
          { category: "Shopping", budget: 5000, spent: 0 },
          { category: "Bills", budget: 5000, spent: 0 },
        ];
  });

  const [category, setCategory] = useState("Food");
  const [expense, setExpense] = useState("");

  useEffect(() => {
    localStorage.setItem("budget_income", income);
  }, [income]);

  useEffect(() => {
    localStorage.setItem("budget_data", JSON.stringify(budgets));
    if (onUpdate) onUpdate();
  }, [budgets]);

  const addExpense = (e) => {
    e.preventDefault();

    if (!expense || Number(expense) <= 0) {
      if (showToast) showToast("Enter a valid expense amount", "error");
      return;
    }

    setBudgets(
      budgets.map((item) => {
        if (item.category === category) {
          const updatedSpent = item.spent + Number(expense);
          if (updatedSpent > item.budget) {
            if (showToast) showToast(`⚠️ Budget exceeded for ${item.category}!`, "error");
          } else {
            if (showToast) showToast(`Added ₹${expense} expense to ${item.category}`, "success");
          }
          return {
            ...item,
            spent: updatedSpent,
          };
        }
        return item;
      })
    );

    setExpense("");
  };

  const resetBudgets = () => {
    setBudgets(
      budgets.map((item) => ({
        ...item,
        spent: 0,
      }))
    );
    setIncome("");
    if (showToast) showToast("Budgets reset successfully!", "info");
  };

  const totalBudget = budgets.reduce((total, item) => total + item.budget, 0);
  const totalSpent = budgets.reduce((total, item) => total + item.spent, 0);
  const remaining = Number(income || 0) - totalSpent;

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>💰 Monthly Budget Manager</h2>
        <p>Allocate funds to specific categories and prevent overspending</p>
      </div>

      {/* Grid of stats */}
      <div className="dashboard-grid">
        <div className="card stat-card">
          <span className="stat-label">Monthly Income</span>
          <span className="stat-value text-indigo">₹{Number(income || 0).toLocaleString()}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">Total Allocated</span>
          <span className="stat-value text-teal">₹{totalBudget.toLocaleString()}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">Total Spent</span>
          <span className="stat-value text-rose">₹{totalSpent.toLocaleString()}</span>
        </div>
        <div className="card stat-card">
          <span className="stat-label">Remaining Balance</span>
          <span className={`stat-value ${remaining >= 0 ? "text-emerald" : "text-danger"}`}>
            ₹{remaining.toLocaleString()}
          </span>
        </div>
      </div>

      <div className="module-grid">
        {/* Form and Configurations */}
        <div className="card form-card">
          <h3>Budget Configurations</h3>
          
          <div className="input-group">
            <label>Update Monthly Income (₹)</label>
            <input
              type="number"
              placeholder="e.g. 50000"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
            />
          </div>

          <hr className="divider" />

          <h3>Log New Expense</h3>
          <form onSubmit={addExpense} className="modern-form">
            <div className="input-group">
              <label>Category</label>
              <select value={category} onChange={(e) => setCategory(e.target.value)}>
                {budgets.map((item) => (
                  <option key={item.category} value={item.category}>
                    {item.category}
                  </option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label>Amount (₹)</label>
              <input
                type="number"
                placeholder="e.g. 150"
                value={expense}
                onChange={(e) => setExpense(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary">
              💸 Log Expense
            </button>
          </form>

          <button onClick={resetBudgets} className="btn btn-secondary mt-3">
            🔄 Reset Spent & Income
          </button>
        </div>

        {/* Budget Status Lists */}
        <div className="card list-card">
          <h3>Category Breakdown</h3>
          <div className="items-list scrollable">
            {budgets.map((item) => {
              const remainingCategory = item.budget - item.spent;
              const percentUsed = Math.min(Math.round((item.spent / item.budget) * 100), 100);
              const isOver = item.spent > item.budget;

              return (
                <div className={`budget-row ${isOver ? "row-warning" : ""}`} key={item.category}>
                  <div className="budget-row-header">
                    <h4>{item.category}</h4>
                    <span className="budget-ratio">
                      ₹{item.spent.toLocaleString()} / <strong>₹{item.budget.toLocaleString()}</strong>
                    </span>
                  </div>

                  <div className="progress-bar-bg">
                    <div
                      className={`progress-bar-fill ${isOver ? "bg-rose" : percentUsed > 80 ? "bg-amber" : "bg-indigo"}`}
                      style={{ width: `${percentUsed}%` }}
                    ></div>
                  </div>

                  <div className="budget-row-footer">
                    <span className="percent-label">{percentUsed}% Used</span>
                    <span className={`status-pill ${isOver ? "pill-danger" : "pill-success"}`}>
                      {isOver ? `Over budget by ₹${Math.abs(remainingCategory).toLocaleString()}` : `₹${remainingCategory.toLocaleString()} Left`}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default BudgetManager;
