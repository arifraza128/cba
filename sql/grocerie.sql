CREATE TABLE Groceries (
    GroceryID INT PRIMARY KEY IDENTITY(1,1),
    GroceryName VARCHAR(100) NOT NULL,
    Category VARCHAR(50),
    Brand VARCHAR(50),
    Quantity INT,
    Unit VARCHAR(20),
    Price DECIMAL(10,2),
    ExpiryDate DATE,
    SupplierName VARCHAR(100)
);

INSERT INTO Groceries
(GroceryName, Category, Brand, Quantity, Unit, Price, ExpiryDate, SupplierName)
VALUES
('Rice', 'Grains', 'India Gate', 10, 'Kg', 750.00, '2027-06-15', 'ABC Suppliers'),
('Wheat Flour', 'Flour', 'Aashirvaad', 5, 'Kg', 300.00, '2027-04-20', 'Fresh Foods'),
('Sugar', 'Sweetener', 'Madhur', 5, 'Kg', 250.00, '2028-01-10', 'ABC Suppliers'),
('Milk', 'Dairy', 'Amul', 2, 'Litre', 120.00, '2026-10-08', 'Amul Distributors'),
('Cooking Oil', 'Oil', 'Fortune', 5, 'Litre', 800.00, '2027-08-25', 'Fresh Foods'),
('Toor Dal', 'Pulses', 'Tata Sampann', 2, 'Kg', 300.00, '2027-09-15', 'XYZ Traders'),
('Salt', 'Spices', 'Tata', 2, 'Kg', 50.00, '2028-03-20', 'XYZ Traders'),
('Tea', 'Beverages', 'Tata Tea', 1, 'Kg', 450.00, '2027-12-10', 'ABC Suppliers'),
('Biscuits', 'Snacks', 'Parle', 10, 'Pack', 100.00, '2027-02-15', 'Fresh Foods'),
('Apples', 'Fruits', 'Fresh Farm', 3, 'Kg', 360.00, '2026-10-12', 'Local Supplier');

SELECT * FROM Groceries;
