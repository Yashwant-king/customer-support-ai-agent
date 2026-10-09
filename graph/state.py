from typing import TypedDict, Any, List, Annotated
from langgraph.graph import add_messages
from langgraph.graph import StateGraph,END,START





class SupportState(TypedDict):
    """
    Represents the state of the support system.
    """
    messages:Annotated[list,add_messages]
    customer_id:Any
    customer_exists:bool
    customer_query:str
    final_result:Any
    
    
    
    




graph=StateGraph(SupportState)
