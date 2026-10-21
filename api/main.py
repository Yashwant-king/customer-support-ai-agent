from typing import Any, cast
from fastapi import Depends
from auth.dependencies import get_current_user
from fastapi import FastAPI,HTTPException
from graph.main import app
from api.checking import Chatrequest,Chatresponse
from langchain_core.runnables import RunnableConfig
import uuid
from dotenv import load_dotenv
load_dotenv()


#--------------------------------------------------------------
from auth.login import authenticate_customer

# result = authenticate_customer(
#     "customer@gmail.com",
#     "customer_password",
# )

# if result["authenticated"]:
#     print("Customer authenticated successfully")
# else:
#     print("Invalid email or password")

#-------------------------------------------------------------

# customer_id="0002414f95344307404f0ace7a26f1d5"

config: RunnableConfig = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
}

  
  
fast_app=FastAPI()


@fast_app.get("/auth/me")
def get_me(user=Depends(get_current_user)):
    return {
        "authenticated": True,
        "user_id": user.id,
        "email": user.email,
    }



@fast_app.post("/chat",response_model=Chatresponse)
def chat_endpoint(request: Chatrequest):
    print("Enter in chat_endpoint")
    
    result = authenticate_customer(
    request.gmail,
    request.password,
)
    print("Authentication result:", result)

    if result["authenticated"]:
        print("Customer authenticated successfully")
        try:
                print("Processing chat request")
                customer_id =request.customer_id                  
                customer_query =request.customer_query
                result = app.invoke(
                    cast(Any, {"customer_id": customer_id, "customer_query": customer_query}),
                    config=config,
                )
                return Chatresponse(final_result=result["final_result"])
        except Exception as e:
            print("Error processing request:", e)
            return HTTPException(status_code=500, detail=f"Error processing request: {e}")
    #    print("Customer authenticated successfully")
    else:
        print("Invalid email or password")
        return HTTPException(status_code=401, detail="Invalid email or password")
  



