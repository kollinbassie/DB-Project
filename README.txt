HOW TO RUN THE DATABASE:
------------------------
1. Download all the Github files.
  
2. In the terminal, go to the directory where the files are and enter command: python setup_database.py
   to setup the database.

**You should see the following message**:  

Connected to SQLite database: business.db

Executed create_tables.sql successfully.
Executed insert_sample_data.sql successfully.

Database setup completed successfully.


3. Then, enter command: python cli_application.py
   to run the CLI application.

**You should see the following user interface**:

=== Business Database CLI Application ===
Please select an option:
1. Add a New Employee
2. Update Product Quantity
3. Delete a Supplier
4. View Sales Report
5. Add a New Order
6. View Employees
7. View Products
8. View Departments
9. View Suppliers
10. View Orders
11. Delete an Order
12. Exit
Enter your choice (1-12):


4. Select an option by entering its corresponding number.


TEST QUERIES:
-------------
Enter the following command in the terminal to test the queries below: sqlite3 business.db < test_queries.sql

1. Display Total Sales per Product

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



2. Display All Employees with Their Details

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



3. Update the Quantity in Stock for a Given Product

UPDATE 
    Inventory
SET 
    quantity_in_stock = 50
WHERE 
    product_id = 201;



4. Add a New Order to the Orders Table

INSERT INTO 
    Orders (order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by)
VALUES 
    ('2024-05-01', 401, 202, 10, 'Smartphone', 101);



5. Add a New Employee to the Employee Table

INSERT INTO 
    Employee (employee_name, employee_position, employee_salary, employee_dept)
VALUES 
    ('John Doe', 'Marketing Manager', 70000, 1);







