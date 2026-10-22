const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;
const FILE = "./patients.json";

// Get all patients
app.get("/patients", (req, res) => {
    const patients = JSON.parse(fs.readFileSync(FILE));
    res.json(patients);
});

// Register patient
app.post("/patients", (req, res) => {
    const patients = JSON.parse(fs.readFileSync(FILE));

    const newPatient = {
        id: Date.now(),
        name: req.body.name,
        age: req.body.age,
        gender: req.body.gender,
        phone: req.body.phone,
        address: req.body.address,
        bloodGroup: req.body.bloodGroup,
        symptoms: req.body.symptoms
    };

    patients.push(newPatient);

    fs.writeFileSync(FILE, JSON.stringify(patients, null, 2));

    res.json(newPatient);
});

// Edit patient
app.put("/patients/:id", (req, res) => {
    const patients = JSON.parse(fs.readFileSync(FILE));

    const id = Number(req.params.id);

    const index = patients.findIndex(patient => patient.id === id);

    if (index === -1) {
        return res.status(404).json({
            message: "Patient not found"
        });
    }

    patients[index] = {
        ...patients[index],
        ...req.body
    };

    fs.writeFileSync(FILE, JSON.stringify(patients, null, 2));

    res.json(patients[index]);
});

// Delete patient
app.delete("/patients/:id", (req, res) => {
    const patients = JSON.parse(fs.readFileSync(FILE));

    const id = Number(req.params.id);

    const filteredPatients = patients.filter(
        patient => patient.id !== id
    );

    fs.writeFileSync(FILE, JSON.stringify(filteredPatients, null, 2));

    res.json({
        message: "Patient deleted successfully"
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
