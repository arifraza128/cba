CREATE TABLE Student_Courses_UNF (
    Student_ID VARCHAR(10),
    Student_Name VARCHAR(50),
    Courses VARCHAR(200)
);

INSERT INTO Student_Courses_UNF VALUES
('S101', 'Rahul', 'DBMS, Java, Python'),
('S102', 'Priya', 'DBMS, Python'),
('S103', 'Amit', 'Java, C#');

CREATE TABLE Student_Courses_1NF (
    Student_ID VARCHAR(10),
    Student_Name VARCHAR(50),
    Course VARCHAR(50),
    PRIMARY KEY (Student_ID, Course)
);

INSERT INTO Student_Courses_1NF VALUES
('S101', 'Rahul', 'DBMS'),
('S101', 'Rahul', 'Java'),
('S101', 'Rahul', 'Python'),
('S102', 'Priya', 'DBMS'),
('S102', 'Priya', 'Python'),
('S103', 'Amit', 'Java'),
('S103', 'Amit', 'C#');

SELECT * FROM Student_Courses_1NF;
