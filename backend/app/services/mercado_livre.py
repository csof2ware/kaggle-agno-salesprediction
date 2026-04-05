import requests

from app.services.ml_auth import MercadoLivreAuthService

BASE_URL = "https://api.mercadolibre.com"

auth_service = MercadoLivreAuthService()

def _auth_headers():
    token = auth_service.get_valid_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }

def get_products(query="tenis"):
    url = f"{BASE_URL}/sites/MLB/search"
    response = requests.get(
        url,
        headers=_auth_headers(),
        params={"q": query},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])