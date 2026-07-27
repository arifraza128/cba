const employees = [
    { id: 1, name: "John", salary: 50000, department: "IT" },
    { id: 2, name: "Emma", salary: 70000, department: "HR" },
    { id: 3, name: "David", salary: 60000, department: "IT" },
    { id: 4, name: "Sophia", salary: 80000, department: "Finance" }
];
let itEmployees = employees.filter(emp => emp.department === "IT");
console.log("IT Employees:", itEmployees);
let totalSalary = 0;
employees.forEach(emp => totalSalary += emp.salary);
console.log("Total Salary:", totalSalary);
let highest = employees[0];
for (let emp of employees) {
    if (emp.salary > highest.salary) {
        highest = emp;
    }
}
console.log("Highest Salary:", highest);
let names = employees.map(emp => emp.name);
console.log("Names:", names);