from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.product import Product, ProductCreate, ProductUpdate
from src.services.product_service import ProductService

router = APIRouter()


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_products(skip: int = 0, limit: int = 100, service: ProductService = Depends(get_product_service)):
    """Get all products with pagination"""
    return service.get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Get a specific product by ID"""
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    """Create a new product"""
    try:
        return service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: ProductUpdate, service: ProductService = Depends(get_product_service)):
    """Update a product"""
    try:
        updated_product = service.update_product(product_id, product)
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a product"""
    try:
        if not service.delete_product(product_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))