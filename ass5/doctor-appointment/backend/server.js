const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();

app.use(cors());
app.use(express.json());


// Get appointments
app.get("/appointments", (req, res) => {

    const data = fs.readFileSync("appointments.json");

    const appointments = JSON.parse(data);

    res.json(appointments);
});


// Book appointment
app.post("/appointments", (req, res) => {

    const data = fs.readFileSync("appointments.json");

    const appointments = JSON.parse(data);

    const newAppointment = {
        id: Date.now(),

        doctor: req.body.doctor,

        date: req.body.date,

        time: req.body.time,

        patientName: req.body.patientName,

        patientAge: req.body.patientAge
    };

    appointments.push(newAppointment);

    fs.writeFileSync(
        "appointments.json",
        JSON.stringify(appointments, null, 2)
    );

    res.json(newAppointment);
});


// Cancel appointment
app.delete("/appointments/:id", (req, res) => {

    const data = fs.readFileSync("appointments.json");

    let appointments = JSON.parse(data);

    appointments = appointments.filter(
        appointment =>
            appointment.id != req.params.id
    );

    fs.writeFileSync(
        "appointments.json",
        JSON.stringify(appointments, null, 2)
    );

    res.json({
        message: "Appointment cancelled"
    });
});


app.listen(5000, () => {

    console.log(
        "Server running on port 5000"
    );

});
