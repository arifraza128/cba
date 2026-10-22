import { useEffect, useState } from "react";
import "./App.css";

function App() {

    const [expenses, setExpenses] = useState([]);

    const [amount, setAmount] = useState("");
    const [category, setCategory] = useState("");
    const [description, setDescription] = useState("");

    // Backend URL
    const API_URL = "http://localhost:5005/expenses";


    // Get expenses from MongoDB
    useEffect(() => {

        fetch(API_URL)
            .then(response => response.json())
            .then(data => {
                setExpenses(data);
            })
            .catch(error => {
                console.error("Error fetching expenses:", error);
            });

    }, []);


    // Add expense
    const addExpense = (e) => {

        e.preventDefault();

        const expense = {
            amount: Number(amount),
            category: category,
            description: description
        };

        fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(expense)
        })
            .then(response => response.json())
            .then(data => {

                setExpenses(prevExpenses => [
                    ...prevExpenses,
                    data
                ]);

                setAmount("");
                setCategory("");
                setDescription("");

            })
            .catch(error => {
                console.error("Error adding expense:", error);
            });
    };


    // Delete expense
    const deleteExpense = (id) => {

        fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        })
            .then(response => response.json())
            .then(() => {

                setExpenses(prevExpenses =>
                    prevExpenses.filter(
                        expense => expense._id !== id
                    )
                );

            })
            .catch(error => {
                console.error("Error deleting expense:", error);
            });
    };


    // Calculate total
    const total = expenses.reduce(
        (sum, expense) =>
            sum + Number(expense.amount),
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
                    onChange={(e) =>
                        setAmount(e.target.value)
                    }
                    required
                />


                <input
                    type="text"
                    placeholder="Category"
                    value={category}
                    onChange={(e) =>
                        setCategory(e.target.value)
                    }
                    required
                />


                <input
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) =>
                        setDescription(e.target.value)
                    }
                    required
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

                    <div
                        className="expense"
                        key={expense._id}
                    >

                        <p>
                            <strong>
                                ₹{expense.amount}
                            </strong>
                        </p>


                        <p>
                            Category: {expense.category}
                        </p>


                        <p>
                            {expense.description}
                        </p>


                        <button
                            onClick={() =>
                                deleteExpense(
                                    expense._id
                                )
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
