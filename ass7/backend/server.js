const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// Opening balance
let openingBalance = 25000;

// Transactions
let transactions = [];

// GET current account information
app.get("/api/account", (req, res) => {
  let currentBalance = openingBalance;

  transactions.forEach((transaction) => {
    if (transaction.type === "credit") {
      currentBalance += transaction.amount;
    } else {
      currentBalance -= transaction.amount;
    }
  });

  res.json({
    openingBalance,
    currentBalance,
    transactions,
  });
});

// POST deposit
app.post("/api/deposit", (req, res) => {
  const { amount } = req.body;

  if (!amount || amount <= 0) {
    return res.status(400).json({
      message: "Enter a valid deposit amount",
    });
  }

  const transaction = {
    id: Date.now(),
    type: "credit",
    amount: Number(amount),
    date: new Date().toLocaleString(),
  };

  transactions.push(transaction);

  res.json({
    message: "Money deposited successfully",
    transaction,
  });
});

// POST withdraw
app.post("/api/withdraw", (req, res) => {
  const { amount } = req.body;

  if (!amount || amount <= 0) {
    return res.status(400).json({
      message: "Enter a valid withdrawal amount",
    });
  }

  // Calculate current balance
  let currentBalance = openingBalance;

  transactions.forEach((transaction) => {
    if (transaction.type === "credit") {
      currentBalance += transaction.amount;
    } else {
      currentBalance -= transaction.amount;
    }
  });

  // Check sufficient balance
  if (amount > currentBalance) {
    return res.status(400).json({
      message: "Insufficient balance",
    });
  }

  const transaction = {
    id: Date.now(),
    type: "debit",
    amount: Number(amount),
    date: new Date().toLocaleString(),
  };

  transactions.push(transaction);

  res.json({
    message: "Money withdrawn successfully",
    transaction,
  });
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});
