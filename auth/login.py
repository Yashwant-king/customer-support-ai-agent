
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"],
)


def authenticate_customer(email: str, password: str) -> dict:
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        if not response.user or not response.session:
            return {"authenticated": False}

        return {
            "authenticated": True,
            "user_id": response.user.id,
            "access_token": response.session.access_token,
        }

    except Exception:
        return {"authenticated": False}
