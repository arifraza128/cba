const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();

app.use(cors());
app.use(express.json());

// GET - Get all expenses
app.get("/expenses", (req, res) => {

    const data = fs.readFileSync("expenses.json");

    res.json(JSON.parse(data));
});

// POST - Add expense
app.post("/expenses", (req, res) => {

    const data = fs.readFileSync("expenses.json");

    const expenses = JSON.parse(data);

    const newExpense = {
        id: Date.now(),
        amount: req.body.amount,
        category: req.body.category,
        description: req.body.description
    };

    expenses.push(newExpense);

    fs.writeFileSync(
        "expenses.json",
        JSON.stringify(expenses, null, 2)
    );

    res.json(newExpense);
});

// DELETE - Delete expense
app.delete("/expenses/:id", (req, res) => {

    const data = fs.readFileSync("expenses.json");

    let expenses = JSON.parse(data);

    expenses = expenses.filter(
        expense => expense.id != req.params.id
    );

    fs.writeFileSync(
        "expenses.json",
        JSON.stringify(expenses, null, 2)
    );

    res.json({
        message: "Expense deleted"
    });
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});
