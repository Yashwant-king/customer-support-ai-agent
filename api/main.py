
from fastapi import Depends, FastAPI, HTTPException
from dotenv import load_dotenv

from auth.dependencies import get_current_user
from api.checking import Chatrequest, Chatresponse

load_dotenv()

fast_app = FastAPI()


@fast_app.get("/auth/me")
def get_me(user=Depends(get_current_user)):
    return {
        "authenticated": True,
        "user_id": user.id,
        "email": user.email,
    }


@fast_app.post("/chat", response_model=Chatresponse)
async def chat_endpoint(
    request: Chatrequest,
    user=Depends(get_current_user),
):
    # Authentication succeeded, but customer authorization
    # has not been implemented yet.
    raise HTTPException(
        status_code=501,
        detail=(
            "Authentication succeeded, but customer account "
            "authorization is not implemented yet."
        ),
    )
