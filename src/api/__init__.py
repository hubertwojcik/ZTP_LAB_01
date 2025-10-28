from fastapi import APIRouter

# Import all routers here
from src.api import products, forbidden_phrases, product_audit

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(forbidden_phrases.router, prefix="/forbidden-phrases", tags=["forbidden-phrases"])
api_router.include_router(product_audit.router, tags=["audit"])

