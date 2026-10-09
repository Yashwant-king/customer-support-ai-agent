from sqlalchemy import text

from database.connection import engine


def get_customer_details(customer_id: str):
    query = text("""
        SELECT
            c.customer_id,
            c.customer_unique_id,
            c.customer_city,
            c.customer_state,

            o.order_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,

            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            oi.price,
            oi.freight_value,

            p.product_category_name,

            pay.payment_sequential,
            pay.payment_type,
            pay.payment_installments,
            pay.payment_value,

            r.review_score,
            r.review_comment_message

        FROM customers c

        LEFT JOIN orders o
            ON c.customer_id = o.customer_id

        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id

        LEFT JOIN products p
            ON oi.product_id = p.product_id

        LEFT JOIN payments pay
            ON o.order_id = pay.order_id

        LEFT JOIN reviews r
            ON o.order_id = r.order_id

        WHERE c.customer_id = :customer_id

        ORDER BY
            o.order_purchase_timestamp DESC,
            oi.order_item_id,
            pay.payment_sequential
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {"customer_id": customer_id},
        ).mappings().all()

    if not rows:
        return None

    first = rows[0]

    customer = {
        "customer_id": first["customer_id"],
        "customer_unique_id": first["customer_unique_id"],
        "city": first["customer_city"],
        "state": first["customer_state"],
        "orders": [],
    }

    orders = {}

    for row in rows:

        order_id = row["order_id"]

        if order_id is None:
            continue

        if order_id not in orders:
            orders[order_id] = {
                "order_id": order_id,
                "status": row["order_status"],
                "purchase_date": row["order_purchase_timestamp"],
                "delivered_date": row["order_delivered_customer_date"],
                "estimated_delivery": row[
                    "order_estimated_delivery_date"
                ],
                "items": [],
                "payments": [],
                "review": None,
            }

        order = orders[order_id]

        # Add item
        item_id = row["order_item_id"]

        if item_id is not None:
            existing_item_ids = {
                item["order_item_id"]
                for item in order["items"]
            }

            if item_id not in existing_item_ids:
                order["items"].append({
                    "order_item_id": item_id,
                    "product_id": row["product_id"],
                    "seller_id": row["seller_id"],
                    "category": row["product_category_name"],
                    "price": row["price"],
                    "freight_value": row["freight_value"],
                })

        # Add payment
        payment_id = row["payment_sequential"]

        if payment_id is not None:
            existing_payment_ids = {
                payment["payment_sequential"]
                for payment in order["payments"]
            }

            if payment_id not in existing_payment_ids:
                order["payments"].append({
                    "payment_sequential": payment_id,
                    "type": row["payment_type"],
                    "installments": row["payment_installments"],
                    "value": row["payment_value"],
                })

        # Add review
        if (
            order["review"] is None
            and row["review_score"] is not None
        ):
            order["review"] = {
                "score": row["review_score"],
                "comment": row["review_comment_message"],
            }

    customer["orders"] = list(orders.values())

    return customer
#------------------------------------------------------------------




def get_order_details(order_id: str):
    query = text("""
        SELECT
            o.order_id,
            o.customer_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_carrier_date,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,

            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            oi.price,
            oi.freight_value,

            p.product_category_name,

            pay.payment_sequential,
            pay.payment_type,
            pay.payment_installments,
            pay.payment_value,

            r.review_score,
            r.review_comment_message

        FROM orders o

        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id

        LEFT JOIN products p
            ON oi.product_id = p.product_id

        LEFT JOIN payments pay
            ON o.order_id = pay.order_id

        LEFT JOIN reviews r
            ON o.order_id = r.order_id

        WHERE o.order_id = :order_id

        ORDER BY
            oi.order_item_id,
            pay.payment_sequential
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {"order_id": order_id},
        ).mappings().all()

    if not rows:
        return None

    first = rows[0]

    order = {
        "order_id": first["order_id"],
        "customer_id": first["customer_id"],
        "status": first["order_status"],
        "purchase_date": first["order_purchase_timestamp"],
        "approved_date": first["order_approved_at"],
        "carrier_date": first["order_delivered_carrier_date"],
        "delivered_date": first["order_delivered_customer_date"],
        "estimated_delivery": first["order_estimated_delivery_date"],
        "items": [],
        "payments": [],
        "review": None,
    }

    seen_items = set()
    seen_payments = set()

    for row in rows:

        item_id = row["order_item_id"]

        if item_id is not None and item_id not in seen_items:
            order["items"].append({
                "order_item_id": item_id,
                "product_id": row["product_id"],
                "seller_id": row["seller_id"],
                "category": row["product_category_name"],
                "price": row["price"],
                "freight_value": row["freight_value"],
            })

            seen_items.add(item_id)

        payment_id = row["payment_sequential"]

        if payment_id is not None and payment_id not in seen_payments:
            order["payments"].append({
                "payment_sequential": payment_id,
                "type": row["payment_type"],
                "installments": row["payment_installments"],
                "value": row["payment_value"],
            })

            seen_payments.add(payment_id)

        if (
            order["review"] is None
            and row["review_score"] is not None
        ):
            order["review"] = {
                "score": row["review_score"],
                "comment": row["review_comment_message"],
            }

    return order


#--------------------------------------------------------

def get_product_details(product_id: str):
    query = text("""
        SELECT
            product_id,
            product_category_name,
            product_name_length,
            product_description_length,
            product_photos_qty,
            product_weight_g,
            product_length_cm,
            product_height_cm,
            product_width_cm
        FROM products
        WHERE product_id = :product_id
    """)

    with engine.connect() as connection:
        row = connection.execute(
            query,
            {"product_id": product_id},
        ).mappings().first()

    if not row:
        return None

    return dict(row)









def get_customer_record(customer_id: str):
    query = text("""
        SELECT *
        FROM customers
        WHERE customer_id = :customer_id
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_orders(customer_id: str):
    query = text("""
        SELECT o.*
        FROM orders o
        WHERE o.customer_id = :customer_id
        ORDER BY o.order_purchase_timestamp DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_order_items(customer_id: str):
    query = text("""
        SELECT oi.*
        FROM order_items oi
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.customer_id = :customer_id
        ORDER BY o.order_purchase_timestamp DESC, oi.order_item_id
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_products(customer_id: str):
    query = text("""
        SELECT DISTINCT p.*
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.customer_id = :customer_id
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_sellers(customer_id: str):
    query = text("""
        SELECT DISTINCT s.*
        FROM sellers s
        JOIN order_items oi ON oi.seller_id = s.seller_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.customer_id = :customer_id
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_payments(customer_id: str):
    query = text("""
        SELECT pay.*
        FROM payments pay
        JOIN orders o ON o.order_id = pay.order_id
        WHERE o.customer_id = :customer_id
        ORDER BY o.order_purchase_timestamp DESC, pay.payment_sequential
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id }
        ).mappings().all()
    return [dict(row) for row in rows]


def get_customer_reviews(customer_id: str):
    query = text("""
        SELECT r.*
        FROM reviews r
        JOIN orders o ON o.order_id = r.order_id
        WHERE o.customer_id = :customer_id
        ORDER BY r.review_creation_date DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(
            query, {"customer_id": customer_id}
        ).mappings().all()
    return [dict(row) for row in rows]
