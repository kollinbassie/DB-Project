CREATE TABLE IF NOT EXISTS Department (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Employee (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    employee_position TEXT NOT NULL,
    employee_salary REAL NOT NULL,
    employee_dept INTEGER,
    FOREIGN KEY (employee_dept) REFERENCES Department(dept_id)
);

CREATE TABLE IF NOT EXISTS Product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    product_quantity INTEGER NOT NULL,
    product_dept INTEGER,
    FOREIGN KEY (product_dept) REFERENCES Department(dept_id)
);

CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity_in_stock INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE IF NOT EXISTS Supplier (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    contact_number TEXT,
    supplier_address TEXT
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    supplier_id INTEGER,
    product_id INTEGER,
    order_quantity INTEGER NOT NULL,
    product_ordered TEXT NOT NULL,
    supplied_by INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity_sold INTEGER NOT NULL,
    products_sold TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);
