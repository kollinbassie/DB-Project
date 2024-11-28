-- insert_sample_data.sql

-- Insert Departments
INSERT INTO Department (dept_id, dept_name) VALUES
(1, 'Sales'),
(2, 'Engineering'),
(3, 'HR');

-- Insert Employees
INSERT INTO Employee (employee_id, employee_name, employee_position, employee_salary, employee_dept) VALUES
(101, 'Alice Johnson', 'Sales Manager', 75000, 1),
(102, 'Bob Smith', 'Engineer', 85000, 2),
(103, 'Carol Williams', 'HR Specialist', 60000, 3);

-- Insert Products
INSERT INTO Product (product_id, product_name, product_price, product_quantity, product_dept) VALUES
(201, 'Laptop', 1200.00, 50, 2),
(202, 'Smartphone', 800.00, 150, 1),
(203, 'Office Chair', 150.00, 85, 3);

-- Insert Inventory
INSERT INTO Inventory (inventory_id, product_id, quantity_in_stock) VALUES
(301, 201, 45),
(302, 202, 140),
(303, 203, 80);

-- Insert Suppliers
INSERT INTO Supplier (supplier_id, supplier_name, contact_number, supplier_address) VALUES
(401, 'Tech Supplies Co.', '555-1234', '123 Tech Lane'),
(402, 'Office Essentials Inc.', '555-5678', '456 Office Blvd');

-- Insert Orders
INSERT INTO Orders (order_id, order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by) VALUES
(501, '2024-01-15', 401, 201, 10, 'Laptop', 101),
(502, '2024-02-20', 402, 203, 15, 'Office Chair', 103),
(503, '2024-03-10', 401, 202, 20, 'Smartphone', 102);

-- Insert Sales
INSERT INTO Sales (sale_id, product_id, quantity_sold, products_sold) VALUES
(601, 201, 5, 'Laptop'),
(602, 202, 20, 'Smartphone'),
(603, 203, 3, 'Office Chair');
