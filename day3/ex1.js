const guesses = [2, 5, 9, 12, 18];
const secret = 12;

for (let guess of guesses) {
    if (guess === secret) {
        console.log("Correct!");
        break;
    } else {
        console.log("Wrong guess");
    }
}