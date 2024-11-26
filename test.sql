.headers on
.mode column

-- Query 1: Show all departments
SELECT * FROM Department;
SELECT '' AS "";

-- Query 2: Show all inventory
SELECT * FROM Inventory;
SELECT '' AS "";

-- Query 3: Show all products
SELECT * FROM Product;
SELECT '' AS "";

-- Query 4: Show all suppliers
SELECT * FROM Supplier;
SELECT '' AS "";

-- Query 5: Find the highest-paid employee in each department
SELECT e.employee_name, e.employee_salary, d.dept_name
FROM Employee e
JOIN Department d ON e.employee_dept = d.dept_id
WHERE e.employee_salary = (
    SELECT MAX(employee_salary)
    FROM Employee e2
    WHERE e2.employee_dept = e.employee_dept
);
SELECT '' AS "";

-- Query 6: List all employees who work in a specific department
SELECT e.employee_name, e.employee_salary
FROM Employee e
JOIN Department d ON e.employee_dept = d.dept_id
WHERE d.dept_name = 'Department Name';

-- Query 7: Retrieve the total number of products and their average price
SELECT COUNT(*) AS total_products, AVG(product_price) AS average_price
FROM Product;
SELECT '' AS "";

-- Query 8: List the total number of employees in each department
SELECT d.dept_name, COUNT(e.employee_id) AS total_employees
FROM Department d
LEFT JOIN Employee e ON d.dept_id = e.employee_dept
GROUP BY d.dept_name;
SELECT '' AS "";

-- Query 9: Find products that are out of stock
SELECT product_name
FROM Product
WHERE product_quantity = 0;

