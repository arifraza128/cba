const company = {
    name: "ABC Ltd",
    address: {
        city: "Mumbai",
        state: "Maharashtra"
    },
    departments: {
        IT: 50,
        HR: 10,
        Finance: 15
    }
};
console.log(company.address.city);
company.departments.Marketing = 20;
company.departments.IT = 60;
console.log(Object.keys(company.departments));