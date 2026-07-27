const employees = [
    { name: "Amit", salary: 30000 },
    { name: "Neha", salary: 45000 },
    { name: "Raj", salary: 28000 },
    { name: "Priya", salary: 50000 }
];

console.log("Employee Names:");

for (let emp of employees) {
    console.log(emp.name);
}

let updatedSalary = employees.map(emp => emp.salary + emp.salary * 0.10);

function getHighestSalary(arr) {
    let highest = arr[0].salary;

    for (let emp of arr) {
        if (emp.salary > highest) {
            highest = emp.salary;
        }
    }

    return highest;
}

console.log("Updated Salaries:", updatedSalary);
console.log("Highest Salary:", getHighestSalary(employees));