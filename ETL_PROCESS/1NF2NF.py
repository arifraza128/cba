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

CREATE TABLE COURSE (
    Course_ID VARCHAR(10) PRIMARY KEY,
    Course_Name VARCHAR(50),
    Instructor VARCHAR(50)
);

INSERT INTO COURSE VALUES
('C01', 'DBMS', 'Sharma'),
('C02', 'Java', 'Rao'),
('C03', 'Python', 'Khan');

CREATE TABLE ENROLLMENT (
    Student_ID VARCHAR(10),
    Course_ID VARCHAR(10),
    Grade CHAR(1),

    PRIMARY KEY (Student_ID, Course_ID),

    FOREIGN KEY (Student_ID)
        REFERENCES STUDENT(Student_ID),

    FOREIGN KEY (Course_ID)
        REFERENCES COURSE(Course_ID)
);
