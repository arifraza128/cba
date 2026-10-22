function AppointmentList({
    appointments,
    cancelAppointment
}) {

    return (

        <div>

            <h2>Upcoming Appointments</h2>

            {appointments.length === 0 ? (

                <p>No appointments.</p>

            ) : (

                appointments.map((appointment) => (

                    <div
                        className="appointment"
                        key={appointment.id}
                    >

                        <h3>
                            Dr. {appointment.doctor}
                        </h3>

                        <p>
                            Patient: {appointment.patientName}
                        </p>

                        <p>
                            Age: {appointment.patientAge}
                        </p>

                        <p>
                            Date: {appointment.date}
                        </p>

                        <p>
                            Time: {appointment.time}
                        </p>

                        <button
                            onClick={() =>
                                cancelAppointment(
                                    appointment.id
                                )
                            }
                        >
                            Cancel
                        </button>

                    </div>

                ))

            )}

        </div>

    );
}

export default AppointmentList;
