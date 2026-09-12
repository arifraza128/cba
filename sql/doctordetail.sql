CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY IDENTITY(1,1),
    DoctorName VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100) NOT NULL,
    Gender VARCHAR(10),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    Qualification VARCHAR(100),
    ExperienceYears INT,
    Department VARCHAR(100),
    ConsultationFee DECIMAL(10,2),
    JoiningDate DATE
);
INSERT INTO Doctors
(DoctorName, Specialization, Gender, Phone, Email, Qualification, ExperienceYears, Department, ConsultationFee, JoiningDate)
VALUES
('Dr. Rahul Sharma', 'Cardiologist', 'Male', '9876543210', 'rahul@gmail.com', 'MBBS, MD', 10, 'Cardiology', 800.00, '2022-06-15'),
('Dr. Priya Singh', 'Dermatologist', 'Female', '9876543211', 'priya@gmail.com', 'MBBS, MD', 7, 'Dermatology', 600.00, '2023-01-10'),
('Dr. Arjun Kumar', 'Orthopedic', 'Male', '9876543212', 'arjun@gmail.com', 'MBBS, MS', 8, 'Orthopedics', 700.00, '2021-08-20');
INSERT INTO Doctor VALUES
(101, 'Rahul Sharma', 'Cardiologist', 45, '9876543210', 90000),
(102, 'Priya Singh', 'Dentist', 38, '9876543211', 70000),
(103, 'Amit Kumar', 'Neurologist', 50, '9876543212', 120000),
(104, 'Sneha Rao', 'Pediatrician', 35, '9876543213', 65000);
