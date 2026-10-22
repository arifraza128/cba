import { useState } from "react";

function AppointmentForm({
    selectedDoctor,
    addAppointment
}) {

    const [date, setDate] = useState("");
    const [time, setTime] = useState("");

    const [patientName, setPatientName] =
        useState("");

    const [patientAge, setPatientAge] =
        useState("");


    const handleSubmit = (e) => {

        e.preventDefault();

        if (!selectedDoctor) {
            alert("Please select a doctor");
            return;
        }

        addAppointment({
            doctor: selectedDoctor,
            date,
            time,
            patientName,
            patientAge
        });

        setDate("");
        setTime("");
        setPatientName("");
        setPatientAge("");
    };


    return (

        <form onSubmit={handleSubmit}>

            <h2>Book Appointment</h2>

            <input
                type="date"
                value={date}
                onChange={(e) =>
                    setDate(e.target.value)
                }
            />

            <input
                type="time"
                value={time}
                onChange={(e) =>
                    setTime(e.target.value)
                }
            />

            <input
                type="text"
                placeholder="Patient Name"
                value={patientName}
                onChange={(e) =>
                    setPatientName(e.target.value)
                }
            />

            <input
                type="number"
                placeholder="Patient Age"
                value={patientAge}
                onChange={(e) =>
                    setPatientAge(e.target.value)
                }
            />

            <button type="submit">
                Book Appointment
            </button>

        </form>

    );
}

export default AppointmentForm;
