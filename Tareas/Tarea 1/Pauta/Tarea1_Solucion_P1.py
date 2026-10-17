import pandas as pd
import sqlite3
import numpy as np

def setup_database(db_path):
    """
    Lee el CSV, limpia los datos y crea las tablas en SQLite
    """
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    order_items = pd.read_csv("data/olist_order_items_dataset.csv")
    order_payments = pd.read_csv("data/olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    products = pd.read_csv("data/olist_products_dataset.csv")
    sellers = pd.read_csv("data/olist_sellers_dataset.csv")
    translation = pd.read_csv("data/product_category_name_translation.csv")
    
    date_cols = [
        'order_purchase_timestamp', 'order_approved_at', 
        'order_delivered_carrier_date', 'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]

    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    order_reviews['review_comment_title'] = order_reviews['review_comment_title'].fillna('Sin titulo')
    order_reviews['review_comment_message'] = order_reviews['review_comment_message'].fillna('Sin mensaje')

    order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    products['product_category_name'] = products['product_category_name'].fillna('desconocido')
    products['product_name_length'] = products['product_name_length'].fillna(0).astype(int)
    products['product_description_length'] = products['product_description_length'].fillna(0).astype(int)
    products['product_photos_qty'] = products['product_photos_qty'].fillna(0).astype(int)

    datasets = [customers, order_items, order_payments, order_reviews, orders, products, sellers, translation]
    for df in datasets:
        df.replace({np.nan: None}, inplace=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS order_payments;
        DROP TABLE IF EXISTS order_reviews;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS category_translation;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS sellers;

        CREATE TABLE customers (
            customer_id TEXT,
            customer_unique_id TEXT,
            customer_zip_code_prefix INTEGER,
            customer_city TEXT,
            customer_state TEXT
        );

        CREATE TABLE sellers (
            seller_id TEXT,
            seller_zip_code_prefix INTEGER,
            seller_city TEXT,
            seller_state TEXT
        );

        CREATE TABLE category_translation (
            product_category_name TEXT,
            product_category_name_english TEXT
        );

        CREATE TABLE products (
            product_id TEXT,
            product_category_name TEXT,
            product_name_length INTEGER,
            product_description_length INTEGER,
            product_photos_qty INTEGER,
            product_weight_g REAL,
            product_length_cm REAL,
            product_height_cm REAL,
            product_width_cm REAL
        );

        CREATE TABLE orders (
            order_id TEXT,
            customer_id TEXT,
            order_status TEXT,
            order_purchase_timestamp TEXT,
            order_approved_at TEXT,
            order_delivered_carrier_date TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT
        );

        CREATE TABLE order_items (
            order_id TEXT,
            order_item_id INTEGER,
            product_id TEXT,
            seller_id TEXT,
            shipping_limit_date TEXT,
            price REAL,
            freight_value REAL
        );

        CREATE TABLE order_payments (
            order_id TEXT,
            payment_sequential INTEGER,
            payment_type TEXT,
            payment_installments INTEGER,
            payment_value REAL
        );

        CREATE TABLE order_reviews (
            review_id TEXT,
            order_id TEXT,
            review_score INTEGER,
            review_comment_title TEXT,
            review_comment_message TEXT,
            review_creation_date TEXT,
            review_answer_timestamp TEXT
        );
    """)

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)", 
        customers.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO sellers VALUES (?, ?, ?, ?)", 
        sellers.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO category_translation VALUES (?, ?)", 
        translation.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        products.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        orders.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?, ?)", 
        order_items.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO order_payments VALUES (?, ?, ?, ?, ?)", 
        order_payments.values.tolist()
    )

    cursor.executemany(
        "INSERT INTO order_reviews VALUES (?, ?, ?, ?, ?, ?, ?)", 
        order_reviews.values.tolist()
    )

    conn.commit()
    conn.close()