let numbers = [10, -5, 0, 20, -8, 15, 0];
let positive = 0;
let negative = 0;
let zero = 0;
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] > 0) {
        positive++;
    } else if (numbers[i] < 0) {
        negative++;
    } else {
        zero++;
    }
}
console.log("Positive:", positive);
console.log("Negative:", negative);
console.log("Zero:", zero);