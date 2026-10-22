import { useEffect, useState } from "react";

function PatientRegistration({ onUpdate, showToast }) {
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    phone: "",
    address: "",
    bloodGroup: "",
    symptoms: "",
  });

  const [search, setSearch] = useState("");
  const [editId, setEditId] = useState(null);

  const fetchPatients = async () => {
    try {
      const response = await fetch("http://localhost:5000/patients");
      const data = await response.json();
      setPatients(data);
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error("Error fetching patients:", error);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.name || !form.age || !form.gender || !form.phone) {
      if (showToast) showToast("Name, Age, Gender and Phone are required!", "error");
      return;
    }

    try {
      if (editId) {
        await fetch(`http://localhost:5000/patients/${editId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        });
        setEditId(null);
        if (showToast) showToast("Patient profile updated!", "success");
      } else {
        await fetch("http://localhost:5000/patients", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        });
        if (showToast) showToast("Patient registered successfully!", "success");
      }

      setForm({
        name: "",
        age: "",
        gender: "",
        phone: "",
        address: "",
        bloodGroup: "",
        symptoms: "",
      });

      fetchPatients();
    } catch (error) {
      console.error(error);
      if (showToast) showToast("Failed to submit patient data.", "error");
    }
  };

  const deletePatient = async (id) => {
    try {
      await fetch(`http://localhost:5000/patients/${id}`, {
        method: "DELETE",
      });
      if (showToast) showToast("Patient record removed.", "info");
      fetchPatients();
    } catch (error) {
      console.error(error);
      if (showToast) showToast("Failed to delete patient.", "error");
    }
  };

  const editPatient = (p) => {
    setForm({
      name: p.name,
      age: p.age,
      gender: p.gender,
      phone: p.phone,
      address: p.address,
      bloodGroup: p.bloodGroup,
      symptoms: p.symptoms,
    });
    setEditId(p.id);
    if (showToast) showToast(`Editing profile of ${p.name}`, "info");
  };

  const filteredPatients = patients.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>📋 Patient Registration System</h2>
        <p>Register new clinical intakes, search database records, and update details</p>
      </div>

      <div className="module-grid wide-grid">
        {/* Form Registration */}
        <div className="card form-card">
          <h3>{editId ? "✏️ Edit Patient Record" : "➕ Patient Intake Form"}</h3>
          <form onSubmit={handleSubmit} className="modern-form">
            <div className="input-group">
              <label>Full Name</label>
              <input
                type="text"
                name="name"
                placeholder="e.g. John Doe"
                value={form.name}
                onChange={handleChange}
              />
            </div>

            <div className="input-row">
              <div className="input-group">
                <label>Age</label>
                <input
                  type="number"
                  name="age"
                  placeholder="e.g. 45"
                  value={form.age}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label>Gender</label>
                <select name="gender" value={form.gender} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="input-row">
              <div className="input-group">
                <label>Phone Number</label>
                <input
                  type="text"
                  name="phone"
                  placeholder="e.g. +91 9876543210"
                  value={form.phone}
                  onChange={handleChange}
                />
              </div>

              <div className="input-group">
                <label>Blood Group</label>
                <select name="bloodGroup" value={form.bloodGroup} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </div>
            </div>

            <div className="input-group">
              <label>Home Address</label>
              <input
                type="text"
                name="address"
                placeholder="e.g. 123 Main St, New Delhi"
                value={form.address}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Reported Symptoms</label>
              <textarea
                name="symptoms"
                rows="3"
                placeholder="e.g. Fever, persistent cough, fatigue"
                value={form.symptoms}
                onChange={handleChange}
              />
            </div>

            <div className="form-actions-row">
              <button type="submit" className="btn btn-primary">
                {editId ? "Update Record" : "Register Intake"}
              </button>
              {editId && (
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setEditId(null);
                    setForm({
                      name: "",
                      age: "",
                      gender: "",
                      phone: "",
                      address: "",
                      bloodGroup: "",
                      symptoms: "",
                    });
                  }}
                >
                  Cancel Edit
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Database Search & List */}
        <div className="card list-card">
          <div className="search-bar-header">
            <h3>Registered Directory</h3>
            <input
              type="text"
              className="search-input"
              placeholder="🔍 Search patients by name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="items-list scrollable patient-list">
            {filteredPatients.length === 0 ? (
              <div className="empty-state">
                <span>📋</span>
                <p>{search ? "No matching patients found." : "No registered patients. Form an intake above."}</p>
              </div>
            ) : (
              filteredPatients.map((p) => (
                <div className="patient-record-card" key={p.id}>
                  <div className="record-header">
                    <div>
                      <h4>{p.name}</h4>
                      <span className="record-sub">
                        {p.gender}, {p.age} Yrs • {p.phone}
                      </span>
                    </div>
                    {p.bloodGroup && (
                      <span className="blood-badge">{p.bloodGroup}</span>
                    )}
                  </div>

                  {p.address && (
                    <div className="record-detail-row">
                      <strong>Address:</strong> <span>{p.address}</span>
                    </div>
                  )}

                  {p.symptoms && (
                    <div className="record-detail-row symptoms-row">
                      <strong>Symptoms:</strong> <span className="symptom-tag">{p.symptoms}</span>
                    </div>
                  )}

                  <div className="record-actions">
                    <button className="btn btn-sm btn-secondary" onClick={() => editPatient(p)}>
                      ✏️ Edit
                    </button>
                    <button className="btn btn-sm btn-danger" onClick={() => deletePatient(p.id)}>
                      🗑️ Remove
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

export default PatientRegistration;
