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
SELECT
    a.Appointment_ID,
    p.Patient_Name,
    d.Doctor_Name,
    d.Specialization,
    d.Room,
    a.Appointment_Date,
    t.Treatment_Name
FROM APPOINTMENT a

JOIN PATIENT p
    ON a.Patient_ID = p.Patient_ID

JOIN DOCTOR d
    ON a.Doctor_ID = d.Doctor_ID

JOIN APPOINTMENT_TREATMENT at
    ON a.Appointment_ID = at.Appointment_ID

JOIN TREATMENT t
    ON at.Treatment_ID = t.Treatment_ID;
