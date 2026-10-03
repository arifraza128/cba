CREATE TABLE APPOINTMENT_TREATMENT (
    Appointment_ID VARCHAR(10),
    Treatment_ID VARCHAR(10),

    PRIMARY KEY (Appointment_ID, Treatment_ID),

    FOREIGN KEY (Appointment_ID)
        REFERENCES APPOINTMENT(Appointment_ID),

    FOREIGN KEY (Treatment_ID)
        REFERENCES TREATMENT(Treatment_ID)
);
