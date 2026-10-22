import { useEffect, useState } from "react";

import DoctorList from "./components/DoctorList";
import AppointmentForm from "./components/AppointmentForm";
import AppointmentList from "./components/AppointmentList";

import "./App.css";


function App() {

    const doctors = [
        "Rahul Sharma",
        "Priya Singh",
        "Amit Kumar"
    ];


    const [selectedDoctor, setSelectedDoctor] =
        useState("");

    const [appointments, setAppointments] =
        useState([]);


    // Get appointments
    useEffect(() => {

        fetch("http://localhost:5000/appointments")
            .then(response => response.json())
            .then(data => {
                setAppointments(data);
            });

    }, []);


    // Add appointment
    const addAppointment = (appointment) => {

        fetch("http://localhost:5000/appointments", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(appointment)

        })
        .then(response => response.json())
        .then(data => {

            setAppointments([
                ...appointments,
                data
            ]);

        });

    };


    // Cancel appointment
    const cancelAppointment = (id) => {

        fetch(
            `http://localhost:5000/appointments/${id}`,
            {
                method: "DELETE"
            }
        )
        .then(() => {

            setAppointments(
                appointments.filter(
                    appointment =>
                        appointment.id !== id
                )
            );

        });

    };


    return (

        <div className="container">

            <h1>
                🩺 Doctor Appointment System
            </h1>


            <DoctorList
                doctors={doctors}
                selectedDoctor={selectedDoctor}
                setSelectedDoctor={setSelectedDoctor}
            />


            <AppointmentForm
                selectedDoctor={selectedDoctor}
                addAppointment={addAppointment}
            />


            <AppointmentList
                appointments={appointments}
                cancelAppointment={cancelAppointment}
            />

        </div>

    );
}

export default App;
