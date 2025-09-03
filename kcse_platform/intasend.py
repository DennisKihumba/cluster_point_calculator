import os
import requests

INTASEND_API_KEY = os.getenv("INTASEND_API_KEY")
BASE_URL = os.getenv("INTASEND_BASE_URL")

def initiate_payment(email, amount, phone):
    url = f"{BASE_URL}/api/v1/checkout/"
    headers = {
        "Authorization": f"Bearer {INTASEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": amount,
        "currency": "KES",
        "email": email,
        "phone_number": phone,
        "redirect_url": "https://yourdomain.com/payment-success",
        "hosted_payment": True
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
