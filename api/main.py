from typing import Any, cast

from fastapi import FastAPI,HTTPException
from graph.main import app
from api.checking import Chatrequest,Chatresponse
from langchain_core.runnables import RunnableConfig
import uuid
customer_id="0002414f95344307404f0ace7a26f1d5"

config: RunnableConfig = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
}

  
  
fast_app=FastAPI()






@fast_app.post("/chat",response_model=Chatresponse)
async def chat_endpoint(request: Chatrequest):
    # Your chat logic here
    try:
        customer_id =request.customer_id                  
        customer_query =request.customer_query
        result = app.invoke(
            cast(Any, {"customer_id": customer_id, "customer_query": customer_query}),
            config=config,
        )
        return Chatresponse(final_resul=result["final_result"])
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error processing request: {e}")


