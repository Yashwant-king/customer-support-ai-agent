from graph.state import SupportState
from llm import llm
from sqlalchemy import text
from sqlalchemy import create_engine
from database.connection import engine
from langgraph.types import Command,interrupt
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from langgraph.graph import END,START
from graph.invoke_tools import llm_with_tools


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
        return Command(
            goto="customer_not_found_node"
        )
    else:
        return Command(
            goto="customer_found_node"
        )    


    




#----------------------------------------------------------------------
def customer_not_found_node(state:SupportState):
    """
    Handle the case where the customer is not found.
    """
    print("Enter in customer_not_found_node")

    return Command(
        update={
            "final_result":"Customer not found. Please check the customer ID and try again."
        },
        goto=END
    )


#-----------------------------------------------------------------------
def customer_found_node(state:SupportState):
    print("Enter in customer_found_node")
    prompt=f"""
    You are a customer support agent. You have access to the following tools to assist customers with their queries:
    tools=[
    lookup_orders,
    lookup_customer,
    lookup_order_items,
    lookup_products,
    lookup_sellers,
    lookup_payments,
    lookup_reviews,
    search_company_policy = RAG tool for comapny policy search
    ]
    \n\n\n
    customer_query={state['customer_query']}\n\n\n
    customer_id={state['customer_id']}\n\n\n
    please provide a detailed response to the customer's query using the available tools. If you need to look up any information, use the appropriate tool. If you cannot find the information, inform the customer politely.
    \n\n
    Analyse the customer query and provide a detailed response. If you need to look up any information, use the appropriate tool. If you cannot find the information, inform the customer politely.

    """
    llm_response=llm_with_tools.invoke(prompt)
    

    




