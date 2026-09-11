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
