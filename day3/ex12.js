const numbers = [12, 5, 8, 19, 22, 7, 30];

let largest = numbers[0];
let sum = 0;
let greaterThanTen = [];

console.log("Even Numbers:");

for (let num of numbers) {

    if (num % 2 === 0) {
        console.log(num);
    }

    if (num > largest) {
        largest = num;
    }

    sum += num;

    if (num > 10) {
        greaterThanTen.push(num);
    }

    if (num === 22) {
        break;
    }
}

console.log("Largest:", largest);
console.log("Sum:", sum);
console.log("Greater than 10:", greaterThanTen);