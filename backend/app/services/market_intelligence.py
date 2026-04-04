import requests
import os

TOKEN = os.getenv("ML_ACCESS_TOKEN")
BASE_URL = "https://api.mercadolibre.com"

def get_trends():
    return requests.get(f"{BASE_URL}/trends/MLB").json()

def get_item_detail(item_id):
    return requests.get(f"{BASE_URL}/items/{item_id}").json()