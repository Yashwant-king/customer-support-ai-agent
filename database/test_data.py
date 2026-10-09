import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)


queries = {

    "customers": """
        SELECT COUNT(*) FROM customers;
    """,

    "orders": """
        SELECT COUNT(*) FROM orders;
    """,

    "order_items": """
        SELECT COUNT(*) FROM order_items;
    """,

    "products": """
        SELECT COUNT(*) FROM products;
    """,

    "sellers": """
        SELECT COUNT(*) FROM sellers;
    """,

    "payments": """
        SELECT COUNT(*) FROM payments;
    """,

    "reviews": """
        SELECT COUNT(*) FROM reviews;
    """,

    "orders_with_customer": """
        SELECT COUNT(*)
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id;
    """,

    "items_with_products": """
        SELECT COUNT(*)
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id;
    """,

    "items_with_sellers": """
        SELECT COUNT(*)
        FROM order_items oi
        JOIN sellers s
            ON oi.seller_id = s.seller_id;
    """
}


with engine.connect() as connection:

    print("\n========== DATABASE TEST ==========\n")

    for name, query in queries.items():

        result = connection.execute(text(query))
        count = result.scalar()

        print(f"{name:25} {count:,}")

    print("\n===================================")
    print("DATABASE TEST COMPLETED")
    print("===================================\n")