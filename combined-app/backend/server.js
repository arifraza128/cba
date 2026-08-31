const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// Path to data files
const DATA_DIR = path.join(__dirname, "data");
const EXPENSES_FILE = path.join(DATA_DIR, "expenses.json");
const PATIENTS_FILE = path.join(DATA_DIR, "patients.json");
const APPOINTMENTS_FILE = path.join(DATA_DIR, "appointments.json");
const BANK_FILE = path.join(DATA_DIR, "bank.json");

// Ensure data folder and files exist
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const initFile = (filePath, defaultData) => {
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, JSON.stringify(defaultData, null, 2));
  }
};

initFile(EXPENSES_FILE, []);
initFile(PATIENTS_FILE, []);
initFile(APPOINTMENTS_FILE, []);
initFile(BANK_FILE, { openingBalance: 25000, transactions: [] });

// Helper to read file safely
const readJson = (filePath) => {
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error);
    return [];
  }
};

// Helper to write file safely
const writeJson = (filePath, data) => {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
  } catch (error) {
    console.error(`Error writing to ${filePath}:`, error);
  }
};

// ==========================================
// 1. EXPENSE TRACKER ENDPOINTS
// ==========================================
app.get("/expenses", (req, res) => {
  res.json(readJson(EXPENSES_FILE));
});

app.post("/expenses", (req, res) => {
  const expenses = readJson(EXPENSES_FILE);
  const newExpense = {
    id: Date.now(),
    amount: Number(req.body.amount),
    category: req.body.category || "General",
    description: req.body.description || ""
  };
  expenses.push(newExpense);
  writeJson(EXPENSES_FILE, expenses);
  res.json(newExpense);
});

app.delete("/expenses/:id", (req, res) => {
  let expenses = readJson(EXPENSES_FILE);
  expenses = expenses.filter(exp => exp.id != req.params.id);
  writeJson(EXPENSES_FILE, expenses);
  res.json({ message: "Expense deleted" });
});

// ==========================================
// 2. LOAN EMI CALCULATOR ENDPOINTS
// ==========================================
app.post("/calculate-emi", (req, res) => {
  const { loanAmount, interestRate, tenure } = req.body;
  
  if (!loanAmount || !interestRate || !tenure) {
    return res.status(400).json({ message: "Invalid input values" });
  }

  // Convert yearly interest rate to monthly
  const monthlyRate = interestRate / 12 / 100;

  // EMI formula
  let emi = 0;
  if (monthlyRate === 0) {
    emi = loanAmount / tenure;
  } else {
    emi = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, tenure) / (Math.pow(1 + monthlyRate, tenure) - 1);
  }

  const totalRepayment = emi * tenure;
  const totalInterest = totalRepayment - loanAmount;

  res.json({
    emi: emi.toFixed(2),
    totalInterest: totalInterest.toFixed(2),
    totalRepayment: totalRepayment.toFixed(2)
  });
});

// ==========================================
// 3. PATIENT REGISTRATION ENDPOINTS
// ==========================================
app.get("/patients", (req, res) => {
  res.json(readJson(PATIENTS_FILE));
});

app.post("/patients", (req, res) => {
  const patients = readJson(PATIENTS_FILE);
  const newPatient = {
    id: Date.now(),
    name: req.body.name,
    age: Number(req.body.age),
    gender: req.body.gender,
    phone: req.body.phone,
    address: req.body.address || "",
    bloodGroup: req.body.bloodGroup || "",
    symptoms: req.body.symptoms || ""
  };
  patients.push(newPatient);
  writeJson(PATIENTS_FILE, patients);
  res.json(newPatient);
});

app.put("/patients/:id", (req, res) => {
  const patients = readJson(PATIENTS_FILE);
  const id = Number(req.params.id);
  const index = patients.findIndex(p => p.id === id);

  if (index === -1) {
    return res.status(404).json({ message: "Patient not found" });
  }

  patients[index] = {
    ...patients[index],
    ...req.body,
    id // preserve original id
  };
  writeJson(PATIENTS_FILE, patients);
  res.json(patients[index]);
});

app.delete("/patients/:id", (req, res) => {
  let patients = readJson(PATIENTS_FILE);
  const id = Number(req.params.id);
  patients = patients.filter(p => p.id !== id);
  writeJson(PATIENTS_FILE, patients);
  res.json({ message: "Patient deleted successfully" });
});

// ==========================================
// 4. DOCTOR APPOINTMENT ENDPOINTS
// ==========================================
app.get("/appointments", (req, res) => {
  res.json(readJson(APPOINTMENTS_FILE));
});

app.post("/appointments", (req, res) => {
  const appointments = readJson(APPOINTMENTS_FILE);
  const newAppointment = {
    id: Date.now(),
    doctor: req.body.doctor,
    date: req.body.date,
    time: req.body.time,
    patientName: req.body.patientName,
    patientAge: Number(req.body.patientAge)
  };
  appointments.push(newAppointment);
  writeJson(APPOINTMENTS_FILE, appointments);
  res.json(newAppointment);
});

app.delete("/appointments/:id", (req, res) => {
  let appointments = readJson(APPOINTMENTS_FILE);
  appointments = appointments.filter(app => app.id != req.params.id);
  writeJson(APPOINTMENTS_FILE, appointments);
  res.json({ message: "Appointment cancelled" });
});

// ==========================================
// 5. BANK TRANSACTION ENDPOINTS
// ==========================================
app.get("/api/account", (req, res) => {
  const account = readJson(BANK_FILE);
  let currentBalance = account.openingBalance;

  account.transactions.forEach((tx) => {
    if (tx.type === "credit") {
      currentBalance += tx.amount;
    } else {
      currentBalance -= tx.amount;
    }
  });

  res.json({
    openingBalance: account.openingBalance,
    currentBalance,
    transactions: account.transactions
  });
});

app.post("/api/deposit", (req, res) => {
  const { amount } = req.body;
  if (!amount || amount <= 0) {
    return res.status(400).json({ message: "Enter a valid deposit amount" });
  }

  const account = readJson(BANK_FILE);
  const transaction = {
    id: Date.now(),
    type: "credit",
    amount: Number(amount),
    date: new Date().toLocaleString()
  };

  account.transactions.push(transaction);
  writeJson(BANK_FILE, account);

  res.json({
    message: "Money deposited successfully",
    transaction
  });
});

app.post("/api/withdraw", (req, res) => {
  const { amount } = req.body;
  if (!amount || amount <= 0) {
    return res.status(400).json({ message: "Enter a valid withdrawal amount" });
  }

  const account = readJson(BANK_FILE);
  
  // Calculate balance
  let currentBalance = account.openingBalance;
  account.transactions.forEach((tx) => {
    if (tx.type === "credit") {
      currentBalance += tx.amount;
    } else {
      currentBalance -= tx.amount;
    }
  });

  if (amount > currentBalance) {
    return res.status(400).json({ message: "Insufficient balance" });
  }

  const transaction = {
    id: Date.now(),
    type: "debit",
    amount: Number(amount),
    date: new Date().toLocaleString()
  };

  account.transactions.push(transaction);
  writeJson(BANK_FILE, account);

  res.json({
    message: "Money withdrawn successfully",
    transaction
  });
});

// Start Server
app.listen(PORT, () => {
  console.log(`Consolidated Server running on http://localhost:${PORT}`);
});
