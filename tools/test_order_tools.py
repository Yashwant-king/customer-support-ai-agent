from tools.order_tools import lookup_order


if __name__ == "__main__":

    order_id = input("Enter Order ID: ").strip()

    result = lookup_order.invoke({
        "order_id": order_id
    })

    print("\nTool result:")
    print(result)