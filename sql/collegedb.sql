CREATE DATABASE CollegeDB;
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Department VARCHAR(50),
    Marks INT
);
INSERT INTO Students (StudentID, Name, Age, Department, Marks)
VALUES
(1, 'Arif', 21, 'CSE', 85),
(2, 'Rahul', 22, 'ECE', 78),
(3, 'Aman', 20, 'CSE', 92),
(4, 'Priya', 21, 'ISE', 88),
(5, 'Sneha', 22, 'CSE', 74);
