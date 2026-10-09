from tools.order_tools import lookup_order
from tools.olist_tools import lookup_customer, lookup_orders, lookup_order_items, lookup_products, lookup_sellers, lookup_payments, lookup_reviews
from llm import llm
from tools.rag_tools import search_company_policy
tools=[
    lookup_orders,
    lookup_customer,
    lookup_order_items,
    lookup_products,
    lookup_sellers,
    lookup_payments,
    lookup_reviews,
    search_company_policy
]



llm_with_tools=llm.bind_tools(tools)
print("llm_with_tools is ready to use")


