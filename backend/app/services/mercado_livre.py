import requests
import os

TOKEN = os.getenv("ML_ACCESS_TOKEN")

def get_products(query="tenis"):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}"

    headers = {"Authorization": f"Bearer {TOKEN}"}

    data = requests.get(url, headers=headers).json()

    return data.get("results", [])