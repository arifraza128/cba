import { useState } from "react";
import "./App.css";

function App() {

  const [income, setIncome] = useState("");

  const [budgets, setBudgets] = useState([
    {
      category: "Food",
      budget: 10000,
      spent: 0
    },
    {
      category: "Travel",
      budget: 5000,
      spent: 0
    },
    {
      category: "Shopping",
      budget: 5000,
      spent: 0
    },
    {
      category: "Bills",
      budget: 5000,
      spent: 0
    }
  ]);

  const [category, setCategory] = useState("Food");
  const [expense, setExpense] = useState("");


  // Add expense
  const addExpense = (e) => {

    e.preventDefault();

    if (!expense || expense <= 0) {
      return;
    }

    setBudgets(
      budgets.map((item) => {

        if (item.category === category) {

          return {
            ...item,
            spent: item.spent + Number(expense)
          };

        }

        return item;

      })
    );

    setExpense("");
  };


  // Total budget
  const totalBudget = budgets.reduce(
    (total, item) => total + item.budget,
    0
  );


  // Total spent
  const totalSpent = budgets.reduce(
    (total, item) => total + item.spent,
    0
  );


  // Remaining income
  const remaining = Number(income || 0) - totalSpent;


  return (

    <div className="container">

      <h1>💰 Monthly Budget Manager</h1>


      {/* Income */}

      <div className="card">

        <h2>Monthly Income</h2>

        <input
          type="number"
          placeholder="Enter income"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
        />

      </div>


      {/* Dashboard */}

      <div className="dashboard">

        <div className="card">
          <h3>Income</h3>
          <p>₹{income || 0}</p>
        </div>

        <div className="card">
          <h3>Total Budget</h3>
          <p>₹{totalBudget}</p>
        </div>

        <div className="card">
          <h3>Total Spent</h3>
          <p>₹{totalSpent}</p>
        </div>

        <div className="card">
          <h3>Remaining</h3>
          <p>₹{remaining}</p>
        </div>

      </div>


      {/* Add Expense */}

      <div className="card">

        <h2>Add Expense</h2>

        <form onSubmit={addExpense}>

          <select
            value={category}
            onChange={(e) =>
              setCategory(e.target.value)
            }
          >

            {budgets.map((item) => (
              <option
                key={item.category}
                value={item.category}
              >
                {item.category}
              </option>
            ))}

          </select>


          <input
            type="number"
            placeholder="Expense amount"
            value={expense}
            onChange={(e) =>
              setExpense(e.target.value)
            }
          />


          <button type="submit">
            Add Expense
          </button>

        </form>

      </div>


      {/* Budget List */}

      <h2>Budgets</h2>

      {budgets.map((item) => {

        const remainingCategory =
          item.budget - item.spent;

        return (

          <div className="card" key={item.category}>

            <h2>{item.category}</h2>

            <p>
              Budget: ₹{item.budget}
            </p>

            <p>
              Spent: ₹{item.spent}
            </p>

            <p>
              Remaining: ₹{remainingCategory}
            </p>


            {/* Warning */}

            {item.spent > item.budget && (

              <p className="warning">
                ⚠️ Budget Exceeded!
              </p>

            )}

          </div>

        );

      })}

    </div>

  );
}

export default App;
