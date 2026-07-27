const numbers = [10, 25, 18, -4, 30, 50];

for (let num of numbers) {
    if (num < 0) {
        break;
    }

    console.log(num);
}