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
INSERT INTO Doctor VALUES
(105, 'Vikram Patel', 'General Physician', 42, '9876543214', 60000),
(106, 'Anjali Mehta', 'Gynecologist', 39, '9876543215', 85000),
(107, 'Karan Verma', 'ENT Specialist', 47, '9876543216', 75000),
(108, 'Neha Kapoor', 'Dermatologist', 34, '9876543217', 70000),
(109, 'Rohit Nair', 'Orthopedic', 51, '9876543218', 95000),
(110, 'Pooja Iyer', 'Psychiatrist', 41, '9876543219', 90000),
(111, 'Sanjay Rao', 'Cardiologist', 55, '9876543220', 110000),
(112, 'Meera Joshi', 'Pediatrician', 36, '9876543221', 65000),
(113, 'Arun Das', 'Neurologist', 49, '9876543222', 105000),
(114, 'Kavya Reddy', 'Ophthalmologist', 37, '9876543223', 72000),
(115, 'Manoj Singh', 'General Surgeon', 46, '9876543224', 100000),
(116, 'Divya Shah', 'Radiologist', 40, '9876543225', 88000);
