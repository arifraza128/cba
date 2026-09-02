CREATE TABLE employees (
    emp_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salary DECIMAL(10,2) CHECK (salary > 0),
    hire_date DATE DEFAULT GETDATE(),
    dept_id INT,
    manager_id INT,

    CONSTRAINT FK_Employees_Department
        FOREIGN KEY (dept_id)
        REFERENCES departments(dept_id),

    CONSTRAINT FK_Employees_Manager
        FOREIGN KEY (manager_id)
        REFERENCES employees(emp_id)
);
GO
