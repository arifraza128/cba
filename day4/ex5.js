const cart = [
    { name: "Phone", price: 20000, quantity: 1 },
    { name: "Headphones", price: 2000, quantity: 2 },
    { name: "Charger", price: 1000, quantity: 3 }
];
let total = 0;
cart.forEach(item => {
    total += item.price * item.quantity;
});
console.log("Cart Value:", total);
let index = cart.findIndex(item => item.name === "Charger");
cart.splice(index, 1);
cart.push({
    name: "Power Bank",
    price: 1500,
    quantity: 2
});
let productNames = cart.map(item => item.name);
console.log(cart);
console.log(productNames);