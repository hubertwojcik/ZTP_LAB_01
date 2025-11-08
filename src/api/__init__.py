from fastapi import APIRouter

from src.api import products, forbidden_phrases, product_audit, product_category

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(forbidden_phrases.router, prefix="/forbidden-phrases", tags=["forbidden-phrases"])
api_router.include_router(product_category.router, prefix="/categories", tags=["categories"])
api_router.include_router(product_audit.router, tags=["audit"])

