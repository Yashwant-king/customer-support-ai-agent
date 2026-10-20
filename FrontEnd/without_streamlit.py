import os
from getpass import getpass
import requests


from dotenv import load_dotenv
from supabase import create_client
import supabase


user_gmail=input("Enter your Gmail to login: ")
if not user_gmail:
    raise ValueError("Gmail cannot be empty. Please provide a valid Gmail address.")
user_password=input("Enter your password: ")
if not user_password:
    raise ValueError("Password cannot be empty. Please provide a valid password.")

#-------------------------------------------
try:
    response = supabase.auth.sign_in_with_password({
        "email": user_gmail,
        "password": user_password,
    })
    if response:
except Exception as e:
    pass
