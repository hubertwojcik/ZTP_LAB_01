from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.product_category import ProductCategory, ProductCategoryCreate
from src.repositories.category_repository import CategoryRepository
from src.models.product_category import ProductCategory as ProductCategoryModel

router = APIRouter()


def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


@router.get("/", response_model=List[ProductCategory], status_code=status.HTTP_200_OK)
def get_categories(repository: CategoryRepository = Depends(get_category_repository)):
    """Get all product categories"""
    categories = repository.find_all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")
    return categories


@router.get("/{category_id}", response_model=ProductCategory, status_code=status.HTTP_200_OK)
def get_category(category_id: int, repository: CategoryRepository = Depends(get_category_repository)):
    """Get a specific category by ID"""
    category = repository.find_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=ProductCategory, status_code=status.HTTP_201_CREATED)
def create_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    """Create a new product category"""
    try:
        existing_category = db.query(ProductCategoryModel).filter(
            ProductCategoryModel.name == category.name
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        if category.min_price >= category.max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="max_price must be greater than min_price"
            )
        
        new_category = ProductCategoryModel(**category.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))