from langchain_core.tools import tool

from database.customer_service import (
    get_customer_details,
    get_order_details,
    get_product_details
)


@tool
def lookup_customer(customer_id: str) -> dict:
    """
    Look up a customer and their order history.

    Use this when customer-specific information is required.
    """

    customer = get_customer_details(customer_id)

    if customer is None:
        return {
            "found": False,
            "message": "Customer not found."
        }

    return {
        "found": True,
        "customer": customer,
    }


#----------------------------------------------------------------


@tool
def lookup_order(order_id: str) -> dict:
    """
    Look up a specific order including its status,
    items, payments, and review information.
    """

    order = get_order_details(order_id)

    if order is None:
        return {
            "found": False,
            "message": "Order not found."
        }

    return {
        "found": True,
        "order": order,
    }




#------------------------------------------------------------------



@tool
def lookup_product(product_id: str) -> dict:
    """
    Look up information about a product.
    """

    product = get_product_details(product_id)

    if product is None:
        return {
            "found": False,
            "message": "Product not found."
        }

    return {
        "found": True,
        "product": product,
    }