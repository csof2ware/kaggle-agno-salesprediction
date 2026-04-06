from app.database.db import SessionLocal
from app.database.models import Product


def save_products(products):
    db = SessionLocal()

    try:
        for item in products:
            product = Product(
                title=item.get("title"),
                price=item.get("price", 0),
                sold=item.get("sold_quantity", 0)
            )
            db.add(product)

        db.commit()

    finally:
        db.close()


def save_analysis(results):
    db = SessionLocal()

    try:
        for trend in results:
            for product in trend.get("products", []):
                db_product = Product(
                    title=product.get("title"),
                    price=product.get("price", 0),
                    sold=product.get("sold", 0)
                )
                db.add(db_product)

        db.commit()

    finally:
        db.close()