from langgraph.graph import END,START
from typing import cast

from graph.state import SupportState, graph
from graph.nodes import  verification_node, customer_not_found_node, customer_found_node
from graph.random_id import get_random_customer_id


#---------------------------------------NODES-------------------------------------------------------------
graph.add_node("verification_node", verification_node)
graph.add_node("customer_not_found_node", customer_not_found_node)
graph.add_node("customer_found_node", customer_found_node)







#-----------------------------------------EDGES-------------------------------------------------------------
graph.add_edge(START, "verification_node")
graph.add_edge("customer_not_found_node", END)
graph.add_edge("customer_found_node", END)


#------------------------------------------------------------------------
app=graph.compile()

#-----------------------------------------------------------------------

output=app.invoke(cast(SupportState, {
    "customer_id":get_random_customer_id(),
    "messages":[],
    "customer_query":"I want to know the status of my order"
}))











#---------------------------------------------------------------------------------
