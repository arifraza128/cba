import { useEffect, useState } from "react";
import "./App.css";

function App() {

    const [expenses, setExpenses] = useState([]);

    const [amount, setAmount] = useState("");
    const [category, setCategory] = useState("");
    const [description, setDescription] = useState("");

    // Get expenses
    useEffect(() => {

        fetch("http://localhost:5000/expenses")
            .then(response => response.json())
            .then(data => {
                setExpenses(data);
            });

    }, []);

    // Add expense
    const addExpense = (e) => {

        e.preventDefault();

        const expense = {
            amount: amount,
            category: category,
            description: description
        };

        fetch("http://localhost:5000/expenses", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(expense)
        })
        .then(response => response.json())
        .then(data => {

            setExpenses([...expenses, data]);

            setAmount("");
            setCategory("");
            setDescription("");

        });
    };

    // Delete expense
    const deleteExpense = (id) => {

        fetch(`http://localhost:5000/expenses/${id}`, {
            method: "DELETE"
        })
        .then(() => {

            setExpenses(
                expenses.filter(expense => expense.id !== id)
            );

        });
    };

    // Calculate total
    const total = expenses.reduce(
        (sum, expense) => sum + Number(expense.amount),
        0
    );

    return (

        <div className="container">

            <h1>Expense Tracker</h1>

            {/* Form */}

            <form onSubmit={addExpense}>

                <input
                    type="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                />

                <input
                    type="text"
                    placeholder="Category"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                />

                <input
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) =>
                        setDescription(e.target.value)
                    }
                />

                <button type="submit">
                    Add Expense
                </button>

            </form>

            {/* Total */}

            <h2>
                Total: ₹{total}
            </h2>

            {/* Expenses */}

            <h2>Expenses</h2>

            {expenses.length === 0 ? (

                <p>No expenses yet.</p>

            ) : (

                expenses.map(expense => (

                    <div className="expense" key={expense.id}>

                        <p>
                            ₹{expense.amount}
                        </p>

                        <p>
                            Category: {expense.category}
                        </p>

                        <p>
                            {expense.description}
                        </p>

                        <button
                            onClick={() =>
                                deleteExpense(expense.id)
                            }
                        >
                            Delete
                        </button>

                    </div>

                ))

            )}

        </div>

    );
}

export default App;
