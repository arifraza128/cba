const students = [
    {
        name: "Alice",
        marks: [80, 85, 90]
    },
    {
        name: "Bob",
        marks: [60, 70, 75]
    },
    {
        name: "Charlie",
        marks: [95, 92, 98]
    }
];
let topper = "";
let highestAvg = 0;
let above80 = [];
students.forEach(student => {
    let total = 0;
    student.marks.forEach(mark => total += mark);
    let avg = total / student.marks.length;
    console.log(student.name, "Average:", avg);
    if (avg > highestAvg) {
        highestAvg = avg;
        topper = student.name;
    }
    if (avg > 80) {
        above80.push(student.name);
    }
});
console.log("Topper:", topper);
console.log("Above 80:", above80);