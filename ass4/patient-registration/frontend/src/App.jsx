import { useEffect, useState } from "react";
import "./App.css";

function App() {

    const [patients, setPatients] = useState([]);

    const [form, setForm] = useState({
        name: "",
        age: "",
        gender: "",
        phone: "",
        address: "",
        bloodGroup: "",
        symptoms: ""
    });

    const [search, setSearch] = useState("");
    const [editId, setEditId] = useState(null);

    // Get patients
    const fetchPatients = async () => {
        const response = await fetch("http://localhost:5000/patients");
        const data = await response.json();

        setPatients(data);
    };

    useEffect(() => {
        fetchPatients();
    }, []);

    // Handle form input
    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    // Register / Update patient
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (editId) {

            await fetch(`http://localhost:5000/patients/${editId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(form)
            });

            setEditId(null);

        } else {

            await fetch("http://localhost:5000/patients", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(form)
            });
        }

        setForm({
            name: "",
            age: "",
            gender: "",
            phone: "",
            address: "",
            bloodGroup: "",
            symptoms: ""
        });

        fetchPatients();
    };

    // Delete patient
    const deletePatient = async (id) => {

        await fetch(`http://localhost:5000/patients/${id}`, {
            method: "DELETE"
        });

        fetchPatients();
    };

    // Edit patient
    const editPatient = (patient) => {

        setForm({
            name: patient.name,
            age: patient.age,
            gender: patient.gender,
            phone: patient.phone,
            address: patient.address,
            bloodGroup: patient.bloodGroup,
            symptoms: patient.symptoms
        });

        setEditId(patient.id);
    };

    // Search
    const filteredPatients = patients.filter((patient) =>
        patient.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="container">

            <h1>Patient Registration System</h1>

            {/* Patient Form */}

            <form onSubmit={handleSubmit}>

                <input
                    type="text"
                    name="name"
                    placeholder="Patient Name"
                    value={form.name}
                    onChange={handleChange}
                    required
                />

                <input
                    type="number"
                    name="age"
                    placeholder="Age"
                    value={form.age}
                    onChange={handleChange}
                    required
                />

                <select
                    name="gender"
                    value={form.gender}
                    onChange={handleChange}
                    required
                >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>

                <input
                    type="text"
                    name="phone"
                    placeholder="Phone"
                    value={form.phone}
                    onChange={handleChange}
                    required
                />

                <input
                    type="text"
                    name="address"
                    placeholder="Address"
                    value={form.address}
                    onChange={handleChange}
                />

                <select
                    name="bloodGroup"
                    value={form.bloodGroup}
                    onChange={handleChange}
                >
                    <option value="">Select Blood Group</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                </select>

                <textarea
                    name="symptoms"
                    placeholder="Symptoms"
                    value={form.symptoms}
                    onChange={handleChange}
                />

                <button type="submit">
                    {editId ? "Update Patient" : "Register Patient"}
                </button>

            </form>

            <hr />

            {/* Search */}

            <input
                type="text"
                placeholder="Search patient by name..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />

            <h2>Patient List</h2>

            {/* Patient List */}

            {filteredPatients.length === 0 ? (

                <p>No patients found.</p>

            ) : (

                filteredPatients.map((patient) => (

                    <div className="patient" key={patient.id}>

                        <h3>{patient.name}</h3>

                        <p>Age: {patient.age}</p>

                        <p>Gender: {patient.gender}</p>

                        <p>Phone: {patient.phone}</p>

                        <p>Address: {patient.address}</p>

                        <p>Blood Group: {patient.bloodGroup}</p>

                        <p>Symptoms: {patient.symptoms}</p>

                        <button onClick={() => editPatient(patient)}>
                            Edit
                        </button>

                        <button onClick={() => deletePatient(patient.id)}>
                            Delete
                        </button>

                    </div>

                ))
            )}

        </div>
    );
}

export default App;
