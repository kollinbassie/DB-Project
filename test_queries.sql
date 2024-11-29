-- Separator for readability
SELECT '';

-- 1. Display Total Sales per Product
-- This query retrieves each product's total quantity sold.
SELECT 
    p.product_id, 
    p.product_name, 
    SUM(s.quantity_sold) AS total_quantity_sold
FROM 
    Sales s
JOIN 
    Product p ON s.product_id = p.product_id
GROUP BY 
    p.product_id, 
    p.product_name
ORDER BY 
    total_quantity_sold DESC;

-- Separator for readability
SELECT '';
SELECT 'Query 1 Successful!';
SELECT '';

-- 2. Display All Employees with Their Details
-- This query lists all employees along with their positions, salaries, and department names.

SELECT 
    e.employee_id, 
    e.employee_name, 
    e.employee_position, 
    e.employee_salary, 
    d.dept_name
FROM 
    Employee e
JOIN 
    Department d ON e.employee_dept = d.dept_id
ORDER BY 
    e.employee_id;

-- Separator for readability
SELECT '';
SELECT 'Query 2 Successful!';
SELECT '';

-- 3. Update the Quantity in Stock for a Given Product
-- Example: Update product with product_id=201 to have quantity_in_stock=50

UPDATE 
    Inventory
SET 
    quantity_in_stock = 50
WHERE 
    product_id = 201;



-- Separator for readability
SELECT '';
SELECT 'Query 3 Successful! Select "7. View Products" on the CLI Application to see the update.';
SELECT '';

-- 4. Add a New Order to the Orders Table
-- Example: Add a new order with the following details
-- Order Date: '2024-05-01'
-- Supplier ID: 401
-- Product ID: 202
-- Order Quantity: 10
-- Product Ordered: 'Smartphone'
-- Supplied By: 101

INSERT INTO 
    Orders (order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by)
VALUES 
    ('2024-05-01', 401, 202, 10, 'Smartphone', 101);



-- Separator for readability
SELECT '';
SELECT 'Query 4 Successful! Select "10. View Orders" on the CLI Application to see the update.';
SELECT '';

-- 5. Add a New Employee to the Employee Table
-- Example: Add a new employee named 'John Doe' with position 'Marketing Manager', salary 70000, department_id=1

INSERT INTO 
    Employee (employee_name, employee_position, employee_salary, employee_dept)
VALUES 
    ('John Doe', 'Marketing Manager', 70000, 1);

SELECT '';
SELECT 'Query 5 Successful! Select "6. View Employees" on the CLI Application to see the update.';




