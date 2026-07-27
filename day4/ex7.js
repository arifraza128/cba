let numbers = [10, 20, 30, 40, 50];
let doubled = numbers.map(num => num * 2);
console.log(doubled);
numbers.shift();
numbers.unshift(5, 15);
numbers.splice(3, 2, 100, 200);
console.log(numbers);