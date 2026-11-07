from langchain_core.runnables import RunnableConfig
import uuid
from graph.random_id import get_random_customer_id
from graph.main import app
from graph.state import SupportState
from graph.state import SupportState
import os



customer_id=os.getenv("customer_id")
config: RunnableConfig = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        },
    }
# state: SupportState = {
#         "messages": [],
#         "customer_id": str(get_random_customer_id()),
#         "customer_query": "give all information of my order",
#         "final_result": None,
#         "node_1": None,
#         "blank_list": None,
#         "risk": None,
#     }

def target(inputs: dict) -> dict:

    # Receive input from LangSmith
    query = inputs["query"]
    
    # Execute your LangGraph agent
    state: SupportState={
        "messages": [],
        "customer_id": customer_id,
        "customer_query": query,
        "final_result": None,
        "node_1": None,
        "blank_list": None,
        "risk": None,
    }
    result = app.invoke(
        state,
        config=config
    )

    # print("Final result from LangGraph agent:", result["final_result"])
    # Return agent output
    return {
        "response": result["final_result"],
        "risk": result["risk"],
        "node_1": result.get("node_1", []),
    }




if __name__ == "__main__":
    # Example input for testing
    test_input = {
        "query": "give all information of my order"
        
    }

    output = target(test_input)
    print(type(output),"----------------------\n")
    print(output)