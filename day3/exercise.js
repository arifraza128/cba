let arr = [];

let n = Number(prompt("How many numbers do you want to enter?"));

for (let i = 0; i < n; i++) {
    let num = Number(prompt("Enter a number:"));
    arr.push(num);
}

console.log(arr);