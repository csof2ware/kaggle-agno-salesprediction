from fastapi import APIRouter
from app.services.mercado_livre import get_products
from app.services.db_service import save_products
from app.services.market_intelligence 
import get_trends, enrich, score

@router.get("/market-analysis")
def analysis():
    trends = get_trends()
    results = []

    for t in trends[:5]:
        keyword = t["keyword"]

        data = get_products(keyword)
        enriched = enrich(data[:5])
        scored = score(enriched)

        results.append({
            "trend": keyword,
            "products": scored
        })

    return results


router = APIRouter()

@router.get("/")
def root():
    return {"message": "API running"}



@router.get("/products")
def products():
    data = get_products("tenis")
    save_products(data)
    return data

    Python
from app.services.market_intelligence import get_trends, enrich, score

@router.get("/market-analysis")
def analysis():
    trends = get_trends()
    results = []

    for t in trends[:5]:
        keyword = t["keyword"]

        data = get_products(keyword)
        enriched = enrich(data[:5])
        scored = score(enriched)

        results.append({
            "trend": keyword,
            "products": scored
        })

    return results