from pydantic import BaseModel, Field
from typing import Literal

FunctionName = Literal[
    "get_customer_record",
    "get_customer_orders",
    "get_customer_order_items",
    "get_customer_products",
    "get_customer_sellers",
    "get_customer_payments",
    "get_customer_reviews",
    "search_company_policy"
]

class RequiredFunctions(BaseModel):
    functions: list[FunctionName] = Field(...,description="Minimum set of functions required to answer the query"
    )

