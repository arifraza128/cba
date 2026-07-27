let marks = [78, 45, 89, 32, 91, 67, 55];
let passed = 0;
let failed = 0;
let highest = marks[0];
let total = 0;
for (let i = 0; i < marks.length; i++) {
    total += marks[i];

    if (marks[i] >= 50) {
        passed++;
    } else {
        failed++;
    }

    if (marks[i] > highest) {
        highest = marks[i];
    }
}
let average = total / marks.length;
console.log("Passed:", passed);
console.log("Failed:", failed);
console.log("Highest Mark:", highest);
console.log("Average Marks:", average);