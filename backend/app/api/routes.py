from fastapi import APIRouter, HTTPException

from app.services.mercado_livre import get_products
from app.services.db_service import save_products, save_analysis
from app.services.market_intelligence import run_market_analysis

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API running"}

@router.get("/products")
def products():
    try:
        data = get_products("tenis")
        save_products(data)
        return {
            "status": "success",
            "results": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-analysis")
def market_analysis():
    try:
        payload = run_market_analysis()

        if payload.get("status") == "success":
            save_analysis(payload.get("results", []))

        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))