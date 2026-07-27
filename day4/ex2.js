const products = [
    { id: 1, name: "Laptop", stock: 10, price: 50000 },
    { id: 2, name: "Mouse", stock: 50, price: 500 },
    { id: 3, name: "Keyboard", stock: 30, price: 1500 }
];
products.push({ id: 4, name: "Monitor", stock: 15, price: 12000 });
console.log(products);
products.pop();
console.log(products);
products[0].stock += 5;
console.log(products);
let lowStock = products.filter(product => product.stock < 20);
console.log(lowStock);