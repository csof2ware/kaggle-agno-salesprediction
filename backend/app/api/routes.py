from fastapi import APIRouter
from app.services.mercado_livre import get_products
from app.services.db_service import save_products


router = APIRouter()

@router.get("/")
def root():
    return {"message": "API running"}



@router.get("/products")
def products():
    data = get_products("tenis")
    save_products(data)
    return data