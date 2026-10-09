
from langchain_core.tools import tool

from database.customer_service import (
    get_customer_record,
    get_customer_orders,
    get_customer_order_items,
    get_customer_products,
    get_customer_sellers,
    get_customer_payments,
    get_customer_reviews,
)


@tool
def lookup_customer(customer_id: str) -> dict:
    """Look up a customer record using their customer ID."""
    rows = get_customer_record(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_orders(customer_id: str) -> dict:
    """Look up all orders belonging to a customer."""
    rows = get_customer_orders(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_order_items(customer_id: str) -> dict:
    """Look up items in all orders belonging to a customer."""
    rows = get_customer_order_items(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_products(customer_id: str) -> dict:
    """Look up distinct products purchased by a customer."""
    rows = get_customer_products(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_sellers(customer_id: str) -> dict:
    """Look up sellers associated with a customer's orders."""
    rows = get_customer_sellers(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_payments(customer_id: str) -> dict:
    """Look up payments associated with a customer's orders."""
    rows = get_customer_payments(customer_id)
    return {"found": bool(rows), "data": rows}


@tool
def lookup_reviews(customer_id: str) -> dict:
    """Look up reviews associated with a customer's orders."""
    rows = get_customer_reviews(customer_id)
    return {"found": bool(rows), "data": rows}
