from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


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
# Load reviews
# -------------------------

reviews = pd.read_csv(
    DATA_DIR / "olist_order_reviews_dataset.csv"
)

# Convert date columns
date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

print(f"Reviews found: {len(reviews):,}")

# Insert into PostgreSQL
try:
    reviews.to_sql(
        "reviews",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print("Reviews loaded successfully!")

except Exception as e:
    print("\n========== ERROR ==========")
    print(type(e).__name__)
    print(e)
    print("===========================\n")
    raise