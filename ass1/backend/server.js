const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose
    .connect(process.env.MONGO_URI)
    .then(() => {
        console.log("MongoDB connected successfully");
    })
    .catch((error) => {
        console.error("MongoDB connection error:", error);
    });


// Expense Schema
const expenseSchema = new mongoose.Schema({
    amount: {
        type: Number,
        required: true
    },
    category: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    }
});

// Expense Model
const Expense = mongoose.model("Expense", expenseSchema);


// GET - Get all expenses
app.get("/expenses", async (req, res) => {
    try {
        const expenses = await Expense.find();

        res.json(expenses);
    } catch (error) {
        res.status(500).json({
            message: "Error fetching expenses",
            error: error.message
        });
    }
});


// POST - Add expense
app.post("/expenses", async (req, res) => {
    try {
        const newExpense = new Expense({
            amount: req.body.amount,
            category: req.body.category,
            description: req.body.description
        });

        const savedExpense = await newExpense.save();

        res.status(201).json(savedExpense);
    } catch (error) {
        res.status(500).json({
            message: "Error adding expense",
            error: error.message
        });
    }
});


// DELETE - Delete expense
app.delete("/expenses/:id", async (req, res) => {
    try {
        const deletedExpense = await Expense.findByIdAndDelete(
            req.params.id
        );

        if (!deletedExpense) {
            return res.status(404).json({
                message: "Expense not found"
            });
        }

        res.json({
            message: "Expense deleted successfully"
        });

    } catch (error) {
        res.status(500).json({
            message: "Error deleting expense",
            error: error.message
        });
    }
});


// Start Server
app.listen(process.env.PORT || 5005, () => {
    console.log(
        `Server running on port ${process.env.PORT || 5005}`
    );
});