from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os


# -------------------------
# Configuration
# -------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = create_engine(DATABASE_URL)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "olist_dataset"


# -------------------------
# Helper function
# -------------------------

def load_csv(filename, table_name, columns=None):
    file_path = DATA_DIR / filename

    print(f"\nLoading {filename}...")

    df = pd.read_csv(file_path)

    if columns:
        df = df[columns]

    print(f"Rows found: {len(df):,}")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"Loaded into table: {table_name}")


# -------------------------
# Load data
# -------------------------

def main():

    # 1. Customers
    load_csv(
        "olist_customers_dataset.csv",
        "customers",
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ]
    )

    # 2. Sellers
    load_csv(
        "olist_sellers_dataset.csv",
        "sellers",
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ]
    )

    # 3. Products
    products = pd.read_csv(
        DATA_DIR / "olist_products_dataset.csv"
    )

    products = products.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        }
    )

    products = products[
        [
            "product_id",
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ]

    print("\nLoading products...")
    print(f"Rows found: {len(products):,}")

    products.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Loaded into table: products")

    # 4. Orders
    orders = pd.read_csv(
        DATA_DIR / "olist_orders_dataset.csv"
    )

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    print("\nLoading orders...")
    print(f"Rows found: {len(orders):,}")

    orders.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Loaded into table: orders")

    # 5. Order items
    order_items = pd.read_csv(
        DATA_DIR / "olist_order_items_dataset.csv"
    )

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce"
    )

    print("\nLoading order_items...")
    print(f"Rows found: {len(order_items):,}")

    order_items.to_sql(
        "order_items",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Loaded into table: order_items")

    # 6. Payments
    payments = pd.read_csv(
        DATA_DIR / "olist_order_payments_dataset.csv"
    )

    print("\nLoading payments...")
    print(f"Rows found: {len(payments):,}")

    payments.to_sql(
        "payments",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Loaded into table: payments")

    # 7. Reviews
    reviews = pd.read_csv(
        DATA_DIR / "olist_order_reviews_dataset.csv"
    )

    review_date_columns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in review_date_columns:
        reviews[column] = pd.to_datetime(
            reviews[column],
            errors="coerce"
        )

    print("\nLoading reviews...")
    print(f"Rows found: {len(reviews):,}")

    reviews.to_sql(
        "reviews",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Loaded into table: reviews")

    print("\n==============================")
    print("ALL DATA LOADED SUCCESSFULLY")
    print("==============================")


if __name__ == "__main__":
    main()