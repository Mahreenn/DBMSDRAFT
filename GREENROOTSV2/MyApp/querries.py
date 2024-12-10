from django.db import connection

def execute_raw_sql():
    sql_queries = [
        """CREATE TABLE warehouse (
            warehouseid INT PRIMARY KEY,
            address VARCHAR(155) NOT NULL
        );""",
        """CREATE TABLE retailer (
            name VARCHAR(65) PRIMARY KEY,
            acceptedgrade CHAR(1) NOT NULL
        );""",
        """CREATE TABLE supplier (
            name VARCHAR(65) PRIMARY KEY
        );""",
        """CREATE TABLE warehouse_distribution (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            warehouseid INT,
            supname VARCHAR(65),
            FOREIGN KEY (warehouseid) REFERENCES warehouse(warehouseid),
            FOREIGN KEY (supname) REFERENCES supplier(name),
            UNIQUE (warehouseid, supname, date)
        );""",
        # Add the remaining SQL queries here
    ]

    # Execute each query
    with connection.cursor() as cursor:
        for query in sql_queries:
            cursor.execute(query)

