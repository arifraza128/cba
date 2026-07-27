function getEvenNumbers(arr) {
    let even = [];

    for (let num of arr) {
        if (num % 2 === 0) {
            even.push(num);
        }
    }

    return even;
}

console.log(getEvenNumbers([3, 8, 11, 14, 20]));