--Display total sales per product:
    
SELECT 
        p.product_id,
        p.product_name,
        SUM(s.quantity_sold) AS total_quantity_sold
    FROM
        Sales s
    JOIN
        Product p ON s.product_id = p.product_id
    GROUP BY
        p.product_id, p.product_name
    ORDER BY
        total_quantity_sold DESC



--Display all employees with their details:
  
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
        e.employee_id




--Update the quantity in stock for a given product:

UPDATE Inventory
SET quantity_in_stock = 10
WHERE product_id = 201





--Add a new order to the Orders table:

INSERT INTO Orders(order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by)
VALUES(2024-11-25, 401, 203, 25, Office Chair, Alice Johnson)





--Add a new employee to the Employee table:
    
INSERT INTO Employee(employee_name, employee_position, employee_salary, employee_dept)
VALUES(Mary Jane, Cashier, 20000, Sales)






