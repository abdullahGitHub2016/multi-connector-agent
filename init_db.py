import sqlite3
import random
import os
from datetime import datetime, timedelta

def create_connected_db():
    db_dir = "data"
    if not os.path.exists(db_dir): os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, 'company_records.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. Enable Foreign Key support in SQLite
    c.execute("PRAGMA foreign_keys = ON")

    # 2. Create Tables with Relationships
    c.execute("DROP TABLE IF EXISTS sales")
    c.execute("DROP TABLE IF EXISTS employees")
    
    c.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL
        )
    ''')

    c.execute('''
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            item_name TEXT,
            amount REAL,
            sale_date TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    ''')

    # 3. Insert 100 Employees
    depts = ['Software', 'Marketing', 'Sales', 'HR', 'Support']
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Edward', 'Fiona', 'George', 'Hannah']
    
    employee_ids = []
    for i in range(1, 101):
        emp_name = f"{random.choice(names)} {random.randint(100, 999)}"
        dept = random.choice(depts)
        sal = random.randint(50000, 120000)
        c.execute("INSERT INTO employees VALUES (?, ?, ?, ?)", (i, emp_name, dept, sal))
        employee_ids.append(i)

    # 4. Insert 1,000 Sales (Linked to Employees)
    items = ['Cloud Sub', 'Laptop', 'Consulting', 'License', 'Support Plan']
    for i in range(1000):
        emp_id = random.choice(employee_ids) # Link to a real employee
        item = random.choice(items)
        amt = round(random.uniform(100, 5000), 2)
        date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        c.execute("INSERT INTO sales (employee_id, item_name, amount, sale_date) VALUES (?, ?, ?, ?)", 
                  (emp_id, item, amt, date))

    conn.commit()
    conn.close()
    print(f"✅ Large Connected Database created at: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    create_connected_db()