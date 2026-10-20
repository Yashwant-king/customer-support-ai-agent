
import os
from getpass import getpass
import requests


from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("Missing Supabase settings in .env")

supabase = create_client(url, key)

email = input("Test user email: ")
password = input("Test user password: ")

try:
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    if not response.session:
        print("Login did not return a session.")
    else:
        print("Login successful!")
        print("Access token received.")
        print("User ID:", response.user.id)
        access_token = response.session.access_token

        api_response = requests.get(
            "http://127.0.0.1:8000/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=10,
        )

        print("API status:", api_response.status_code)
        print("API response:", api_response.json())

except Exception:
    print("Login failed. Check the credentials and email confirmation.")
