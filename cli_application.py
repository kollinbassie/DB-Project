# cli_application.py

import sqlite3
from datetime import datetime

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = 1")
        print(f"Connected to SQLite database: {db_file}\n")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def add_employee(conn):
    """
    Adds a new employee to the Employee table.
    """
    print("\n=== Add a New Employee ===")
    employee_name = input("Enter employee name: ").strip()
    employee_position = input("Enter employee position: ").strip()
    
    while True:
        try:
            employee_salary = float(input("Enter employee salary: ").strip())
            break
        except ValueError:
            print("Invalid input for salary. Please enter a numeric value.")
    
    print("\nAvailable Departments:")
    departments = get_departments(conn)
    if not departments:
        print("No departments found. Please add a department first.\n")
        return
    for dept in departments:
        print(f"{dept[0]}. {dept[1]}")
    
    while True:
        try:
            employee_dept = int(input("Enter department ID from the list above: ").strip())
            if any(dept[0] == employee_dept for dept in departments):
                break
            else:
                print("Invalid department ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for department ID. Please enter a numeric value.")
    
    sql = '''INSERT INTO Employee(employee_name, employee_position, employee_salary, employee_dept)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (employee_name, employee_position, employee_salary, employee_dept))
        conn.commit()
        print(f"Employee '{employee_name}' added successfully with ID {cur.lastrowid}.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while adding employee: {e}\n")

def update_product_quantity(conn):
    """
    Updates the quantity_in_stock for a given product.
    """
    print("\n=== Update Product Quantity ===")
    print("\nAvailable Products:")
    products = get_products(conn)
    if not products:
        print("No products found. Please add a product first.\n")
        return
    for product in products:
        print(f"{product[0]}. {product[1]} (Current Stock: {product[5]})")
    
    while True:
        try:
            product_id = int(input("Enter product ID to update: ").strip())
            if any(prod[0] == product_id for prod in products):
                break
            else:
                print("Invalid product ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for product ID. Please enter a numeric value.")
    
    while True:
        try:
            new_quantity = int(input("Enter new quantity: ").strip())
            if new_quantity < 0:
                print("Quantity cannot be negative. Please enter a valid number.")
            else:
                break
        except ValueError:
            print("Invalid input for quantity. Please enter a numeric value.")
    
    sql = '''UPDATE Inventory
             SET quantity_in_stock = ?
             WHERE product_id = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (new_quantity, product_id))
        if cur.rowcount == 0:
            print("Product ID not found in Inventory.\n")
        else:
            conn.commit()
            print(f"Product ID {product_id} quantity updated to {new_quantity}.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while updating product quantity: {e}\n")

def delete_supplier(conn):
    """
    Deletes a supplier from the Supplier table after ensuring no dependent orders exist.
    Offers the option to delete dependent orders.
    """
    print("\n=== Delete a Supplier ===")
    print("\nAvailable Suppliers:")
    suppliers = get_suppliers(conn)
    if not suppliers:
        print("No suppliers found.\n")
        return
    for supplier in suppliers:
        print(f"{supplier[0]}. {supplier[1]}")
    
    while True:
        try:
            supplier_id = int(input("Enter supplier ID to delete: ").strip())
            if any(sup[0] == supplier_id for sup in suppliers):
                break
            else:
                print("Invalid supplier ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for supplier ID. Please enter a numeric value.")
    
    # Check for dependent orders
    dependent_orders = get_orders_by_supplier(conn, supplier_id)
    if dependent_orders:
        print(f"\nSupplier ID {supplier_id} has {len(dependent_orders)} order(s) associated with it.")
        print("1. Cancel Deletion")
        print("2. Delete Supplier and All Associated Orders")
        
        while True:
            choice = input("Enter your choice (1-2): ").strip()
            if choice == '1':
                print("Deletion canceled.\n")
                return
            elif choice == '2':
                # Delete dependent orders first
                delete_orders_by_supplier(conn, supplier_id)
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    confirmation = input(f"Are you sure you want to delete supplier ID {supplier_id}? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Deletion canceled.\n")
        return
    
    sql = '''DELETE FROM Supplier WHERE supplier_id = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (supplier_id,))
        if cur.rowcount == 0:
            print("Supplier ID not found.\n")
        else:
            conn.commit()
            print(f"Supplier ID {supplier_id} deleted successfully.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting supplier: {e}\n")

def delete_order(conn):
    """
    Deletes an order from the Orders table.
    """
    print("\n=== Delete an Order ===")
    print("\nAvailable Orders:")
    orders = get_all_orders(conn)
    if not orders:
        print("No orders found.\n")
        return
    for order in orders:
        print(f"{order[0]}. Order Date: {order[1]}, Supplier: {order[2]}, Product: {order[3]}, Quantity: {order[4]}, Supplied By: {order[6]}")
    
    while True:
        try:
            order_id = int(input("Enter order ID to delete: ").strip())
            if any(ordr[0] == order_id for ordr in orders):
                break
            else:
                print("Invalid order ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for order ID. Please enter a numeric value.")
    
    confirmation = input(f"Are you sure you want to delete order ID {order_id}? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Deletion canceled.\n")
        return
    
    sql = '''DELETE FROM Orders WHERE order_id = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (order_id,))
        if cur.rowcount == 0:
            print("Order ID not found.\n")
        else:
            conn.commit()
            print(f"Order ID {order_id} deleted successfully.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting order: {e}\n")

def view_sales_report(conn):
    """
    Displays total sales per product.
    """
    print("\n=== Sales Report ===")
    sql = '''
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
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No sales data available.\n")
            return
        
        print("\nSales Report:")
        print("{:<10} {:<25} {:<20}".format("Product ID", "Product Name", "Total Quantity Sold"))
        print("-" * 60)
        for row in rows:
            print("{:<10} {:<25} {:<20}".format(row[0], row[1], row[2]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving sales report: {e}\n")

def add_order(conn):
    """
    Adds a new order to the Orders table.
    """
    print("\n=== Add a New Order ===")
    
    print("\nAvailable Suppliers:")
    suppliers = get_suppliers(conn)
    if not suppliers:
        print("No suppliers found. Please add a supplier first.\n")
        return
    for supplier in suppliers:
        print(f"{supplier[0]}. {supplier[1]}")
    
    while True:
        try:
            supplier_id = int(input("Enter supplier ID from the list above: ").strip())
            if any(sup[0] == supplier_id for sup in suppliers):
                break
            else:
                print("Invalid supplier ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for supplier ID. Please enter a numeric value.")
    
    print("\nAvailable Products:")
    products = get_products(conn)
    if not products:
        print("No products found. Please add a product first.\n")
        return
    for product in products:
        print(f"{product[0]}. {product[1]}")
    
    while True:
        try:
            product_id = int(input("Enter product ID from the list above: ").strip())
            if any(prod[0] == product_id for prod in products):
                break
            else:
                print("Invalid product ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for product ID. Please enter a numeric value.")
    
    while True:
        try:
            order_quantity = int(input("Enter order quantity: ").strip())
            if order_quantity <= 0:
                print("Order quantity must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid input for order quantity. Please enter a numeric value.")
    
    product_ordered = input("Enter product ordered: ").strip()
    
    print("\nAvailable Employees:")
    employees = get_employees(conn)
    if not employees:
        print("No employees found. Please add an employee first.\n")
        return
    for emp in employees:
        print(f"{emp[0]}. {emp[1]}")
    
    while True:
        try:
            supplied_by = int(input("Enter employee ID who supplied the order: ").strip())
            if any(emp[0] == supplied_by for emp in employees):
                break
            else:
                print("Invalid employee ID. Please choose a valid ID from the list.")
        except ValueError:
            print("Invalid input for employee ID. Please enter a numeric value.")
    
    order_date = datetime.now().strftime("%Y-%m-%d")
    
    sql = '''INSERT INTO Orders(order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by)
             VALUES(?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by))
        conn.commit()
        print(f"Order added successfully with Order ID {cur.lastrowid}.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while adding order: {e}\n")

def view_employees(conn):
    """
    Displays all employees with their details.
    """
    print("\n=== View Employees ===")
    sql = '''
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
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No employees found.\n")
            return
        
        print("\nEmployees:")
        print("{:<12} {:<25} {:<20} {:<15} {:<15}".format("Employee ID", "Name", "Position", "Salary", "Department"))
        print("-" * 90)
        for row in rows:
            print("{:<12} {:<25} {:<20} {:<15} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving employees: {e}\n")

def view_products(conn):
    """
    Displays all products with their details and inventory quantities.
    """
    print("\n=== View Products ===")
    sql = '''
    SELECT 
        p.product_id,
        p.product_name,
        p.product_price,
        p.product_quantity,
        d.dept_name,
        i.quantity_in_stock
    FROM 
        Product p
    LEFT JOIN 
        Department d ON p.product_dept = d.dept_id
    LEFT JOIN 
        Inventory i ON p.product_id = i.product_id
    ORDER BY 
        p.product_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No products found.\n")
            return
        
        print("\nProducts:")
        print("{:<10} {:<25} {:<15} {:<18} {:<15} {:<20}".format(
            "Product ID", "Product Name", "Price", "Total Quantity", "Department", "Quantity in Stock"))
        print("-" * 100)
        for row in rows:
            qty_in_stock = row[5] if row[5] is not None else "N/A"
            print("{:<10} {:<25} {:<15} {:<18} {:<15} {:<20}".format(
                row[0], row[1], row[2], row[3], row[4], qty_in_stock))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving products: {e}\n")

def view_departments(conn):
    """
    Displays all departments.
    """
    print("\n=== View Departments ===")
    sql = '''
    SELECT 
        dept_id,
        dept_name
    FROM 
        Department
    ORDER BY 
        dept_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No departments found.\n")
            return
        
        print("\nDepartments:")
        print("{:<10} {:<25}".format("Dept ID", "Department Name"))
        print("-" * 35)
        for row in rows:
            print("{:<10} {:<25}".format(row[0], row[1]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving departments: {e}\n")

def view_suppliers(conn):
    """
    Displays all suppliers with their details.
    """
    print("\n=== View Suppliers ===")
    sql = '''
    SELECT 
        supplier_id,
        supplier_name,
        contact_number,
        supplier_address
    FROM 
        Supplier
    ORDER BY 
        supplier_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No suppliers found.\n")
            return
        
        print("\nSuppliers:")
        print("{:<12} {:<25} {:<15} {:<30}".format("Supplier ID", "Supplier Name", "Contact Number", "Address"))
        print("-" * 85)
        for row in rows:
            contact = row[2] if row[2] is not None else "N/A"
            address = row[3] if row[3] is not None else "N/A"
            print("{:<12} {:<25} {:<15} {:<30}".format(row[0], row[1], contact, address))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving suppliers: {e}\n")

def view_orders(conn):
    """
    Displays all orders with their details.
    """
    print("\n=== View Orders ===")
    sql = '''
    SELECT 
        o.order_id,
        o.order_date,
        s.supplier_name,
        p.product_name,
        o.order_quantity,
        o.product_ordered,
        e.employee_name
    FROM 
        Orders o
    LEFT JOIN 
        Supplier s ON o.supplier_id = s.supplier_id
    LEFT JOIN 
        Product p ON o.product_id = p.product_id
    LEFT JOIN 
        Employee e ON o.supplied_by = e.employee_id
    ORDER BY 
        o.order_date DESC;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        if not rows:
            print("No orders found.\n")
            return
        
        print("\nOrders:")
        print("{:<10} {:<12} {:<25} {:<25} {:<15} {:<20} {:<25}".format(
            "Order ID", "Order Date", "Supplier Name", "Product Name",
            "Quantity", "Product Ordered", "Supplied By"))
        print("-" * 130)
        for row in rows:
            supplier = row[2] if row[2] is not None else "N/A"
            product = row[3] if row[3] is not None else "N/A"
            supplied_by = row[6] if row[6] is not None else "N/A"
            print("{:<10} {:<12} {:<25} {:<25} {:<15} {:<20} {:<25}".format(
                row[0], row[1], supplier, product, row[4], row[5], supplied_by))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving orders: {e}\n")

def get_departments(conn):
    """
    Retrieves all departments.
    """
    sql = '''
    SELECT 
        dept_id,
        dept_name
    FROM 
        Department
    ORDER BY 
        dept_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving departments: {e}\n")
        return []

def get_products(conn):
    """
    Retrieves all products along with inventory quantities.
    """
    sql = '''
    SELECT 
        p.product_id,
        p.product_name,
        p.product_price,
        p.product_quantity,
        d.dept_name,
        i.quantity_in_stock
    FROM 
        Product p
    LEFT JOIN 
        Department d ON p.product_dept = d.dept_id
    LEFT JOIN 
        Inventory i ON p.product_id = i.product_id
    ORDER BY 
        p.product_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving products: {e}\n")
        return []

def get_suppliers(conn):
    """
    Retrieves all suppliers.
    """
    sql = '''
    SELECT 
        supplier_id,
        supplier_name,
        contact_number,
        supplier_address
    FROM 
        Supplier
    ORDER BY 
        supplier_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving suppliers: {e}\n")
        return []

def get_employees(conn):
    """
    Retrieves all employees.
    """
    sql = '''
    SELECT 
        employee_id,
        employee_name
    FROM 
        Employee
    ORDER BY 
        employee_id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving employees: {e}\n")
        return []

def get_orders_by_supplier(conn, supplier_id):
    """
    Retrieves all orders associated with a given supplier ID.
    """
    sql = '''
    SELECT 
        order_id,
        order_date,
        product_ordered,
        order_quantity
    FROM 
        Orders
    WHERE 
        supplier_id = ?
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (supplier_id,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving orders: {e}\n")
        return []

def delete_orders_by_supplier(conn, supplier_id):
    """
    Deletes all orders associated with a given supplier ID.
    """
    sql = '''DELETE FROM Orders WHERE supplier_id = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (supplier_id,))
        deleted_count = cur.rowcount
        conn.commit()
        print(f"{deleted_count} order(s) associated with supplier ID {supplier_id} deleted successfully.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting orders: {e}\n")

def get_all_orders(conn):
    """
    Retrieves all orders with detailed information.
    """
    sql = '''
    SELECT 
        o.order_id,
        o.order_date,
        s.supplier_name,
        p.product_name,
        o.order_quantity,
        o.product_ordered,
        e.employee_name
    FROM 
        Orders o
    LEFT JOIN 
        Supplier s ON o.supplier_id = s.supplier_id
    LEFT JOIN 
        Product p ON o.product_id = p.product_id
    LEFT JOIN 
        Employee e ON o.supplied_by = e.employee_id
    ORDER BY 
        o.order_date DESC;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving orders: {e}\n")
        return []

def main_menu():
    """
    Displays the main menu.
    """
    print("=== Business Database CLI Application ===")
    print("Please select an option:")
    print("1. Add a New Employee")
    print("2. Update Product Quantity")
    print("3. Delete a Supplier")
    print("4. View Sales Report")
    print("5. Add a New Order")
    print("6. View Employees")
    print("7. View Products")
    print("8. View Departments")
    print("9. View Suppliers")
    print("10. View Orders")
    print("11. Delete an Order")
    print("12. Exit")

def main():
    database = "business.db"
    conn = create_connection(database)
    if not conn:
        return

    while True:
        main_menu()
        choice = input("Enter your choice (1-12): ").strip()

        if choice == '1':
            # Add a New Employee
            add_employee(conn)

        elif choice == '2':
            # Update Product Quantity
            update_product_quantity(conn)

        elif choice == '3':
            # Delete a Supplier
            delete_supplier(conn)

        elif choice == '4':
            # View Sales Report
            view_sales_report(conn)

        elif choice == '5':
            # Add a New Order
            add_order(conn)

        elif choice == '6':
            # View Employees
            view_employees(conn)

        elif choice == '7':
            # View Products
            view_products(conn)

        elif choice == '8':
            # View Departments
            view_departments(conn)

        elif choice == '9':
            # View Suppliers
            view_suppliers(conn)

        elif choice == '10':
            # View Orders
            view_orders(conn)

        elif choice == '11':
            # Delete an Order
            delete_order(conn)

        elif choice == '12':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.\n")

    conn.close()

if __name__ == "__main__":
    main()
