import sqlite3
from datetime import datetime

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}\n")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def add_employee(conn, employee_name, employee_position, employee_salary, employee_dept):
    """
    Adds a new employee to the Employee table.
    """
    sql = '''INSERT INTO Employee(employee_name, employee_position, employee_salary, employee_dept)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    try:
        cur.execute(sql, (employee_name, employee_position, employee_salary, employee_dept))
        conn.commit()
        print(f"Employee '{employee_name}' added successfully with ID {cur.lastrowid}.\n")
    except sqlite3.Error as e:
        print(f"An error occurred while adding employee: {e}\n")

def update_product_quantity(conn, product_id, new_quantity):
    """
    Updates the quantity_in_stock for a given product.
    """
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

def delete_supplier(conn, supplier_id):
    """
    Deletes a supplier from the Supplier table.
    """
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

def view_sales_report(conn):
    """
    Displays total sales per product.
    """
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
        
        print("\nSales Report:")
        print("{:<10} {:<25} {:<20}".format("Product ID", "Product Name", "Total Quantity Sold"))
        print("-" * 60)
        for row in rows:
            print("{:<10} {:<25} {:<20}".format(row[0], row[1], row[2]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving sales report: {e}\n")

def add_order(conn, supplier_id, product_id, order_quantity, product_ordered, supplied_by):
    """
    Adds a new order to the Orders table.
    """
    sql = '''INSERT INTO Orders(order_date, supplier_id, product_id, order_quantity, product_ordered, supplied_by)
             VALUES(?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    order_date = datetime.now().strftime("%Y-%m-%d")
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
        e.employee_id
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\nEmployees List:")
        print("{:<12} {:<20} {:<25} {:<15} {:<15}".format("Employee ID", "Name", "Position", "Salary", "Department"))
        print("-" * 90)
        for row in rows:
            print("{:<12} {:<20} {:<25} {:<15} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving employees: {e}\n")

def view_product_quantities(conn):
    """
    Displays all products with their current inventory quantities.
    """
    sql = '''
    SELECT 
        p.product_id,
        p.product_name,
        p.product_price,
        p.product_quantity,
        d.dept_name,
        IFNULL(i.quantity_in_stock, 0) AS quantity_in_stock
    FROM 
        Product p
    LEFT JOIN 
        Department d ON p.product_dept = d.dept_id
    LEFT JOIN 
        Inventory i ON p.product_id = i.product_id
    ORDER BY 
        p.product_id
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\nProduct Quantities:")
        print("{:<10} {:<25} {:<15} {:<18} {:<15} {:<20}".format(
            "Product ID", "Product Name", "Price", "Total Quantity", "Department", "Quantity In Stock"))
        print("-" * 100)
        for row in rows:
            print("{:<10} {:<25} {:<15} {:<18} {:<15} {:<20}".format(
                row[0], row[1], f"${row[2]:.2f}", row[3], row[4], row[5]))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving product quantities: {e}\n")

def view_suppliers(conn):
    """
    Displays all suppliers with their details.
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
        supplier_id
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\nSuppliers List:")
        print("{:<12} {:<25} {:<15} {:<30}".format("Supplier ID", "Supplier Name", "Contact Number", "Address"))
        print("-" * 90)
        for row in rows:
            print("{:<12} {:<25} {:<15} {:<30}".format(row[0], row[1], row[2] if row[2] else "N/A", row[3] if row[3] else "N/A"))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving suppliers: {e}\n")

def view_orders(conn):
    """
    Displays all orders with their details.
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
        o.order_date DESC
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\nOrders List:")
        print("{:<10} {:<12} {:<25} {:<20} {:<15} {:<20} {:<20}".format(
            "Order ID", "Order Date", "Supplier Name", "Product Name", "Quantity", "Product Ordered", "Supplied By"))
        print("-" * 120)
        for row in rows:
            print("{:<10} {:<12} {:<25} {:<20} {:<15} {:<20} {:<20}".format(
                row[0], row[1], row[2] if row[2] else "N/A", 
                row[3] if row[3] else "N/A", row[4], 
                row[5] if row[5] else "N/A", row[6] if row[6] else "N/A"))
        print()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving orders: {e}\n")

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
    print("6. View All Employees")
    print("7. View Product Quantities")
    print("8. View Suppliers")
    print("9. View Orders")
    print("10. Exit")

def main():
    database = "business.db"
    conn = create_connection(database)
    if not conn:
        return

    while True:
        main_menu()
        choice = input("Enter your choice (1-10): ").strip()

        if choice == '1':
            # Add a New Employee
            employee_name = input("Enter employee name: ").strip()
            employee_position = input("Enter employee position: ").strip()
            try:
                employee_salary = float(input("Enter employee salary: ").strip())
                employee_dept = int(input("Enter department ID: ").strip())
            except ValueError:
                print("Invalid input for salary or department ID. Please enter numeric values.\n")
                continue
            add_employee(conn, employee_name, employee_position, employee_salary, employee_dept)

        elif choice == '2':
            # Update Product Quantity
            try:
                product_id = int(input("Enter product ID to update: ").strip())
                new_quantity = int(input("Enter new quantity: ").strip())
            except ValueError:
                print("Invalid input for product ID or quantity. Please enter numeric values.\n")
                continue
            update_product_quantity(conn, product_id, new_quantity)

        elif choice == '3':
            # Delete a Supplier
            try:
                supplier_id = int(input("Enter supplier ID to delete: ").strip())
            except ValueError:
                print("Invalid input for supplier ID. Please enter a numeric value.\n")
                continue
            delete_supplier(conn, supplier_id)

        elif choice == '4':
            # View Sales Report
            view_sales_report(conn)

        elif choice == '5':
            # Add a New Order
            try:
                supplier_id = int(input("Enter supplier ID: ").strip())
                product_id = int(input("Enter product ID: ").strip())
                order_quantity = int(input("Enter order quantity: ").strip())
                product_ordered = input("Enter product ordered: ").strip()
                supplied_by = int(input("Enter employee ID who supplied the order: ").strip())
            except ValueError:
                print("Invalid input for IDs or quantity. Please enter numeric values where required.\n")
                continue
            add_order(conn, supplier_id, product_id, order_quantity, product_ordered, supplied_by)

        elif choice == '6':
            # View All Employees
            view_employees(conn)

        elif choice == '7':
            # View Product Quantities
            view_product_quantities(conn)

        elif choice == '8':
            # View Suppliers
            view_suppliers(conn)

        elif choice == '9':
            # View Orders
            view_orders(conn)

        elif choice == '10':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.\n")

    conn.close()

if __name__ == "__main__":
    main()
