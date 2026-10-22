import { useState, useEffect } from "react";
import HomeDashboard from "./components/HomeDashboard";
import ExpenseTracker from "./components/ExpenseTracker";
import BudgetManager from "./components/BudgetManager";
import EmiCalculator from "./components/EmiCalculator";
import PatientRegistration from "./components/PatientRegistration";
import DoctorAppointment from "./components/DoctorAppointment";
import MedicineReminder from "./components/MedicineReminder";
import BankManager from "./components/BankManager";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("home");
  const [toast, setToast] = useState({ show: false, message: "", type: "success" });
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Trigger metrics update for the dashboard dynamically
  const [triggerUpdate, setTriggerUpdate] = useState(0);
  const handleUpdate = () => {
    setTriggerUpdate((prev) => prev + 1);
  };

  const showToast = (message, type = "success") => {
    setToast({ show: true, message, type });
    setTimeout(() => {
      setToast({ show: false, message: "", type: "success" });
    }, 4000);
  };

  return (
    <div className="app-container">
      {/* Toast Alert */}
      {toast.show && (
        <div className={`toast ${toast.type}`}>
          <span className="toast-icon">
            {toast.type === "success" && "✨"}
            {toast.type === "error" && "⚠️"}
            {toast.type === "info" && "ℹ️"}
          </span>
          <p className="toast-msg">{toast.message}</p>
        </div>
      )}

      {/* Sidebar Nav */}
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-logo">
          <h2>🏥 Finance &amp; Health</h2>
          <span className="suite-tag">Dashboard Suite</span>
        </div>

        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeTab === "home" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("home");
              setSidebarOpen(false);
            }}
          >
            🏠 Home Dashboard
          </button>
          <button
            className={`nav-item ${activeTab === "expenses" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("expenses");
              setSidebarOpen(false);
            }}
          >
            📊 Expense Tracker
          </button>
          <button
            className={`nav-item ${activeTab === "budget" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("budget");
              setSidebarOpen(false);
            }}
          >
            💰 Budget Manager
          </button>
          <button
            className={`nav-item ${activeTab === "emi" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("emi");
              setSidebarOpen(false);
            }}
          >
            🧮 EMI Calculator
          </button>
          <button
            className={`nav-item ${activeTab === "patients" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("patients");
              setSidebarOpen(false);
            }}
          >
            📋 Patient Intake
          </button>
          <button
            className={`nav-item ${activeTab === "appointments" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("appointments");
              setSidebarOpen(false);
            }}
          >
            🩺 Doctor Booking
          </button>
          <button
            className={`nav-item ${activeTab === "medicines" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("medicines");
              setSidebarOpen(false);
            }}
          >
            💊 Med Reminder
          </button>
          <button
            className={`nav-item ${activeTab === "bank" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("bank");
              setSidebarOpen(false);
            }}
          >
            🏦 Bank Accounts
          </button>
        </nav>

        <div className="sidebar-footer">
          <p>© 2026 Integrated Suite</p>
        </div>
      </aside>

      {/* Main Panel Content */}
      <main className="main-content">
        <header className="main-header">
          <button
            className="menu-toggle-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰ Menu
          </button>
          <div className="user-profile">
            <span className="pulse-dot"></span>
            <strong>Local Host Operator</strong>
          </div>
        </header>

        <section className="content-area">
          {activeTab === "home" && (
            <HomeDashboard setTab={setActiveTab} key={triggerUpdate} />
          )}
          {activeTab === "expenses" && (
            <ExpenseTracker onUpdate={handleUpdate} showToast={showToast} />
          )}
          {activeTab === "budget" && (
            <BudgetManager onUpdate={handleUpdate} showToast={showToast} />
          )}
          {activeTab === "emi" && (
            <EmiCalculator showToast={showToast} />
          )}
          {activeTab === "patients" && (
            <PatientRegistration onUpdate={handleUpdate} showToast={showToast} />
          )}
          {activeTab === "appointments" && (
            <DoctorAppointment onUpdate={handleUpdate} showToast={showToast} />
          )}
          {activeTab === "medicines" && (
            <MedicineReminder onUpdate={handleUpdate} showToast={showToast} />
          )}
          {activeTab === "bank" && (
            <BankManager onUpdate={handleUpdate} showToast={showToast} />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
