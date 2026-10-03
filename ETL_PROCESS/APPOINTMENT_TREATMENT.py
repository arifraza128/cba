CREATE TABLE APPOINTMENT_TREATMENT (
    Appointment_ID VARCHAR(10),
    Treatment_ID VARCHAR(10),

    PRIMARY KEY (Appointment_ID, Treatment_ID),

    FOREIGN KEY (Appointment_ID)
        REFERENCES APPOINTMENT(Appointment_ID),

    FOREIGN KEY (Treatment_ID)
        REFERENCES TREATMENT(Treatment_ID)
);
INSERT INTO APPOINTMENT_TREATMENT VALUES
('A001', 'T01'),
('A001', 'T02'),
('A002', 'T03'),
('A003', 'T03'),
('A003', 'T04'),
('A004', 'T01');
