import { useEffect, useState } from "react";

function DoctorAppointment({ onUpdate, showToast }) {
  const doctors = [
    { name: "Rahul Sharma", specialty: "Cardiologist (Heart Specialist)", icon: "❤️" },
    { name: "Priya Singh", specialty: "Dermatologist (Skin Care)", icon: "✨" },
    { name: "Amit Kumar", specialty: "General Physician", icon: "🩺" },
  ];

  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");

  const fetchAppointments = () => {
    fetch("http://localhost:5000/appointments")
      .then((res) => res.json())
      .then((data) => {
        setAppointments(data);
        if (onUpdate) onUpdate();
      })
      .catch((err) => console.error("Error fetching appointments:", err));
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const bookAppointment = (e) => {
    e.preventDefault();

    if (!selectedDoctor) {
      if (showToast) showToast("Please select a Doctor first!", "error");
      return;
    }
    if (!date || !time || !patientName || !patientAge) {
      if (showToast) showToast("Please fill in all appointment fields!", "error");
      return;
    }

    const newAppointment = {
      doctor: selectedDoctor,
      date,
      time,
      patientName,
      patientAge,
    };

    fetch("http://localhost:5000/appointments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newAppointment),
    })
      .then((res) => res.json())
      .then((data) => {
        setAppointments([...appointments, data]);
        setDate("");
        setTime("");
        setPatientName("");
        setPatientAge("");
        if (showToast) showToast("Appointment booked successfully!", "success");
        if (onUpdate) onUpdate();
      })
      .catch((err) => {
        console.error(err);
        if (showToast) showToast("Booking failed.", "error");
      });
  };

  const cancelAppointment = (id) => {
    fetch(`http://localhost:5000/appointments/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setAppointments(appointments.filter((app) => app.id !== id));
        if (showToast) showToast("Appointment cancelled successfully.", "info");
        if (onUpdate) onUpdate();
      })
      .catch((err) => {
        console.error(err);
        if (showToast) showToast("Failed to cancel appointment.", "error");
      });
  };

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>🩺 Doctor Appointment System</h2>
        <p>Choose an expert medical officer and schedule a visitation slot</p>
      </div>

      {/* Select Doctor Section */}
      <div className="card full-width-card">
        <h3>1. Select Medical Professional</h3>
        <div className="doctors-grid">
          {doctors.map((doc) => {
            const isSelected = selectedDoctor === doc.name;
            return (
              <div
                key={doc.name}
                className={`doctor-selection-card ${isSelected ? "selected" : ""}`}
                onClick={() => setSelectedDoctor(doc.name)}
              >
                <div className="doc-avatar">{doc.icon}</div>
                <div className="doc-meta">
                  <h4>Dr. {doc.name}</h4>
                  <p>{doc.specialty}</p>
                </div>
                <div className="selection-indicator">
                  {isSelected ? "✅ Selected" : "Choose"}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="module-grid">
        {/* Booking Form */}
        <div className="card form-card">
          <h3>2. Book Appointment</h3>
          {selectedDoctor ? (
            <p className="booking-notice">
              Booking slot with: <strong>Dr. {selectedDoctor}</strong>
            </p>
          ) : (
            <p className="booking-notice warning-notice">
              ⚠️ Please select a doctor above.
            </p>
          )}

          <form onSubmit={bookAppointment} className="modern-form">
            <div className="input-row">
              <div className="input-group">
                <label>Preferred Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  disabled={!selectedDoctor}
                />
              </div>

              <div className="input-group">
                <label>Preferred Time</label>
                <input
                  type="time"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  disabled={!selectedDoctor}
                />
              </div>
            </div>

            <div className="input-group">
              <label>Patient Name</label>
              <input
                type="text"
                placeholder="Enter patient full name"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                disabled={!selectedDoctor}
              />
            </div>

            <div className="input-group">
              <label>Patient Age</label>
              <input
                type="number"
                placeholder="Enter patient age"
                value={patientAge}
                onChange={(e) => setPatientAge(e.target.value)}
                disabled={!selectedDoctor}
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={!selectedDoctor}
            >
              📅 Schedule Consultation
            </button>
          </form>
        </div>

        {/* Booked Appointments List */}
        <div className="card list-card">
          <h3>3. Upcoming Schedule ({appointments.length})</h3>
          <div className="items-list scrollable">
            {appointments.length === 0 ? (
              <div className="empty-state">
                <span>📆</span>
                <p>No active appointments scheduled.</p>
              </div>
            ) : (
              appointments.map((app) => (
                <div className="appointment-card" key={app.id}>
                  <div className="app-main-details">
                    <div className="app-doctor-title">
                      Dr. {app.doctor}
                    </div>
                    <div className="app-patient-sub">
                      Patient: {app.patientName} ({app.patientAge} Yrs)
                    </div>
                    <div className="app-datetime-tag">
                      <span>📅 {app.date}</span>
                      <span>⏰ {app.time}</span>
                    </div>
                  </div>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => cancelAppointment(app.id)}
                  >
                    Cancel
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DoctorAppointment;
