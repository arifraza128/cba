```sql
CREATE DATABASE CompanyDB;
GO

USE CompanyDB;
GO

CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);
GO

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    salary DECIMAL(10,2),
    hire_date DATE,
    department_id INT,
    manager_id INT NULL,

    CONSTRAINT FK_Employees_Department
        FOREIGN KEY (department_id)
        REFERENCES Departments(department_id),

    CONSTRAINT FK_Employees_Manager
        FOREIGN KEY (manager_id)
        REFERENCES Employees(employee_id)
);
GO

CREATE TABLE Projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    department_id INT,

    CONSTRAINT FK_Projects_Department
        FOREIGN KEY (department_id)
        REFERENCES Departments(department_id)
);
GO

CREATE TABLE EmployeeProjects (
    employee_id INT,
    project_id INT,
    assigned_date DATE,

    PRIMARY KEY (employee_id, project_id),

    CONSTRAINT FK_EmployeeProjects_Employee
        FOREIGN KEY (employee_id)
        REFERENCES Employees(employee_id),

    CONSTRAINT FK_EmployeeProjects_Project
        FOREIGN KEY (project_id)
        REFERENCES Projects(project_id)
);
GO

INSERT INTO Departments
(department_id, department_name, location)
VALUES
(1, 'IT', 'Bangalore'),
(2, 'HR', 'Mumbai'),
(3, 'Finance', 'Delhi'),
(4, 'Marketing', 'Hyderabad'),
(5, 'Sales', 'Chennai');
GO

INSERT INTO Employees
(employee_id, first_name, last_name, email, salary, hire_date, department_id, manager_id)
VALUES
(101, 'Rahul', 'Sharma', 'rahul@company.com', 75000, '2022-01-15', 1, NULL),
(102, 'Priya', 'Singh', 'priya@company.com', 65000, '2022-03-20', 2, NULL),
(103, 'Amit', 'Kumar', 'amit@company.com', 70000, '2023-02-10', 1, 101),
(104, 'Sneha', 'Patel', 'sneha@company.com', 60000, '2023-05-12', 3, NULL),
(105, 'Arjun', 'Verma', 'arjun@company.com', 55000, '2024-01-08', 1, 101),
(106, 'Neha', 'Gupta', 'neha@company.com', 52000, '2024-02-15', 4, NULL),
(107, 'Rohit', 'Yadav', 'rohit@company.com', 48000, '2024-04-10', 5, NULL),
(108, 'Anjali', 'Mehta', 'anjali@company.com', 58000, '2024-06-01', 2, 102);
GO

INSERT INTO Projects
(project_id, project_name, start_date, end_date, budget, department_id)
VALUES
(201, 'Cloud Migration', '2025-01-01', '2025-06-30', 500000, 1),
(202, 'Employee Portal', '2025-02-01', '2025-05-31', 300000, 1),
(203, 'Recruitment System', '2025-03-01', '2025-07-31', 250000, 2),
(204, 'Financial Analysis', '2025-01-15', '2025-04-30', 200000, 3),
(205, 'Marketing Campaign', '2025-04-01', '2025-08-31', 350000, 4);
GO

INSERT INTO EmployeeProjects
(employee_id, project_id, assigned_date)
VALUES
(101, 201, '2025-01-01'),
(103, 201, '2025-01-05'),
(105, 201, '2025-01-10'),
(101, 202, '2025-02-01'),
(103, 202, '2025-02-05'),
(102, 203, '2025-03-01'),
(108, 203, '2025-03-05'),
(104, 204, '2025-01-15'),
(106, 205, '2025-04-01');
GO

SELECT * FROM Departments;
SELECT * FROM Employees;
SELECT * FROM Projects;
SELECT * FROM EmployeeProjects;
GO

SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    e.salary,
    d.department_name,
    d.location
FROM Employees e
JOIN Departments d
ON e.department_id = d.department_id;
GO

SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    p.project_name,
    ep.assigned_date
FROM Employees e
JOIN EmployeeProjects ep
ON e.employee_id = ep.employee_id
JOIN Projects p
ON ep.project_id = p.project_id;
GO

SELECT
    p.project_id,
    p.project_name,
    p.start_date,
    p.end_date,
    p.budget,
    d.department_name
FROM Projects p
JOIN Departments d
ON p.department_id = d.department_id;
GO

SELECT *
FROM Employees
WHERE salary > 60000;
GO

SELECT
    d.department_name,
    AVG(e.salary) AS average_salary
FROM Departments d
JOIN Employees e
ON d.department_id = e.department_id
GROUP BY d.department_name;
GO

SELECT TOP 1
    employee_id,
    first_name,
    last_name,
    salary
FROM Employees
ORDER BY salary DESC;
GO

SELECT
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM Departments d
LEFT JOIN Employees e
ON d.department_id = e.department_id
GROUP BY d.department_name;
GO

SELECT
    d.department_name,
    COUNT(p.project_id) AS project_count
FROM Departments d
LEFT JOIN Projects p
ON d.department_id = p.department_id
GROUP BY d.department_name;
GO

SELECT
    e.employee_id,
    e.first_name + ' ' + e.last_name AS employee_name,
    m.first_name + ' ' + m.last_name AS manager_name
FROM Employees e
LEFT JOIN Employees m
ON e.manager_id = m.employee_id;
GO

SELECT
    d.department_name,
    SUM(p.budget) AS total_budget
FROM Departments d
JOIN Projects p
ON d.department_id = p.department_id
GROUP BY d.department_name;
GO
```
