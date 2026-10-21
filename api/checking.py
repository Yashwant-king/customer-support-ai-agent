from pydantic import BaseModel,Field
from typing import Any

class Chatrequest(BaseModel):
    customer_id:str
    customer_query:str
    gmail:Any
    password:Any
    # final_result:str
    # node_1:Any
    # node_2:Any
    # blank_list:Any



class Chatresponse(BaseModel):
    final_result:str
        

