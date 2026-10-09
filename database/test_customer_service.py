from database.customer_service import get_customer_details,get_customer_reviews,get_customer_payments,get_customer_orders,get_customer_order_items,get_customer_products,get_customer_sellers


if __name__ == "__main__":

    customer_id = input("Enter Customer ID: ").strip()

    customer = get_customer_products(customer_id)

    if customer is None:
        print("Customer not found.")
    else:
        print("\nCustomer:")
        print(customer)