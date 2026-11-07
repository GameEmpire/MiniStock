import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Database file location
DB_PATH = Path(__file__).resolve().parent / "ministock.db"


# -------------------------------
# DATABASE CONNECTION
# -------------------------------

@contextmanager
def get_connection():

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        with connection:
            yield connection
    finally:
        connection.close()


# -------------------------------
# INITIALIZE DATABASE
# -------------------------------

def initialize_database():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0),
                min_stock INTEGER NOT NULL DEFAULT 5
                    CHECK(min_stock >= 0)
            )
        """)


# -------------------------------
# ADD PRODUCT
# -------------------------------

def add_product(name, category, price, quantity, min_stock=5):

    name = name.strip()
    category = category.strip()

    if not name or not category:
        raise ValueError("Product name and category are required.")

    if price < 0 or quantity < 0 or min_stock < 0:
        raise ValueError("Values cannot be negative.")

    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO products
            (name, category, price, quantity, min_stock)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, price, quantity, min_stock))

        return cursor.lastrowid


# -------------------------------
# GET ALL PRODUCTS
# -------------------------------

def get_products(search=""):

    with get_connection() as connection:

        return connection.execute("""
            SELECT * FROM products
            WHERE name LIKE ? OR category LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%")).fetchall()


# -------------------------------
# UPDATE PRODUCT
# -------------------------------

def update_product(product_id, name, category, price, quantity, min_stock=5):

    name = name.strip()
    category = category.strip()

    if not name or not category:
        raise ValueError("Product name and category are required.")

    if price < 0 or quantity < 0 or min_stock < 0:
        raise ValueError("Values cannot be negative.")

    with get_connection() as connection:

        cursor = connection.execute("""
            UPDATE products
            SET name = ?, category = ?, price = ?,
                quantity = ?, min_stock = ?
            WHERE id = ?
        """, (
            name, category, price, quantity, min_stock, product_id
        ))

        return cursor.rowcount > 0


# -------------------------------
# DELETE PRODUCT
# -------------------------------

def delete_product(product_id):

    with get_connection() as connection:

        cursor = connection.execute("""
            DELETE FROM products WHERE id = ?
        """, (product_id,))

        return cursor.rowcount > 0


# -------------------------------
# DASHBOARD STATISTICS
# -------------------------------

def get_statistics():

    with get_connection() as connection:

        return connection.execute("""
            SELECT
                COUNT(*) AS total_products,
                COALESCE(SUM(quantity), 0) AS total_units,
                COALESCE(SUM(
                    CASE WHEN quantity > 0
                    AND quantity <= min_stock
                    THEN 1 ELSE 0 END
                ), 0) AS low_stock,
                COALESCE(SUM(
                    CASE WHEN quantity = 0
                    THEN 1 ELSE 0 END
                ), 0) AS out_of_stock,
                COALESCE(SUM(price * quantity), 0) AS stock_value
            FROM products
        """).fetchone()


# -------------------------------
# LOW STOCK PRODUCTS
# -------------------------------

def get_low_stock_products():

    with get_connection() as connection:

        return connection.execute("""
            SELECT * FROM products
            WHERE quantity <= min_stock
            ORDER BY quantity ASC
        """).fetchall()


# -------------------------------
# INITIALIZE ON IMPORT
# -------------------------------

initialize_database()