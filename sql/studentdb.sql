CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    email VARCHAR(100),
    phone VARCHAR(15),
    department VARCHAR(50),
    year INT,
    cgpa DECIMAL(3,2)
);
INSERT INTO Students
(student_id, name, age, gender, email, phone, department, year, cgpa)
VALUES
(1, 'Arif', 21, 'Male', 'arif@gmail.com', '9876543210', 'CSE', 4, 8.5),
(2, 'Rahul', 22, 'Male', 'rahul@gmail.com', '9876543211', 'ECE', 4, 7.8),
(3, 'Priya', 21, 'Female', 'priya@gmail.com', '9876543212', 'CSE', 3, 9.1),
(4, 'Anjali', 20, 'Female', 'anjali@gmail.com', '9876543213', 'ISE', 2, 8.7),
(5, 'Amit', 22, 'Male', 'amit@gmail.com', '9876543214', 'CSE', 4, 7.2);
/* selecting all from student */

SELECT * FROM Students;

/* select name and dept */

SELECT name, department
FROM Students;
/* finding cse students */
SELECT *
FROM Students
WHERE department = 'CSE';
/* find student whose cgpa is greater then 8 */
SELECT *
FROM Students
WHERE cgpa > 8;
