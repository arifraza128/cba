const library = {
    books: [
        { title: "JavaScript", available: true },
        { title: "Python", available: false },
        { title: "Java", available: true }
    ]
};
library.books.forEach(book => {
    if (book.available) {
        console.log(book.title);
    }
});
library.books.push({
    title: "C++",
    available: true
});
library.books[1].available = true;
let titles = library.books.map(book => book.title);
console.log(titles);