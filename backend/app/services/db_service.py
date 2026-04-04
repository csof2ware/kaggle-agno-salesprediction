from app.database.db import SessionLocal
from app.database.models import Product

def save_products(products):
    db = SessionLocal()

    for p in products:
        product = Product(
            title=p.get("title"),
            price=p.get("price", 0),
            sold=p.get("sold_quantity", 0)
        )
        db.add(product)

    db.commit()
    db.close()