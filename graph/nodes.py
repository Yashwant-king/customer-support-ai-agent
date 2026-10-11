from click import prompt

from graph.state import SupportState
from llm import llm
from sqlalchemy import text
from sqlalchemy import create_engine
from database.connection import engine
from langgraph.types import Command,interrupt
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from langgraph.graph import END,START
# from graph.invoke_tools import llm_with_tools
from pydantic import BaseModel,Field
from typing import Literal
from graph.pydantic_classes import RequiredFunctions
from database.customer_service import (
    get_customer_record,
    get_customer_orders,
    get_customer_order_items,
    get_customer_products,
    get_customer_sellers,
    get_customer_payments,
    get_customer_reviews,
)
from tools.rag_tools import search_company_policy


#----------------------------------------------------------------------
def verification_node(state:SupportState):
    """"
    Verify the customer's information.
    """
    print("Enter in verification_node")
    
    customer_id=state["customer_id"]    
    query = text("""
        SELECT 1
        FROM customers
        WHERE customer_id = :customer_id
        LIMIT 1
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"customer_id": customer_id},
        ).first()

    if not result:
        print(f"Customer with ID {customer_id} does not exist.")
        return Command(
            goto=END
        )


#------------------------------------------------------------------------


def node_1(state:SupportState):
    """
    Handle the case where the customer is found.
    """
    print("Enter in node_1")

    prompt=f"""
    You are a query-analysis component in a customer support system.

Customer query:
{state['customer_query']}

Available functions and their purposes:

- `get_customer_record`: Retrieves the customer's profile and basic customer information.
- `get_customer_orders`: Retrieves orders belonging to the customer.
- `get_customer_order_items`: Retrieves items purchased in the customer's orders.
- `get_customer_products`: Retrieves product details for products purchased by the customer.
- `get_customer_sellers`: Retrieves sellers associated with the customer's orders.
- `get_customer_payments`: Retrieves payment records associated with the customer's orders.
- `get_customer_reviews`: Retrieves reviews associated with the customer's orders.
- `search_company_policy`: Searches the company's policy documents for relevant information.

Instructions:
1. Carefully analyze what information is required to answer the customer query.
2. Select only the functions whose results are necessary to answer the query accurately.
3. Select the minimum number of functions needed. Do not select functions merely because they might be useful.
4. If the query can be answered without retrieving customer-specific database information, return an empty list.
5. Use only the exact function names provided above.
6. Return only a valid Python list of strings. Do not include explanations, Markdown, or additional text.

Expected output format:
['get_customer_orders', 'get_customer_payments']

If no functions are required, return:
[]
"""
    llm_sto = llm.with_structured_output(
    RequiredFunctions,
    method="json_schema",
    strict=True,
)
    try:
       llm_response = llm_sto.invoke(prompt)
       return {"node_1": llm_response.functions}
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return {"node_1": []}   
   
#--------------------------------------------------------------------



#-----------------------------------------------------------------------

def node_2(state:SupportState):
    """
    Handle the case where the customer is found.
    """
    print("Enter in node_2")
    prompt=f"""You analyze customer queries to determine which database functions are needed.

Customer query:
{state['customer_query']}

Available functions:
- `get_customer_record`: Fetch customer profile information.
- `get_customer_orders`: Fetch the customer's orders.
- `get_customer_order_items`: Fetch items included in the customer's orders.
- `get_customer_products`: Fetch products purchased by the customer.
- `get_customer_sellers`: Fetch sellers linked to the customer's orders.
- `get_customer_payments`: Fetch payment records for the customer's orders.
- `get_customer_reviews`: Fetch reviews associated with the customer's orders.
- `search_company_policy`: Search the company's policy documents for relevant information.

Instructions:
1. Identify the information needed to answer the query.
2. Choose only the necessary functions, using the smallest sufficient set.
3. Do not include functions that are not required.
4. If no customer-specific database lookup is needed, return an empty list.
5. Use only the function names listed above.
6. Output only a valid Python list of strings, without explanations or Markdown.

Example output:
['get_customer_orders', 'get_customer_payments']

If no functions are needed:
[]
"""
    llm_sto = llm.with_structured_output(
    RequiredFunctions,
    method="json_schema",
    strict=True,
)

    try:
        llm_response = llm_sto.invoke(prompt)
        return {"node_2": llm_response.functions}
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return {"node_2": []}

  


#-----------------------------------------------------------------------
# def time_node(state:SupportState):
#     print("Enter in time_node")
#     time.sleep(5)
    
#     print("5 seconds have passed")
    
#-----------------------------------------------------------------------------
def merge_list_node(state:SupportState):
    """
    Handle the case where the customer is found.
    """
    print("Enter in merge_list_node")
    merged_list=list(set(state["node_1"] + state["node_2"]))
    blank_list=[]
    if merged_list==[] or merged_list==[""] or len(merged_list)==0:
        return {"blank_list": []}
    for item in merged_list:
        item=item.strip()
        if item=="get_customer_record":
            blank_list.append(get_customer_record(state["customer_id"]))
        elif item=="get_customer_orders":
            blank_list.append(get_customer_orders(state["customer_id"]))
        elif item=="get_customer_order_items":
            blank_list.append(get_customer_order_items(state["customer_id"]))
        elif item=="get_customer_products":
            blank_list.append(get_customer_products(state["customer_id"]))
        elif item=="get_customer_sellers":
            blank_list.append(get_customer_sellers(state["customer_id"]))
        elif item=="get_customer_payments":
            blank_list.append(get_customer_payments(state["customer_id"]))
        elif item=="get_customer_reviews":
            blank_list.append(get_customer_reviews(state["customer_id"]))
        elif item=="search_company_policy":
            blank_list.append(search_company_policy(state["customer_query"]))                            

    return {"blank_list": blank_list}    

#-------------------------------------------------------------------------

def analyse_answer_node(state:SupportState):
    print("Enter in analyse_answer_node")
    if state["blank_list"]==[] or state["blank_list"]==[""] or len(state["blank_list"])==0:
        return {"final_result": llm.invoke(f"""Explain the topic:\n\ncustomer query:{state['customer_query']} \n\nAlso mention that the information provided is insufficient to answer the query.""").content}
    else:
        prompt = f"""
You are a customer support assistant. Answer the customer's query using only the information provided.

Customer query:
{state['customer_query']}

Retrieved information:
{state['blank_list']}

Instructions:
1. Use only the retrieved information to answer the query.
2. If the information is insufficient, clearly state that you don't have enough information.
3. Do not invent facts or make unsupported promises.
4. Provide a clear, concise, and helpful response.

Explain the answer in a way that is easy for the customer to understand. If you cannot answer the query based on the provided information, respond with a polite message indicating that you don't have enough information to provide an answer.
If Customer query is not related to the retrieved information, respond with a polite message indicating that you don't have enough information to provide an answer.
"""
    
    llm_response=llm.invoke(prompt)
    return {"final_result": llm_response.content}
    
