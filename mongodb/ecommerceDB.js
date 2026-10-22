use ecommerceDB

db.customers.insertMany([
  {
    customerId: 101,
    name: "Rahul Sharma",
    city: "Hyderabad",
    age: 29,
    gender: "Male",
    email: "rahul@gmail.com",
    membership: "Gold",
    skills: ["Java", "MongoDB", "Spring Boot"],
    orders: [
      {
        orderId: "O1001",
        product: "Laptop",
        category: "Electronics",
        amount: 75000,
        status: "Delivered"
      },
      {
        orderId: "O1002",
        product: "Mouse",
        category: "Electronics",
        amount: 1500,
        status: "Delivered"
      }
    ]
  },
  {
    customerId: 102,
    name: "Priya Reddy",
    city: "Bangalore",
    age: 34,
    gender: "Female",
    email: "priya@gmail.com",
    membership: "Silver",
    skills: ["Python", "SQL", "Power BI"],
    orders: [
      {
        orderId: "O1003",
        product: "Mobile",
        category: "Electronics",
        amount: 45000,
        status: "Delivered"
      },
      {
        orderId: "O1004",
        product: "Headphones",
        category: "Electronics",
        amount: 5000,
        status: "Cancelled"
      }
    ]
  }

  // Add remaining customers here
])
