import { useEffect, useState } from "react";

function HomeDashboard({ setTab }) {
  const [bankBalance, setBankBalance] = useState(0);
  const [totalExpenses, setTotalExpenses] = useState(0);
  const [patientCount, setPatientCount] = useState(0);
  const [appointmentCount, setAppointmentCount] = useState(0);
  const [medicineRate, setMedicineRate] = useState(0);
  const [budgetPercent, setBudgetPercent] = useState(0);

  useEffect(() => {
    // 1. Fetch Bank balance
    fetch("http://localhost:5000/api/account")
      .then((res) => res.json())
      .then((data) => setBankBalance(data.currentBalance))
      .catch((e) => console.log("Bank server offline"));

    // 2. Fetch Expenses
    fetch("http://localhost:5000/expenses")
      .then((res) => res.json())
      .then((data) => {
        const sum = data.reduce((acc, exp) => acc + Number(exp.amount), 0);
        setTotalExpenses(sum);
      })
      .catch((e) => console.log("Expenses server offline"));

    // 3. Fetch Patient registration count
    fetch("http://localhost:5000/patients")
      .then((res) => res.json())
      .then((data) => setPatientCount(data.length))
      .catch((e) => console.log("Patient server offline"));

    // 4. Fetch Doctor appointments count
    fetch("http://localhost:5000/appointments")
      .then((res) => res.json())
      .then((data) => setAppointmentCount(data.length))
      .catch((e) => console.log("Appointment server offline"));

    // 5. Read Medicine reminders from localStorage
    const savedMeds = localStorage.getItem("medicines");
    if (savedMeds) {
      const meds = JSON.parse(savedMeds);
      const total = meds.length;
      const taken = meds.filter((m) => m.taken).length;
      setMedicineRate(total > 0 ? Math.round((taken / total) * 100) : 0);
    }

    // 6. Read Budget Manager from localStorage
    const income = Number(localStorage.getItem("budget_income") || 0);
    const savedBudgets = localStorage.getItem("budget_data");
    if (savedBudgets) {
      const budgets = JSON.parse(savedBudgets);
      const spent = budgets.reduce((acc, item) => acc + item.spent, 0);
      const totalAllocated = budgets.reduce((acc, item) => acc + item.budget, 0);
      setBudgetPercent(totalAllocated > 0 ? Math.min(Math.round((spent / totalAllocated) * 100), 100) : 0);
    }
  }, []);

  return (
    <div className="module-container">
      <div className="dashboard-welcome">
        <h1>👋 Welcome to Health &amp; Finance Suite</h1>
        <p>Your comprehensive personal dashboard to track both health records and financial transactions.</p>
      </div>

      {/* Grid of cards */}
      <div className="metrics-summary-grid">
        {/* Card 1: Bank Balance */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("bank")}>
          <div className="card-badge bg-emerald-trans">🏦 Finance</div>
          <span className="card-lbl">Current Bank Balance</span>
          <h2 className="card-val text-emerald">₹{bankBalance.toLocaleString()}</h2>
          <span className="card-action-hint">Manage Transactions →</span>
        </div>

        {/* Card 2: Total Expenses */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("expenses")}>
          <div className="card-badge bg-rose-trans">📊 Expenses</div>
          <span className="card-lbl">Total Expenses Recorded</span>
          <h2 className="card-val text-rose">₹{totalExpenses.toLocaleString()}</h2>
          <span className="card-action-hint">Add Expenses →</span>
        </div>

        {/* Card 3: Budget Utilization */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("budget")}>
          <div className="card-badge bg-indigo-trans">💰 Budgets</div>
          <span className="card-lbl">Monthly Budget Allocation</span>
          <h2 className="card-val text-indigo">{budgetPercent}% Used</h2>
          <div className="progress-bar-bg mini-bar">
            <div className="progress-bar-fill bg-indigo" style={{ width: `${budgetPercent}%` }}></div>
          </div>
          <span className="card-action-hint">Check Allocations →</span>
        </div>

        {/* Card 4: Medicine Compliance */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("medicines")}>
          <div className="card-badge bg-teal-trans">💊 Medicine</div>
          <span className="card-lbl">Prescription Compliance</span>
          <h2 className="card-val text-teal">{medicineRate}% Taken</h2>
          <div className="progress-bar-bg mini-bar">
            <div className="progress-bar-fill bg-teal" style={{ width: `${medicineRate}%` }}></div>
          </div>
          <span className="card-action-hint">Log Prescriptions →</span>
        </div>

        {/* Card 5: Appointments */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("appointments")}>
          <div className="card-badge bg-amber-trans">🩺 Clinical</div>
          <span className="card-lbl">Active Consultations</span>
          <h2 className="card-val text-amber">{appointmentCount} Booked</h2>
          <span className="card-action-hint">Schedule Slots →</span>
        </div>

        {/* Card 6: Patients */}
        <div className="dashboard-card hover-glow" onClick={() => setTab("patients")}>
          <div className="card-badge bg-blue-trans">📋 Patient Database</div>
          <span className="card-lbl">Total Intake Intake Records</span>
          <h2 className="card-val text-blue">{patientCount} Patients</h2>
          <span className="card-action-hint">Intake Directory →</span>
        </div>
      </div>

      <div className="quick-start-section">
        <h3>⚡ Quick Navigation Tools</h3>
        <div className="tools-buttons-grid">
          <button className="quick-btn" onClick={() => setTab("emi")}>
            🧮 Loan EMI Calculator
          </button>
          <button className="quick-btn" onClick={() => setTab("expenses")}>
            💸 Record Expense
          </button>
          <button className="quick-btn" onClick={() => setTab("medicines")}>
            🔔 Take Prescriptions
          </button>
          <button className="quick-btn" onClick={() => setTab("bank")}>
            🏦 Manage Bank Cash
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomeDashboard;
