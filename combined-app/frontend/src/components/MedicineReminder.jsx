import { useState, useEffect } from "react";

function MedicineReminder({ onUpdate, showToast }) {
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

  const [filter, setFilter] = useState("all");

  useEffect(() => {
    localStorage.setItem("medicines", JSON.stringify(medicines));
    if (onUpdate) onUpdate();
  }, [medicines]);

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
      if (showToast) showToast("Please fill in all fields", "error");
      return;
    }

    const start = new Date(medicine.startDate);
    const end = new Date(medicine.endDate);
    if (end < start) {
      if (showToast) showToast("End Date cannot be before Start Date", "error");
      return;
    }

    const newMedicine = {
      ...medicine,
      id: Date.now(),
      taken: false,
    };

    setMedicines([...medicines, newMedicine]);
    if (showToast) showToast(`${medicine.name} added successfully!`, "success");

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
          if (showToast) {
            showToast(
              updatedTaken
                ? `Marked ${item.name} as taken!`
                : `Marked ${item.name} as pending`,
              updatedTaken ? "success" : "info"
            );
          }
          return { ...item, taken: updatedTaken };
        }
        return item;
      })
    );
  };

  const deleteMedicine = (id, name) => {
    setMedicines(medicines.filter((item) => item.id !== id));
    if (showToast) showToast(`Removed ${name}`, "info");
  };

  const formatTime12hr = (timeStr) => {
    if (!timeStr) return "";
    const [hourStr, minStr] = timeStr.split(":");
    let hour = parseInt(hourStr, 10);
    const ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12;
    hour = hour ? hour : 12;
    return `${hour.toString().padStart(2, "0")}:${minStr} ${ampm}`;
  };

  const formatDatePretty = (dateStr) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const totalCount = medicines.length;
  const takenCount = medicines.filter((m) => m.taken).length;
  const completionRate = totalCount > 0 ? Math.round((takenCount / totalCount) * 100) : 0;

  const filteredMedicines = medicines.filter((item) => {
    if (filter === "taken") return item.taken;
    if (filter === "pending") return !item.taken;
    return true;
  });

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>💊 Medicine Reminder</h2>
        <p>Keep track of your active drug prescriptions, dosages, and compliance schedules</p>
      </div>

      {/* Progress section */}
      {totalCount > 0 && (
        <div className="card full-width-card stats-full-card">
          <div className="progress-info-row">
            <h3>Today's Medication Compliance</h3>
            <span className="percent-indicator">{completionRate}% Completed</span>
          </div>
          <div className="progress-bar-bg large-bar">
            <div className="progress-bar-fill bg-emerald" style={{ width: `${completionRate}%` }}></div>
          </div>
          <p className="compliance-text">
            You have taken <strong>{takenCount}</strong> out of <strong>{totalCount}</strong> scheduled prescriptions today.
          </p>
        </div>
      )}

      <div className="module-grid">
        {/* Medicine Form */}
        <div className="card form-card">
          <h3>Add Prescription</h3>
          <form onSubmit={addMedicine} className="modern-form">
            <div className="input-group">
              <label>Medicine Name</label>
              <input
                type="text"
                name="name"
                placeholder="e.g. Lipitor, Paracetamol"
                value={medicine.name}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Dosage</label>
              <input
                type="text"
                name="dosage"
                placeholder="e.g. 10mg or 1 tablet"
                value={medicine.dosage}
                onChange={handleChange}
              />
            </div>

            <div className="input-row">
              <div className="input-group">
                <label>Start Date</label>
                <input
                  type="date"
                  name="startDate"
                  value={medicine.startDate}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label>End Date</label>
                <input
                  type="date"
                  name="endDate"
                  value={medicine.endDate}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="input-row">
              <div className="input-group">
                <label>Time</label>
                <input
                  type="time"
                  name="time"
                  value={medicine.time}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label>Frequency</label>
                <select name="frequency" value={medicine.frequency} onChange={handleChange}>
                  <option value="Daily">Daily</option>
                  <option value="Twice a day">Twice a day</option>
                  <option value="Weekly">Weekly</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn btn-primary">
              💊 Register Prescription
            </button>
          </form>
        </div>

        {/* Medicine Listing */}
        <div className="card list-card">
          <div className="list-tab-header">
            <h3>Schedule Intake</h3>
            {totalCount > 0 && (
              <div className="mini-tabs">
                <button
                  className={filter === "all" ? "active-tab" : ""}
                  onClick={() => setFilter("all")}
                >
                  All ({totalCount})
                </button>
                <button
                  className={filter === "pending" ? "active-tab" : ""}
                  onClick={() => setFilter("pending")}
                >
                  Pending ({totalCount - takenCount})
                </button>
                <button
                  className={filter === "taken" ? "active-tab" : ""}
                  onClick={() => setFilter("taken")}
                >
                  Taken ({takenCount})
                </button>
              </div>
            )}
          </div>

          <div className="items-list scrollable">
            {filteredMedicines.length === 0 ? (
              <div className="empty-state">
                <span>🔔</span>
                <p>
                  {filter === "all"
                    ? "No medications scheduled yet."
                    : filter === "pending"
                    ? "All done! No pending medications left."
                    : "No medications marked as taken."}
                </p>
              </div>
            ) : (
              [...filteredMedicines]
                .sort((a, b) => a.time.localeCompare(b.time))
                .map((item) => (
                  <div className={`medicine-card-row ${item.taken ? "taken" : ""}`} key={item.id}>
                    <div className="med-row-info">
                      <div className="med-time-header">
                        <span className="time-badge">{formatTime12hr(item.time)}</span>
                        <h4>{item.name}</h4>
                      </div>
                      <div className="med-sub-details">
                        <span className="med-pill-badge">💊 {item.dosage}</span>
                        <span className="med-pill-badge">🔄 {item.frequency}</span>
                      </div>
                      <div className="med-duration">
                        📅 {formatDatePretty(item.startDate)} to {formatDatePretty(item.endDate)}
                      </div>
                    </div>
                    <div className="med-row-actions">
                      <button
                        onClick={() => markAsTaken(item.id)}
                        className={`btn btn-sm ${item.taken ? "btn-secondary" : "btn-emerald"}`}
                      >
                        {item.taken ? "✓ Taken" : "Take"}
                      </button>
                      <button
                        onClick={() => deleteMedicine(item.id, item.name)}
                        className="btn-icon-delete"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MedicineReminder;
