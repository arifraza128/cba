CREATE TABLE STUDENT (
    Student_ID VARCHAR(10) PRIMARY KEY,
    Student_Name VARCHAR(50)
);

INSERT INTO STUDENT VALUES
('S101', 'Rahul'),
('S102', 'Priya'),
('S103', 'Amit');

CREATE TABLE COURSE (
    Course_ID VARCHAR(10) PRIMARY KEY,
    Course_Name VARCHAR(50),
    Instructor VARCHAR(50)
);

INSERT INTO COURSE VALUES
('C01', 'DBMS', 'Sharma'),
('C02', 'Java', 'Rao'),
('C03', 'Python', 'Khan');
