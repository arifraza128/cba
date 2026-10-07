CREATE DATABASE SchoolAdmission;
USE SchoolAdmission;
CREATE TABLE Students (
    StudentID INT PRIMARY KEY IDENTITY(1,1),
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(200)
);
