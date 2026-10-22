function DoctorList({ doctors, selectedDoctor, setSelectedDoctor }) {

    return (

        <div>

            <h2>Doctors</h2>

            {doctors.map((doctor) => (

                <button
                    key={doctor}
                    onClick={() =>
                        setSelectedDoctor(doctor)
                    }
                >
                    {doctor}
                </button>

            ))}

            {selectedDoctor && (

                <p>
                    Selected Doctor: {selectedDoctor}
                </p>

            )}

        </div>

    );
}

export default DoctorList;
