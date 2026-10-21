
from getpass import getpass
from auth.login import authenticate_customer

email = input("Gmail: ").strip()
password = getpass("Password: ")

result = authenticate_customer(email, password)

if result["authenticated"]:
    print("Valid authenticated user!")
    print("User ID:", result["user_id"])
    print("Email:", result["email"])
else:
    raise ValueError("Authentication failed:", result["message"])
