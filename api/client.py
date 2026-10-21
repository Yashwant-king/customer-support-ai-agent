import requests
from graph.random_id import get_random_customer_id

data = {
    "customer_id": str(get_random_customer_id()),
    "customer_query": "where is my order ?",
    "gmail": "yashwantchauhan2911@gmail.co",
    "password": "@dodo@",
}


def posting(data):
    r = requests.post("http://localhost:8000/chat",json=data)
    return r


r = posting(data)

if r.status_code == 200:
    print("Request successful!")
    print("Response:", r.json()["final_result"])
else:
    print("Request failed with status code:", r.status_code)
    print("Response:", r.json())
