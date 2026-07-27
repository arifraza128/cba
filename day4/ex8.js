const orders = [
    {
        orderId: 101,
        customer: "John",
        items: ["Laptop", "Mouse"]
    },
    {
        orderId: 102,
        customer: "Emma",
        items: ["Phone", "Charger"]
    }
];
orders[0].items.push("Keyboard");
let customer = orders.find(order => order.items.includes("Phone"));
console.log(customer.customer);
let allItems = [];
orders.forEach(order => {
    allItems.push(...order.items);
});
console.log(allItems);
let count = 0;
orders.forEach(order => {
    count += order.items.length;
});
console.log(count);