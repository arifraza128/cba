const ecommerceOrders = [
    {
        id: 1,
        customer: "John",
        products: [
            { name: "Laptop", price: 50000 },
            { name: "Mouse", price: 500 }
        ]
    },
    {
        id: 2,
        customer: "Emma",
        products: [
            { name: "Phone", price: 30000 },
            { name: "Headphones", price: 2000 }
        ]
    }
];
let maxAmount = 0;
let richCustomer = "";
let productList = [];
let totalProducts = 0;
ecommerceOrders.forEach(order => {
    let amount = 0;
    order.products.forEach(product => {
        amount += product.price;
        productList.push(product.name);
        totalProducts++;
        if (product.price > 10000) {
            console.log(product);
        }
    });
    console.log(order.customer, "Spent:", amount);
    if (amount > maxAmount) {
        maxAmount = amount;
        richCustomer = order.customer;
    }
});
console.log("Highest Spent:", richCustomer);
console.log("Products:", productList);
console.log("Total Products:", totalProducts);