import { useState, useEffect } from "react";
import "./App.css";

function App() {
  // Initialize medicines from local storage or empty array
  const [medicines, setMedicines] = useState(() => {
    const saved = localStorage.getItem("medicines");
    return saved ? JSON.parse(saved) : [];
  });

  const [medicine, setMedicine] = useState({
    name: "",
    dosage: "",
    startDate: "",
    endDate: "",
    time: "",
    frequency: "Daily",
  });

  // Filter state: 'all', 'pending', 'taken'
  const [filter, setFilter] = useState("all");

  // Custom notification state (removes standard browser alert)
  const [notification, setNotification] = useState({
    show: false,
    message: "",
    type: "", // 'success', 'error', 'info'
  });

  // Save to local storage whenever medicines change
  useEffect(() => {
    localStorage.setItem("medicines", JSON.stringify(medicines));
  }, [medicines]);

  const showToast = (message, type = "success") => {
    setNotification({ show: true, message, type });
    setTimeout(() => {
      setNotification({ show: false, message: "", type: "" });
    }, 4000);
  };

  const handleChange = (e) => {
    setMedicine({
      ...medicine,
      [e.target.name]: e.target.value,
    });
  };

  const addMedicine = (e) => {
    e.preventDefault();

    if (
      !medicine.name ||
      !medicine.dosage ||
      !medicine.startDate ||
      !medicine.endDate ||
      !medicine.time
    ) {
      showToast("Please fill in all fields", "error");
      return;
    }

    // Validate dates
    const start = new Date(medicine.startDate);
    const end = new Date(medicine.endDate);
    if (end < start) {
      showToast("End Date cannot be before Start Date", "error");
      return;
    }

    const newMedicine = {
      ...medicine,
      id: Date.now(),
      taken: false,
    };

    setMedicines([...medicines, newMedicine]);
    showToast(`${medicine.name} added successfully!`, "success");

    setMedicine({
      name: "",
      dosage: "",
      startDate: "",
      endDate: "",
      time: "",
      frequency: "Daily",
    });
  };

  const markAsTaken = (id) => {
    setMedicines(
      medicines.map((item) => {
        if (item.id === id) {
          const updatedTaken = !item.taken;
          showToast(
            updatedTaken
              ? `Marked ${item.name} as taken!`
              : `Marked ${item.name} as pending`,
            updatedTaken ? "success" : "info"
          );
          return { ...item, taken: updatedTaken };
        }
        return item;
      })
    );
  };

  const deleteMedicine = (id, name) => {
    setMedicines(medicines.filter((item) => item.id !== id));
    showToast(`Removed ${name}`, "info");
  };

  // Convert time input (HH:MM) to readable AM/PM format
  const formatTime12hr = (timeStr) => {
    if (!timeStr) return "";
    const [hourStr, minStr] = timeStr.split(":");
    let hour = parseInt(hourStr, 10);
    const ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12;
    hour = hour ? hour : 12; // the hour '0' should be '12'
    return `${hour.toString().padStart(2, "0")}:${minStr} ${ampm}`;
  };

  // Format YYYY-MM-DD to a prettier date format
  const formatDatePretty = (dateStr) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  // Stats calculations
  const totalCount = medicines.length;
  const takenCount = medicines.filter((m) => m.taken).length;
  const completionRate = totalCount > 0 ? Math.round((takenCount / totalCount) * 100) : 0;

  // Filter medicines list
  const filteredMedicines = medicines.filter((item) => {
    if (filter === "taken") return item.taken;
    if (filter === "pending") return !item.taken;
    return true; // 'all'
  });

  return (
    <div className="container">
      {/* Toast Notification */}
      {notification.show && (
        <div className={`toast-notification ${notification.type}`}>
          <div className="toast-content">
            <span className="toast-icon">
              {notification.type === "success" && "✨"}
              {notification.type === "error" && "⚠️"}
              {notification.type === "info" && "ℹ️"}
            </span>
            <p>{notification.message}</p>
          </div>
        </div>
      )}

      <header className="app-header">
        <h1>💊 Medicine Reminder</h1>
        <p className="app-subtitle">Track and manage your daily prescriptions seamlessly</p>
      </header>

      {/* Stats Section */}
      {totalCount > 0 && (
        <div className="stats-container">
          <div className="stats-info">
            <span>Today's Progress</span>
            <span className="stats-percentage">{completionRate}% Completed</span>
          </div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill" style={{ width: `${completionRate}%` }}></div>
          </div>
          <p className="stats-summary">
            Taken <strong>{takenCount}</strong> of <strong>{totalCount}</strong> scheduled medications.
          </p>
        </div>
      )}

      <div className="app-layout">
        {/* Medicine Form */}
        <section className="form-section">
          <h2>Add New Medication</h2>
          <form onSubmit={addMedicine} className="medicine-form">
            <div className="input-group">
              <label htmlFor="med-name">Medicine Name</label>
              <input
                id="med-name"
                type="text"
                name="name"
                placeholder="e.g. Paracetamol"
                value={medicine.name}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label htmlFor="med-dosage">Dosage</label>
              <input
                id="med-dosage"
                type="text"
                name="dosage"
                placeholder="e.g. 500mg or 1 tablet"
                value={medicine.dosage}
                onChange={handleChange}
              />
            </div>

            <div className="input-row">
              <div className="input-group">
                <label htmlFor="med-start">Start Date</label>
                <input
                  id="med-start"
                  type="date"
                  name="startDate"
                  value={medicine.startDate}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label htmlFor="med-end">End Date</label>
                <input
                  id="med-end"
                  type="date"
                  name="endDate"
                  value={medicine.endDate}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="input-row">
              <div className="input-group">
                <label htmlFor="med-time">Time</label>
                <input
                  id="med-time"
                  type="time"
                  name="time"
                  value={medicine.time}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label htmlFor="med-freq">Frequency</label>
                <select
                  id="med-freq"
                  name="frequency"
                  value={medicine.frequency}
                  onChange={handleChange}
                >
                  <option value="Daily">Daily</option>
                  <option value="Twice a day">Twice a day</option>
                  <option value="Weekly">Weekly</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn-submit">Add Medicine</button>
          </form>
        </section>

        {/* Medicine List */}
        <section className="list-section">
          <div className="list-header">
            <h2>Today's Medicines</h2>
            {totalCount > 0 && (
              <div className="filter-tabs">
                <button
                  onClick={() => setFilter("all")}
                  className={filter === "all" ? "active" : ""}
                >
                  All ({totalCount})
                </button>
                <button
                  onClick={() => setFilter("pending")}
                  className={filter === "pending" ? "active" : ""}
                >
                  Pending ({totalCount - takenCount})
                </button>
                <button
                  onClick={() => setFilter("taken")}
                  className={filter === "taken" ? "active" : ""}
                >
                  Taken ({takenCount})
                </button>
              </div>
            )}
          </div>

          <div className="medicine-list">
            {filteredMedicines.length === 0 ? (
              <div className="empty-state">
                <span className="empty-icon">🔔</span>
                <p>
                  {filter === "all"
                    ? "No medicines added yet. Fill out the form to start tracking!"
                    : filter === "pending"
                    ? "All done! You have no pending medications."
                    : "No medications have been marked as taken today."}
                </p>
              </div>
            ) : (
              // Sort medications by time
              [...filteredMedicines]
                .sort((a, b) => a.time.localeCompare(b.time))
                .map((item) => (
                  <div className={`medicine-card ${item.taken ? "card-taken" : ""}`} key={item.id}>
                    <div className="card-info">
                      <div className="card-header-row">
                        <span className="time-badge">{formatTime12hr(item.time)}</span>
                        <h3 className="med-title">{item.name}</h3>
                      </div>

                      <div className="med-details">
                        <span className="detail-pill dosage-pill">💊 {item.dosage}</span>
                        <span className="detail-pill freq-pill">🔄 {item.frequency}</span>
                      </div>

                      <p className="med-dates">
                        📅 {formatDatePretty(item.startDate)} to {formatDatePretty(item.endDate)}
                      </p>
                    </div>

                    <div className="card-actions">
                      <button
                        onClick={() => markAsTaken(item.id)}
                        className={`btn-taken-toggle ${item.taken ? "taken" : ""}`}
                      >
                        {item.taken ? "✅ Taken" : "Mark as Taken"}
                      </button>
                      <button
                        onClick={() => deleteMedicine(item.id, item.name)}
                        className="btn-delete"
                        title="Delete Medication"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
