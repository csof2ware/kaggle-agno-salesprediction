import time
from app.services.mercado_livre import get_products
from app.services.db_service import save_products

def run():
    while True:
        data = get_products("tenis")
        save_products(data)
        time.sleep(3600)