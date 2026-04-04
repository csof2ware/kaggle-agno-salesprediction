import requests
import os

TOKEN = os.getenv("ML_ACCESS_TOKEN")
BASE_URL = "https://api.mercadolibre.com"

def get_trends():
    return requests.get(f"{BASE_URL}/trends/MLB").json()

def get_item_detail(item_id):
    return requests.get(f"{BASE_URL}/items/{item_id}").json()



def enrich(products):
    result = []

    for p in products:
        detail = get_item_detail(p["id"])

        price = detail.get("price", 0)
        sold = detail.get("sold_quantity", 0)

        result.append({
            "title": detail.get("title"),
            "price": price,
            "sold": sold,
            "revenue": price * sold
        })

    return result