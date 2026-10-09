
from sqlalchemy import text
from database.connection import engine

def get_random_customer_id():
    query = text("""
        SELECT customer_id
        FROM customers
        ORDER BY RANDOM()
        LIMIT 1
    """)

    with engine.connect() as connection:
        result = connection.execute(query).scalar_one_or_none()

    return result


